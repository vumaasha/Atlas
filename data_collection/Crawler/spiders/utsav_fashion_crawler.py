import pandas as pd
import requests
import scrapy
from tqdm import tqdm
from ..items import UtsavFashionItem
from ..Utils import write_into_json


def get_url_for_items(items_to_search):
    search_url = 'https://www.utsavfashion.in/catalogsearch/result/?q='
    item_list = []
    start_url_list = []
    for item in items_to_search:
        search_key = item.replace(' ', '%20')
        product_search_url = search_url + search_key
        search_result = requests.get(url=product_search_url)
        if search_result.url:
            item_list.append(item)
            start_url_list.append(search_result.url)
    return item_list, start_url_list


class UtsavFashion(scrapy.Spider):
    name = "utsav_fashion_crawler"
    custom_settings = {
        'IMAGES_STORE': '/home/et/Desktop/Atlas/dataset/',
        'ITEM_PIPELINES': {
            'Crawler.pipelines.UtsavFashionPipeline': 1
        }
    }

    source_urls_col = 'Utsav'  # Column name having the source URL's in CSV file
    taxonomy_col = 'Taxonomy'  # Column name having the taxonomy of the product

    def start_requests(self):
        input_csv_file = '/home/et/Desktop/Atlas/data_collection/dataset.csv'  # csv file containing the taxonomy and website source URL's
        map_file = pd.read_csv(input_csv_file)
        start_request_list = []
        for index, row in map_file.dropna(subset=[self.source_urls_col]).iterrows():
            taxonomy = row[self.taxonomy_col]
            source_url = row[self.source_urls_col]
            start_request_list.append(scrapy.Request(source_url, callback=self.parse, meta={'taxonomy': taxonomy}))
        return start_request_list


    def parse(self, response):

        # all_items = response.css('li.item.uf-product-griditem')
        all_items = response.css('div.category-products li.item.uf-product-griditem a.product-image::attr(href)').extract()
        self.logger.info('All items for {} is {}'.format(response.meta['taxonomy'], len(all_items)))
        for item in all_items:

            #product_title = item.css('div.product-name a::attr(title)').extract_first()
            #product_price = item.css('div.price-box span.price::text').extract_first()
            taxonomy = response.meta['taxonomy']
            #product_page_url = item.css('div.product-name a::attr(href)').extract_first()
            product_page_url = item
            yield scrapy.Request(product_page_url, callback=self.parse_product,
                                 meta={'product_page_url': product_page_url, 'taxonomy': taxonomy})

        # check if next page is available
        next_page = response.css('a.next.ic.ic-right::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, meta={'taxonomy': taxonomy})

    def parse_product(self, response):
        dict_of_items = {}
        dict_of_items['product_title'] = response.css('div.product-name h1::text').extract_first()
        price_box = response.css('div.bundle-top-price div.price-box')
        product_price = price_box.css('p.special-price span.price span.price::text').extract_first()
        if not product_price:
            product_price = price_box.css('span.price::text').extract_first()
        dict_of_items['product_price'] = product_price
        product_image_url = response.css('img#image-main::attr(src)').extract_first()
        dict_of_items['product_image_url'] = product_image_url
        dict_of_items['Product_Highlights'] = ', '.join(response.css('div.dg-product-description li::text').extract())
        product_header = response.css('table#product-attribute-specs-table th::text').extract()
        product_info = response.css('table#product-attribute-specs-table td::text').extract()
        for header, item in zip(product_header,product_info):
            dict_of_items[header] = item
        image_file_name = product_image_url.split('/')[-1]
        temp_taxonomy = response.meta['taxonomy'].replace(" ", "_")
        file_path = 'atlas_dataset/' + temp_taxonomy.replace("->",
                                                             "-") + "/images/" + image_file_name
        dict_of_items['file_path'] = file_path
        dict_of_items['product_page_url'] = response.meta['product_page_url']
        dict_of_items['taxonomy'] = response.meta['taxonomy']

        json_path = '/home/et/Desktop/Atlas/dataset/atlas_dataset/' + temp_taxonomy.replace("->",
                                                                                            "-") + "/"

        write_into_json(json_path,dict_of_items)

        yield UtsavFashionItem(image_url=product_image_url, image_name=image_file_name, image_path=file_path)

