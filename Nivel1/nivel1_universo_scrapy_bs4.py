import scrapy
from scrapy.item import Field, Item
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
from bs4 import BeautifulSoup

#https://www.eluniverso.com/deportes/columnistas-deportes/

class Noticias(Item):
  titular = Field()
  descripcion = Field()

class ElUniversoSpider(Spider):
  name="MiSegundoSpider"
  
  custom_settings = {
   'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
  }

  start_urls = ["https://www.eluniverso.com/deportes/"]
  
  def parse(self, response):
    sel = Selector(response)
    noticias = sel.xpath('//div[contains(@class, "content-feed")]/ul/li')
    
    for i,elem in enumerate(noticias):
      print("\nEleM : ",elem)
      item = ItemLoader(Noticias(),elem)
      item.add_xpath("titular",'.//h2/a/text()')
      item.add_xpath("descripcion",'.//p/text()')
      yield item.load_item()
    
    # Ahora con BS4
    # soup = BeautifulSoup(response.body)
    # contenedor_noticias = soup.find_all("div",class_="feed | divide-y relative  ")
    # for contenedor in contenedor_noticias:
      
    
process = CrawlerProcess({
  "FEED_FORMAT":"csv",
  "FEED_URI":"resultados.csv"
})

process.crawl(ElUniversoSpider)
process.start()