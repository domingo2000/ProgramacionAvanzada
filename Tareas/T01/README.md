
# Tarea 1: DCC Cumbre Olimpica :trophy::trophy:


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

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

* Manejo de archivos<sub>5</sub> :
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```archivo.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```archivo.ext``` en ```ubicación```
2. ```directorio``` en ```ubicación```
3. ...


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```librería_1```: ```función() / módulo```
2. ```librería_2```: ```función() / módulo``` (debe instalarse)
3. ...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```librería_1```: Contiene a ```ClaseA```, ```ClaseB```, (ser general, tampoco es necesario especificar cada una)...
2. ```librería_2```: Hecha para <insertar descripción **breve** de lo que hace o qué contiene>
3. ...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <Descripción/consideración 1 y justificación del por qué es válido/a> 
2. <Descripción/consideración 2 y justificación del por qué es válido/a>
3. ...

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>


-------



**EXTRA:** si van a explicar qué hace específicamente un método, no lo coloquen en el README mismo. Pueden hacerlo directamente comentando el método en su archivo. Por ejemplo:

```python
class Corrector:

    def __init__(self):
          pass

    # Este método coloca un 6 en las tareas que recibe
    def corregir(self, tarea):
        tarea.nota  = 6
        return tarea
```

Si quieren ser más formales, pueden usar alguna convención de documentación. Google tiene la suya, Python tiene otra y hay muchas más. La de Python es la [PEP287, conocida como reST](https://www.python.org/dev/peps/pep-0287/). Lo más básico es documentar así:

```python
def funcion(argumento):
    """
    Mi función hace X con el argumento
    """
    return argumento_modificado
```
Lo importante es que expliquen qué hace la función y que si saben que alguna parte puede quedar complicada de entender o tienen alguna función mágica usen los comentarios/documentación para que el ayudante entienda sus intenciones.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<link de código>: este hace \<lo que hace> y está implementado en el archivo <nombre.py> en las líneas <número de líneas> y hace <explicación breve de que hace>



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).
