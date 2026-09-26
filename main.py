# Fecha de creacion: 22/09/26
# Actualizacion: 24/09/26
# V1.2.0
# Autor: AFML

#se importa el modulo os y el modulo time
import os  # Para crear carpetas, listar archivos y verificar si existen
import time # Para simular el tiempo de espera de "carga"

# Importamos la aplicacion grafica ya construida (papeleria_app.py).
# Este import NO abre la ventana todavia, solo la deja lista para usarse
import papeleria_app


# Validamos el acceso con un usuario y contraseña 
USUARIO_VALIDO = "Dalis"
CONTRASENA_VALIDA = "123"

# En esta carpeta es donde se guardan y leen los archivos de texto del sistema
CARPETA_ARCHIVOS = "archivos_papeleria"



# Aquí se crean archivos de ejemplo si todavia no existen

def preparar_archivos_iniciales(): # Hacemos un def para que se pueda llamar esta funcion desde main() y no se ejecute automaticamente al importar el modulo
    # Si la carpeta no existe, la creamos
    if not os.path.exists(CARPETA_ARCHIVOS): # Usamos un if not para que solo se cree la carpeta si no existe todavia
        os.makedirs(CARPETA_ARCHIVOS) # Este comando crea la carpeta y subcarpetas si fueran necesarias

    # Primer diccionario en el que el nombre de archivo iguale el contenido inicial que va a tener
    archivos_ejemplo = {
        "bienvenida.txt": "Bienvenido al sistema de la papeleria.\n",
        "inventario_notas.txt": "Aqui puedes anotar observaciones del inventario.\n",
        "proveedores_notas.txt": "Aqui puedes anotar observaciones de los proveedores.\n",
        "historial.txt": "Historial de movimientos del sistema.\n",
    }

    # Recorremos el diccionario y creamos cada archivo SOLO si no existe todavia
    # (para no borrar accidentalmente algo que el usuario ya haya escrito)
    for nombre_archivo, contenido_inicial in archivos_ejemplo.items():
        ruta = os.path.join(CARPETA_ARCHIVOS, nombre_archivo)
        if not os.path.exists(ruta):
            # "w" = write (escribir desde cero, crea el archivo si no existe)
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(contenido_inicial)



# El mensaje de bienvenida usando operadores de string

def mostrar_bienvenida(nickname): # Se crea un def para que se pueda llamar esta funcion desde main() y no se ejecute automaticamente al importar el modulo
    linea_decorativa = "=" * 50 # el * repite "=" 50 veces 
    mensaje = "¡Hola, " + nickname.upper() + "! Bienvenido al sistema."  # el + une texto
    print(linea_decorativa)
    print(mensaje)
    print(linea_decorativa)



# Se simula una espera de carga de maximo 5 segundos

def simular_carga(segundos=3): # Ponemos el =3 para que si no se pasa un valor, por defecto sea 3 segundos
    segundos = min(segundos, 5)  # nos aseguramos de nunca pasar de 5 segundos
    print("Cargando el sistema", end="", flush=True) # El flush=True fuerza a que se muestre inmediatamente
    for _ in range(segundos): # se pone un _ porque no necesitamos el valor del contador, solo repetir la accion
        time.sleep(1) # pausa de 1 segundo real
        print(".", end="", flush=True) # va imprimiendo puntos sin saltar de linea
    print(" ¡Listo!\n")



# El inicio de sesion por terminal.
# Devuelve el nickname una vez que el usuario y la contraseña sean correctos

def iniciar_sesion():
    print("----- INICIO DE SESION -----")
    # Se repite hasta que el usuario y la contraseña sean correctos
    while True:
        usuario_ingresado = input("Usuario: ")
        contrasena_ingresada = input("Contraseña: ")

        if usuario_ingresado == USUARIO_VALIDO and contrasena_ingresada == CONTRASENA_VALIDA:
            print("Acceso concedido.\n")
            break
        else:
            print("Usuario o contraseña incorrectos. Intenta de nuevo.\n")

    # Ya dentro, pedimos el nickname para personalizar el saludo
    nickname = input("¿Cual es tu nombre?: ")
    mostrar_bienvenida(nickname)
    simular_carga(3) # Simulamos una carga de 3 segundos antes de entrar al menu principal
    return nickname


# Lista los archivos disponibles en la carpeta.
# Los muestra en pantalla como un diccionario numerado {numero: nombre}

