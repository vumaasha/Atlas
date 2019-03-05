# -*- coding: utf-8 -*-
import scrapy
import hashlib
import csv
import os.path
from ..Utils import ipReader
from ..items import AmazonItem

amazonReader = ipReader()


# Class to write extracted dataSet details into csv
class csvWriter():
    def initiate(self, path):
        filePath = "dataSet/Amazon/amazon_" + path.lower() + ".csv"
        if not os.path.exists(os.path.dirname("dataSet/Amazon/")):
            os.makedirs(os.path.dirname("dataSet/Amazon/"))
        if not os.path.isfile(filePath):
            with open(filePath, 'w') as csvfile:
                self.fieldname = ['Id', 'Name', 'ProductId', 'ImageUrl', 'ProductUrl', 'Review', 'Cost', 'Category',
                                  'ImagePath']
                self.writer = csv.DictWriter(csvfile, fieldnames=self.fieldname)
                self.writer.writeheader()

    def write(self, pId, name, p_id, imgUrl, pUrl, review, cost, cat, imgPath):
        filePath = "dataSet/Amazon/amazon_" + cat + ".csv"
        with open(filePath, 'a') as csvfile:
            self.fieldname = ['Id', 'Name', 'ProductId', 'ImageUrl', 'ProductUrl', 'Review', 'Cost', 'Category',
                              'ImagePath']
            self.writer = csv.DictWriter(csvfile, fieldnames=self.fieldname)
            self.writer.writerow(
                {'Id': pId, 'Name': name, 'ProductId': p_id, 'ImageUrl': imgUrl, 'ProductUrl': pUrl, 'Review': review,
                 'Cost': cost, 'Category': cat, 'ImagePath': imgPath})


csvObj = csvWriter()


# Main scrapy class
class AmazoncrawlerSpider(scrapy.Spider):
    name = 'AmazonCrawler'
    custom_settings = {
        'ITEM_PIPELINES': {
            'Crawler.pipelines.AmazonPipeline': 1
        }
    }

    # Function that finds the page number for consecutive searching
    def findBetween(self, s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    amazonReader.readFile('Amazon_Map.csv')
    start_urls = amazonReader.url_list

    def parse(self, response):
        category = response.css('h4.a-size-small.a-color-base.a-text-bold::text').extract_first()
        category = category.replace("\n", "")
        category = category.replace(" ", "")
        superCat = ""
        for superCategory in response.css('li.s-ref-indent-neg-micro'):
            catName = superCategory.css('span.a-size-small.a-color-base::text').extract_first()
            superCat += catName + ":"
        superCat = superCat.replace("\n", "")
        superCat = superCat.replace(" ", "")
        wholeCat = superCat + category  # Used for mapping the extracted title to the available category title
        csvObj.initiate(amazonReader.category_title[wholeCat])

        for product in response.css('li.s-result-item'):
            image_url = product.css('img.s-access-image.cfMarker::attr(src)').extract_first()
            hashObj = hashlib.sha1(image_url.encode('utf-8'))
            hashDig = hashObj.hexdigest()
            image_path = amazonReader.category_path[wholeCat].replace(">", "/") + "/" + hashDig + ".jpg"
            if image_url:
                yield AmazonItem(image_urls=[image_url], image_paths=str(image_path))
            id = product.css('li::attr(id)').extract_first()
            if id:
                id = int(id.replace("result_", "")) + 1
            p_id = product.css('li::attr(data-asin)').extract_first()
            p_name = product.css('h2.a-size-base.s-inline.s-access-title.a-text-normal::text').extract_first()
            p_url = product.css(
                'a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal::attr(href)').extract_first()
            p_review = product.css(
                'div.s-item-container div.a-spacing-none div.a-spacing-top-mini span span.a-declarative a.a-popover-trigger i.a-icon span.a-icon-alt::text').extract_first()
            p_cost = product.css('span.a-size-base.a-color-price.s-price.a-text-bold::text').extract_first()
            if p_cost:
                p_cost = p_cost.replace("-", "")
                p_cost = p_cost.replace(" ", "")
            csvObj.write(id, p_name, p_id, image_url, p_url, p_review, p_cost, amazonReader.category_title[wholeCat],
                         image_path)
            image_url = product.css(
                'div.s-hidden a.a-link-normal.a-text-normal div::attr(data-search-image-source)').extract_first()
            if image_url:
                hashObj = hashlib.sha1(image_url.encode('utf-8'))
                hashDig = hashObj.hexdigest()
                image_path = amazonReader.category_path[wholeCat].replace(">", "/") + "/" + hashDig + ".jpg"
                yield AmazonItem(image_urls=[image_url], image_paths=str(image_path))
                csvObj.write(id, p_name, p_id, image_url, p_url, p_review, p_cost,
                             amazonReader.category_title[wholeCat], image_path)

        next_page = response.css('a.pagnNext::attr(href)').extract_first()
        curPg = int(self.findBetween(next_page, "page=", "&rh="))
        if curPg <= 100:
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
