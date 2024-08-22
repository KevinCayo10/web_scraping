import scrapy
from scrapy.item import Field, Item
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose


class Articulo(Item):
  titulo = Field()
  contenido = Field()
  
class Review(Item):
  titulo = Field()
  calificacion = Field()

class Video(Item):
  titulo = Field()
  fecha_de_publicacion = Field()
  
class IGNCrawler(CrawlSpider):
  name="IGN"
  
  custom_settings={
  'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'CLOSESPIDER_PAGECOUNT':100 #Cantidad de paginas que va a scrapear
}
  allowed_domains = ['latam.ign.com']
  
  start_urls = [
    'https://latam.ign.com/se/?model=article&q=ps5&order_by='
  ]
  
  rules = (
    #Horizontalidad por tipo de informacion
    Rule(
        LinkExtractor(
          allow=r'/se/?type='
        )
      ),
    #Horizontalidad por paginador
    Rule(
        LinkExtractor(
          allow=r'&page=\d+'
        )
      ),
    #Regla por cada tipo de contenido donde ire verticalmente
    #ARTICULOS
    Rule(
          LinkExtractor(
            allow=r'/news/'
          ),follow=True,callback="parse_new"
      ),
    #VIDEOS
    Rule(
          LinkExtractor(
            allow=r'/video/'
          ),follow=True,callback="parse_video"
      ),
    #REVIEW
    Rule(
        LinkExtractor(
          allow=r'/review/'
        ),follow=True,callback="parse_review"
    )
  )
  
  def parse_new(self,response):
    item = ItemLoader(Articulo(),response)
    item.add_xpath("titulo",'//h1[@id="id_title"]/text()')
    item.add_xpath("contenido",'//div[@id="id_text"]//*/text()')
    yield item.load_item()

  
  def parse_review(self,response):
    item = ItemLoader(Review(),response)
    item.add_xpath("titulo",'//h1[@class="strong"]/text()')
    item.add_xpath("calificacion",'//span[@class="side-wrapper side-wrapper hexagon-content"]/div/text()')
    yield item.load_item()

    
  def parse_video(self,response):
    item = ItemLoader(Video(),response)
    item.add_xpath("titulo",'//h1[@id="id_title"]/text()')
    item.add_xpath("fecha_de_publicacion",'//span[@class="publish-date"]/text()')
    
    yield item.load_item()
    


