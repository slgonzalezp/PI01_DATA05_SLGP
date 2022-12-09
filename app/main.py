from app.model import ModelETL

from fastapi import FastAPI

# Cargar los componentes necesarios para iniciar el framework de flask api
app = FastAPI()
# Se carga el modelo en la variable model para iniciar el constructor de la clase
model = ModelETL()


# Por medio de la clase main se crean los endpoints para acceder a las funciones que realizan la busqueda
# Endpoint para realizar la consulta:
#  Máxima duración según tipo de film (película/serie), por plataforma
#    y por año: El request debe ser: get_max_duration(año, plataforma, [min o season])
# Ejemplo link: http://127.0.0.1/max-duration-by-film/2014?platform=netflix&film_type=Movie
@app.get("/max-duration-by-film/{year}")
def read_root(year: int, platform: str, film_type: str):
    return model.get_max_duration(year, platform, film_type)

# Endpoint para realizar la consulta:
#   Cantidad de películas y series (separado) por plataforma El request debe ser: get_count_plataform(plataforma)
# Ejemplo link: http://127.0.0.1/quantity-by-platform/netflix
@app.get("/quantity-by-platform/{platform}")
def read_item(platform: str):
    return model.get_count_platform(platform)

# Endpoint para realizar la consulta:
#    Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
#      El request debe ser: get_listedin('genero')
#       Como ejemplo de género pueden usar 'comedy', el cuál deberia devolverles un
#       count de 2099 para la plataforma de amazon.
# http://127.0.0.1/repetition-by-gender/Action-Adventure
@app.get("/repetition-by-gender/{gender}")
def read_item(gender: str):
    return model.get_listedin(gender)

# Endpoint para realizar la consulta:
#   Actor que más se repite según plataforma y año. El request debe ser: get_actor(plataforma, año)
# http://127.0.0.1/repetition-actor/netflix?year=2022
@app.get("/repetition-actor/{platform}")
def read_item(platform: str, year: int):
    return model.get_actor(platform, year)
