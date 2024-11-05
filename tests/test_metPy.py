import unittest
from unittest.mock import patch, mock_open
import json
from src.data_processing.metPy import cargar_traducciones

class TestMetPy(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "no_files_available": "No hay archivos disponibles.",
        "available_files": "Archivos disponibles:"
    }))
    def test_cargar_traducciones(self, mock_file):
        traducciones = cargar_traducciones('es')  # Carga las traducciones en español
        self.assertIn("no_files_available", traducciones)  # Verifica que una clave de traducción esté presente
        self.assertIn("available_files", traducciones)  # Verifica que otra clave de traducción esté presente

    @patch('builtins.open', side_effect=FileNotFoundError)  # Simula que no se encuentra el archivo
    def test_cargar_traducciones_file_not_found(self, mock_file):
        with patch('src.data_processing.metPy.open', mock_open(read_data=json.dumps({
            "no_files_available": "No hay archivos disponibles.",
            "available_files": "Archivos disponibles:"
        }))) as mock_file:
            traducciones = cargar_traducciones('es')  # Debería cargar el idioma por defecto
            self.assertIn("no_files_available", traducciones)  # Verifica que cargó el idioma por defecto

if __name__ == "__main__":
    unittest.main()
