from collections import namedtuple
from copy import deepcopy


class BolsilloCriaturas(list):

    def append(self, criatura):
        if len(self) < 6:
            super().append(criatura)
        else:
            print("Error: Ha llegado al limite de creaturas")

    def cantidad_criaturas_estrella(self):
        cantidad_estrallas = 0
        for creatura in self:
            suma_puntos = creatura.hp_base + creatura.atk + creatura.sp_atk + \
                          creatura.defense
            if suma_puntos > 400:
                cantidad_estrallas += 1
        return cantidad_estrallas

    def __add__(self, bolsillo_enemigo):
        bolsillo_enemigo = sorted(bolsillo_enemigo, key=lambda criatura: criatura.atk + criatura.sp_atk)
        self = sorted(self, key=lambda criatura: criatura.atk + criatura.sp_atk)
        creatura_recibida = bolsillo_enemigo.pop(0)
        creatura_dada = self.pop()
        bolsillo_enemigo.append(creatura_dada)
        self.append(creatura_recibida)



if __name__ == '__main__':
    # NO MODIFICAR
    # El siguiente codigo te ayudara a hacer debugging,
    # simplemente ejecútalo para ver cómo vas

    # Criaturas de prueba
    # (Se deja hp_base por simplicidad)
    Criatura = namedtuple(
        "Criatura",
        ["nombre", "tipo", "hp_base", "atk", "sp_atk", "defense"],
    )
    criaturas_de_prueba = [
        Criatura("Cristian", "Water", 44, 48, 50, 65),
        Criatura("María José", "Fire", 78, 84, 109, 78),
        Criatura("Antonio", "Poison", 40, 60, 31, 30),
        Criatura("Joaquín", "Grass", 60, 62, 80, 63),
        Criatura("Dani", "Normal", 110, 160, 80, 110),
        Criatura("Tomás", "Rock", 35, 60, 40, 44),
    ]

    # Bolsillo de prueba
    bolsillo = BolsilloCriaturas()
    print("El bolsillo debería tener 0 criaturas")
    print(f"Tiene {len(bolsillo)} criaturas")
    # print(bolsillo)
    print()

    # Aquí se prueba si el método append esta correctamente implmentado
    for criatura in criaturas_de_prueba:
        bolsillo.append(criatura)
    print("El bolsillo debería tener 6 criaturas")
    print(f"El bolsillo tiene... {len(bolsillo)} criaturas")
    # print(bolsillo)
    print()

    bolsillo.append(Criatura("Benja", "Electric", 50, 60, 120, 95))
    print(f"(Deberías ver un mensaje de error porque no puedes agregar una séptima criatura)")
    print(f"El bolsillo tiene... {len(bolsillo)} criaturas")
    # print(bolsillo)
    print()

    print("El bolsillo debería tener 1 criatura estrella")
    n = bolsillo.cantidad_criaturas_estrella()
    if type(n) is int:
        print(f"El bolsillo tiene... {n} criaturas estrella")
    else:
        print("El método cantidad_criaturas_estrella aún no esta completado correctamente")
    print()

    # Bolsillo enemigo de prueba
    bolsillo_enemigo = deepcopy(bolsillo)
    bolsillo + bolsillo_enemigo
    contador_fuerte = len([criatura for criatura in bolsillo if criatura.nombre == "Dani"])
    contador_debil = len([criatura for criatura in bolsillo if criatura.nombre == "Antonio"])
    if contador_fuerte == 2 and contador_debil == 0:
        print("Método __add__ de Bolsillo: OK")
    else:
        print("El método __add__ aún no esta completado correctamente")
