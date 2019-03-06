import pandas as pd
import requests
import scrapy
from tqdm import tqdm
import re

from ..Utils import write_into_json
from ..items import CraftsvillaItem


class CraftsVillaFashion(scrapy.Spider):
    name = "craftsvilla_crawler"
    custom_settings = {
        'IMAGES_STORE': '/home/et/Desktop/Atlas/dataset/',
        'ITEM_PIPELINES': {
            'Crawler.pipelines.CraftsvillaPipeline': 1
        }
    }
    source_urls_col = 'Craftsvilla'  # Column name having the source URL's in CSV file
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
        all_items = response.css('div.col-xs-6.col-sm-3.product-box a.product-image::attr(href)').extract()
        self.logger.info('All items for {} is {}'.format(response.meta['taxonomy'], len(all_items)))
        for item in all_items:
            taxonomy = response.meta['taxonomy']
            product_page_url = 'https://www.craftsvilla.com'+ item
            yield scrapy.Request(product_page_url, callback=self.parse_product,
                                 meta={'product_page_url': product_page_url, 'taxonomy': taxonomy})


        # check if next page is available
        base_product_url = response._url.split('/?')[0]
        input_tag_data = response.xpath('//input[@id=$val]', val='feedid').extract_first()
        feed_id_selector = scrapy.Selector(text=input_tag_data)
        feed_id = feed_id_selector.xpath('//input/@*').extract()[-1]
        page_data = response.css('a.paginate').extract()
        if len(page_data) > 1:
            page_data = page_data[1]
            next_page_id = page_data[page_data.find(">") + 1: page_data.find("</")]
            if next_page_id and feed_id:
                next_page = "{}/?pageId={}&feedId={}".format(base_product_url, next_page_id, feed_id)
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse, meta={'taxonomy': taxonomy})


    def parse_product(self, response):
        dict_of_items = {}
        dict_of_items['product_title'] = re.sub('\s+',' ',response.css('div.col-xs-12.col-sm-6 h1::text').extract_first())
        dict_of_items['product_price'] = response.css('div.col-xs-12.col-sm-6 div.pdp-price-offer sup::text').extract_first()+ response.css('div.col-xs-12.col-sm-6 div.pdp-price-offer span::text').extract_first()
        product_image_url = response.css('div.pdp-thumb-viewer img::attr(src)').extract_first()
        dict_of_items['product_image_url'] = product_image_url
        detail_header = response.css('div#product-specification div.col-xs-12.col-sm-4 li span::text').extract()
        detail_body = response.css('div#product-specification div.col-xs-12.col-sm-4 li::text').extract()
        detail_body = [w.replace(':', '') for w in detail_body]
        for detail_header, detail_body in zip(detail_header, detail_body):
            dict_of_items[detail_header] = detail_body
        dict_of_items['product_description'] = re.sub('\s+',' ',''.join(response.css('div#product-specification div.col-xs-12.nopadding p.show-read-more::text').extract()))
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

        yield CraftsvillaItem(image_url=product_image_url, image_name=image_file_name, image_path=file_path)

