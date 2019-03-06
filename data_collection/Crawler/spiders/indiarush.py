import pandas as pd
import requests
import scrapy
from tqdm import tqdm
import re
from ..Utils import write_into_json
from ..items import IndiaRushItem

class IndiaRush(scrapy.Spider):
    name = "indiarush_crawler"
    custom_settings = {
        'IMAGES_STORE': '/home/et/Desktop/Atlas/dataset/',
        'ITEM_PIPELINES': {
            'Crawler.pipelines.IndiaRushPipeline': 1
        }
    }


    source_urls_col = 'IndiaRush'  # Column name having the source URL's in CSV file
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
        all_items = response.css('div.category-products a.product-image.product-page-click-category::attr(href)').extract()
        self.logger.info('All items for {} is {}'.format(response.meta['taxonomy'], len(all_items)))
        for product_page_url in all_items:
            taxonomy = response.meta['taxonomy']
            yield scrapy.Request(product_page_url, callback=self.parse_product,
                                 meta={'product_page_url': product_page_url, 'taxonomy': taxonomy})

        # check if next page is available
        next_page = response.xpath('//a[@title = $val]/@href', val='Next').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, meta={'taxonomy': taxonomy})

    def parse_product(self, response):
        dict_of_items = {}
        dict_of_items['product_title'] = response.css('div.product-shop h1::text').extract_first()
        dict_of_items['product_price'] = re.sub('\s+','',response.css('div.product-prices-wrapper span#regular_price_id::text').extract_first())
        product_image_url = response.css('div#slider-image-brick img::attr(src)').extract_first()
        dict_of_items['product_image_url'] = product_image_url
        dict_of_items['product_page_url'] = response.meta['product_page_url']
        list_of_specs = response.css('div#detail-left p::text').extract()
        for i in range(0, len(list_of_specs) - 1, 2):
            dict_of_items[re.sub(':', ' ', list_of_specs[i])] = list_of_specs[i+1]
        image_file_name = product_image_url.split('/')[-1]
        temp_taxonomy = response.meta['taxonomy'].replace(" ","_")
        file_path = 'atlas_dataset/'+temp_taxonomy.replace("->",
                                                      "-") + "/images/" + image_file_name
        dict_of_items['file_path'] = file_path
        dict_of_items['taxonomy'] = response.meta['taxonomy']

        json_path = '/home/et/Desktop/Atlas/dataset/atlas_dataset/'+temp_taxonomy.replace("->",
                                                      "-") + "/"
        write_into_json(json_path,dict_of_items)

        yield IndiaRushItem(image_url=product_image_url, image_name=image_file_name, image_path=file_path)

