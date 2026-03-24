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


class Restauracion:
    def __init__(self, obra, tipo, motivo=""):
        self.id = str(uuid.uuid4())[:8]  # id único
        self.obra = obra  # obra asociada
        self.tipo = tipo  # tipo de restauración
        self.motivo = motivo  # motivo
        self.fecha_inicio = date.today()  # fecha inicio
        self.fecha_fin = None  # fecha fin
        self.terminada = False  # estado
        log.info("Restauracion iniciada | id=%s | obra=%s | tipo=%s",
                 self.id, obra.titulo, tipo.value)

    def finalizar(self):
        self.fecha_fin = date.today()  # asigna fecha fin
        self.terminada = True  # marca como terminada
        log.info("Restauracion finalizada | id=%s | obra=%s",
                 self.id, self.obra.titulo)

    def mostrar(self):
        estado = "Finalizada" if self.terminada else "En proceso"  # estado texto
        print(f"  [REST-{self.id}] {self.tipo.value} | Inicio: {self.fecha_inicio}")
        print(f"         Estado: {estado} | Motivo: {self.motivo or 'Preventiva'}")
        if self.fecha_fin:
            print(f"         Fin: {self.fecha_fin}")  # muestra fin


class Cesion:
    def __init__(self, obra, museo_destino, importe, fecha_inicio, fecha_fin):
        self.id = str(uuid.uuid4())[:8]  # id único
        self.obra = obra  # obra cedida
        self.museo_destino = museo_destino  # destino
        self.importe = importe  # valor
        self.fecha_inicio = fecha_inicio  # inicio
        self.fecha_fin = fecha_fin  # fin
        self.activa = True  # estado
        log.info("Cesion registrada | obra=%s | museo=%s | importe=$%.2f",
                 obra.titulo, museo_destino, importe)

    def ha_terminado(self):
        return date.today() >= self.fecha_fin  # verifica fin

    def mostrar(self):
        estado = "Activa" if self.activa else "Finalizada"  # estado texto
        print(f"  [CES-{self.id}] Museo: {self.museo_destino}")
        print(f"         Importe: ${self.importe:,.2f} | Estado: {estado}")
        print(f"         Periodo: {self.fecha_inicio} al {self.fecha_fin}")


class MuseoColaborador:
    def __init__(self, nombre, ciudad, contacto):
        self.nombre = nombre  # nombre
        self.ciudad = ciudad  # ciudad
        self.contacto = contacto  # contacto

    def mostrar(self):
        print(f"  {self.nombre} | Ciudad: {self.ciudad} | Contacto: {self.contacto}")  # mostrar info


class Catalogo:
    def __init__(self):
        self.obras = {}  # obras por id
        log.info("Catalogo iniciado")

    def agregar_obra(self, obra, encargado):
        if not encargado.verificar_acceso():
            return False
        self.obras[obra.id] = obra  # agrega obra
        log.info("Obra agregada | %s por %s", obra.titulo, encargado.nombre)
        return True

    def buscar_por_sala(self, sala):
        return [o for o in self.obras.values() if o.sala == sala]  # filtra por sala

    def buscar_por_autor(self, autor):
        return [o for o in self.obras.values()
                if autor.lower() in o.autor.lower()]  # filtra por autor

    def listar_todas(self):
        print("\n=== CATALOGO COMPLETO ===")
        for obra in self.obras.values():
            obra.mostrar()  # muestra obra
            print()

    def listar_por_sala(self, sala):
        print(f"\n=== SALA {sala} ===")
        obras = self.buscar_por_sala(sala)
        if not obras:
            print("  No hay obras en esta sala.")
            return
        for obra in obras:
            obra.mostrar()  # muestra por sala

    def valor_total(self, director):
        if not director.verificar_acceso():
            return 0
        total = sum(o.valor for o in self.obras.values())  # suma valores
        log.info("Valor total consultado por %s: $%.2f", director.nombre, total)
        return total

    def obras_para_restaurar(self):
        return [o for o in self.obras.values()
                if o.necesita_restauracion() and o.estado == EstadoObra.EXPUESTA]  # filtra obras


