# Sistema de Gestión de Papelería

Sistema en Python que administra el inventario y los*proveedores de una papelería, combinando un menú de acceso y gestión de archivos por terminal con una interfaz gráfica (Tkinter) para visualizar y editar las tablas del negocio.

## Tabla de contenidos

- [Descripción general](#-descripción-general)
- [Requisitos](#️-requisitos)
- [Instalación y ejecución](#-instalación-y-ejecución)
- [Inicio de sesión y bienvenida](#-inicio-de-sesión-y-bienvenida)
- [Tecnologías utilizadas](#-tecnologías-utilizadas)
- [Autor](#-autor)

## Descripción general

El sistema está compuesto por dos archivos principales:
 `main.py`| Controla el acceso (login) y la gestión de archivos de texto desde la terminal 
 `papeleria_app.py`  Contiene la interfaz gráfica (Tkinter) con las tablas de Inventario y Proveedores

`main.py` es el punto de entrada del programa: primero corre el inicio de sesión y el menú por consola, y desde ahí mismo se puede abrir la ventana gráfica.

La carpeta `archivos_papeleria/`*no se sube al repositorio — se genera sola la primera vez que corres `main.py`.


## Requisitos

- Python 3.10 o superior
  *Tkinter (incluido con Python; en Linux puede requerir instalarse aparte: `sudo apt install python3-tk`)

No se necesita instalar ninguna librería externa con `pip` — todo el proyecto usa únicamente módulos estándar de Python (`os`, `time`, `tkinter`).



## Instalación y ejecución

1. Clona o descarga este repositorio.
2. Abre una terminal dentro de la carpeta del proyecto.
3. Ejecuta:

   ```bash
   python3 main.py
   ```

4. Sigue las instrucciones en pantalla (inicio de sesión → menú principal).


## Inicio de sesión y bienvenida

Al ejecutar `main.py`, el programa solicita un usuario y contraseña para continuar. Una vez validado el acceso:

1. Se pide un nombre y se imprime un mensaje de bienvenida, construido con operadores de *string*:
   - Concatenación con `+`
   - Repetición de caracteres con `*` (para las líneas decorativas)
2. Se ejecuta una función que simula la carga del sistema, mostrando puntos suspensivos durante un máximo de 5 segundos.


## Tecnologías utilizadas

- Python 3
- Tkinter / ttk — interfaz gráfica
- os — manejo de carpetas y archivos
- time — simulación de carga del sistema



## Autor

**AFML**
Proyecto desarrollado como parte de la materia de Fundamentos de Programación.
