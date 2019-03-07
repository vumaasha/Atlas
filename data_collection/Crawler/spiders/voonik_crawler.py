import pandas as pd
import requests
import scrapy
from tqdm import tqdm
import re
from ..Utils import write_into_json
from ..items import VoonikItem

class Voonik(scrapy.Spider):
    name = "voonik_crawler"
    custom_settings = {
        'IMAGES_STORE': '/home/et/Desktop/Atlas/dataset/',
        'ITEM_PIPELINES': {
            'Crawler.pipelines.VoonikPipeline': 1
        }
    }

    source_urls_col = 'Voonik'  # Column name having the source URL's in CSV file
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

        all_items = []
        total = response.css('div.flex.feed-item-title span::text').extract()
        total_products = [num for num in total if num.isdigit()]
        total_products = int(total_products[0])

        page_limit = int(total_products/24) + 1
        pages = list(range(1,page_limit))
        for p in pages:
            headers = {'USER-AGENT': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
            URL = response.request.url+".json?limit=24&page={}".format(p)
            r = requests.get(url=URL,headers=headers)
            data = r.json()
            for i in range(0, 24):
                all_items.append('https://www.voonik.com/recommendations/' + data['results'][i]['permalink'])
        self.logger.info('All items for {} is {}'.format(response.meta['taxonomy'], len(all_items)))

        for item in all_items:
            taxonomy = response.meta['taxonomy']
            # product_page_url = 'https://www.voonik.com'+ item
            product_page_url = item
            yield scrapy.Request(product_page_url, callback=self.parse_product,
                                 meta={'product_page_url': product_page_url, 'taxonomy': taxonomy})

    def parse_product(self, response):
        dict_of_items = {}
        dict_of_items['product_title'] = response.css('div.pdp-det-box h1::text').extract_first()
        dict_of_items['product_price'] = response.css('h2.primo_unsubcribed span::text').extract_first()
        product_image_url = 'https://'+response.css('img#pdpMainImage::attr(src)').extract_first().lstrip('//')
        dict_of_items['product_image_url'] = product_image_url
        dict_of_items['product_page_url'] = response.meta['product_page_url']
        list_of_specs_head = response.css('ul.list-unstyled div.property::text').extract()
        list_of_specs_body =  response.css('ul.list-unstyled div.value::text').extract()
        temp = response.css('ul.list-unstyled div.value a::text').extract()
        for i in range(0,len(temp)):
            list_of_specs_body.insert(i+1, temp[i])
        for head,body in zip(list_of_specs_head,list_of_specs_body):
            dict_of_items[head] = body
        image_file_name = product_image_url.split('/')[-1]
        dict_of_items['taxonomy'] = response.meta['taxonomy']
        temp_taxonomy = response.meta['taxonomy'].replace(" ", "_")
        file_path = 'atlas_dataset/' + temp_taxonomy.replace("->",
                                                             "-") + "/images/" + image_file_name

        dict_of_items['file_path'] = file_path
        json_path = '/home/et/Desktop/Atlas/dataset/atlas_dataset/' + temp_taxonomy.replace("->",
                                                                                            "-") + "/"
        write_into_json(json_path,dict_of_items)

        yield VoonikItem(image_url=product_image_url, image_name=image_file_name, image_path=file_path)

