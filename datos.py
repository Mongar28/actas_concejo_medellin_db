import datetime
import pandas as pd
import sqlite3 as sql
from sqlite3_tools.sql_t import (
    create_inteventions_db,
    create_authors_table,
    create_inteventions_table,
    insert_rows_authors,
    insert_rows_interventions
)

df_inter = pd.read_csv("intervenciones_concejo_medellin.csv")
df_inter = df_inter[df_inter['intervino'].str.len() <= 50]

# Construir la tupla de los autores
authors_sin_filtro: list = [autor for autor in df_inter['intervino']]
authors: list = set(authors_sin_filtro)
tuples_authors: list = [(id, author)
                        for id, author in enumerate(authors, start=1)]

# Construir el diccionario de autores con su id como valor
dict_authors: dict = {p_author[1]: p_author[0] for p_author in tuples_authors}

# Ahora que tenemos el diccionario de los autores y su id
# Poidemos construir la tupla de las intervenciones


def convertir_fecha(fecha):
    # Diccionario para mapear los meses en español a sus números correspondientes
    meses = {
        'Enero': '01',
        'Febrero': '02',
        'Marzo': '03',
        'Abril': '04',
        'Mayo': '05',
        'Junio': '06',
        'Julio': '07',
        'Agosto': '08',
        'Septiembre': '09',
        'Octubre': '10',
        'Noviembre': '11',
        'Diciembre': '12'
    }

    # Dividir la fecha en sus componentes
    partes = fecha.split(' ')

    if len(partes) == 4:
        dia = partes[1]
        mes = meses[partes[0]]
        año = partes[3]

        # Formatear la fecha en el nuevo formato
        nueva_fecha = f"{año}-{mes}-{dia.zfill(2)}"
    else:
        mes = meses[partes[0]]
        año = partes[-1]

        nueva_fecha = f"{año}-{mes}"

    return nueva_fecha


tuples_interventions: list = []
for index, fila in df_inter.iterrows():

    author: str = fila['intervino']

    id_int: int = index + 1
    id_author: int = dict_authors[author]
    acta: str = fila['acta']
    date = convertir_fecha(fila['fecha'])
    intervention: str = fila['intervencion'].replace('@@@', '').strip()

    tuples_interventions.append(
        (id_int, id_author, acta, date, intervention)
    )

# Ya uqe contamos con las listas de tuplas de autores e intervenciones
# procedemos a crear las base de datos de las intervenciones del concejo

# Cremaos la base de datos
create_inteventions_db()

# Creamos la tabla authors
create_authors_table()

# Creamos la tabla interventions
create_inteventions_table()

# Insertamos las tuplas a la tabla authors
insert_rows_authors(tuples_authors)

# Insertamos los tuplas a la tabla interventions
insert_rows_interventions(tuples_interventions)
