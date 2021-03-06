import scrapy
import json
import re
import csv
import requests
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

import pdb
from lxml import html

class Hendrickauto(scrapy.Spider):
    name = "hendrickauto"

    domain = "http://www.85cbakerycafe.com"
    start_urls = ["http://www.85cbakerycafe.com/wp-admin/admin-ajax.php?action=store_search&lat=33.6881056&lng=-117.8339795&max_results=25&radius=50&autoload=1"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = store['lat']
            item['longitude'] = store['lng']
            item['store_name'] = store['store']
            item['other_fields'] = ""
            if item['store_name'].find('(Baking Soon!)') != -1:
                item['store_name'] = item['store_name'].replace('(Baking Soon!)', '')
                item['coming_soon'] = "1"
            else:
                item['coming_soon'] = "0"
            item['address'] = store['address']
            item['address2'] = store['address2']
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['zip']
            item['phone_number'] =  store['phone']

            item['store_hours'] = store['description'].replace('<p>', '').replace('</p>', '').replace('<br />', '').replace('&#8211;', '-').replace('\n', '; ').replace('<span>', '').replace('</span>', '').replace('<b>', '').replace('</b>', '').replace('<!--; <p class="p1">', '').replace('Soft Opening Hours 10AM - 8PM daily until Dec. 29; ; -->', '').strip()
      
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

