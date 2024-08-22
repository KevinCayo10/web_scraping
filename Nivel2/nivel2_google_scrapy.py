import scrapy
from scrapy.item import Field, Item
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose


class Articulo(Item):
  titulo = Field()
  citaciones = Field()
  autores = Field()
  url = Field()
  
class GoogleScholar(CrawlSpider):
  name = "google_scholar"
  custom_settings={
    'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/',
    'DEPTH_LIMIT':1, #Escrapea con un limite de profundidad, es decir repite las reglas una sola vez
    "FEED_EXPORT_ENCODING":'utf-8', #Caracteres especiales 
    'DOWNLOAD_DELAY': 1
  }
  
  download_delay=2
  
  start_urls=[
    'https://scholar.google.com/scholar?hl=es&as_sdt=0%2C5&q=web+scraping&btnG='
  ]
  
  allowed_domains=['scholar.google.com']
  
  rules=(
    Rule(
      LinkExtractor(
        restrict_xpaths='//div[@class="gs_ri"]', #Restringe la busqueda que sea donde solo tenga ese XPATH
        allow=r'\?cites='
      ),follow=True,callback="parse_start_url"
    ),
  )
  #Escrapear url semilla
  def parse_start_url(self,response):
    sel =  Selector(response)
    articulos = sel.xpath('//div[@class="gs_ri"]')
    
    for articulo in articulos:
      item = ItemLoader(Articulo(),articulo)
      titulo = articulo.xpath('.//h3/a//text()').getall()
      titulo = "".join(titulo)
      item.add_value("titulo",titulo)
      url= articulo.xpath('.//h3/a/@href').get()
      item.add_value("url",url)
      #.get() solo devuelve el primer objeto que obtenga
      autores = articulo.xpath('.//div[@class="gs_a"]//text()').getall()
      autores = "".join(autores)
      #[D Glez-Peña, A Lourenço… , Briefings in …, 2014 , academic.oup.com]
      autores = autores.split("-")[0]
      item.add_value("autores",autores)
      #Citado por 291
      citaciones=0
      try:
        citaciones = articulo.xpath(".//a[contains(@href,'cites')]/text()").get()
        citaciones = citaciones.replace('Citado por',' ')
        item.add_value("citaciones",citaciones)
      except:
        pass
      item.add_value("citaciones",citaciones)

      yield item.load_item()