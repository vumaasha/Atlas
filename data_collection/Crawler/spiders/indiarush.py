import pandas as pd
import requests
import scrapy
import re
from ..Utils import write_into_json
from ..items import IndiaRushItem

class IndiaRush(scrapy.Spider):
    name = "indiarush_crawler"
    custom_settings = {
        'IMAGES_STORE': '',
        'ITEM_PIPELINES': {
            'Crawler.pipelines.IndiaRushPipeline': 1
        }
    }

    source_urls_col = 'indiarush'  # Column name having the source URL's in CSV file
    taxonomy_col = 'Taxonomy'  # Column name having the taxonomy of the product

    def __init__(self,input_csv_path="",*args, **kwargs):
        super(IndiaRush, self).__init__(*args, **kwargs)
        self.input_csv_path = input_csv_path

    def start_requests(self):
        map_file = pd.read_csv(self.input_csv_path)
        start_request_list = []
        for index, row in map_file.dropna(subset=[self.source_urls_col]).iterrows():
            taxonomy = row[self.taxonomy_col]
            source_url = row[self.source_urls_col]
            start_request_list.append(scrapy.Request(source_url, callback=self.parse, meta={'taxonomy': taxonomy}))
        return start_request_list

    def parse(self, response):
        #gets list of product page urls from source url specified
        all_items_in_url = response.css('div.category-products a.product-image.product-page-click-category::attr(href)').extract()
        self.logger.info('All items for {} is {}'.format(response.meta['taxonomy'], len(all_items_in_url)))
        for product_page_url in all_items_in_url:
            taxonomy = response.meta['taxonomy']
            yield scrapy.Request(product_page_url, callback=self.parse_product,
                                 meta={'product_page_url': product_page_url, 'taxonomy': taxonomy})

        # check if next page is available
        next_page = response.xpath('//a[@title = $val]/@href', val='Next').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, meta={'taxonomy': taxonomy})

    def parse_product(self, response):
        #Parses each product page and retrieves product details
        product_details = {}
        product_details['product_title'] = response.css('div.product-shop h1::text').extract_first()
        product_details['product_price'] = re.sub('\s+','',response.css('div.product-prices-wrapper span#regular_price_id::text').extract_first())
        product_image_url = response.css('div#slider-image-brick img::attr(src)').extract_first()
        product_details['product_image_url'] = product_image_url
        product_details['product_page_url'] = response.meta['product_page_url']
        product_specs_list = response.css('div#detail-left p::text').extract()
        for i in range(0, len(product_specs_list) - 1, 2):
            product_details[re.sub(':', ' ', product_specs_list[i])] = product_specs_list[i+1]
        image_file_name = product_image_url.split('/')[-1]
        temp_taxonomy = response.meta['taxonomy'].replace(" ","_")
        file_path = 'atlas_dataset/'+temp_taxonomy.replace("->",
                                                      "-") + "/images/" + image_file_name
        product_details['file_path'] = file_path
        product_details['taxonomy'] = response.meta['taxonomy']

        #Writes product page details into json file called data.json
        json_path = self.settings.get('IMAGES_STORE')+'atlas_dataset/'+temp_taxonomy.replace("->",
                                                      "-") + "/"
        write_into_json(json_path,product_details)

        yield IndiaRushItem(image_url=product_image_url, image_name=image_file_name, image_path=file_path)

