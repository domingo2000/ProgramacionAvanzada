# PARAMETROS

IMAGENES = {
    "imagen_inicio": ["sprites", "logo.png"],
    "imagen_fondo": ["sprites", "fondos", "fondo.png"],
    "imagen_flecha_izquerda_1": ["sprites", "flechas", "left_1.png"],
    "imagen_flecha_derecha_1": ["sprites", "flechas", "right_1.png"],
    "imagen_flecha_arriba_1": ["sprites", "flechas", "up_1.png"],
    "imagen_flecha_abajo_1": ["sprites", "flechas", "down_1.png"],

    "imagen_flecha_izquerda_2": ["sprites", "flechas", "left_2.png"],
    "imagen_flecha_derecha_2": ["sprites", "flechas", "right_2.png"],
    "imagen_flecha_arriba_2": ["sprites", "flechas", "up_2.png"],
    "imagen_flecha_abajo_2": ["sprites", "flechas", "down_2.png"],

    "imagen_flecha_izquerda_3": ["sprites", "flechas", "left_3.png"],
    "imagen_flecha_derecha_3": ["sprites", "flechas", "right_3.png"],
    "imagen_flecha_arriba_3": ["sprites", "flechas", "up_3.png"],
    "imagen_flecha_abajo_3": ["sprites", "flechas", "down_3.png"],

    "imagen_flecha_izquerda_4": ["sprites", "flechas", "left_4.png"],
    "imagen_flecha_derecha_4": ["sprites", "flechas", "right_4.png"],
    "imagen_flecha_arriba_4": ["sprites", "flechas", "up_4.png"],
    "imagen_flecha_abajo_4": ["sprites", "flechas", "down_4.png"],

    "imagen_flecha_izquerda_5": ["sprites", "flechas", "left_5.png"],
    "imagen_flecha_derecha_5": ["sprites", "flechas", "right_5.png"],
    "imagen_flecha_arriba_5": ["sprites", "flechas", "up_5.png"],
    "imagen_flecha_abajo_5": ["sprites", "flechas", "down_5.png"],
}

# Parametros Tamaño ventanas
TAMANO_VENTANAS = {
    "ventana_inicio": [500, 500],
    "ventana_ranking": [500, 500],
    "ventana_juego": [900, 630]
}

UBICACION_VENTANAS = {
    "ventana_inicio": [100, 100],
    "ventana_ranking": [100, 100],
    "ventana_juego": [100, 100]
}

# Propiedades Graficas
TASA_DE_REFRESCO = 0.01
# Parametros Flechas
DIRECCIONES = ["derecha", "izquerda", "arriba", "abajo"]
ALTURA_INICIAL_FLECHA = 100
VELOCIDAD_FLECHA = 100
PUNTOS_FLECHA = 1
# Flecha Normal
PROB_NORMAL = 0.5
# Flecha x2
PROB_FLECHA_X2 = 0.2
# Flecha Dorada
PROB_FLECHA_DORADA = 0.1
VELOCIDAD_FLECHA_DORADA = 1.5 * VELOCIDAD_FLECHA
PUNTOS_FLECHA_DORADA = 10 * PUNTOS_FLECHA
# Flecha Hielo
PROB_FLECHA_HIELO = 0.2
REDUCCION_VELOCIDAD_HIELO = 0.2
