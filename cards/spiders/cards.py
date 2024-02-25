import scrapy
from cards.items import CardsItem
from cards.items import CardsItem2
from cards.items import TcgplayersItem
from cards.items import TcgplayersItem1
from math import ceil
import pandas as pd

class HareruyamtgSpider(scrapy.Spider):
    name = "hareruyamtg"
    allowed_domains = ["www.hareruyamtg.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'cards.pipelines.CardsPipeline': 100,
        },
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'hareruyamtg_single_cards_normal_jp_in_stock.csv'
    }
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    start_urls = ["https://www.hareruyamtg.com/en/products/search?product=&category=1&cardset=&colorsType=0&cardtypesType=0&subtype=&format=&illustrator=&foilFlg%5B%5D=0&language%5B%5D=1&stock=1&search=%E6%A4%9C%E7%B4%A2"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)
    
    def parse(self, response):
        pages_count = int(response.xpath('//span[@class="navipage_last_"]/a/@href').extract_first().split('page=')[-1])
        for i in range(1,pages_count+1):
            yield response.follow('https://www.hareruyamtg.com/en/products/search?product=&category=1&cardset=&colorsType=0&cardtypesType=0&subtype=&format=&illustrator=&foilFlg%5B%5D=0&language%5B%5D=1&stock=1&search=%E6%A4%9C%E7%B4%A2&page='+str(i), headers=self.headers, callback=self.parse_card)

    def parse_card(self, response):
        # Your scraping logic for individual product pages
        for row in response.xpath('//ul[@class="itemListLine itemListLine--searched"]/li'):
            card = CardsItem()
            card['url'] = row.xpath('.//a[@class="itemName"]/@href').extract_first() # Card Url
            card['name'] = row.xpath('.//a[@class="itemName"]/text()').extract_first() # Card Name
            card['price'] = row.xpath('.//p[@class="itemDetail__price"]/text()').extract_first() # Price
            card['stock'] = row.xpath('.//p[@class="itemDetail__stock"]/text()').extract_first() # Stock
            yield card

class CardkingdomSpider(scrapy.Spider):
    name = "cardkingdom"
    allowed_domains = ["www.cardkingdom.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            "cards.pipelines.CardsPipeline2": 100,
        },
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'cardkingdom_mtg_singles_usd.csv'
    }
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Cookie':'limit=100'}
    start_urls = ["https://www.cardkingdom.com/purchasing/mtg_singles?filter%5Bsort%5D=price_desc&filter%5Bsearch%5D=mtg_advanced&filter%5Bname%5D=&filter%5Bedition%5D=&filter%5Bformat%5D=&filter%5Bsingles%5D=1&filter%5Bprice_op%5D=&filter%5Bprice%5D="]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)
    
    def parse(self, response):
        per_page = int(response.xpath('//div[@class="resultsCount bottom-nav-col"]/text()').extract_first().split('of')[0].split()[-1])
        total = int(response.xpath('//div[@class="resultsCount bottom-nav-col"]/text()').extract_first().split('of')[1].split()[0])
        pages_count = ceil(total/per_page)
        for i in range(1,pages_count+1):
            yield response.follow('https://www.cardkingdom.com/purchasing/mtg_singles?filter%5Bsort%5D=price_desc&filter%5Bsearch%5D=mtg_advanced&filter%5Bname%5D=&filter%5Bedition%5D=&filter%5Bformat%5D=&filter%5Bsingles%5D=1&filter%5Bprice_op%5D=&filter%5Bprice%5D=&page='+str(i), headers=self.headers, callback=self.parse_card)

    def parse_card(self, response):
        # Your scraping logic for individual product pages
        for row in response.xpath('//div[@class="productItemWrapper productCardWrapper"]'):
            card = CardsItem2()
            card['url'] = row.xpath('.//mtg-card-image/@href').extract_first() # Url
            card['name'] = row.xpath('.//mtg-card-image/@alt').extract_first() # Name
            card['price'] = row.xpath('.//div[@class="usdSellPrice"]/span[@class="sellDollarAmount"]/text()').extract_first() # Price
            yield card

class TcgplayerSpider(scrapy.Spider):
    name = "tcgplayer"
    allowed_domains = ["www.tcgplayer.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'tcgplayers_details.csv'
    }
    apis_df = pd.read_csv('ids.csv')
    card = TcgplayersItem()
    start_urls = ["https://www.tcgplayer.com/search/magic/product?productLineName=magic&view=grid&page=1&ProductTypeName=Cards"]
    def start_requests(self):
        for row in self.apis_df.itertuples():
            yield scrapy.Request('https://mp-search-api.tcgplayer.com/v1/product/'+str(row.ids)+'/details?mpfev=1798', callback=self.parse, meta={'id':row.ids})

    def parse(self, response):
        details_js = response.json()
        self.card['ID'] = response.meta['id']
        self.card['set_name'] = details_js['setName']
        self.card['product_name'] = details_js['productUrlName']
        self.card['set_code'] = details_js['setCode']
        self.card['url'] = 'https://www.tcgplayer.com/product/'+str(response.meta['id'])
        yield self.card

class TcgplayerSpider1(scrapy.Spider):
    name = "tcgplayer1"
    allowed_domains = ["www.tcgplayer.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'tcgplayers_price.csv'
    }
    apis_df = pd.read_csv('ids.csv')
    card = TcgplayersItem1()
    start_urls = ["https://www.tcgplayer.com/search/magic/product?productLineName=magic&view=grid&page=1&ProductTypeName=Cards"]
    def start_requests(self):
        for line in self.apis_df.itertuples():
            yield scrapy.Request('https://mpapi.tcgplayer.com/v2/product/'+str(line.ids)+'/pricepoints?mpfev=1798', callback=self.parse2, meta={'id':line.ids})

    def parse2(self, response):
        price_js = response.json()
        self.card['ID'] = response.meta['id']
        if len(price_js)==2:
            self.card['buy_list_market_price'] = price_js[0]['buylistMarketPrice']
        else:
            self.card['buy_list_market_price'] = price_js['buylistMarketPrice']
        yield self.card
