# Tarea 01: DCCumbre Olímpica

## Consideraciones generales :octocat:

Entrega_Tarea_temprana:
EL funcionamiento general es a traves de los menus de interacción con el usuario, los cuales tendrán acceso al campeonato, que contendrá todos los datos necesarios para maneajar la simulación.

La tarea usa un diccionario de menus para moverse de menu en menu y poder volver atras en varios de los menus.
Para ejecutar la tarea se debe correr el archivo main.py
(Se asuma que todos los archivos estan en la misma carpeta)

### Cosas implementadas y no implementadas :white_check_mark: :x:

* <Nombre item pauta<sub>1</sub>>: Hecha completa
* <Nombre item pauta<sub>2</sub>>: Me faltó hacer <insertar qué cosa faltó>
    * <Nombre subitem pauta<sub>2.1</sub>>: Hecha completa 
    * <Nombre subitem pauta<sub>2.2</sub>>: Me faltó hacer <insertar qué cosa faltó>
    * ...
* <Nombre item pauta<sub>3</sub>>: Me faltó hacer <insertar qué cosa faltó>
* ...
* <Nombre item pauta<sub>n</sub>>: Me faltó hacer <insertar qué cosa faltó>

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
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

1. ```clases_simulacion```: Contiene a ```Delegacion```, ```IEEEsport(Delegacion)```, ```DCCrotona(Delegacion)```, ```Deportista```
2. ```campeonato```: Contiene a ```Campeonato```
3. ```lectura_datos```: Contiene funciones para leer los archivos csv, y la funcion ``leer_bool(string)`` que sirve para transformar un string que dice "True" o "False" en ``True`` y ``False`` respectivamente
4. ```menus```: Contiene a ```Menu(ABC)``` que es una clase abstracta para implementar otros menus, ``MenuInicio``, ``MenuPrincipal``, ``MenuEntrenador`` que heredan de ``Menu`` y la clase ``MenuDict(dict)`` la cual es un diccionario de menus que sirve para moverse entre los menus que estan dentro del diccionario
5. ```parametros```: contiene todos los parametros usados para la ejecucion de la tarea

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
