import os

from cargar_archivos import cargar_aeropuertos, cargar_conexiones
from entidades import Aeropuerto, Conexion
from collections import deque


UMBRAL = 40000


class RedesMundiales:

    def __init__(self):
        # Estructura donde se guardaran los aeropuertos
        # Cada llave es un id y el valor es una instancia de Aeropuerto
        self.aeropuertos = {}

    def agregar_aeropuerto(self, aeropuerto_id, nombre):
        # Agregar un aeropuerto a la estructura
        aeropuerto = Aeropuerto(aeropuerto_id, nombre)
        self.aeropuertos[aeropuerto_id] = aeropuerto

    def bfs(self, id_aeropuerto_inicio):
        # Vamos a mantener una lista con los nodos visitados.
        visitados = []
        aeropuerto_inicio = self.aeropuertos[id_aeropuerto_inicio]
        # La cola de siempre, comienza desde el nodo inicio.
        queue = deque([aeropuerto_inicio])

        while len(queue) > 0:
            vertice = queue.popleft()
            # Detalle clave: si ya visitamos el nodo, no hacemos nada!
            if vertice in visitados:
                continue

            # Lo visitamos
            visitados.append(vertice)
            # Agregamos los vecinos a la cola si es que no han sido visitados.
            for conexion in vertice.conexiones:
                for aeropuerto in self.aeropuertos.values():
                    if aeropuerto.id == conexion.aeropuerto_llegada_id:
                        vecino = aeropuerto
                        break
                if vecino not in visitados:
                    queue.append(vecino)
        return visitados

    def agregar_conexion(self, aeropuerto_id_partida, aeropuerto_id_llegada, infectados):
        # Crear la conexion de partida-llegada para el par de aeropuertos
        hay_aeropuerto_salida = False
        hay_aeropuerto_llegada = False
        hay_conexion_en_salida = False
        for aeropuerto in self.aeropuertos.values():
            if aeropuerto.id == aeropuerto_id_partida:
                aeropuerto_partida = aeropuerto
                hay_aeropuerto_salida = True
                for conexion in aeropuerto_partida.conexiones:
                    if conexion.aeropuerto_llegada_id == aeropuerto_id_llegada and\
                       conexion.aeropuerto_inicio_id == aeropuerto_id_partida:
                        hay_conexion_en_salida = True
                        break
            elif aeropuerto.id == aeropuerto_id_llegada:
                aeropuerto_llegada = aeropuerto
                hay_aeropuerto_llegada = True

        if hay_aeropuerto_salida and hay_aeropuerto_llegada and not hay_conexion_en_salida:
            conexion = Conexion(aeropuerto_id_partida, aeropuerto_id_llegada, infectados)
            aeropuerto_partida.conexiones.append(conexion)

    def cargar_red(self, ruta_aeropuertos, ruta_conexiones):

        # Primero se crean todos los aeropuertos
        for aeropuerto_id, nombre in cargar_aeropuertos(ruta_aeropuertos):
            self.agregar_aeropuerto(aeropuerto_id, nombre)

        # Después generamos las conexiones
        for id_partida, id_salida, infectados in cargar_conexiones(ruta_conexiones):
            self.agregar_conexion(id_partida, id_salida, infectados)

    def eliminar_conexion(self, conexion):
        id_partida = conexion.aeropuerto_inicio_id
        id_llegada = conexion.aeropuerto_llegada_id
        aeropuerto_inicio = self.aeropuertos.get(id_partida)
        for c in aeropuerto_inicio.conexiones:
            if c.aeropuerto_llegada_id == id_llegada:
                aeropuerto_inicio.conexiones.remove(c)
                break

    def eliminar_aeropuerto(self, aeropuerto_id):
        if aeropuerto_id not in self.aeropuertos:
            raise ValueError(f"No puedes eliminar un aeropuerto que no existe ({aeropuerto_id})")
        if self.aeropuertos[aeropuerto_id].conexiones:
            raise ValueError(f"No puedes eliminar un aeropuerto con conexiones ({aeropuerto_id})")
        del self.aeropuertos[aeropuerto_id]

    def infectados_generados_desde_aeropuerto(self, aeropuerto_id):
        infectados = 0
        aeropuertos_recorridos = self.bfs(aeropuerto_id)
        for aeropuerto in aeropuertos_recorridos:
            if aeropuerto.id == aeropuerto_id:
                aeropuerto_inicio = aeropuerto
            for conexion in aeropuerto.conexiones:
                infectados += conexion.infectados
        print(f"La cantidad estimada de infectados generados por el aeropuerto\
             {aeropuerto_inicio.nombre} es de {infectados}")
        return(infectados)

    def verificar_candidatos(self, ruta_aeropuertos_candidatos, ruta_conexiones_candidatas):
        # Se revisa cada aeropuerto candidato con las agregars conexiones candidatas.
        # Se elimina el aeropuerto en caso de que este genere muchos infectados
        generador_aeropuertos = cargar_aeropuertos(ruta_aeropuertos_candidatos)

        for dato_aeropuerto in generador_aeropuertos:
            aeropuerto = Aeropuerto(*dato_aeropuerto)
            self.aeropuertos[aeropuerto.id] = aeropuerto
            # Hace un generador cada vez que ve un aeropuerto
            datos_conexiones = cargar_conexiones(ruta_conexiones_candidatas)
            # Agrega las conexiones al aeropuerto candidato
            for dato_conexion in datos_conexiones:
                conexion = Conexion(*dato_conexion)
                if conexion.aeropuerto_inicio_id == aeropuerto.id:
                    aeropuerto.conexiones.append(conexion)
                    # Para cada conexion agregada chequeamos el umbral
                    id_salida = conexion.aeropuerto_inicio_id
                    infectados = self.infectados_generados_desde_aeropuerto(id_salida)
                    if infectados > UMBRAL:
                        print(f"La conexión {conexion} rompe las reglas de seguridad")
                        self.eliminar_conexion(conexion)

            if len(aeropuerto.conexiones) == 0:
                self.eliminar_aeropuerto(aeropuerto.id)


if __name__ == "__main__":
    # I: Construcción de la red
    # Instanciación de la red de aeropuertos
    redmundial = RedesMundiales()
    # Carga de datos (utiliza agregar_aeropuerto y agregar_conexion)
    redmundial.cargar_red(
        os.path.join("datos", "aeropuertos.txt"),
        os.path.join("datos", "conexiones.txt"),
    )

    # II: Consultas sobre la red
    # Verificar si conteo de infectados funciona
    # Para el aeropuerto 8 debería ser 2677
    redmundial.infectados_generados_desde_aeropuerto(8)
    # Para el aeropuerto 7 debería ser 10055
    redmundial.infectados_generados_desde_aeropuerto(7)
    # Para el aeropuerto 12 debería ser 30000
    redmundial.infectados_generados_desde_aeropuerto(4)

    # III: Simulación sobre la red
    # Utilizamos lo que hemos hecho para aplicar los cambios sobre la red
    redmundial.verificar_candidatos(
        os.path.join("datos", "aeropuertos_candidatos.txt"),
        os.path.join("datos", "conexiones_candidatas.txt"),
    )
