# -*- coding: utf-8 -*-

import scrapy
import hashlib
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class AmazonPipeline(ImagesPipeline):
    # Name thumbnail version
    def thumb_path(self, request, thumb_id, response=None, info=None):
        image_guid = thumb_id + response.url.split('/')[-1]
        return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)

    def file_path(self, request, response=None, info=None):
        return 'Amazon/' + request.meta.get('filename', '')

    def get_media_requests(self, item, info):
        meta = {'filename': item['image_paths']}
        for image_url in item['image_urls']:
            yield scrapy.Request(url=image_url, meta=meta)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
            item['image_paths'] = image_paths
            return item

class BollywoodkartPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['image_path']

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_url'], meta=item)


class CraftsvillaPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['image_path']

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_url'], meta=item)


class FlipkartPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        try:
            image_path = request.meta['page_url']
            image_guid = 'Flipkart/' + image_path[0] + '/' + hashlib.sha1(
                request.url.encode('utf-8')).hexdigest() + '.jpg'
            return image_guid
        except Exception as e:
            print("Exception during crawling images: " + e)

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_urls'][0], meta=item)


class IndianClothStorePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['image_path']

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_url'], meta=item)


class IndiaEmporiumPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['image_path']

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_url'], meta=item)

class IndiaRushPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['image_path']

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_url'], meta=item)

class MirrawPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['image_path']

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_url'], meta=item)

class SnapdealPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['image_path']

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_url'], meta=item)


class UtsavFashionPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['image_path']

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_url'], meta=item)


class VoonikPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['image_path']

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_url'], meta=item)


class ZipkerPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['image_path']

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_url'], meta=item)
