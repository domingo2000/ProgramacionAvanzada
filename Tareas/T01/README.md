
# Tarea 1: DCC Cumbre Olimpica :trophy::trophy:

## Consideraciones generales 

Por la tarea hace la gran mayoria de las cosas que pide en el enunciado, corre fluidamente y no debería caerse durante que se corre. La tarea funciona por medio de un diccionario de menus el cual pertenece a la clase propia ``DictMenu`` . Esta tiene un atributo ``key`` que va cambiando al ir pasando de un menu a otro, por lo tanto el flujo general es de ir pasando de un menu a otro del diccionario, para ir mostrando las diferentes acciones del programa, estos menus contienen el campeonato y acceden a el para que el programa funcione de forma correcta segun las entradas del usuario.

P.D. : El archivo ``resultados.txt`` debe estar creado en la misma carpeta que se encuentra el ``main.py``, como esta subido en el repositorio de github de la entrega

### Cosas implementadas y no implementadas :white_check_mark: :x:

* :white_check_mark: Programacion Orientada a objetos<sub>1</sub>: Hecha completa.
	* :white_check_mark: Diagrama<sub>1.1</sub> :  El diagrama se encuentra en el repositorio ``T01``.
	* :white_check_mark: Definicion de clases, atributos y métodos<sub>1.2</sub> : La modelacion de las delegaciones y deportistas se encuentra en el archivo ``clases_simulacion.py``, mientras que los deportes se encuentran en el archivo ``deportes.py`` y el campeonato en el archivo ``campeonato.py`` los cuales contienen las clases abstractas e hijas modeladas en el diagrama de clases.

* :white_check_mark: Partidas<sub>2</sub>: Hecha completa
	*  :white_check_mark: Crear Partida<sub>2.1</sub> : La creación de la partida funciona correctamente, esta se encuentra en el archivo ``menus.py`` y lo hace la clase ``MenuInicio`` a través del atributo ``iniciar_nueva_partida()`` el cual se encarga de leer los datos, instanciar los deportistas, las delegaciones, asociar los deportistas y fijas cada entrenador a la delegación correspondiente. 
	*  :white_check_mark: Guardar<sub>2.2</sub> : La información se actualiza en el archivo resultados.txt el cual debe estar creado en la misma carpeta que el archivo ``mani.py`` como viene en el repositorio. este se sobreescribe cuando se empieza una nueva partida, por lo que si se sale del programa antes de iniciar una nueva partida quedará toda la información de la última competencia.

*  :white_check_mark: :x: Acciones<sub>3</sub>>: Me faltó hacer que la moral aumente al doble y disminuya al doble al premiarse las competencias. El resto esta hecho.
	* :white_check_mark: :x: Delegaciones <sub>3.1</sub> : Se puede hacer todo menos lo que se dijo anteriormente. La implementacion de la posibilidad de recuperacion está en el archivo ``clases_simulacion.py`` en la clase ``Delegación`` en el atributo ``sanar_lesiones`` el cual se encarga de sanar al deportista de manera correcta, y tiene un ponderador de costo que se sobreescribe para cobrar mas por lesion. En segundo lugar la implementacion de la habilidad especial se encuentra como atributo en las clases hijas ``IEEEsparta`` y ``DCCrotona`` en el mismo archivo, mediante el método ``utilizar_habilidad_especial`` y solo se puede usar una vez pues las delegaciones implementan un booleano para que esta no se pueda usar dos veces. En tercer lugar, los cobros de los costos se encuentran en diferentes partes, pero dentro de los metodos de las delegaciones los cuales realizan las acciones. Por último de los beneficios especiales si se implementa el pago doble por lesion y el entrenamiento ponderado de 1.7 los cuales funcionan ponderando las acciones de la clase padre ``Delegacion``, pero no se implementa la subida y disminucion doble de moral al ganar una competencia.
	* :white_check_mark: Deportistas <sub>3.2</sub> : Las acciones de los deportistas se encuentran en el archivo ``clases_simulacion.py`` que contiene la clase ``Deportista``. En primer lugar tiene el metodo ``entrenar`` para el entrenamiento. En segundo lugar, se calcula la probabilidad de lesión en el metodo ``lesionarse`` .
	* :white_check_mark: Competencia<sub>3.3</sub> : Se cumple todo lo pedido, asumiendo que el usuario puede enviar deportistas lesionados a competir, el calculo de la moral de la delegación se realiza con un getter de la clase ``Delegacion`` pues al llamar a la moral en cualquier parte del programa se recalcula basandose en el equipo actual de la delegación. Esta se muestra en la consola a traves de los menus. Como dato, hay medallas :moneybag::moneybag: echas con strings y copas :trophy: :trophy: hechas con strings cuando se ganan las competencias y cuando termina la DCCumbre.
