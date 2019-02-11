import pandas as pd
import requests
import scrapy
from tqdm import tqdm
import re

from ..Utils import write_into_json
from ..items import BollywoodKartItem

class BollywoodKart(scrapy.Spider):
    name = "bollywoodkart_crawler"
    custom_settings = {
        'ITEM_PIPELINES': {
            'Crawler.pipelines.BollywoodKartPipeline': 1
        }
    }

    input_csv_file = 'IndianClothesWomen.csv'  # csv file containing the taxonomy and website source URL's
    source_urls_col = 'BollywoodKart'  # Column name having the source URL's in CSV file
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
        all_items = response.css('div.category-products li.item a.product-image::attr(href)').extract()
        self.logger.info('All items for {} is {}'.format(response.meta['taxonomy'], len(all_items)))
        for product_page_url in all_items:
            taxonomy = response.meta['taxonomy']
            yield scrapy.Request(product_page_url, callback=self.parse_product,
                                 meta={'product_page_url': product_page_url, 'taxonomy': taxonomy})

        next_page = response.css('div.pages a[title=Next]::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, meta={'taxonomy': taxonomy})

    def parse_product(self, response):
        dict_of_items = {}
        dict_of_items['product_title'] = response.css('div.product-shop div.product-name h1::text').extract_first()
        dict_of_items['product_price'] = response.css('div.price-info div.price-box span.price::text').extract_first()
        product_image_url = response.css('div.product-img-box div.product-image-gallery img#image-main::attr(src)').extract_first()
        dict_of_items['product_image_url'] = product_image_url
        dict_of_items['Product Details'] = response.css('div.product_info div.std p::text').extract_first()
        detail_header = response.css('div.product_info div.tab-content table#product-attribute-specs-table th.label::text').extract()
        detail_body =  response.css('div.product_info div.tab-content table#product-attribute-specs-table td.data::text').extract()
        for head, body in zip(detail_header,detail_body):
            dict_of_items[head] =body

        image_file_name = product_image_url.split('/')[-1]
        file_path = response.meta['taxonomy'].replace("->",
                                                      "/") + "/" + self.source_urls_col + "/images/" + image_file_name
        dict_of_items['taxonomy'] = response.meta['taxonomy']
        dict_of_items['file_path'] = file_path
        json_path = 'images/' + response.meta['taxonomy'].replace("->",
                                                                  "/") + "/" + self.source_urls_col + '/'
        write_into_json(json_path, dict_of_items)

        yield BollywoodKartItem(image_url=product_image_url, image_name=image_file_name, image_path=file_path)

