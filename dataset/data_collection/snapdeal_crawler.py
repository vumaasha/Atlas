import pandas as pd
import requests
import scrapy
from tqdm import tqdm
from ..items import SnapdealItem
from ..Utils import write_into_json


class Snapdeal(scrapy.Spider):
    name = "snapdeal_crawler"
    custom_settings = {
        'ITEM_PIPELINES': {
            'Crawler.pipelines.SnapdealPipeline': 1
        }
    }

    input_csv_file = 'Sheet11.csv'  # csv file containing the taxonomy and website source URL's
    source_urls_col = 'Snapdeal'  # Column name having the source URL's in CSV file
    taxonomy_col = 'Taxonomy'  # Column name having the taxonomy of the product
    list_of_items = []
    map_file = pd.read_csv(input_csv_file)

    def start_requests(self):
        start_request_list = []
        for index, row in self.map_file.dropna(subset=[self.source_urls_col]).iterrows():
            taxonomy = row[self.taxonomy_col]
            source_url = row[self.source_urls_col]
            start_request_list.append(scrapy.Request(source_url, callback=self.parse, meta={'taxonomy': taxonomy}))
        return start_request_list


    def parse(self, response):

        all_items = response.css('div#products div.product-tuple-image a::attr(href)').extract()
        self.logger.info('All items for {} is {}'.format(response.meta['taxonomy'], len(all_items)))
        for item in all_items:
            taxonomy = response.meta['taxonomy']
            product_page_url = item
            yield scrapy.Request(product_page_url, callback=self.parse_product,
                                 meta={'product_page_url': product_page_url, 'taxonomy': taxonomy})

        # check if next page is available
        # next_page = response.css('a.next.ic.ic-right::attr(href)').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse, meta={'taxonomy': taxonomy})

    def parse_product(self, response):
        dict_of_items = {}
        dict_of_items['product_title'] = response.css('h1[itemprop=name]::text').extract_first().strip()
        product_price = response.css('span.pdp-final-price span[itemprop=price]::text').extract_first()
        dict_of_items['product_price'] = 'Rs.'+product_price
        product_image_url = response.css('ul#bx-slider-left-image-panel img::attr(src)').extract_first()
        dict_of_items['product_image_url'] = product_image_url
        product_highlights = response.css('div.p-keyfeatures.kf-below-name span.h-content::text').extract()
        for i in product_highlights:
            dict_of_items[i.split(":")[0]] = i.split(":")[1]

        image_file_name = product_image_url.split('/')[-1]
        file_path = response.meta['taxonomy'].replace("->",
                                                      "/") + "/" + self.source_urls_col + '/images/'+ image_file_name
        dict_of_items['file_path'] = file_path
        dict_of_items['product_page_url'] = response.meta['product_page_url']
        dict_of_items['taxonomy'] = response.meta['taxonomy']

        json_path = 'images/'+response.meta['taxonomy'].replace("->",
                                                      "/") + "/" + self.source_urls_col + '/'
        write_into_json(json_path,dict_of_items)

        yield SnapdealItem(image_url=product_image_url, image_name=image_file_name, image_path=file_path)

