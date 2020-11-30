def generar_dict_costos(parametro_costo):
    dict_costo = {"madera": int, "arcilla": int, "trigo": int}
    for key in parametro_costo:
        if key == "CANTIDAD_MADERA_CARTA_DESARROLLO":
            dict_costo["madera"] = parametro_costo[key]
        elif key == "CANTIDAD_TRIGO_CARTA_DESARROLLO":
            dict_costo["trigo"] = parametro_costo[key]
        elif key == "CANTIDAD_ARCILLA_CARTA_DESARROLLO":
            dict_costo["arcilla"] = parametro_costo[key]

    return dict_costo

if __name__ == "__main__":
    import json
    with open("parametros.json") as file:
        P = json.load(file)
        COSTOS = P["costos"]
        COSTO_DESARROLLO = COSTOS["carta_desarrollo"]

    print(generar_dict_costos(COSTO_DESARROLLO))