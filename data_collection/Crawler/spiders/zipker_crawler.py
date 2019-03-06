import pandas as pd
import requests
import scrapy
from tqdm import tqdm
import re
from ..Utils import write_into_json

from ..items import ZipkerItem

class Zipker(scrapy.Spider):
    name = "zipker_crawler"
    custom_settings = {
        'IMAGES_STORE': '/home/et/Desktop/Atlas/dataset/',
        'ITEM_PIPELINES': {
            'Crawler.pipelines.ZipkerPipeline': 1
        }
    }

    source_urls_col = 'Zipker'  # Column name having the source URL's in CSV file
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
        all_items = response.css('div#catalog-listing a.product-image::attr(href)').extract()
        self.logger.info('All items for {} is {}'.format(response.meta['taxonomy'], len(all_items)))
        for product_page_url in all_items:
            taxonomy = response.meta['taxonomy']
            yield scrapy.Request(product_page_url, callback=self.parse_product,
                                 meta={'product_page_url': product_page_url, 'taxonomy': taxonomy})

        #check if next page is available
        next_page = response.css('div.pages.dv-newzip-pager a.next.i-next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, meta={'taxonomy': taxonomy})

    def parse_product(self, response):
        dict_of_items = {}
        dict_of_items['product_title'] = response.css('div.product-mainp div.product-name.product_name_h1 span.h1::text').extract_first()
        dict_of_items['product_price'] = re.sub("\s+"," ",response.css('div.product-mainp div.Product-price div.price-box span.price::text').extract_first())
        product_image_url = response.css('div.product-mainp div.box1 img::attr(src)').extract_first()
        dict_of_items['product_image_url'] = product_image_url

        product_specs = response.css('div.short-description.desc_pro div.std::text').extract()
        product_specs = [a for a in product_specs if a != '\n']
        product_specs = list(map(lambda x: x.strip("*\n"), product_specs))
        for spec in product_specs:
            spec_split = spec.split(":")
            if len(spec_split) > 1:
                dict_of_items[spec_split[0]] = spec_split[1]
        dict_of_items.pop('Note',None)

        image_file_name = product_image_url.split('/')[-1]
        temp_taxonomy = response.meta['taxonomy'].replace(" ", "_")
        file_path = 'atlas_dataset/' + temp_taxonomy.replace("->",
                                                             "-") + "/images/" + image_file_name
        dict_of_items['taxonomy'] = response.meta['taxonomy']
        dict_of_items['file_path'] = file_path
        json_path = '/home/et/Desktop/Atlas/dataset/atlas_dataset/' + temp_taxonomy.replace("->",
                                                                                            "-") + "/"
        write_into_json(json_path,dict_of_items)

        yield ZipkerItem(image_url=product_image_url, image_name=image_file_name, image_path=file_path)

