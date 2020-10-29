def buscar_info_artista(plataforma, artista_seleccionado):
    # Completar
    for nodo_genero in plataforma.raiz.hijos:
        for nodo_artista in nodo_genero.hijos:
            if nodo_artista.valor == artista_seleccionado:
                for nodo_album in nodo_artista.hijos:
                    album = nodo_album.valor
                    numero_canciones = len(nodo_album.hijos)
                    print(f"Álbum: {album}, {numero_canciones} cancion(es)")


def buscar_mejor_plataforma(genero, plataformas):
    mejor_plataforma = None
    cantidad_canciones_maxima = 0
    cantidad_canciones_genero = 0
    for plataforma in plataformas:
        nombre_plataforma = plataforma.raiz.valor
        for nodo_genero in plataforma.raiz.hijos:
            if nodo_genero.valor == genero:
                for nodo_album in nodo_genero.hijos:
                    for nodo_cancion in nodo_album.hijos:
                        cantidad_canciones_genero += 1
        if cantidad_canciones_genero > cantidad_canciones_maxima:
            mejor_plataforma = plataforma
            cantidad_canciones_maxima = cantidad_canciones_genero
        cantidad_canciones_genero = 0
    return mejor_plataforma


def buscar_artistas_parecidos(nombre_cancion, plataforma):
    # Completar
    pass


def crear_playlist(plataforma, genero_seleccionado, conceptos_canciones):
    # Completar
    pass
