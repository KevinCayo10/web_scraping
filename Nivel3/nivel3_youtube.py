from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager

def obtener_script_scrolling(iteration):
  scrollingScript="""
  window.scrollTo(0,20000)
  """
  return scrollingScript.replace('2000',str(20000*(iteration+1)))

opts=Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

opt=Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
opts.add_argument("--disable-search-engine-choice-screen")

driver.get("https://www.youtube.com/playlist?list=PLuaGRMrO-j-8NndtkHMA7Y_7798tdJWKH")
sleep(2)

try:
  boton_disclaimer = driver.find_element(By.XPATH,"//button[@aria-label='Accept all']")
  boton_disclaimer.click
except:
  print("error")
  pass

videos = driver.find_elements(By.XPATH,'//div[@id="content"]//ytd-thumbnail')
urls_videos = []
for video in videos:
  url=video.find_element(By.XPATH,".//a[@id='thumbnail']").get_attribute("href")
  urls_videos.append(url)
  
for url in urls_videos:
  driver.get(url)
  sleep(3)
  driver.execute_script("window.scrollTo(0,600)")
  sleep(3)
  print("paso 1")
  num_comentario_totales = driver.find_element(By.XPATH,'//h2[@id="count"]//span[1]').text
  print("paso 2")
  num_comentario_totales = int(num_comentario_totales)*0.90
  print("Comentarios totales : ",num_comentario_totales)
  comentarios_cargados=driver.find_elements(By.XPATH,'//yt-attributed-string[@id="content-text"]')
  n_scrolling=0
  max_scrolling=10
  while len(comentarios_cargados) <num_comentario_totales and n_scrolling<max_scrolling:
    driver.execute_script(obtener_script_scrolling(n_scrolling))
    n_scrolling+=1
    sleep(2)
    comentarios_cargados=driver.find_elements(By.XPATH,'//yt-attributed-string[@id="content-text"]')
  comentarios = driver.find_elements(By.XPATH,'//yt-attributed-string[@id="content-text"]')
  for comentario in comentarios:
    texto_comentario = comentario.find_element(By.XPATH,'./span').text
    print(texto_comentario)