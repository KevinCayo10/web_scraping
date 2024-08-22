import scrapy
from scrapy.item import Field, Item
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose

class Farmacia(Item):
  Nombre = Field()
  Precio = Field()
  
class CruzVerde(CrawlSpider):
  name="CruzVerde"
  
  custom_settings={
  'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/',
  'CLOSESPIDER_PAGECOUNT':20 #Cantidad de paginas que va a scrapear
}
  
  allowed_domains = ["cruzverde.cl"]
  
  start_urls=["https://www.cruzverde.cl/medicamentos/"]
  
  
  rules=(
    Rule(
      LinkExtractor(
        allow=r'/start=',
        tags=('a','button'), #Busca no solo de la etiqueta <a> sino tambien a <button>
        attrs=('href','data-url')#Busca en los atributos data-url=""
      ),follow=True, callback="parse_farmacia"
    )
  )