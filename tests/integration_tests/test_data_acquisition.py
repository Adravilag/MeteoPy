import unittest
from src.data_processing.metPy import obtener_datos_meteo

class TestDataAcquisition(unittest.TestCase):

    def test_obtener_datos_meteo(self):
        # Configura datos de prueba
        latitud = 37.3891
        longitud = -5.9845
        fecha = "2024-11-05"  # Ejemplo de fecha

        # Llama a la función de adquisición de datos
        datos = obtener_datos_meteo(latitud, longitud, fecha)

        # Verifica que los datos no son None y contienen la información esperada
        self.assertIsNotNone(datos)
        self.assertIn('daily', datos)
        self.assertIn('temperature_2m_min', datos['daily'])
        self.assertIn('temperature_2m_max', datos['daily'])

if __name__ == '__main__':
    unittest.main()
