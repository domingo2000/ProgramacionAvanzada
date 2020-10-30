# parametros

# Flechas
VELOCIDAD_FLECHA = 200
VELOCIDAD_FLECHA_DORADA = 1.5 * VELOCIDAD_FLECHA
PUNTOS_FLECHA = 10

PROB_NORMAL = 0.5
PROB_FLECHA_X2 = 0.2
PROB_FLECHA_DORADA = 0.2
PROB_FLECHA_HIELO = 0.1

DURACION_EFECTO_HIELO = 0.2
TASA_REDUCCION_VELOCIDAD_HIELO = 0.5


# Combos
COMBO_INCIAL = 0
AUMENTO_COMBO = 1
VALOR_COMBO_ERRADO = 0

# Niveles
NIVELES = {
    "Principiante": {
        "duracion": 30,
        "tiempo_entre_pasos": 1,
        "aprobacion": 30
    },
    "Aficionado": {
        "duracion": 45,
        "tiempo_entre_pasos": 0.5,
        "aprobacion": 50
    },
    "Maestro Cumbia": {
        "duracion": 20,
        "tiempo_entre_pasos": 0.5,
        "aprobacion": 70
    }
}


# Calculo de puntaje
MULTIPLCIADOR_APROBACION = 100
MULT_FLECHA_X2 = 2
MUTL_FLECHA_DORADA = 10

# Tienda
DINERO_INCIAL = 1000
PRECIO_PINGUIRIN = 500
DINERO_TRAMPA = 1000
# Ranking
CANTIDAD_RANKING = 7

# Teclas Juego
FLECHA_ARRIBA = "w"
FLECHA_ABAJO = "s"
FLECHA_DERECHA = "d"
FLECHA_IZQUIERDA = "a"

# Dimensiones
ALTO_FLECHA = 50
ALTO_CAPTURA = 50

CANCIONES = {
    "Shingeki": ["songs", "cancion_1.wav"],
    "Cumbia": ["songs", "cancion_2.wav"]
}

IMAGENES_FLECHA = {
    "izquierda_hielo": ["sprites", "flechas", "left_1.png"],
    "derecha_hielo": ["sprites", "flechas", "right_1.png"],
    "arriba_hielo": ["sprites", "flechas", "up_1.png"],
    "abajo_hielo": ["sprites", "flechas", "down_1.png"],
    "izquierda_dorada": ["sprites", "flechas", "left_2.png"],
    "derecha_dorada": ["sprites", "flechas", "right_2.png"],
    "arriba_dorada": ["sprites", "flechas", "up_2.png"],
    "abajo_dorada": ["sprites", "flechas", "down_2.png"],
    "izquierda_normal": ["sprites", "flechas", "left_3.png"],
    "derecha_normal": ["sprites", "flechas", "right_3.png"],
    "arriba_normal": ["sprites", "flechas", "up_3.png"],
    "abajo_normal": ["sprites", "flechas", "down_3.png"],
    "izquierda_x2": ["sprites", "flechas", "left_4.png"],
    "derecha_x2": ["sprites", "flechas", "right_4.png"],
    "arriba_x2": ["sprites", "flechas", "up_4.png"],
    "abajo_x2": ["sprites", "flechas", "down_4.png"],
    "izquierda_5": ["sprites", "flechas", "left_5.png"],
    "derecha_5": ["sprites", "flechas", "right_5.png"],
    "arriba_5": ["sprites", "flechas", "up_5.png"],
    "abajo_5": ["sprites", "flechas", "down_5.png"],
    "izquierda_6": ["sprites", "flechas", "left_6.png"],
    "derecha_6": ["sprites", "flechas", "right_6.png"],
    "arriba_6": ["sprites", "flechas", "up_6.png"],
    "abajo_6": ["sprites", "flechas", "down_6.png"],
    "izquierda_7": ["sprites", "flechas", "left_7.png"],
    "derecha_7": ["sprites", "flechas", "right_7.png"],
    "arriba_7": ["sprites", "flechas", "up_7.png"],
    "abajo_7": ["sprites", "flechas", "down_7.png"],
    "izquierda_8": ["sprites", "flechas", "left_8.png"],
    "derecha_8": ["sprites", "flechas", "right_8.png"],
    "arriba_8": ["sprites", "flechas", "up_8.png"],
    "abajo_8": ["sprites", "flechas", "down_8.png"],
}

