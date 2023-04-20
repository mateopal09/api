import requests
import locale
import json


from datetime import datetime
from bs4 import BeautifulSoup

#Ajustar la zona horaria para usar los meses en español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class API:
    """ Clase representando una API """

    def search_year(self):
        """ Método Search year

        Buscará toda la información que se le indique según el año.

        Retorna la información según el año y el año 
        """
        year = int(input('Escribe el año a consultar: '))
        url = f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm'
        response = requests.get(url)
        if response.status_code != 200: 
            #Eleva un error si el año no está.
            raise Exception('Error en el año del que intenta obtener datos')
        data = response.text
        return data, year

    def read_data(self, data):
        """ Método para leer la información según el año

        Va a analizar la información que recibe según el año a buscar
        y lo hará por medio de BeautifulSoup ya que la información la 
        entrega en formato html

        Parametros:
        -data : Será la información que recibe según el año que se quiere buscar

        Retorna la información completa buscando especifícamente en el id mes_all
        porque es una tabla que contiene toda la información de los valores por 
        día,mes y año
        """
        soup = BeautifulSoup(data, 'html.parser')
        #Busca el div con la clase 'meses' y el id 'mes_all'
        date_data = soup.find('div', {'class': 'meses', 'id': 'mes_all'})
        return date_data

    def search_date_value(self, date_data, year):
        """ Método search date_value Docs
        Recibe toda la información según el año y el año.

        Parámetros:
        - date_data : Será toda la información según el año, con todos los días
                      meses y valores correspondientes
        - year : Año a consultar

        Retorna En un formato json el valor junto con la fecha indicada   

        """
        day = int(input('Escribe el número del día '))
        month = int(input('Escribe el número del mes: '))
        if day < 1 or day > 31:
            #Si el valor dia está por fuera de 1 y 31 eleva el siguiente error.
            raise ValueError(
                'El día que está intentando acceder no está entre el 1 y el 31')
        if month < 1 or month > 12:
            #Si el valor mes está por fuera de 1 y 12 eleva el siguiente error.
            raise ValueError(
                'El month al que intenta acceder no está entre el 1 y el 12')
        table = date_data.find('table', {'id': 'table_export'})
        fecha = datetime(year=year, month=month, day=day)

        # Formatea la fecha dejandola ejemplo: Ene, Feb, Nov...
        month = fecha.strftime('%b')
        month = month.replace('.', '')
        month = month.capitalize()

        # Buscar la fila de encabezados y obtener el índice del mes
        # Si el número es 1 osea enero entonces va a buscar en los indices
        # del encabezado el número 1, ubicando esa columna
        header_month = table.find('thead').find('tr')
        month_index = None
        for index, th in enumerate(header_month.find_all('th')):
            if th.text == str(month):
                month_index = index
                break

        # Buscar la fila del día específico
        # Si el día es 14 por ejemplo va a recorrer esas filas
        # y la que coincida por la dígitada anteriormente guardará ese indice 
        day_row = None
        for tr in table.find('tbody').find_all('tr'):
            if tr.find('th').text == str(day):
                day_row = tr
                break
        #Luego de tener el dia y el mes, buscará el valor. obteniendo su información
        valor = day_row.find_all('td')[month_index - 1].text
        if not valor or valor.isspace():
            #Si el valor no está o es un espacio en blanco ya que se actualiza constantemente la página
            #entonces eleva el siguiente valor
            raise ValueError(f'No hay información disponible para la fecha {day}/{month}/{year}')
        #Se guarda la información en un diccionario
        data_dict = {'Year': year, 'Month': month, 'Day': day, 'Value': valor}
        #Convierto el anterior diccionario a un formato json
        json_data = json.dumps(data_dict)
        return json_data

if __name__ == '__main__':
    #instancia de la clase API
    api = API()
    data, year = api.search_year()
    date_data = api.read_data(data)
    print(api.search_date_value(date_data, year))
