from juego.mapa.mapa import Mapa
from juego.entidades.usuario import Usuario
from juego.items.construcciones import Camino


mapa = Mapa()
mapa.cargar_mapa()
print(mapa)


def back_track_mapa(mapa, id_nodo):
    visitados = []
    stack = []
    endpoint = None
    id_nodo_inicial = id_nodo
    nodo_actual = id_nodo

    largo_rama = 0
    largos_ramas = []

    #  Comineza el backtrack
    visitados.append(nodo_actual)
    stack.append(nodo_actual)
    while True:

        # Verifica que no sea un endpoint
        while not endpoint:
            # Si es que es endpoint agrega el largo de la rama a la que llego
            if is_end_point(mapa, nodo_actual, visitados):
                endpoint = nodo_actual
                print(f"LLEGANDO A ENDPOINT {nodo_actual}")
                # Caso especial en que hay un camino extra a un nodo ya visitado
                vecinos = vecinos_conectados(mapa, nodo_actual)
                for vecino in vecinos:
                    print(f"CASO ESPECIAL nodo actual: {nodo_actual}")
                    print(f" Anterior {stack[len(stack) - 2]}")
                    if vecino != stack[len(stack) - 2]:
                        largo_rama += 1
                        print(f"largo camino rama {largo_rama}")
                        largos_ramas.append(largo_rama)
                        break
                # Caso no especial
                print(f"largo camino rama {largo_rama}")
                largos_ramas.append(largo_rama)
                break
            # Si no es un endpoint sigue avanzando por el grafo
            else:
                print(f"Visitando Nodo: {nodo_actual}")
                #print("Sumando camino")
                largo_rama += 1
                vecinos = vecinos_conectados(mapa, nodo_actual)
                vecino = vecinos.pop()
                while vecino in visitados:
                    vecino = vecinos.pop()
                nodo_actual = vecino
                stack.append(nodo_actual)
                visitados.append(nodo_actual)
        # Una vez que ya llego al endpoint se devuelve por el grafo por los visitados
        # hasta que el nodo no sea un endpoint
        while True:
            nodo_actual = stack.pop()
            if is_end_point(mapa, nodo_actual, visitados):
                #print(f"Hechando hacia atras {nodo_actual}")
                largo_rama -= 1

                # Si es que se devuelve hasta el nodo inicial retorna los largos encontrados
                # y termina el algoritmo
                if nodo_actual == id_nodo_inicial:
                    return largos_ramas
            else:
                stack.append(nodo_actual)
                break
        endpoint = None

def is_end_point(mapa, id_nodo, id_visitados):
    vecinos_con = vecinos_conectados(mapa, id_nodo)
    for id_nodo_vecino in vecinos_con:
        if id_nodo_vecino not in id_visitados:
            return False
    return True


def vecinos_conectados(mapa, id_nodo):
    vecinos_con = []
    nodo = mapa.nodos[id_nodo]
    ids_vecinos_nodo = nodo.vecinos
    for conexion in nodo.conexiones:
        if conexion.camino:
            vecino = conexion.id_nodo_2
            vecinos_con.append(vecino)
    return(vecinos_con)


mapa.conexiones[("1", "5")].camino = True
mapa.conexiones[("5", "1")].camino = True
mapa.conexiones[("5", "6")].camino = True
mapa.conexiones[("6", "2")].camino = True
mapa.conexiones[("6", "11")].camino = True
mapa.conexiones[("6", "11")].camino = True
mapa.conexiones[("11", "16")].camino = True
mapa.conexiones[("16", "15")].camino = True
mapa.conexiones[("15", "10")].camino = True
mapa.conexiones[("10", "9")].camino = True
mapa.conexiones[("10", "5")].camino = True
mapa.conexiones[("16", "21")].camino = True
mapa.conexiones[("21", "22")].camino = True
mapa.conexiones[("22", "27")].camino = True
mapa.conexiones[("27", "28")].camino = True
mapa.conexiones[("28", "23")].camino = True
mapa.conexiones[("23", "18")].camino = True
mapa.conexiones[("18", "17")].camino = True
mapa.conexiones[("17", "22")].camino = True


#usuario = Usuario("juanito")
#camino = Camino(usuario)
"""
mapa.anadir_camino("0", "1")
#mapa.anadir_camino("1", "5")
#mapa.anadir_camino("0", "4")
#mapa.anadir_camino("4", "9")
#mapa.anadir_camino("9", "10")
#mapa.anadir_camino("10", "5")
"""
#a = set(back_track_mapa(mapa, "0"))


largos = set()
for id_nodo in mapa.nodos:
    a = set(back_track_mapa(mapa, id_nodo))
    largos = (largos | a)


print(max(largos))