def listar_archivos():
    archivos = os.listdir(CARPETA_ARCHIVOS) # nombres de todo lo que hay en la carpeta
    archivos_numerados = {}  # aqui el {} crea un diccionario vacio para ir guardando los archivos con su numero correspondiente
    for indice, nombre in enumerate(archivos, start=1): # Por indice y nombre, empezando a contar desde 1 (no desde 0)
        archivos_numerados[indice] = nombre # guardamos en el diccionario el numero como clave y el nombre del archivo como valor

    print("\n----- ARCHIVOS DISPONIBLES -----")
    for numero, nombre in archivos_numerados.items(): # items() devuelve una lista de tuplas (clave, valor) del diccionario, que podemos recorrer con un for
        print(f"  {numero}. {nombre}")

    return archivos_numerados # El return permite que la funcion devuelva el diccionario para que pueda ser usado en otras funciones (como leer_archivo() o escribir_en_archivo())


# Se abre y muestra el contenido de un archivo elegido por numero

def leer_archivo(): 
    archivos_numerados = listar_archivos()
    if not archivos_numerados:
        print("No hay archivos disponibles todavia.")
        return

    try: # Ponemos un try/except para capturar errores si la persona escribe algo que no sea un numero valido
        numero = int(input("¿Cual archivo quieres abrir? (numero): "))
        nombre_archivo = archivos_numerados[numero] # puede lanzar KeyError si no existe ese numero
        ruta = os.path.join(CARPETA_ARCHIVOS, nombre_archivo) # Ruta es la carpeta + el nombre del archivo

        with open(ruta, "r", encoding="utf-8") as archivo: # En este with, el archivo se abre y se cierra automaticamente al terminar el bloque y el encoding="utf-8" asegura que se lean correctamente los caracteres especiales
            contenido = archivo.read() # Usamos .read() para leer todo el contenido del archivo de una sola vez

        print(f"\n----- CONTENIDO DE '{nombre_archivo}' -----")
        print(contenido)
    # Excepts para capturar errores y mostrar mensajes al usuario en lo que se equivoca
    except ValueError:
        # Sale si la persona escribio texto en vez de un numero
        print("Error: debes escribir un numero de la lista, no texto.")
    except KeyError:
        # Sale si el numero no corresponde a ningun archivo listado
        print("Error: ese numero no corresponde a ningun archivo.")
    except FileNotFoundError:
        # Sale si el archivo fue borrado despues de listarlo
        print("Error: el archivo ya no existe en la carpeta.")


# Aqui se pide una fecha en formato dd/mm/aaaa y la devuelve como una tupla (dia, mes, año)

def pedir_fecha():
    while True:
        texto_fecha = input("Fecha (formato dd/mm/aaaa): ")
        try: # Se pone el try/except para capturar errores si la persona escribe algo que no sea un formato valido
            partes = texto_fecha.split("/")  # separa el texto donde esten las diagonales
            if len(partes) != 3: # Usamos len() para contar cuantas partes hay, si no son 3 (dia, mes, año) lanzamos un error
                raise ValueError # forzamos el error si no hay exactamente 3 partes

            dia, mes, año = int(partes[0]), int(partes[1]), int(partes[2]) # convertimos cada parte a entero, si no son numeros lanzara un ValueError automaticamente
            return (dia, mes, año)             # se devuelve como TUPLA (no se puede modificar despues)

        except ValueError:
            print("Formato invalido. Ejemplo correcto: 28/09/2026")


# Se agrega texto nuevo a un archivo ya existente

def escribir_en_archivo():
    archivos_numerados = listar_archivos() # archivos_numerados es un diccionario {numero: nombre} que devuelve listar_archivos()
    if not archivos_numerados:
        print("No hay archivos disponibles todavia.")
        return

    try: # Ponemos un try/except para capturar errores si la persona escribe algo que no sea un numero valido
        numero = int(input("¿En cual archivo quieres escribir? (numero): "))
        nombre_archivo = archivos_numerados[numero]
        ruta = os.path.join(CARPETA_ARCHIVOS, nombre_archivo) # ponemos otro .join() para unir la carpeta con el nombre del archivo y obtener la ruta completa

        texto_nuevo = input("Escribe el texto que quieres agregar: ")
        fecha_tupla = pedir_fecha() # se pide la fecha para dejar registro de cuando se modifico

        # el "a" = append (agregar al final, sin borrar lo que ya habia)
        with open(ruta, "a", encoding="utf-8") as archivo: # El with abre el archivo y lo cierra automaticamente al terminar el bloque, y el encoding="utf-8" asegura que se escriban correctamente los caracteres especiales
            archivo.write( # usamos .write() para escribir el texto en el archivo
                f"[Modificado el {fecha_tupla[0]:02d}/{fecha_tupla[1]:02d}/{fecha_tupla[2]}] {texto_nuevo}\n" # usamos el :02d para que el dia y mes siempre tengan 2 digitos, en la ultima no se pone :02d porque el año siempre tiene 4 digitos y no queremos que se recorte a 2
            )

        print("Texto agregado correctamente.")

    except ValueError:
        print("Error: debes escribir un numero de la lista, no texto.")
    except KeyError:
        print("Error: ese numero no corresponde a ningun archivo.")