IMAGENES_PINGUINO = {
    "amarillo_tres_flechas": ["sprites", "pinguirin_amarillo", "amarillo_tres_flechas.png"],
    "celeste_tres_flechas": ["sprites", "pinguirin_celeste", "celeste_tres_flechas.png"],
    "morado_tres_flechas": ["sprites", "pinguirin_morado", "morado_tres_flechas.png"],
    "rojo_tres_flechas": ["sprites", "pinguirin_rojo", "rojo_tres_flechas.png"],
    "verde_tres_flechas": ["sprites", "pinguirin_verde", "verde_tres_flechas.png"],

    "amarillo_abajo_derecha": ["sprites", "pinguirin_amarillo", "amarillo_abajo_derecha.png"],
    "celeste_abajo_derecha": ["sprites", "pinguirin_celeste", "celeste_abajo_derecha.png"],
    "morado_abajo_derecha": ["sprites", "pinguirin_morado", "morado_abajo_derecha.png"],
    "rojo_abajo_derecha": ["sprites", "pinguirin_rojo", "rojo_abajo_derecha.png"],
    "verde_abajo_derecha": ["sprites", "pinguirin_verde", "verde_abajo_derecha.png"],

    "amarillo_abajo_izquierda": ["sprites", "pinguirin_amarillo", "amarillo_abajo_izquierda.png"],
    "celeste_abajo_izquierda": ["sprites", "pinguirin_celeste", "celeste_abajo_izquierda.png"],
    "morado_abajo_izquierda": ["sprites", "pinguirin_morado", "morado_abajo_izquierda.png"],
    "rojo_abajo_izquierda": ["sprites", "pinguirin_rojo", "rojo_abajo_izquierda.png"],
    "verde_abajo_izquierda": ["sprites", "pinguirin_verde", "verde_abajo_izquierda.png"],

    "amarillo_abajo": ["sprites", "pinguirin_amarillo", "amarillo_abajo.png"],
    "celeste_abajo": ["sprites", "pinguirin_celeste", "celeste_abajo.png"],
    "morado_abajo": ["sprites", "pinguirin_morado", "morado_abajo.png"],
    "rojo_abajo": ["sprites", "pinguirin_rojo", "rojo_abajo.png"],
    "verde_abajo": ["sprites", "pinguirin_verde", "verde_abajo.png"],

    "amarillo_arriba_derecha": ["sprites", "pinguirin_amarillo", "amarillo_arriba_derecha.png"],
    "celeste_arriba_derecha": ["sprites", "pinguirin_celeste", "celeste_arriba_derecha.png"],
    "morado_arriba_derecha": ["sprites", "pinguirin_morado", "morado_arriba_derecha.png"],
    "rojo_arriba_derecha": ["sprites", "pinguirin_rojo", "rojo_arriba_derecha.png"],
    "verde_arriba_derecha": ["sprites", "pinguirin_verde", "verde_arriba_derecha.png"],

    "amarillo_arriba_izquierda": ["sprites", "pinguirin_amarillo", "amarillo_arriba_izquierda.png"],
    "celeste_arriba_izquierda": ["sprites", "pinguirin_celeste", "celeste_arriba_izquierda.png"],
    "morado_arriba_izquierda": ["sprites", "pinguirin_morado", "morado_arriba_izquierda.png"],
    "rojo_arriba_izquierda": ["sprites", "pinguirin_rojo", "rojo_arriba_izquierda.png"],
    "verde_arriba_izquierda": ["sprites", "pinguirin_verde", "verde_arriba_izquierda.png"],

    "amarillo_arriba": ["sprites", "pinguirin_amarillo", "amarillo_arriba.png"],
    "celeste_arriba": ["sprites", "pinguirin_celeste", "celeste_arriba.png"],
    "morado_arriba": ["sprites", "pinguirin_morado", "morado_arriba.png"],
    "rojo_arriba": ["sprites", "pinguirin_rojo", "rojo_arriba.png"],
    "verde_arriba": ["sprites", "pinguirin_verde", "verde_arriba.png"],

    "amarillo_cuatro_flechas": ["sprites", "pinguirin_amarillo", "amarillo_cuatro_flechas.png"],
    "celeste_cuatro_flechas": ["sprites", "pinguirin_celeste", "celeste_cuatro_flechas.png"],
    "morado_cuatro_flechas": ["sprites", "pinguirin_morado", "morado_cuatro_flechas.png"],
    "rojo_cuatro_flechas": ["sprites", "pinguirin_rojo", "rojo_cuatro_flechas.png"],
    "verde_cuatro_flechas": ["sprites", "pinguirin_verde", "verde_cuatro_flechas.png"],

    "amarillo_derecha": ["sprites", "pinguirin_amarillo", "amarillo_derecha.png"],
    "celeste_derecha": ["sprites", "pinguirin_celeste", "celeste_derecha.png"],
    "morado_derecha": ["sprites", "pinguirin_morado", "morado_derecha.png"],
    "rojo_derecha": ["sprites", "pinguirin_rojo", "rojo_derecha.png"],
    "verde_derecha": ["sprites", "pinguirin_verde", "verde_derecha.png"],

    "amarillo_izquierda": ["sprites", "pinguirin_amarillo", "amarillo_izquierda.png"],
    "celeste_izquierda": ["sprites", "pinguirin_celeste", "celeste_izquierda.png"],
    "morado_izquierda": ["sprites", "pinguirin_morado", "morado_izquierda.png"],
    "rojo_izquierda": ["sprites", "pinguirin_rojo", "rojo_izquierda.png"],
    "verde_izquierda": ["sprites", "pinguirin_verde", "verde_izquierda.png"],

    "amarillo_neutro": ["sprites", "pinguirin_amarillo", "amarillo_neutro.png"],
    "celeste_neutro": ["sprites", "pinguirin_celeste", "celeste_neutro.png"],
    "morado_neutro": ["sprites", "pinguirin_morado", "morado_neutro.png"],
    "rojo_neutro": ["sprites", "pinguirin_rojo", "rojo_neutro.png"],
    "verde_neutro": ["sprites", "pinguirin_verde", "verde_neutro.png"]
}
TASA_REFRESCO = 0.01
DELAY_PASO = 100


TIEMPO_GRATIS = 10

if __name__ == "__main__":
    a = tuple(NIVELES["Principiante"].values())
    print(a)
