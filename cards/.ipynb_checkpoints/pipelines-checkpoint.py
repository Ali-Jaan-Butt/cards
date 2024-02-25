# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class CardsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['url'] = 'https://www.hareruyamtg.com'+adapter['url'].strip()
        adapter['name'] = adapter['name'].strip() # Name
        # value = adapter['name'].strip()
        # name = re.search('《(.+?)》',value) # Name
        # Set = re.search('\[(.+?)\]',value) # Set
        stock = re.search(':(.+?)】',adapter['stock']) # Stock
        # adapter['name'] = name.group(1) if name is not None else None
        # adapter['Set'] = Set.group(1) if Set is not None else None
        adapter['price'] = adapter['price'].replace('¥ ','')
        adapter['stock'] = stock.group(1) if stock is not None else None
        return item

class CardsPipeline2:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['url'] = 'https://www.cardkingdom.com'+adapter['url']
        # value = adapter['name'].split(': ')
        # adapter['Set'] = value[0] # Set
        # adapter['name'] = value[1] # Name
        adapter['price'] = adapter['price'].replace('$','')
        return item

class TcgplayersPipeline:
    def process_item(self, item, spider):
        return item

class TcgplayersPipeline1:
    def process_item(self, item, spider):
        return item