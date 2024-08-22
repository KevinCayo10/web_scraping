import scrapy
from scrapy.item import Field, Item
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose

class Departamento(Item):
  nombre = Field()
  direccion = Field()
  
class Urbaniape(CrawlSpider):
  name="Departamentos"
  custom_settings={
    'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/',
    'CLOSESPIDER_PAGECOUNT':5 #Cantidad de paginas que va a scrapear
  }
  
  allowed_domains=["urbania.pe"]
  
  download_delay=1
  
  start_urls=[
    "https://urbania.pe/buscar/venta-de-departamentos?page=1",
    "https://urbania.pe/buscar/venta-de-departamentos?page=2",
    "https://urbania.pe/buscar/venta-de-departamentos?page=3",
    "https://urbania.pe/buscar/venta-de-departamentos?page=4"
  ]
  
  rules=(
    Rule(
      LinkExtractor(
        allow=[r'/proyecto/',r'/clasificado/']
      ),follow=True,callback="parse_departamento"
    ),
    )
  def parse_departamento(self,response):
    sel = Selector(response)
    item = ItemLoader(Departamento(),sel)
    item.add_xpath("nombre",'//span[@class="price-value"]//*/text()')
    item.add_xpath("direccion",'/div[@id="longDescription"]/text()')
    
    yield item.load_item()