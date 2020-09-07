from menus import DictMenu, MenuInicio, MenuPrincipal, MenuEntrenador

menus = DictMenu()
menu_inicio = MenuInicio()
menus[menu_inicio.nombre] = menu_inicio

while True:

    if menus.key == "Inicio":
        campeonato = menus.invocar()[0]
        menu_principal = MenuPrincipal(campeonato)
        menu_entrenador = MenuEntrenador(campeonato)
        menus[menu_principal.nombre] = menu_principal
        menus[menu_entrenador.nombre] = menu_entrenador
    else:
        menus.invocar()

print("FIN")
