import pandas as pd
import requests
import scrapy
from tqdm import tqdm
import re

from ..items import MirrawItem
from ..Utils import write_into_json

class MirrawFashion(scrapy.Spider):
    name = "mirraw_crawler"
    custom_settings = {
        'IMAGES_STORE': '/home/et/Desktop/Atlas/dataset/',
        'ITEM_PIPELINES': {
            'Crawler.pipelines.MirrawPipeline': 1
        }
    }

    source_urls_col = 'Mirraw'  # Column name having the source URL's in CSV file
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
        all_items = response.css('span[itemprop=mainEntity] li[itemprop = itemListElement] p.listing-title.row a::attr(href)').extract()
        self.logger.info('All items for {} is {}'.format(response.meta['taxonomy'], len(all_items)))
        for item in all_items:
            taxonomy = response.meta['taxonomy']
            product_page_url = 'https://www.mirraw.com'+ item
            yield scrapy.Request(product_page_url, callback=self.parse_product,
                                 meta={'product_page_url': product_page_url, 'taxonomy': taxonomy})

        # check if next page is available
        url_split = response._url.split('?page=')
        base_product_url = url_split[0]
        if len(url_split) == 1:
            prev_page_number = 1
        else:
            prev_page_number = int(url_split[1].split('&')[0])
        response_selector = scrapy.Selector(response)
        api_result = response_selector.xpath('//h1[@class="text-center"]/text()').extract_first()
        if api_result is None:
            page_number = prev_page_number + 1
            next_page = "{}?page={}&more_designs=true".format(base_product_url, str(page_number))
            yield response.follow(next_page, callback=self.parse, meta={'taxonomy': response.meta['taxonomy']})

    def parse_product(self, response):
        dict_of_items = {}
        temp_product_title = response.css('h1#design_title::text').extract_first()
        if not temp_product_title:
            temp_product_title = response.css('div.listing_panel_block::text').extract()
            temp_product_title = re.sub('\s+', ' ', temp_product_title[1])

        dict_of_items['product_title'] = temp_product_title
        product_price = response.css('h3.floatl.new_price_label::text').extract_first()
        if not product_price:
            product_price = re.sub('\s+', ' ',response.css('div.product_discount_price.left::text').extract_first())
        dict_of_items['product_price'] = product_price
        product_image_url = response.css('img#master::attr(src)').extract_first()
        if not product_image_url:
            product_image_url = response.css('img#myImg::attr(src)').extract_first()
        dict_of_items['product_image_url'] = product_image_url
        list_of_specs = response.css('div.key_specifications table td::text').extract()
        list_of_specs = list(filter((':').__ne__, list_of_specs))
        list_of_specs = list(filter(('•').__ne__, list_of_specs))

        if not list_of_specs:
            detail_header = response.css('div#design_description p::text').extract_first()
            if detail_header:
                detail_header = re.sub("\s+", " ", detail_header)
                detail_body = response.css('table#one td::text').extract_first()
                dict_of_items[detail_header] = detail_body

                blocks = response.xpath('//table[@class="sub-specs-table"]')
                if blocks:
                    for sub_block in blocks:
                        sub_block_title = sub_block.css('table::attr(id)').extract_first()
                        for row in sub_block.xpath('tr'):
                            row_title = row.xpath('td[2]/text()').extract_first()
                            row_value = row.xpath('td[4]/text()').extract_first()
                            dict_of_items[sub_block_title + '_' + row_title] = row_value
                else:
                    list_of_specs = response.css('div.specifications-table table.sub-specs-line td::text').extract()
                    clean_list_of_specs = str.maketrans('', '', '•:')
                    list_of_specs = [s.translate(clean_list_of_specs) for s in list_of_specs]
                    list_of_specs = list(filter(None, list_of_specs))
                    for i in range(0, len(list_of_specs) - 1, 2):
                        dict_of_items[list_of_specs[i]] = list_of_specs[i + 1]
            else:
                list_of_specs = response.css('div#specs div#spec-1 table.table.table-bordered.product_specif_detail tr td::text').extract()
                list_of_specs.remove('Other Details')


        if list_of_specs:
            for i in range(0, len(list_of_specs) - 1, 2):
                dict_of_items[list_of_specs[i]] = list_of_specs[i + 1]

        image_file_name = product_image_url.split('/')[-1]
        temp_taxonomy = response.meta['taxonomy'].replace(" ", "_")
        file_path = 'atlas_dataset/' + temp_taxonomy.replace("->",
                                                             "-") + "/images/" + image_file_name
        dict_of_items['taxonomy'] = response.meta['taxonomy']
        dict_of_items['file_path'] = file_path
        json_path = '/home/et/Desktop/Atlas/dataset/atlas_dataset/' + temp_taxonomy.replace("->",
                                                                                            "-") + "/"
        write_into_json(json_path,dict_of_items)

        yield MirrawItem(image_url=product_image_url, image_name=image_file_name, image_path=file_path)

