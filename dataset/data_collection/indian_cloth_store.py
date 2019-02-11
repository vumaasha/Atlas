import pandas as pd
import requests
import scrapy
from tqdm import tqdm
import re
from ..Utils import write_into_json
from ..items import IndianClothStoreItem

class IndianClothStore(scrapy.Spider):
    name = "indianclothstore_crawler"
    custom_settings = {
        'ITEM_PIPELINES': {
            'Crawler.pipelines.IndianClothStorePipeline': 1
        }
    }

    input_csv_file = 'Men.csv'  # csv file containing the taxonomy and website source URL's
    source_urls_col = 'IndianClothStore'  # Column name having the source URL's in CSV file
    taxonomy_col = 'Taxonomy'  # Column name having the taxonomy of the product

    map_file = pd.read_csv(input_csv_file)

    def start_requests(self):
        start_request_list = []
        for index, row in self.map_file.dropna(subset=[self.source_urls_col]).iterrows():
            taxonomy = row[self.taxonomy_col]
            source_url = row[self.source_urls_col]
            start_request_list.append(scrapy.Request(source_url, callback=self.parse, meta={'taxonomy': taxonomy}))
        return start_request_list

    def parse(self, response):
        all_items = response.css('div[itemprop=itemListElement] a.display-block.product-detail-lnk::attr(href)').extract()
        self.logger.info('All items for {} is {}'.format(response.meta['taxonomy'], len(all_items)))
        for item in all_items:
            taxonomy = response.meta['taxonomy']
            product_page_url = 'https://www.indianclothstore.com'+ item
            yield scrapy.Request(product_page_url, callback=self.parse_product,
                                 meta={'product_page_url': product_page_url, 'taxonomy': taxonomy})

        # check if next page is available
        next_page = response.css('ul.pagination.display-flex.align-items-center.justify-center a[title=Next]::attr(href)').extract_first()
        if next_page is not None:
            next_page = response._url.split('?')[0] + next_page
            yield response.follow(next_page, callback=self.parse, meta={'taxonomy': taxonomy})

    def parse_product(self, response):
        dict_of_items = {}
        dict_of_items['product_title'] = response.css('div.left h1::text').extract_first()
        dict_of_items['product_price'] = response.css('div.price-section.d-col.d10 span.a-price::text').extract_first()
        product_image_url = response.css('div#divgalleryimage img::attr(src)').extract_first()
        dict_of_items['product_image_url'] = product_image_url
        dict_of_items['product_page_url'] = response.meta['product_page_url']
        list_of_specs = response.css('div.styling-option.d-row.links p.d-col.col-6')
        for i in range(0, len(list_of_specs)):
            dict_of_items[re.sub(':', ' ', list_of_specs[i].css('span::text').extract_first())] = ','.join(list_of_specs[i].css('a::text').extract()) + list_of_specs[i].css('p::text').extract_first()
        image_file_name = product_image_url.split('/')[-1]
        dict_of_items['taxonomy'] = response.meta['taxonomy']
        file_path = response.meta['taxonomy'].replace("->",
                                                      "/") + "/" + self.source_urls_col + "/images/" + image_file_name
        dict_of_items['file_path'] = file_path
        json_path = 'images/' + response.meta['taxonomy'].replace("->",
                                                                  "/") + "/" + self.source_urls_col + '/'
        write_into_json(json_path,dict_of_items)

        yield IndianClothStoreItem(image_url=product_image_url, image_name=image_file_name, image_path=file_path)

