# Tarea 00: DCCombateNaval


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales
Para inciar el programa se debe correr el archivo main.py, y no los otros, pues los otros son funciones y clases necesarias para el funcionamiento del juego.

En el programa se implementó todo lo pedido para la tarea, en la consola se va mostrando las opciones que se tienen ingresar para ir moviendose entre menu y menu, y para poder jugar. En el menu de juego, cuando uno le achunta a un barco este se marca en el mapa y automaticamente empieza un nuevo turno, en caso contrario pasa el turno al oponente, quien al no achuntar a un barco pasa automaticamente al turno propio (por lo tanto hay mensajes como "Le achuntaste a un barco" o "Te toca denuevo", pues toda esta informacion se deduce del mapa de barcos que se muestra entre turno y turno). Por ultimo, se subio al repositorio un archivo texto.txt, el cual se me "colo", pues lo puse a ultimo minuto en un coomit probando algo con mi codigo.

## Cosas implementadas y no implementadas
### Inicio del programa:
* Menu de incio: Hecho completo, se encuentra en ``menus.py``
* Funcionalidades: Hecho completo
* Puntajes: Hecho completo, el menu de rankings se encuentra en ``menus.py``
### Flujo del juego:
* Menú de Juego: Hecho completo, se encuentra en ``menus.py``
* Tablero: Hecho completo
* Turnos: Hecho completo, pero como nota, no se muestran mensajes de que le achunto a un barco, sino que se repite el turno automaticamente, es decir si se repite el turno pero no se muestra un mensaje que lo diga
* Bombas: Hecho completo
* Barcos: Hecho completo, al iniciar la partida se crea un objeto de la clase `Partida`, la cual se encuentra en ``Main.py`` en el constructor ``__init__`` de esta clase se crean los tableros y se le insertan los barcos de ambos jugadores de manera aleatoria, hay un comentario en el codigo que explicita cuando se agregan los barcos al tablero, para hacerlo de forma aleatoria se usan coordenadas aleatorias con ``random`` hasta que haya una cantidad de barcos suficientes en cada lado del tablero.
* Oponente: Hecho completo

### Termino de juego:
* Fin del juego: Hecho completo
* Puntajes: Hecho completo, el codigo que calcula el puntajes se encuentra en la clase ``Partida``, la cual esta en el archivo ``clases.py``, y se implementa en el método ``calcular_puntaje(self)``, el cual lo asigna a un atributo del objeto ``Partida``, luego este puntaje se guarda con otro metodo de la misma clase el cual recibe una instancia de la clase partida y la direccion del archivo ``puntajes.txt``, para asi guardar el puntaje.

### Archivos
* Manejo de Archivo: Hecho completo, como se mencionó anteriormente se usa el metodo ``guardar_puntaje`` de la clase ``Partida`` para guardar el puntaje, este metodo se llama tanto cuando el jugador se rinde como si la partida termina en la función ``menu_de_juego``, que se encuentra en el archivo ``menus.py``.
Por otro lado el archivo se carga en la funcion ``menu_ranking``, que se encuentra también en ``menus.py``, ahi se lee el archivo, se ordenan los puntajes, y se muestra en consola en caso de que uno acceda a los rankings de puntaje desde el menu de inicio.


## Ejecución
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se deben tener los siguientes archivos en la misma carpeta que el archivo main.py:
1. funciones.py
2. menus.py
3. clases.py
4. parametros.py
5. puntajes.txt
6. tablero.py


## Librerías
### Librerías externas utilizadas
No se usaron librerías externas

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```funciones.py```: Contiene a ``lanzar_bomba``, junto con funciones ``coordenadas_bomba_{tipo de bomba}``, ``atacar_ coordenadas`` y ``coordenadas_en_mapa`` las cuales se encargan de al funcionalidad de las bombas al jugar. Ademas contiene la funcion ``ataque_oponente`` que se encarga de la funcionalidad de cuando ataca el oponente en vez del jugador, por ultimo contiene un par de funciones mas que validan el apodo y validan cierto uso de coordenadas para que estas esten dentro del mapa.
2. ```menus.py```: Esta contiene 3 funciones, una para el menu de incio, otra para el menu de juego, y otra para el menu de ranking de puntajes. en el archivo ``main.py`` se llama basicamente a la funcion ``menu_de_inicio`` y luego se siguen llamando otras funciones que en conunto forman todo el programa.
3. ``clases.py``: Esta contiene a la clase ``Partida`` la cual es un objeto que tiene como atributos la mayoria de los "estaods" de la partida, como los tableros, el puntaje obtenido en esa partida, la cantidad de barcos descubiertos, si es que ya se uso la bomba especial, entre otros.

## Supuestos y consideraciones adicionales
Los supuestos que realicé durante la tarea son los siguientes:

1. Siempre que se llene el tablero al iniciar la partida se tendra el tiempo suficiente para que la "aleatoridad" de coordenadas para llenar el tablero sea la suficiente para que no se repitan todo el tiempo las mismas coordenadas para fijar las bombas, dado que son artas casillas en general y pocos barcos. pero en caso de que sean muchas casillas y muchos barcos podria demorar un poco mas en que el random tire justo una coordenada que aun no tiene un barco.
2. El usuario que este usando la consola debe siempre estar fijandose en el mapa del tablero mostrado para saber que esta pasando, asi el se da cuenta de cuando ataca su oponente, cuando el repite turno, etc. pues no se muestran tantos mensajes dando informacion en la consola para mantener mayor orden.
3. Los archivos estan todos en la misma carpeta, sin hacer "sub carpetas".
