import unittest
from src.data_processing.metPy import procesar_datos, cargar_configuracion, copiar_plantilla
from datetime import datetime

class TestFullProcessing(unittest.TestCase):

    def setUp(self):
        # Configuración inicial de prueba
        self.fecha = datetime.now()
        self.config = cargar_configuracion()
        self.data_dir = "data"
        self.plantilla = self.config.get("template_path", "config/templates/MeteoData.xlsx")
        self.comunidad = "ANDALUCIA"

    def test_procesar_datos(self):
        # Proceso completo de adquirir, procesar y guardar datos
        archivo_destino = copiar_plantilla(self.fecha, self.plantilla, self.data_dir)
        procesar_datos(self.fecha, self.comunidad, self.data_dir, archivo_destino)

        # Aquí podrías añadir verificaciones para asegurar que el archivo Excel se creó correctamente
        # y que contiene los datos esperados

if __name__ == '__main__':
    unittest.main()
