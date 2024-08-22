import scrapy
from scrapy.item import Field, Item
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose

class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()
    
class MercadoLibreCrawler(CrawlSpider):
  name="mercadoLibre"
  
  custom_settings={
  'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'CLOSESPIDER_PAGECOUNT':20 #Cantidad de paginas que va a scrapear
}
  download_delay=1
  allowed_domains=[
    'listado.mercadolibre.com.ec','articulo.mercadolibre.com.ec'
  ]
  start_urls = ['https://listado.mercadolibre.com.ec/laptop-hp#D[A:laptop%20hp,on]']
   
  rules=(
    #paginación
    Rule(
      LinkExtractor(
        allow=r'/computacion-notebooks/laptop-hp_Desde'
      ),follow=True
    ),
    #Detalle del productos
    Rule(
      LinkExtractor(
        allow=[r'/MEC-', r'/laptop-']
      ), follow=True, callback='parse_items'
    )
  )
  
  def limpiarTexto(self, texto):
    nuevoTexto = texto.replace('\n',' ').replace('\r',' ').replace('\t',' ').strip()
    return nuevoTexto
    
  
  def parse_items(self, response):
    item = ItemLoader(Articulo(),response)
    
    item.add_xpath("titulo","//h1[@class='ui-pdp-title']/text()", MapCompose(self.limpiarTexto))
    item.add_xpath("descripcion","//div[@class='ui-pdp-description']/p/text()",MapCompose(self.limpiarTexto))
    item.add_xpath("precio","//div[@class='ui-pdp-price__second-line']//span[@class='andes-money-amount__fraction']/text()")
    
    yield item.load_item()
        