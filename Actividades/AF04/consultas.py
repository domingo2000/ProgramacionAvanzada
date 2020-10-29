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
    # Completar
    pass


def buscar_artistas_parecidos(nombre_cancion, plataforma):
    # Completar
    pass


def crear_playlist(plataforma, genero_seleccionado, conceptos_canciones):
    # Completar
    pass
