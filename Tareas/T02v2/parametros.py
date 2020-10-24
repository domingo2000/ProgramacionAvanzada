# PARAMETROS

IMAGENES = {
    "imagen_inicio": ["sprites", "logo.png"],
    "imagen_fondo": ["sprites", "fondos", "fondo.png"],
    "imagen_flecha_izquierda_1": ["sprites", "flechas", "left_1.png"],
    "imagen_flecha_derecha_1": ["sprites", "flechas", "right_1.png"],
    "imagen_flecha_arriba_1": ["sprites", "flechas", "up_1.png"],
    "imagen_flecha_abajo_1": ["sprites", "flechas", "down_1.png"],

    "imagen_flecha_izquierda_2": ["sprites", "flechas", "left_2.png"],
    "imagen_flecha_derecha_2": ["sprites", "flechas", "right_2.png"],
    "imagen_flecha_arriba_2": ["sprites", "flechas", "up_2.png"],
    "imagen_flecha_abajo_2": ["sprites", "flechas", "down_2.png"],

    "imagen_flecha_izquierda_3": ["sprites", "flechas", "left_3.png"],
    "imagen_flecha_derecha_3": ["sprites", "flechas", "right_3.png"],
    "imagen_flecha_arriba_3": ["sprites", "flechas", "up_3.png"],
    "imagen_flecha_abajo_3": ["sprites", "flechas", "down_3.png"],

    "imagen_flecha_izquierda_4": ["sprites", "flechas", "left_4.png"],
    "imagen_flecha_derecha_4": ["sprites", "flechas", "right_4.png"],
    "imagen_flecha_arriba_4": ["sprites", "flechas", "up_4.png"],
    "imagen_flecha_abajo_4": ["sprites", "flechas", "down_4.png"],

    "imagen_flecha_izquierda_5": ["sprites", "flechas", "left_5.png"],
    "imagen_flecha_derecha_5": ["sprites", "flechas", "right_5.png"],
    "imagen_flecha_arriba_5": ["sprites", "flechas", "up_5.png"],
    "imagen_flecha_abajo_5": ["sprites", "flechas", "down_5.png"],

    "imagen_flecha_izquierda_6": ["sprites", "flechas", "left_6.png"],
    "imagen_flecha_derecha_6": ["sprites", "flechas", "right_6.png"],
    "imagen_flecha_arriba_6": ["sprites", "flechas", "up_6.png"],
    "imagen_flecha_abajo_6": ["sprites", "flechas", "down_6.png"],

    "imagen_flecha_izquierda_7": ["sprites", "flechas", "left_7.png"],
    "imagen_flecha_derecha_7": ["sprites", "flechas", "right_7.png"],
    "imagen_flecha_arriba_7": ["sprites", "flechas", "up_7.png"],
    "imagen_flecha_abajo_7": ["sprites", "flechas", "down_7.png"],

    "imagen_flecha_izquierda_8": ["sprites", "flechas", "left_8.png"],
    "imagen_flecha_derecha_8": ["sprites", "flechas", "right_8.png"],
    "imagen_flecha_arriba_8": ["sprites", "flechas", "up_8.png"],
    "imagen_flecha_abajo_8": ["sprites", "flechas", "down_8.png"],

    "imagen_explosion_izquierda": ["sprites", "flechas", "boom_1.png"],
    "imagen_explosion_derecha": ["sprites", "flechas", "boom_4.png"],
    "imagen_explosion_arriba": ["sprites", "flechas", "boom_3.png"],
    "imagen_explosion_abajo": ["sprites", "flechas", "boom_2.png"],
}

# Parametros Tamaño ventanas
TAMANO_VENTANAS = {
    "ventana_inicio": [500, 500],
    "ventana_ranking": [500, 500],
    "ventana_juego": [900, 630],
    "ventana_nivel": [200, 500],
    "zona_captura": 50,
    "flecha": 50
}

UBICACION_VENTANAS = {
    "ventana_inicio": [100, 100],
    "ventana_ranking": [100, 100],
    "ventana_juego": [100, 100],
    "ventana_nivel": [50, 50]
}
# Colores
COLORES = {
    "ventana_nivel": "#D2B2F3",
    "zona_captura": "#99CCFF"
}
# Propiedades Graficas
TASA_DE_REFRESCO = 0.01 #En segundos

# Parametros Flechas
DIRECCIONES = ["izquierda", "arriba", "abajo", "derecha"]

FLECHA_ARRIBA = "w"
FLECHA_izquierda = "a"
FLECHA_ABAJO = "s"
FLECHA_DERECHA = "d"

ALTURA_INICIAL_FLECHA = 0
VELOCIDAD_FLECHA = 200
PUNTOS_FLECHA = 1
# Flecha Normal
PROB_NORMAL = 0.5
# Flecha x2
PROB_FLECHA_X2 = 0.2
PUNTOS_FLECHA_x2 = 2 * PUNTOS_FLECHA
# Flecha Dorada
PROB_FLECHA_DORADA = 0.1
VELOCIDAD_FLECHA_DORADA = 1.5 * VELOCIDAD_FLECHA
PUNTOS_FLECHA_DORADA = 10 * PUNTOS_FLECHA
# Flecha Hielo
PROB_FLECHA_HIELO = 0.2
REDUCCION_VELOCIDAD_HIELO = 0.2

# DELAY ANIMACIONES
DELAY_EXPLOSION = 10

# Parametros Niveles
NIVEL_PRINCIPIANTE = {
    "duracion": 30,
    "tiempo_entre_pasos": 1,
    "aprobacion_necesaria": 30,
}
NIVEL_AFICIONADO = {
    "duracion": 30,
    "tiempo_entre_pasos": 0.75,
    "aprobacion_necesaria": 30,
}
NIVEL_MAESTRO_CUMBIA = {
    "duracion": 30,
    "tiempo_entre_pasos": 0.5,
    "aprobacion_necesaria": 30,
}
