import pandas as pd
import requests
import scrapy
import re
from ..Utils import write_into_json

from ..items import ZipkerItem

class Zipker(scrapy.Spider):
    name = "zipker_crawler"
    custom_settings = {
        'IMAGES_STORE': '',
        'ITEM_PIPELINES': {
            'Crawler.pipelines.ZipkerPipeline': 1
        }
    }

    source_urls_col = 'zipker'  # Column name having the source URL's in CSV file
    taxonomy_col = 'Taxonomy'  # Column name having the taxonomy of the product


    def __init__(self,input_csv_path="",*args, **kwargs):
        super(Zipker, self).__init__(*args, **kwargs)
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
        # gets list of product page urls from source url specified
        all_items_in_url = response.css('div#catalog-listing a.product-image::attr(href)').extract()
        self.logger.info('All items for {} is {}'.format(response.meta['taxonomy'], len(all_items_in_url)))
        for product_page_url in all_items_in_url:
            taxonomy = response.meta['taxonomy']
            yield scrapy.Request(product_page_url, callback=self.parse_product,
                                 meta={'product_page_url': product_page_url, 'taxonomy': taxonomy})

        #check if next page is available
        next_page = response.css('div.pages.dv-newzip-pager a.next.i-next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, meta={'taxonomy': taxonomy})

    def parse_product(self, response):
        # Parses each product page and retrieves product details
        product_details = {}
        product_details['product_title'] = response.css('div.product-mainp div.product-name.product_name_h1 span.h1::text').extract_first()
        product_details['product_price'] = re.sub("\s+"," ",response.css('div.product-mainp div.Product-price div.price-box span.price::text').extract_first())
        product_image_url = response.css('div.product-mainp div.box1 img::attr(src)').extract_first()
        product_details['product_image_url'] = product_image_url
        product_details['product_page_url'] = response.meta['product_page_url']

        product_specs = response.css('div.short-description.desc_pro div.std::text').extract()
        product_specs = [a for a in product_specs if a != '\n']
        product_specs = list(map(lambda x: x.strip("*\n"), product_specs))
        for spec in product_specs:
            spec_split = spec.split(":")
            if len(spec_split) > 1:
                product_details[spec_split[0]] = spec_split[1]
        product_details.pop('Note',None)

        image_file_name = product_image_url.split('/')[-1]
        temp_taxonomy = response.meta['taxonomy'].replace(" ", "_")
        file_path = 'atlas_dataset/' + temp_taxonomy.replace("->",
                                                             "-") + "/images/" + image_file_name
        product_details['taxonomy'] = response.meta['taxonomy']
        product_details['file_path'] = file_path

        # Writes product page details into json file called data.json
        json_path = '/home/et/Desktop/Atlas/dataset/atlas_dataset/' + temp_taxonomy.replace("->",
                                                                                            "-") + "/"
        write_into_json(json_path,product_details)

        yield ZipkerItem(image_url=product_image_url, image_name=image_file_name, image_path=file_path)

