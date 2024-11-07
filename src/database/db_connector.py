from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

# Configuración de MongoDB
MONGO_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("MONGODB_DATABASE")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION")

# Conectar a MongoDB y exponer `db` para otros módulos
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]  # <- Aquí definimos `db` globalmente
collection = db[COLLECTION_NAME]

def verificar_conexion():
    """Verifica que la conexión a MongoDB esté activa."""
    try:
        # Intentar acceder a la base de datos
        if collection.find_one():
            print("Conexión a MongoDB exitosa.")
        else:
            print("Conexión a MongoDB exitosa, pero la colección está vacía.")
    except Exception as e:
        print("Error en la conexión a MongoDB:", e)

def insertar_datos(datos):
    """Inserta o sobrescribe documentos en la colección de MongoDB."""
    for dato in datos:
        try:
            criterio = {
                "localidad_id": dato["localidad_id"],
                "fecha": dato["fecha"]
            }
            result = collection.replace_one(criterio, dato, upsert=True)
            if result.matched_count > 0:
                print(f"Documento sobrescrito: {dato}")
            else:
                print(f"Documento insertado: {dato}")
        except Exception as e:
            print(f"Error al insertar o sobrescribir el documento en MongoDB: {e}")

 
def obtener_datos(filtro=None):
    """Obtiene datos de la colección de MongoDB según el filtro especificado."""
    return collection.find(filtro or {})

# Cerrar la conexión cuando ya no se necesite
def cerrar_conexion():
    client.close()
