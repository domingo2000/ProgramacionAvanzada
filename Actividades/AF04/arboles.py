class Nodo:
    def __init__(self, tipo, valor, padre):
        self.tipo = tipo
        self.valor = valor
        self.padre = padre

        self.hijos = []


class PlataformaMusical:
    def __init__(self, nombre_plataforma):
        self.raiz = Nodo("plataforma", nombre_plataforma, None)

    def agregar_cancion(self, info_cancion):
        cancion = info_cancion["nombre"]
        artista = info_cancion["artista"]
        album = info_cancion["album"]
        genero = info_cancion["genero"]
        genero_encontrado = False
        for nodo_genero in self.raiz.hijos:
            valor = nodo_genero.valor
            if valor == genero:
                genero_encontrado = True
                break
        if genero_encontrado:
            artista_encontrado = False
            for nodo_artista in nodo_genero.hijos:
                valor = nodo_artista.valor
                if valor == artista:
                    artista_encontrado = True
                    break
            if artista_encontrado:
                album_encontrado = False
                for nodo_album in nodo_artista.hijos:
                    valor = nodo_album.valor
                    if valor == album:
                        album_encontrado = True
                        break
                if album_encontrado:
                    print("Album Encontrado")
                    cancion_encontrada = False
                    for nodo_cancion in nodo_album.hijos:
                        valor = nodo_cancion.valor
                        if valor == cancion:
                            cancion_encontrada = True
                            break
                    if cancion_encontrada:
                        print("Ya existe el nodo de la cancion")
                    else:
                        nodo_cancion = Nodo("cancion", f"{cancion}", nodo_album)
                        nodo_album.hijos.append(nodo_cancion)
                else:
                    print("Agregando Album")
                    nodo_album = Nodo("album", f"{album}", nodo_artista)
                    nodo_artista.hijos.append(nodo_album)
                    nodo_cancion = Nodo("cancion", f"{cancion}", nodo_album)
                    nodo_album.hijos.append(nodo_cancion)
            else:
                nodo_artista = Nodo("artista", f"{artista}", nodo_genero)
                nodo_genero.hijos.append(nodo_artista)
                nodo_album = Nodo("album", f"{album}", nodo_artista)
                nodo_artista.hijos.append(nodo_album)
                nodo_cancion = Nodo("cancion", f"{cancion}", nodo_album)
                nodo_album.hijos.append(nodo_cancion)
        else:
            nodo_genero = Nodo("genero", f"{genero}", self.raiz)
            self.raiz.hijos.append(nodo_genero)
            nodo_artista = Nodo("artista", f"{artista}", nodo_genero)
            nodo_genero.hijos.append(nodo_artista)
            nodo_album = Nodo("album", f"{album}", nodo_artista)
            nodo_artista.hijos.append(nodo_album)
            nodo_cancion = Nodo("cancion", f"{cancion}", nodo_album)
            nodo_album.hijos.append(nodo_cancion)

    def armar_arbol(self, informacion_canciones):
        print(f" Armando plataforma {self.raiz.valor} ".center(80, "*"))

        for cancion in informacion_canciones:
            self.agregar_cancion(cancion)

    def visualizar_arbol(self, nodo, margen=0):
        print(f'{"  " * margen}{nodo.valor}')
        if len(nodo.hijos) > 0:
            margen += 1
            for hijo in nodo.hijos:
                self.visualizar_arbol(hijo, margen)