class GestorRestauraciones:
    def __init__(self, catalogo):
        self.catalogo = catalogo  # referencia al catálogo
        self.restauraciones = []  # lista de restauraciones

    def iniciar_restauracion(self, obra_id, tipo, restaurador, motivo=""):
        if not restaurador.verificar_acceso():
            return None
        obra = self.catalogo.obras.get(obra_id)
        if not obra:
            print(f"Obra {obra_id} no encontrada")
            return None
        if obra.estado == EstadoObra.RESTAURACION:
            print(f"La obra '{obra.titulo}' ya esta en restauracion")
            return None
        rest = Restauracion(obra, tipo, motivo)  # crea restauración
        obra.estado = EstadoObra.RESTAURACION  # cambia estado
        obra.restauraciones.append(rest)  # guarda en obra
        self.restauraciones.append(rest)  # guarda global
        return rest

    def finalizar_restauracion(self, rest_id, restaurador):
        if not restaurador.verificar_acceso():
            return False
        rest = next((r for r in self.restauraciones if r.id == rest_id), None)
        if not rest:
            print(f"Restauracion {rest_id} no encontrada")
            return False
        rest.finalizar()  # finaliza restauración
        rest.obra.estado = EstadoObra.EXPUESTA  # vuelve a expuesta
        rest.obra.ultima_restauracion = date.today()  # actualiza fecha
        return True

    def proceso_diario(self, restaurador):
        if not restaurador.verificar_acceso():
            return
        obras = self.catalogo.obras_para_restaurar()  # obras pendientes
        print(f"\n=== PROCESO DIARIO: {len(obras)} obras para restaurar ===")
        for obra in obras:
            self.iniciar_restauracion(
                obra.id, TipoRestauracion.PREVENTIVA,
                restaurador, "Preventiva 5 anos"
            )

    def historial_obra(self, obra_id, restaurador):
        if not restaurador.verificar_acceso():
            return
        obra = self.catalogo.obras.get(obra_id)
        if not obra:
            print("Obra no encontrada")
            return
        print(f"\n=== HISTORIAL: {obra.titulo} ===")
        historico = sorted(obra.restauraciones, key=lambda r: r.fecha_inicio)  # ordena
        if not historico:
            print("  Sin restauraciones registradas")
            return
        for rest in historico:
            rest.mostrar()  # muestra historial


class GestorCesiones:
    def __init__(self, catalogo):
        self.catalogo = catalogo  # referencia catálogo
        self.museos_colaboradores = {}  # museos
        self.cesiones = []  # lista de cesiones

    def agregar_museo(self, museo, director):
        if not director.verificar_acceso():
            return False
        self.museos_colaboradores[museo.nombre] = museo  # agrega museo
        log.info("Museo colaborador agregado: %s", museo.nombre)
        return True

    def ceder_obra(self, obra_id, nombre_museo, importe,
                   fecha_inicio, fecha_fin, director):
        if not director.verificar_acceso():
            return None
        obra = self.catalogo.obras.get(obra_id)
        if not obra:
            print("Obra no encontrada")
            return None
        if obra.estado != EstadoObra.EXPUESTA:
            print(f"'{obra.titulo}' no disponible. Cesion queda pendiente.")
        museo = self.museos_colaboradores.get(nombre_museo)
        if not museo:
            print(f"Museo '{nombre_museo}' no es colaborador")
            return None
        cesion = Cesion(obra, nombre_museo, importe, fecha_inicio, fecha_fin)  # crea cesión
        obra.estado = EstadoObra.CEDIDA  # cambia estado
        self.cesiones.append(cesion)  # guarda cesión
        return cesion

    def listar_museos(self):
        print("\n=== MUSEOS COLABORADORES ===")
        for museo in self.museos_colaboradores.values():
            museo.mostrar()  # muestra museos

    def listar_cesiones(self, director):
        if not director.verificar_acceso():
            return
        print("\n=== CESIONES ACTIVAS ===")
        activas = [c for c in self.cesiones if c.activa]  # filtra activas
        if not activas:
            print("  No hay cesiones activas")
            return
        for ces in activas:
            ces.mostrar()  # muestra cesiones