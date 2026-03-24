"""
Sistema de Gestion del Museo
Autor: Juan Camilo Moreno Perez

"""
 
import logging  #manejo de registros
import uuid  #generar identificadores únicos
from datetime import date, timedelta  #manejo de fechas
from enum import Enum  #enumeraciones

logging.basicConfig(
    level=logging.INFO,  # nivel de mensajes
    format="%(asctime)s [%(levelname)s] - %(message)s",  #formato del log
    handlers=[
        logging.StreamHandler(),  #salida en consola
        logging.FileHandler("museo.log"),  #guardar en archivo
    ],
)
log = logging.getLogger("Museo")  #crear logger

#cvalores fijos
class EstadoObra(Enum):
    EXPUESTA     = "EXPUESTA"
    RESTAURACION = "RESTAURACION"
    CEDIDA       = "CEDIDA"
 
 
class TipoRestauracion(Enum):
    PREVENTIVA = "PREVENTIVA"
    EMERGENCIA = "EMERGENCIA"
 
 
class Periodo(Enum):
    PREHISTORIA   = "Prehistoria"
    ANTIGUA       = "Antigua"
    MEDIEVAL      = "Medieval"
    RENACIMIENTO  = "Renacimiento"
    BARROCO       = "Barroco"
    MODERNO       = "Moderno"
    CONTEMPORANEO = "Contemporaneo"
 
 
class Estilo(Enum):
    REALISMO      = "Realismo"
    IMPRESIONISMO = "Impresionismo"
    ABSTRACTO     = "Abstracto"
    CLASICO       = "Clasico"
    BARROCO       = "Barroco"
    GOTICO        = "Gotico"