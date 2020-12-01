class Comando:

    def __init__(self, nombre_comando, *args):
        self.nombre = nombre_comando
        if len(args) > 0:
            self.parametros = args
        else:
            self.parametros = None

    def __repr__(self):

        return f"({self.nombre}: {self.parametros})"