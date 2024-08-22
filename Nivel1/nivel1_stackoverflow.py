import requests 
from bs4 import BeautifulSoup

headers={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

url = "https://stackoverflow.com/questions"

respuesta = requests.get(url, headers=headers)

# print(respuesta.text)

# Crea el objeto BeautifulSoup y especifica el parser
soup = BeautifulSoup(respuesta.text,  "html.parser")

# Encuentra el contenedor padre
contenedor_padre = soup.find(id="questions")

if contenedor_padre:
    # Encuentra todos los elementos div con la clase 's-post-summary' dentro del contenedor padre
    lista_preguntas = contenedor_padre.find_all("div", class_="s-post-summary")
    for pregunta in lista_preguntas:
        elemento_texto_pregunta = pregunta.find("h3")
        titulo = elemento_texto_pregunta.text
        #mover al hermano siguiente
        hermano_siguiente = elemento_texto_pregunta.find_next_sibling("div").text
        descripcion = pregunta.find(class_="s-post-summary--content-excerpt").text
        descripcion = descripcion.replace('\n','').replace('\r','').strip()
        hermano_siguiente = hermano_siguiente.replace('\n','').replace('\r','').strip()

        print(titulo)
        print(descripcion)
        print(hermano_siguiente)

else:
    print("No se encontró el contenedor padre con el id 'question-mini-list'.")