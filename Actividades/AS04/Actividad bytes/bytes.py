import os


def reparar_imagen(ruta_entrada, ruta_salida):
    #--- COMPLETAR ---#
    byte_nuevo = bytearray()
    with open(ruta_entrada, "rb") as file:
        datos = file.read()
        byte_nuevo = bytearray()
        tamaño_chunk = 32
        for i in range(0, len(datos), tamaño_chunk):
            chunk = bytearray(datos[i:i+tamaño_chunk])
            chunk = chunk[0:16]
            if chunk[0] == 1:
                chunk = chunk[::-1]
            byte_nuevo.extend(chunk)

    with open(ruta_salida, "wb") as file:
        file.write(byte_nuevo)

#--- NO MODIFICAR ---#
def reparar_imagenes(carpeta_entrada, carpeta_salida):
    for filename in os.listdir(os.path.join(os.getcwd(), carpeta_entrada)):
        reparar_imagen(
            os.path.join(os.getcwd(), carpeta_entrada, filename),
            os.path.join(os.getcwd(), carpeta_salida, filename)
        )


if __name__ == '__main__':
    try:
        reparar_imagenes('corruptas', 'caratulas')
        print("Imagenes reparadas (recuerda revisar que se carguen correctamente)")
    except Exception as error:
        print(f'Error: {error}')
        print("No has podido reparar las caratulas :'c")
