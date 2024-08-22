import requests
from lxml import html 
encabezados = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

url = "https://wikipedia.org/"

respuesta = requests.get(url, headers=encabezados)

parser = html.fromstring(respuesta.text)

# titulo = parser.get_element_by_id("Oh_Father")
# print(titulo.text_content())

# titulo = parser.xpath("//h2[@id='Oh_Father']/a/text()")
# print(titulo)

# Cuando la clase tiene varias clases en el mismo o tiene espacios entonces se debe poner contains
idiomas = parser.xpath("//div[contains(@class,'central-featured-lang')]//strong/text()")
print(idiomas)
for idima in idiomas:
    print(idima)
    # print(idima.text_content())