# Se crea un archivo de texto nuevo desde cero

def crear_archivo():
    nombre_archivo = input("Nombre del nuevo archivo (ejemplo: notas2.txt): ").strip() # Hacemos uso de .strip() para quitar espacios al inicio y final del texto, por si la persona los pone accidentalmente

    if not nombre_archivo: # Si no se puso ningun nombre, mostramos un mensaje de error y salimos de la funcion con return
        print("Error: el nombre del archivo no puede estar vacio.")
        return # El return hace que la funcion termine y no se ejecute el resto del codigo

    # Si la persona no puso el .txt, se la agregamos automaticamente
    if not nombre_archivo.endswith(".txt"):
        nombre_archivo += ".txt" # el += es un atajo para concatenar texto

    ruta = os.path.join(CARPETA_ARCHIVOS, nombre_archivo) # La ruta completa del archivo es la carpeta + el nombre del archivo, usando os.path.join() para que funcione en cualquier sistema operativo

    if os.path.exists(ruta):
        print("Ya existe un archivo con ese nombre, elige otro.")
        return

    contenido_inicial = input("Escribe el contenido inicial del archivo: ")
    fecha_tupla = pedir_fecha()

    try:
        with open(ruta, "w", encoding="utf-8") as archivo: 
            archivo.write(f"Archivo creado el {fecha_tupla[0]:02d}/{fecha_tupla[1]:02d}/{fecha_tupla[2]}\n")
            archivo.write(contenido_inicial + "\n")

        print(f"Archivo '{nombre_archivo}' creado correctamente.")

    except OSError:
        # Cubre errores raros del sistema de archivos (permisos, nombre invalido, etc.)
        print("Error: no se pudo crear el archivo. Verifica que el nombre sea valido.")



# Mostramos el menu principal en formato de columnas

def mostrar_menu():
    print("\n" + "=" * 60)
    print("MENU PRINCIPAL - Sistema de Papeleria")
    print("=" * 60)
    # ":<30" fuerza un ancho fijo de 30 caracteres, para que las columnas queden alineadas
    print(f"{'1. Leer archivo':<30}{'2. Escribir en archivo':<30}")
    print(f"{'3. Crear archivo nuevo':<30}{'4. Listar archivos':<30}")
    print(f"{'5. Abrir aplicacion (ventana)':<30}{'6. Cambiar de usuario':<30}")
    print(f"{'7. Salir':<30}")
    print("=" * 60)


# Esta es la que controla el flujo completo del programa

def main():
    preparar_archivos_iniciales() # aseguramos que existan los 4 archivos de ejemplo
    nickname = iniciar_sesion() # login por terminal

    opcion = "" # Se queda vacio
    # El menu se repite (ciclo while) hasta que la persona elija "7" (Salir)
    while opcion != "7": # Mientras sea diferente a 7 sigue
        mostrar_menu()
        opcion = input(f"[{nickname}] Elige una opcion: ").strip()

        try:
            if opcion == "1":
                leer_archivo()
            elif opcion == "2":
                escribir_en_archivo()
            elif opcion == "3":
                crear_archivo()
            elif opcion == "4":
                listar_archivos()
            elif opcion == "5":
                print("Abriendo la aplicacion grafica...")
                app = papeleria_app.AppPapeleria()
                app.mainloop() # el programa se queda aqui hasta que cierres la ventana
            elif opcion == "6":
                print("\nCerrando sesion actual...\n")
                nickname = iniciar_sesion()
            elif opcion == "7":
                print("Cerrando el sistema. ¡Hasta luego!")
            else:
                # Atrapa cualquier numero fuera de rango o texto que no sea valido
                print("Opcion invalida, intenta de nuevo.")

        except Exception as error:
            # Red de seguridad general: si algo inesperado falla, se avisa el error pero el programa SIGUE corriendo, en vez de cerrarse de golpe
            print(f"Ocurrio un error inesperado: {error}")

# Punto de entrada: esto solo corre si ejecutas este archivo directamente
if __name__ == "__main__": # Python le pone a __name__ el valor especial "__main__"
    main()