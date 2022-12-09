import pandas as pd
import numpy as np


class ModelETL:

    def __init__(self):  # Constructor
        self.load_data()  # Se cargan los datos de los CSV y JSON a sus respectivos dataframe
        # Se divide todos los datos en 3 tablas ya que algunas columnas tienen campos nulos
        self.film_details_concat()  # Concatena la tabla de detalles de la pelicula
        self.film_score_concat()  # Concatena la tabla de puntaje de la pelicula
        self.film_distribution_concat()  # Concatena la tabla de distribucion de la pelicula

    def load_data(self):  # Crea los dataframe de acuerdo a los CSV y JSON
        self.df_amazon = pd.read_csv('./datasets/amazon_prime_titles.csv', sep=',')
        self.df_disney = pd.read_csv('./datasets/disney_plus_titles.csv', sep=',')
        self.df_hulu = pd.read_csv('./datasets/hulu_titles.csv', sep=',')
        self.df_netflix = pd.read_json('./datasets/netflix_titles.json')

    def film_details_concat(self):  # Toma todos los dataframe y trae los detalles de las peliculas
        # Teniendo en cuenta que el detalle de la pelicula comprende:
        # show_id, title, release_year, listed_in, type, duration, description
        self.df_film_details = self.film_details(self.df_amazon, 'amazon')
        self.df_film_details = self.df_film_details.append(self.film_details(self.df_disney, 'disney_plus'))
        self.df_film_details = self.df_film_details.append(self.film_details(self.df_hulu, 'hulu'))
        self.df_film_details = self.df_film_details.append(self.film_details(self.df_netflix, 'netflix'))

    def film_score_concat(self):  # Toma todos los dataframe y trae los datos de puntajes de las peliculas
        # Teniendo en cuenta que los datos de puntajes de la pelicula comprende:
        # show_id, date_added, rating
        self.df_film_score = self.film_score(self.df_amazon, 'amazon')
        self.df_film_score = self.df_film_score.append(self.film_score(self.df_disney, 'disney_plus'))
        self.df_film_score = self.df_film_score.append(self.film_score(self.df_hulu, 'hulu'))
        self.df_film_score = self.df_film_score.append(self.film_score(self.df_netflix, 'netflix'))

    def film_distribution_concat(self):  # Toma todos los dataframe y trae los datos de distribucion de las peliculas
        # Teniendo en cuenta que los datos de distribucion de la pelicula comprende:
        # show_id, director, cast, country
        self.df_film_distribution = self.film_distribution(self.df_amazon, 'amazon')
        self.df_film_distribution = self.df_film_distribution.append(
            self.film_distribution(self.df_disney, 'disney_plus'))
        self.df_film_distribution = self.df_film_distribution.append(self.film_distribution(self.df_hulu, 'hulu'))
        self.df_film_distribution = self.df_film_distribution.append(self.film_distribution(self.df_netflix, 'netflix'))

    def film_details(self, df, platform_name):  # Concatenar las columnas de interes
        return pd.concat([df.show_id, df.title, df.description, df.duration, df.release_year, df.listed_in, df.type],
                         axis=1) \
            .assign(platform=platform_name)

    def film_distribution(self, df, platform_name):  # Concatenar las columnas de interes
        return pd.concat([df.show_id, df.director, df.cast, df.country], axis=1).assign(platform=platform_name)

    def film_score(self, df, platform_name):  # Concatenar las columnas de interes
        return pd.concat([df.show_id, df.date_added, df.rating], axis=1).assign(platform=platform_name)

    def get_max_duration(self, year, platform, film_type):
        df = self.df_film_details[self.df_film_details['type'] == film_type]
        df = df[df['platform'] == platform]
        df = df[df['release_year'] == year]
        df_season = df.loc[df['duration'].str.contains('season|seasons', case=False)]
        df_min = df.loc[df['duration'].str.contains('min', case=False)]
        df_season['duration'] = df_season['duration'].str.extract('(\d+)').astype(int)
        df_min['duration'] = df_min['duration'].str.extract('(\d+)').astype(int)
        result: str = df_season['duration'].max(), " seasons and ", df_min['duration'].max(), "min"
        return str(result)

    def get_count_platform(self, platform):
        df = self.df_film_details[self.df_film_details['platform'] == platform]
        result: str = df[df['type'] == 'Movie']['show_id'].count(), " movies and ", df[df['type'] == 'TV Show']['show_id'].count(), " TV Shows"
        return str(result)

    def get_listedin(self, gender):
        df_by_gender = self.df_film_details.loc[self.df_film_details['listed_in'].str.contains(gender, case=False)]
        return str([('amazon', df_by_gender[df_by_gender['platform'] == 'amazon']['show_id'].count()),
                ('disney_plus', df_by_gender[df_by_gender['platform'] == 'disney_plus']['show_id'].count()),
                ('hulu', df_by_gender[df_by_gender['platform'] == 'hulu']['show_id'].count()),
                ('netflix', df_by_gender[df_by_gender['platform'] == 'netflix']['show_id'].count())])

    def get_actor(self, platform, year):
        df = self.df_film_details.copy()
        df['cast'] = self.df_film_distribution['cast']
        df = df[df['release_year'] == year]
        df = df[df['platform'] == platform]
        return str(df['cast'].value_counts().nlargest(1))

    def missing_values(self, df):  # Función auxiliar para calcular valores nulos
        missing_values_count = df.isnull().sum()
        total_cells = np.product(df.shape)
        total_missing_values = missing_values_count.sum()
        missing_values_rate = total_missing_values // total_cells * 100
        return missing_values_rate

    def show_data_specs(self, original_df, clean_df):  # Función auxiliar para calcular valores nulos respecto al df original
        print("Datos originales:\n")
        print("Valores nulos:\n", original_df.isnull().sum(), "\nRegistros totales:\n", original_df.count())
        print("Datos limpios:\n")
        print("Valores nulos:\n", clean_df.isnull().sum(), "\nRegistros totales:\n", clean_df.count())
