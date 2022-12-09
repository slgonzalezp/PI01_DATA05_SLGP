# PI01_DATA05_SLGP

El proyecto realizado utiliza conjuntos de datos provistos por amazon, disney, hulu y netflix, se realizan las siguiente __consultas__:

Máxima duración según tipo de film (película/serie), por plataforma y por año: El request debe ser: get_max_duration(año, plataforma, [min o season])

Cantidad de películas y series (separado) por plataforma El request debe ser: get_count_plataform(plataforma)

Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo. El request debe ser: get_listedin('genero')
Como ejemplo de género pueden usar 'comedy', el cuál deberia devolverles un cunt de 2099 para la plataforma de amazon.

Actor que más se repite según plataforma y año. El request debe ser: get_actor(plataforma, año)

## Comandos para la ejecución de docker
Comando para construir la imagen docker:

docker build -t fast_api-gunicorn .

Comando para construir el contenedor docker:

docker run -d --name fast_api-container -p 80:80 fast_api-gunicorn

Links de ejemplo

- http://127.0.0.1/max-duration-by-film/2014?platform=netflix&film_type=Movie
- http://127.0.0.1/quantity-by-platform/amazon
- http://127.0.0.1/repetition-by-gender/Comedy
- http://127.0.0.1/repetition-actor/amazon?year=2014