import unittest
from src.visualization.geoPy import cargar_configuracion, cargar_traducciones  # Ajusta la ruta según tu estructura de proyecto

class TestGeoPy(unittest.TestCase):
    def test_cargar_configuracion(self):
        config = cargar_configuracion()
        self.assertIsInstance(config, dict)  # Verifica que el resultado sea un diccionario
        self.assertIn("label_threshold", config)  # Verifica que una clave esperada esté presente
        self.assertIn("data_directory", config)  # Verifica que la clave también esté presente

    def test_cargar_traducciones(self):
        traducciones = cargar_traducciones('es')  # Carga las traducciones en español
        self.assertIn("no_files_available", traducciones)  # Verifica que una clave de traducción esté presente
        self.assertIn("available_files", traducciones)  # Verifica que otra clave de traducción esté presente

    def test_cargar_traducciones_en(self):
        traducciones = cargar_traducciones('en')  # Carga las traducciones en inglés
        self.assertIn("no_files_available", traducciones)  # Verifica que una clave de traducción esté presente
        self.assertIn("available_files", traducciones)  # Verifica que otra clave de traducción esté presente

if __name__ == "__main__":
    unittest.main()
