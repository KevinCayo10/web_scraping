import scrapy
from scrapy.item import Field, Item
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider

class Pregunta(Item):
    id = Field()
    pregunta = Field()
    descripcion = Field()

class StackOverflowSpider(Spider):
    name = "MiPrimerSpider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    start_urls = ['https://stackoverflow.com/questions']
    
    def parse(self, response):
        sel = Selector(response)
        preguntas = sel.xpath('//div[@id="questions"]//div[contains(@class,"s-post-summary ")]') 
        i=0
        for pregunta in preguntas:
            item = ItemLoader(Pregunta(), pregunta)
            item.add_xpath('pregunta', './/h3/a/text()') 
            item.add_value("id",1)
            # item.add_xpath('descripcion', './/div[@class="s-post-summary--content-excerpt"]/text()')
            i += 1
            yield item.load_item()
