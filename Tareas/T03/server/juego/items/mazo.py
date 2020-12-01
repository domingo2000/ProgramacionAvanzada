from networking import interfaz_network


class Mazo(dict):

    def __init__(self, nombre_usuario):
        self.usuario = nombre_usuario
        self["madera"] = 0
        self["arcilla"] = 0
        self["trigo"] = 0
        super().__init__()

    def __setitem__(self, key, value):
        keys = {"madera", "arcilla", "trigo"}
        if key not in keys:
            raise KeyError("No existe la materia prima dada")

        #print(f"Enviando Comando: {key}: {value}: {self.usuario}")
        interfaz_network.send_command_to_all("update_resource", self.usuario, key, value)
        super().__setitem__(key, value)
        # Completar Enviar comando


if __name__ == "__main__":
    mazo = Mazo()
    mazo["madera"] += 5
    mazo["madera"] += 5
