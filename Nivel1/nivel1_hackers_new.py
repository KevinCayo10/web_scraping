import requests
from bs4 import BeautifulSoup

url ="https://news.ycombinator.com/"

headers = {
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

respuesta = requests.get(url, headers=headers)

# Si el codigo responde 200:  entonces si se puede
# Si el codigo responde 400 >: entonces no se puede hacer web scraping
print(respuesta)

soup = BeautifulSoup(respuesta.text, "html.parser")

lista_noticias = soup.find_all("tr",class_ = "athing")
# find_all : Busca todos
# find : solo busca uno
for noticia in lista_noticias:
  titulo  = noticia.find("span",class_="titleline").text
  print(titulo)
  url = noticia.find("span",class_="titleline").find('a').get('href')
  print(url)
  
  metadata = noticia.find_next_sibling()

  puntos = 0
  comentarios = 0
  
  try:
    puntos = metadata.find("span",class_="score").text
    print(puntos)
  except :
    print("No hay score")
    
  try:
     comentarios_tmp = metadata.find("span",attrs={"class":"subline"}).text
     comentarios = comentarios_tmp.split("|")[-1]
     print(comentarios)
     
  except:
    print("No hay comentarios")


  print("\n")
  