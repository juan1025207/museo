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


class Usuario:
    def __init__(self, nombre, contrasena, rol):
        self.nombre = nombre  # nombre del usuario
        self._contrasena = contrasena  # contraseña privada
        self.rol = rol  # tipo de usuario
        self.autenticado = False  # estado de sesión

    def iniciar_sesion(self, contrasena):
        if self._contrasena == contrasena:
            self.autenticado = True  # marca como autenticado
            log.info("Usuario %s inicio sesion", self.nombre)  # log inicio
            return True
        log.warning("Sesion fallida para %s", self.nombre)  # log error
        print(f"Contrasena incorrecta para {self.nombre}")
        return False

    def cerrar_sesion(self):
        self.autenticado = False  # cierra sesión
        log.info("Usuario %s cerro sesion", self.nombre)

    def verificar_acceso(self):
        if not self.autenticado:
            print(f"Acceso denegado. {self.nombre} debe iniciar sesion")  # acceso inválido
            return False
        return True  # acceso permitido