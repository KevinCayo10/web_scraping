import scrapy
from scrapy.item import Field, Item
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()

class Expedia(CrawlSpider):
    name = "Hoteles"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'COOKIES_ENABLED': True,
        'REDIRECT_ENABLED': True,
        'HTTPERROR_ALLOWED_CODES': [302, 403]
    }

    allowed_domains = ['hotelscombined.com']
    start_urls = [
        "https://www.hotelscombined.com/hotels/Guayaquil,Ecuador-p50440/2024-07-30/2024-07-31/2adults;map?sort=rank_a"
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/hotels/'
            ),
            follow=True,
            callback="parse_hotel"
        ),
    )

    def parse_hotel(self, response):
        if response.status == 403:
            self.logger.error("Forbidden access: %s", response.url)
            return
        if response.status == 302:
            self.logger.info("Redirection: %s", response.url)
            return
        
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath("nombre", '//h1[contains(@class,"hotel-name")]/text()')
        item.add_xpath("precio", '//span[contains(@class,"price")]/span/text()')
        item.add_xpath("descripcion", '//div[contains(@class,"desc-text")]/text()')
        item.add_xpath("amenities", '//span[contains(@class,"amenity-name")]/text()')

        yield item.load_item()