* :white_check_mark: Consola<sub>4</sub> : La consola se modelo a través de un diccionario de menus como se explicó al principio de las consideraciones. En este diccionario se encuentran los menus de incio principal y de entrenador, los cuales corresponden a las clases ``MenuPrincipal``, ``MenuIncio``, ``MenuEntrenador`` respectivamente, y todas heredan de la clase abstracta ``Menu`` la cual modela la forma de mostrar los datos en consola de manera correcta.

* :white_check_mark: Manejo de archivos<sub>5</sub> : Se hace todo lo pedido en la pauta
	* :white_check_mark: Archivos CSV<sub>5.1</sub> : En el archivo ``lectura_datos`` se encuentran las funciones que leen los datos de los archivos ``.csv`` entregados, los cuales tienen que estar en la misma carpeta que el resto de los archivos del programa. Estos devuelven los datos en una forma practica para luego ser usados en el flujo del programa. Estas funciones se llaman en el menu de inicio al iniciar una nueva partida.
	* :white_check_mark: Parametros.py<sub>5.2</sub> : Los parametros se importan en diferentes archivos del programa, para no hardcodear ninguno. En el archivo ``parametros.py`` se encuentran todos los parametros pedidos, y hay comentarios que ayudan a ver que parametro corresponde a que además de los nombres descriptivos de cada parametro.
	* :white_check_mark: resultados.txt<sub>5.3</sub> : El archivo ``resultados.txt`` debe estar creado en la misma carpeta que el resto de los archivos para que este se escriba de manera correcta, puesto que el programa sobreescribe el archivo, pero no lo "crea" en caso de que al archivo no exista, no importa si el archivo ya contiene o no texto para que este se sobreescriba. En caso de cerrar el programa en la mitad de la ejecución se mostrarán los resultados hasta el dia en que se llegó de la DCCumbre. 
	
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```resultados.txt``` en ```T01``` que debe ser la misma carpeta que todos los archivos. Igual este viene en el repositorio de github, pero en caso de que no lo hayan copiado, debe estar creado al momento de la ejecución del programa.

## Librerías :books:
### Librerías externas utilizadas
No se utilizaron librerías externas, solo algunas built-in. Estas fueron

1. ```random```: ```random()``` y ``uniform()``
2. ```abc```: ``ABC`` y ``abstractmethod``

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```clases_simulacion```: Contiene a ``Delegacion(ABC)``, ``IEEEsparta(Delegacion)``, ``DCCrotona(Delegacion)`` las cuales modelan las delegaciones. Ademas contiene a ``Deportista`` la cual modela a los deportistas.
2. ```campeonato```: Contiene a ``Campeonato`` la cual se encarga de modelar el campeonato
3. ``deportes`` : Contiene a ``Deporte(ABC)``, ``Atletismo(Deporte)``, ``Ciclismo(Deporte)``,  ``Gimnacia(Deporte)`` y ``Natacion(Deporte)`` las cuales se encargan de modelar los deportes del campeonato
4. ``lectura_datos`` : Contiene varias funciones que se encargan de leer los archivos ``.csv`` o escribir y leer los archivos ``.txt`` para el archivo ``resultados.txt`` además contiene la función ``leer_bool(string)`` que sirve para leer un string que representa un booleano.
5.  ``menus`` : Contiene a ``Menu(ABC)``, junto con ``MenuInicio(Menu)``, ``MenuPrincipal(Menu)``, ``MenuEntrenador(Menu)`` los cuales modelas los menus que se muestran en consola. Además contiene a ``DictMenu(dict)`` el cual es un diccionario personalizado que contiene instancias de menu, que se encarga de mostrar el menu adecuado para las diferentes partes del programa segun las acciones de los otros menus.
6. ``imagenes_string`` : Contiene algunas funciones para imprimir una medalla y una copa hecha con strings, las cuales se muestran durante las simulaciones.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. El jugador puede enviar deportistas lesionados a competir, esto es válido porque en caso de que solo tenga deportistas lesionados igual debe competir, por lo que queda en sus manos discriminar en que condiciones envia a sus jugadores a competir/a> 
2. El jugador puede seguir entrenando aunque los stats de los deportistas estén al máximo, esto es valido porque aunque un stat esté al máximo, al entrenar igual se subirá la moral del deportista. Además se muestran todos los atributos de los deportistas, por lo que es trabajo del usuario el ver si ya no quiere gastar dinero en algo que no se puede seguir mejorando.


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://ascii.co.uk/art/: de esta página saque algunos strings para imprimir copas y medallas, esto igual se encuentra documentado en el archivo ``imagenes_string`` de forma espec+ifica.
