import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath('Utils.py'))))
from Utils import write_into_json
import selenium as se
import urllib.request
from selenium import webdriver
import pandas as pd
from tqdm import tqdm
import os
from selenium.common.exceptions import NoSuchElementException

class MyntraFashion:
    def __init__(self):
        self.input_csv_file = 'dataset.csv'  # csv file containing the taxonomy and website source URL's
        self.source_urls_col = 'Myntra'  # Column name having the source URL's in CSV file
        self.taxonomy_col = 'Taxonomy'  # Column name having the taxonomy of the product
        self.map_file = pd.read_csv(self.input_csv_file)
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = se.webdriver.Chrome(chrome_options=options)
#         print("Constructor done")

    def start_requests(self):
        start_request_list = []
        taxonomy_list = []
        for index, row in self.map_file.dropna(subset=[self.source_urls_col]).iterrows():
            taxonomy = row[self.taxonomy_col]
            source_url = row[self.source_urls_col]
            start_request_list.append(source_url)
            taxonomy_list.append(taxonomy)
#             print("Control moving to Parse_items")
        self.parse_items(start_request_list, taxonomy_list)

    def parse_items(self,source_url_list, taxonomy_list):
        try:

            urls = []
            # Each Category URL
            for url,tax in zip(source_url_list,taxonomy_list):
                self.driver.get(url)
#                 print("Moving to next page")
                count = 0
                # nextpage navigation
                while True:
                    try:
                        count = count + 1
                        print("Count"+str(count))
                        if count > 10:
                            break
                        else:
                            next = self.driver.find_element_by_class_name("results-showmore")
                    except NoSuchElementException:
                        break
                    next.click()
                    print("Clicked next")
                    self.driver.implicitly_wait(10)
                    print("Waiting")

                print("Gathering all_items")
                p_element = self.driver.find_elements_by_css_selector(".results-base li.product-base a")
                for e in p_element:
                    print("Getting product URLS")
                    # Gets product urls
                    urls.append(e.get_attribute("href"))

                urls = list(set(urls))
                f = len(urls)
                for each in tqdm(urls):
                    print("Processing URL:"+each)
                    self.parse_product(each,tax)
        except Exception as e:
            # print("Unable to retreive product details"+p_element)
            print("Error in parse_items due to"+str(e))

    def parse_product(self,each_url,taxonomy):
        try:

            dict_of_items = {}
            self.driver.get(each_url)

            web_image_url = self.driver.find_elements_by_css_selector(".image-grid-imageContainer div.image-grid-image")[0]
            web_image_url = web_image_url.get_attribute("style")
            web_image_url = web_image_url.split('url("')[1]
            web_image_url = web_image_url.split('"')[0]
            dict_of_items['product_image_url'] = web_image_url

            file_path = taxonomy.replace("->","/") + "/" + self.source_urls_col + "/images/"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            image_name = file_path + web_image_url.split('-')[1]
            dict_of_items['file_path'] = image_name
            urllib.request.urlretrieve(web_image_url, image_name)

            dict_of_items['product_page_url'] = each_url
            dict_of_items['product_price'] = self.driver.find_elements_by_css_selector(".pdp-discount-container strong.pdp-price")[0].text
            dict_of_items['product_title'] = self.driver.find_elements_by_css_selector(".pdp-price-info h1.pdp-title")[0].text + self.driver.find_elements_by_css_selector(".pdp-price-info h1.pdp-name")[0].text
            dict_of_items['taxonomy'] = taxonomy
            dict_of_items['product_description'] = self.driver.find_elements_by_css_selector(".pdp-product-description-content")[0].text
            json_path = taxonomy.replace("->","/") + "/" + self.source_urls_col + '/'
            write_into_json(json_path, dict_of_items)

        except Exception as e:
            print("Unable to crawl for "+each_url)
            print("Reason: "+str(e))

if __name__ == '__main__':
  mf = MyntraFashion()
  mf.start_requests()
