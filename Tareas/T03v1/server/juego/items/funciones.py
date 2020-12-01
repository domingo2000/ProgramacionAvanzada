def crear_diccionario_costos(data_costos):
    costos = list(data_costos.values())
    dict_costo = {"madera": costos[0], "trigo": costos[1], "arcilla": costos[2]}
    return dict_costo


if __name__ == "__main__":
    import json
    with open("parametros.json") as file:
        data = json.load(file)
    data_costos = data["costos"]
    costo = crear_diccionario_costos(data_costos["carta_desarrollo"])
    costo = crear_diccionario_costos(data_costos["carretera"])
    print(costo)
