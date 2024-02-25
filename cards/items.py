# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CardsItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    #Set = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    pass
    
class CardsItem2(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    #Set = scrapy.Field()
    price = scrapy.Field()
    pass

class TcgplayersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()
    set_name = scrapy.Field()
    product_name = scrapy.Field()
    set_code = scrapy.Field()
    # buy_list_market_price = scrapy.Field()
    url = scrapy.Field()
    pass

class TcgplayersItem1(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # set_name = scrapy.Field()
    # product_name = scrapy.Field()
    # set_code = scrapy.Field()
    ID = scrapy.Field()
    buy_list_market_price = scrapy.Field()
    # url = scrapy.Field()
    pass