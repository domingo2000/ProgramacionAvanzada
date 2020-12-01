def generar_dict_costos(parametro_costo, nombre):
    dict_costo = {"madera": int, "arcilla": int, "trigo": int}
    nombre = nombre.upper()
    for key in parametro_costo:
        if key == f"CANTIDAD_MADERA_{nombre}":
            dict_costo["madera"] = parametro_costo[key]
        elif key == f"CANTIDAD_TRIGO_{nombre}":
            dict_costo["trigo"] = parametro_costo[key]
        elif key == f"CANTIDAD_ARCILLA_{nombre}":
            dict_costo["arcilla"] = parametro_costo[key]

    return dict_costo

if __name__ == "__main__":
    import json
    with open("parametros.json") as file:
        P = json.load(file)
        COSTOS = P["costos"]
        COSTO_DESARROLLO = COSTOS["carta_desarrollo"]

    print(generar_dict_costos(COSTO_DESARROLLO))