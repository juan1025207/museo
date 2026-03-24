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

class ObraArte:
    def __init__(self, titulo, autor, periodo, valor, fecha_creacion, sala):
        self.id = str(uuid.uuid4())[:8]  # id único
        self.titulo = titulo  # título de la obra
        self.autor = autor  # autor
        self.periodo = periodo  # periodo artístico
        self.valor = valor  # valor económico
        self.fecha_creacion = fecha_creacion  # fecha de creación
        self.fecha_entrada = date.today()  # fecha de ingreso al museo
        self.estado = EstadoObra.EXPUESTA  # estado actual
        self.sala = sala  # sala asignada
        self.ultima_restauracion = date.today()  # última restauración
        self.restauraciones = []  # historial de restauraciones
        log.info("Obra registrada | id=%s | titulo=%s", self.id, self.titulo)

    def necesita_restauracion(self):
        cinco_anos = timedelta(days=5 * 365)  # periodo de 5 años
        return (date.today() - self.ultima_restauracion) >= cinco_anos  # verifica restauración

    def mostrar(self):
        print(f"  [{self.id}] {self.titulo} | Autor: {self.autor}")  # info básica
        print(f"         Periodo: {self.periodo.value} | Valor: ${self.valor:,.2f}")
        print(f"         Estado: {self.estado.value} | Sala: {self.sala}")

    def tipo(self):
        return "Obra de Arte"  # tipo de objeto

class Cuadro(ObraArte):
    def __init__(self, titulo, autor, periodo, valor,
                 fecha_creacion, sala, estilo, tecnica):
        super().__init__(titulo, autor, periodo, valor, fecha_creacion, sala)  # hereda de ObraArte
        self.estilo = estilo  # estilo del cuadro
        self.tecnica = tecnica  # técnica usada

    def mostrar(self):
        super().mostrar()  # muestra info base
        print(f"         Estilo: {self.estilo.value} | Tecnica: {self.tecnica}")

    def tipo(self):
        return "Cuadro"  # tipo de obra


class Escultura(ObraArte):
    def __init__(self, titulo, autor, periodo, valor,
                 fecha_creacion, sala, estilo, material):
        super().__init__(titulo, autor, periodo, valor, fecha_creacion, sala)  # hereda
        self.estilo = estilo  # estilo
        self.material = material  # material

    def mostrar(self):
        super().mostrar()  # muestra base
        print(f"         Estilo: {self.estilo.value} | Material: {self.material}")

    def tipo(self):
        return "Escultura"  # tipo de obra


class OtroObjeto(ObraArte):
    def __init__(self, titulo, autor, periodo, valor,
                 fecha_creacion, sala, descripcion):
        super().__init__(titulo, autor, periodo, valor, fecha_creacion, sala)  # hereda
        self.descripcion = descripcion  # descripción

    def mostrar(self):
        super().mostrar()  # muestra base
        print(f"         Descripcion: {self.descripcion}")

    def tipo(self):
        return "Otro Objeto"  # tipo de obra
    