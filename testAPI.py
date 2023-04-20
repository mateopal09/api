import unittest

from API import API

class TestApi(unittest.TestCase):
    """ Clase TestAPi heredando de el módulo unittest la clase TestCase"""

    def setUp(self):
        #Método para preparar el elemento fijo a testear
        self.api = API()
    
    def test_search_year(self, ):
        """ Método test_search_year
        Este método lo que hará es verificar que el año ingresado si exista
        Y retorne una información
        """
        #Recibo los valores data, year
        data, year = self.api.search_year()
        # Verificar que los valores recibidos son correctos
        assert isinstance(data, str)
        assert isinstance(year, int)

    def test_read_data(self):
        """Clase test_read_data
        Defino 2 valores para prueba, y se los paso al método
        self.api.read_data, esos resultados los verifico 
        si el primer resultado es igual al primer valor definido está bien
        si el segundo resutado es none retorna True sino entonces el
        método recibe cualquier valor, osea no está funcionando
        """
        # Definir algunos datos de prueba
        data1 = '<div class="meses" id="mes_all">datos1</div>'
        data2 = '<div class="meses" id="otro_id">datos2</div>'

        # Llamar al método read_data con diferentes datos de prueba
        result1 = self.api.read_data(data1)
        result2 = self.api.read_data(data2)

        # Verificar que los valores devueltos son correctos
        self.assertEqual(result1.text, 'datos1')
        self.assertIsNone(result2)

if __name__ == '__main__':
    unittest.main()