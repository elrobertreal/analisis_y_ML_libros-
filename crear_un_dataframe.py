from bs4 import BeautifulSoup
import requests
import pandas
from urllib.parse import urljoin
lista_nombres = []
precio = []
cantidad_estrellas = []
tipo_libros = []
# Se crea un loop para iterar por las 50 paginas de Books to Scrape, generando un pedido para cada i
for i in range(1,51):
    print(f"Consultando pagina {i}/50...", flush=True)
    url = f"https://books.toscrape.com/catalogue/page-{i}.html"
    pedido = requests.get(url, timeout=30)
    pedido.raise_for_status()
    soup = BeautifulSoup(pedido.content, 'html.parser')
    contenedor = soup.select("article.product_pod")
    # Se crea el contenedor que guarda todos los datos como, ratings, nombre y precio
    for libros in contenedor:
        # Se busca cada atributo del libro identificando cada clase en el HTML
        estrellas = libros.find("p", class_="star-rating")
        numero = estrellas["class"]
        cantidad_estrellas.append(numero[1])
        precio_libro = libros.find("p", class_="price_color")
        precio.append(precio_libro.get_text(strip=True))
        titulo = libros.find("h3").find("a")["title"]
        print(
            f"Analizando libro {len(lista_nombres) + 1}/1000 | Pagina {i}/50: {titulo}",
            flush=True
        )
        lista_nombres.append(titulo)
        enlace = libros.find("h3").find("a")["href"]
        url_libro = urljoin(url, enlace)
        # Como la forma de ver el genero de cada libro es mediante el ingreso a una segunda URL, generamos la ulr de ese libro y la juntamos con su respectivo URL de la pagina inicial
        try:
            pedido_libro = requests.get(url_libro, timeout=(10, 15))
            pedido_libro.raise_for_status()
            # Se genera una excepcion en el caso de que request envie un error de servidor
        except requests.RequestException as error:
            print(f"No se pudo consultar {url_libro}: {error}", flush=True)
            tipo_libros.append(None)
            continue
        detalle = BeautifulSoup(pedido_libro.content, "html.parser")
        categoria = detalle.select_one("ul.breadcrumb li:nth-of-type(3) a")
        # Se busca la clase dentro de esa nueva URL y se extrae el texto mediante el metodo get_text
        if categoria is None:
            print(f"No se encontro la categoria en {url_libro}", flush=True)
        tipo_libros.append(categoria.get_text(strip=True) if categoria else None)

# Crear y guardar el DataFrame al terminar de consultar los libros.
df = pandas.DataFrame({
    "Titulo": lista_nombres,
    "Precio": precio,
    "Estrellas": cantidad_estrellas,
    "Categoria": tipo_libros
})
df.to_csv("libros.csv", index=False, encoding="utf-8-sig")
# Aqui el archivo queda guardado en la misma ruta donde esta este codigo, y luego puedo importarlo usando Pandas








