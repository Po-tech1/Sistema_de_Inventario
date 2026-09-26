# Fecha de creacion: 02/09/26
# Actualizacion: 24/09/26
# V1.4.0
# Autor: AFML

import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog # Messagebox son las ventanitas emergentes que solo muestran información, Simpledialog sí le pide algo a la persona

# Misma carpeta que usa main.py, para que los archivos exportados
# desde aqui tambien se puedan leer despues desde el menu de terminal
CARPETA_ARCHIVOS = "archivos_papeleria"


def _asegurar_carpeta_archivos():
    # Crea la carpeta de archivos si todavia no existe
    if not os.path.exists(CARPETA_ARCHIVOS):
        os.makedirs(CARPETA_ARCHIVOS)

# Generamos los numeros de ID "DAL-001", "DAL-002", "DAL-"

def formatear_id(numero):
    return f"DAL-{numero:03d}" # el :03d hace que siempre hayan solo 3 numeros, si no se rellena con 0

# Son nuestros datos pre-cargados

inventario = [
    {"id": formatear_id(1), "nombre": "Lapiz",     "stock": 30, "precio": 7.25,  "demanda": 8, "fecha_vencimiento": "N/A"},
    {"id": formatear_id(2), "nombre": "Borrador",  "stock": 20, "precio": 15.00, "demanda": 7, "fecha_vencimiento": "N/A"},
    {"id": formatear_id(3), "nombre": "Libreta",   "stock": 24, "precio": 34.00, "demanda": 6, "fecha_vencimiento": "N/A"},
    {"id": formatear_id(4), "nombre": "Cartulina", "stock": 33, "precio": 25.00, "demanda": 9, "fecha_vencimiento": "N/A"},
    {"id": formatear_id(5), "nombre": "Pegamento", "stock": 18, "precio": 15.00, "demanda": 4, "fecha_vencimiento": "2027-06-01"},
]

# El siguiente producto que se agregue toma este numero de ID en adelante
siguiente_id = 6

proveedores = {
    "Omar_Proveedor": [
        {"id": formatear_id(1), "producto": "Lapiz",     "precio_proveedor": 4.50},
        {"id": formatear_id(2), "producto": "Borrador",  "precio_proveedor": 8.00},
        {"id": formatear_id(3), "producto": "Libreta",   "precio_proveedor": 20.00},
        {"id": formatear_id(4), "producto": "Cartulina", "precio_proveedor": 15.00},
        {"id": formatear_id(5), "producto": "Pegamento", "precio_proveedor": 9.00},
    ],
    "Materiales_Chidos": [
        {"id": formatear_id(1), "producto": "Lapiz",     "precio_proveedor": 5.00},
        {"id": formatear_id(2), "producto": "Borrador",  "precio_proveedor": 7.50},
        {"id": formatear_id(3), "producto": "Libreta",   "precio_proveedor": 22.00},
        {"id": formatear_id(4), "producto": "Cartulina", "precio_proveedor": 13.50},
        {"id": formatear_id(5), "producto": "Pegamento", "precio_proveedor": 9.50},
    ],
}


# Funciones de logica

def nivel_demanda(demanda):
    # Clasifica la demanda
    if 1 <= demanda <= 4:
        return "Baja"
    elif 5 <= demanda <= 7:
        return "Media"
    else:
        return "Alta"


def umbral_alerta(nivel):
    # Stock minimo requerido segun el nivel de demanda.
    # Si el stock cae POR DEBAJO de este numero, se alerta en rojo (riesgo de quedarse sin producto)
    return {"Baja": 10, "Media": 20, "Alta": 30}[nivel]


def demanda_de_producto(nombre_producto):
    # Busca la demanda de un producto en el inventario
    for producto in inventario:
        if producto["nombre"] == nombre_producto:
            return producto["demanda"]
    return 0


def precio_minimo_por_producto():
    """Compara TODOS los proveedores y devuelve, para cada producto,
    el precio mas bajo encontrado entre todos ellos."""
    minimos = {}
    for lista_productos in proveedores.values():
        for item in lista_productos:
            nombre = item["producto"]
            precio = item["precio_proveedor"]
            if nombre not in minimos or precio < minimos[nombre]:
                minimos[nombre] = precio
    return minimos


# Interfaz grafica

class AppPapeleria(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestion - Papeleria")
        self.geometry("820x600")

        # Hacemos la barra superior: titulo + boton de ayuda, todo esto va arriba a la derecha
        barra_superior = ttk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=(10, 0))
        ttk.Label(
            barra_superior, text="Sistema de Gestion - Papeleria", font=("", 13, "bold")
        ).pack(side="left")
        ttk.Button(
            barra_superior, text="❓ Ayuda", command=self._mostrar_ayuda_alertas
        ).pack(side="right")

        # El Notebook son las tipo pestañas que se hacen
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_inventario = ttk.Frame(notebook)
        self.tab_proveedores = ttk.Frame(notebook)
        notebook.add(self.tab_inventario, text="Tabla de Inventario")
        notebook.add(self.tab_proveedores, text="Tabla de Proveedores")

        self._crear_tab_inventario()
        self._crear_tab_proveedores()

    # Borón de ayuda para metrica de alerta de stock

    def _mostrar_ayuda_alertas(self):
        mensaje = (
            "¿Como funciona la alerta de stock?\n\n"
            "Cada producto tiene un nivel de demanda (Baja, Media o Alta), "
            "segun un numero del 1 al 10:\n\n"
            "  •  Demanda 1-4  →  Baja\n"
            "  •  Demanda 5-7  →  Media\n"
            "  •  Demanda 8-10 →  Alta\n\n"
            "Ese nivel define el stock minimo que deberia haber. Si el stock "
            "cae POR DEBAJO de ese minimo, se alerta (riesgo de quedarse sin "
            "producto):\n\n"
            "  •  Demanda Baja  → alerta si el stock es menor a 10\n"
            "  •  Demanda Media → alerta si el stock es menor a 20\n"
            "  •  Demanda Alta  → alerta si el stock es menor a 30\n\n"
            "Las filas marcadas en rojo en la Tabla de Inventario son las que "
            "ya estan por debajo de ese minimo para su nivel de demanda."
        )
        messagebox.showinfo("Metrica de alerta de stock", mensaje)

    def _buscar_producto_por_id(self, id_producto):
        for producto in inventario:
            if producto["id"] == id_producto:
                return producto
        messagebox.showerror("Error", "No se encontro el producto seleccionado.")
        return None

    # Pestaña 1 de inventario
    def _crear_tab_inventario(self):
        # Barra de busqueda 
        barra_busqueda = ttk.Frame(self.tab_inventario)
        barra_busqueda.pack(fill="x", pady=(0, 8))
        ttk.Label(barra_busqueda, text="Buscar (ID o nombre):").pack(side="left")
        self.entry_busqueda_inv = ttk.Entry(barra_busqueda, width=25)
        self.entry_busqueda_inv.pack(side="left", padx=5)
        self.entry_busqueda_inv.bind("<Return>", lambda e: self._buscar_inventario())
        ttk.Button(barra_busqueda, text="Buscar", command=self._buscar_inventario).pack(
            side="left", padx=2
        )
        ttk.Button(
            barra_busqueda, text="Limpiar", command=self._limpiar_busqueda_inventario
        ).pack(side="left")

        # Tabla 
        columnas = ("id", "producto", "stock", "precio", "demanda", "nivel", "vencimiento")
        self.tree_inv = ttk.Treeview(
            self.tab_inventario, columns=columnas, show="headings", height=12
        )
        titulos = ["ID", "Producto", "Stock", "Precio", "Demanda", "Nivel", "Vencimiento"]
        for col, titulo in zip(columnas, titulos):
            self.tree_inv.heading(col, text=titulo)
            self.tree_inv.column(col, anchor="center")
        self.tree_inv.pack(fill="both", expand=True, pady=(0, 10))

        # Fila resaltada en rojo claro cuando el stock esta POR DEBAJO del minimo requerido
        self.tree_inv.tag_configure("alerta", background="#ffcccc")

        # Botones 
        botones = ttk.Frame(self.tab_inventario)
        botones.pack()
        ttk.Button(
            botones, text="Agregar producto nuevo", command=self._agregar_producto
        ).pack(side="left", padx=5)
        ttk.Button(
            botones, text="Agregar stock (reabastecer)", command=self._agregar_stock
        ).pack(side="left", padx=5)
        ttk.Button(
            botones, text="Descontar stock (venta)", command=self._eliminar_producto
        ).pack(side="left", padx=5)
        ttk.Button(
            botones, text="Exportar tabla a .txt", command=self._exportar_inventario_txt
        ).pack(side="left", padx=5)

        self._refrescar_inventario()

    def _refrescar_inventario(self, filtro=None):
        """Vuelve a dibujar la tabla completa (equivale a 'MostrarTablaInventario').
        Si se da un 'filtro', solo muestra productos cuyo ID o nombre lo contengan."""
        self.tree_inv.delete(*self.tree_inv.get_children())
        texto_filtro = filtro.lower().strip() if filtro else None

        for producto in inventario:
            if texto_filtro:
                if (
                    texto_filtro not in producto["id"].lower()
                    and texto_filtro not in producto["nombre"].lower()
                ):
                    continue

            nivel = nivel_demanda(producto["demanda"])
            fila = self.tree_inv.insert(
                "",
                "end",
                iid=producto["id"],
                values=(
                    producto["id"],
                    producto["nombre"],
                    producto["stock"],
                    f"${producto['precio']:.2f}",
                    producto["demanda"],
                    nivel,
                    producto["fecha_vencimiento"],
                ),
            )
            if producto["stock"] < umbral_alerta(nivel):
                self.tree_inv.item(fila, tags=("alerta",))

    def _buscar_inventario(self):
        texto = self.entry_busqueda_inv.get().strip()
        if not texto:
            messagebox.showinfo("Buscar", "Escribe un ID o nombre para buscar.")
            return
        self._refrescar_inventario(filtro=texto)

    def _limpiar_busqueda_inventario(self):
        self.entry_busqueda_inv.delete(0, "end")
        self._refrescar_inventario()

    def _agregar_producto(self):
        """Ventana emergente para capturar un producto nuevo (equivale a 'AgregarProducto')."""
        ventana = tk.Toplevel(self)
        ventana.title("Agregar producto nuevo")
        ventana.geometry("300x330")
        ventana.grab_set()

        campos = {}
        for etiqueta, clave in [
            ("Nombre del producto:", "nombre"),
            ("Stock disponible:", "stock"),
            ("Precio al cliente:", "precio"),
            ("Demanda (1 a 10):", "demanda"),
            ("Fecha de vencimiento\n(AAAA-MM-DD, opcional):", "fecha_vencimiento"),
        ]:
            ttk.Label(ventana, text=etiqueta).pack(pady=(10, 0))
            entrada = ttk.Entry(ventana)
            entrada.pack()
            campos[clave] = entrada

        def guardar():
            global siguiente_id # global sirve para indicar que una variable dentro de una función no es local, sino que corresponde a la definida en el nivel global (fuera de la función)
            try:
                nombre = campos["nombre"].get().strip()
                stock = int(campos["stock"].get())
                precio = float(campos["precio"].get())
                demanda = int(campos["demanda"].get())
                fecha = campos["fecha_vencimiento"].get().strip()
                if not nombre or not (1 <= demanda <= 10):
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Datos invalidos",
                    "Revisa que el nombre no este vacio, y que stock/precio/demanda"
                    " sean numeros validos (demanda entre 1 y 10).",
                )
                return

            nuevo_id = formatear_id(siguiente_id)
            siguiente_id += 1

            inventario.append(
                {
                    "id": nuevo_id,
                    "nombre": nombre,
                    "stock": stock,
                    "precio": precio,
                    "demanda": demanda,
                    "fecha_vencimiento": fecha if fecha else "N/A",
                }
            )
            self._refrescar_inventario()
            ventana.destroy()

        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)

    def _agregar_stock(self):
        """Reabastece un producto ya existente (suma unidades a su stock actual)."""
        seleccion = self.tree_inv.selection()
        if not seleccion:
            messagebox.showwarning("Atencion", "Selecciona primero un producto de la tabla.")
            return

        producto = self._buscar_producto_por_id(seleccion[0])
        if producto is None:
            return

        cantidad = simpledialog.askinteger(
            "Agregar stock",
            f"Stock actual de '{producto['nombre']}': {producto['stock']}\n"
            f"¿Cuantas unidades vas a agregar?",
            minvalue=1,
        )
        if cantidad is None:
            return

        producto["stock"] += cantidad
        messagebox.showinfo(
            "Stock actualizado",
            f"Se agregaron {cantidad} unidades. Stock nuevo: {producto['stock']}",
        )
        self._refrescar_inventario()

    def _eliminar_producto(self):
        """Descuenta unidades vendidas del stock (equivale a 'EliminarProducto').
        Solo si el stock llega a 0 se elimina el producto por completo."""
        seleccion = self.tree_inv.selection()
        if not seleccion:
            messagebox.showwarning("Atencion", "Selecciona primero un producto de la tabla.")
            return

        producto = self._buscar_producto_por_id(seleccion[0])
        if producto is None:
            return

        cantidad = simpledialog.askinteger(
            "Descontar stock",
            f"Stock actual de '{producto['nombre']}': {producto['stock']}\n"
            f"¿Cuantas unidades se vendieron/eliminaron?",
            minvalue=1,
        )
        if cantidad is None:
            return

        if cantidad > producto["stock"]:
            messagebox.showerror(
                "Cantidad invalida",
                f"No hay suficiente stock (solo hay {producto['stock']}).",
            )
            return

        producto["stock"] -= cantidad

        if producto["stock"] == 0:
            inventario.remove(producto)
            messagebox.showinfo(
                "Producto eliminado",
                f"'{producto['nombre']}' se quedo sin stock y fue eliminado del inventario.",
            )
        else:
            messagebox.showinfo(
                "Stock actualizado",
                f"Se descontaron {cantidad} unidades. Stock nuevo: {producto['stock']}",
            )

        self._refrescar_inventario()

    def _exportar_inventario_txt(self):
        """Guarda la tabla de Inventario completa como archivo de texto,
        en la misma carpeta que usa el menu de terminal (main.py)."""
        _asegurar_carpeta_archivos()
        ruta = os.path.join(CARPETA_ARCHIVOS, "inventario_exportado.txt")

        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("TABLA DE INVENTARIO\n")
                archivo.write("ID | Producto | Stock | Precio | Demanda | Nivel | Vencimiento\n")
                for producto in inventario:
                    nivel = nivel_demanda(producto["demanda"])
                    archivo.write(
                        f"{producto['id']} | {producto['nombre']} | {producto['stock']} | "
                        f"${producto['precio']:.2f} | {producto['demanda']} | {nivel} | "
                        f"{producto['fecha_vencimiento']}\n"
                    )
            messagebox.showinfo("Exportado", f"Tabla guardada en '{ruta}'")
        except OSError as error:
            messagebox.showerror("Error al exportar", f"No se pudo guardar el archivo: {error}")


    # Pestaña numero 2 de proveedores

    def _crear_tab_proveedores(self):
        top = ttk.Frame(self.tab_proveedores)
        top.pack(fill="x", pady=(0, 5))

        ttk.Label(top, text="Selecciona un proveedor:").pack(side="left", padx=(0, 10))
        self.combo_proveedor = ttk.Combobox(
            top, values=list(proveedores.keys()), state="readonly", width=25
        )
        self.combo_proveedor.pack(side="left")
        self.combo_proveedor.bind(
            "<<ComboboxSelected>>", lambda e: self._mostrar_tabla_proveedor()
        )

        # Barra de busqueda
        barra_busqueda = ttk.Frame(self.tab_proveedores)
        barra_busqueda.pack(fill="x", pady=(0, 8))
        ttk.Label(barra_busqueda, text="Buscar (ID o nombre):").pack(side="left")
        self.entry_busqueda_prov = ttk.Entry(barra_busqueda, width=25)
        self.entry_busqueda_prov.pack(side="left", padx=5)
        self.entry_busqueda_prov.bind("<Return>", lambda e: self._mostrar_tabla_proveedor())
        ttk.Button(
            barra_busqueda, text="Buscar", command=self._mostrar_tabla_proveedor
        ).pack(side="left", padx=2)
        ttk.Button(
            barra_busqueda, text="Limpiar", command=self._limpiar_busqueda_proveedor
        ).pack(side="left")

        # Tabla
        columnas = ("id", "producto", "precio_proveedor", "demanda")
        self.tree_prov = ttk.Treeview(
            self.tab_proveedores, columns=columnas, show="headings", height=12
        )
        titulos = ["ID", "Producto", "Precio Proveedor", "Demanda"]
        for col, titulo in zip(columnas, titulos):
            self.tree_prov.heading(col, text=titulo)
            self.tree_prov.column(col, anchor="center")
        self.tree_prov.pack(fill="both", expand=True)

        # Fila en verde claro cuando ese proveedor tiene el mejor precio
        self.tree_prov.tag_configure("mejor_precio", background="#c8f7c5")

        ttk.Label(
            self.tab_proveedores,
            text="Verde = el precio mas bajo entre TODOS los proveedores para ese producto",
            font=("", 8),
        ).pack(pady=(5, 0))

        ttk.Button(
            self.tab_proveedores,
            text="Exportar tabla a .txt",
            command=self._exportar_proveedor_txt,
        ).pack(pady=(8, 0))

        if proveedores:
            self.combo_proveedor.current(0)
        self._mostrar_tabla_proveedor()

    def _mostrar_tabla_proveedor(self):
        """Se ejecuta al elegir un proveedor o al buscar
        (equivale al 'selector' del pseudocodigo, MostrarTablaProveedores)."""
        self.tree_prov.delete(*self.tree_prov.get_children())
        nombre_proveedor = self.combo_proveedor.get()
        if not nombre_proveedor:
            return

        filtro = self.entry_busqueda_prov.get().strip().lower()
        minimos = precio_minimo_por_producto()

        for item in proveedores.get(nombre_proveedor, []):
            if filtro:
                if filtro not in item["id"].lower() and filtro not in item["producto"].lower():
                    continue

            demanda = demanda_de_producto(item["producto"])
            fila = self.tree_prov.insert(
                "",
                "end",
                iid=item["id"],
                values=(item["id"], item["producto"], f"${item['precio_proveedor']:.2f}", demanda),
            )
            if item["precio_proveedor"] == minimos.get(item["producto"]):
                self.tree_prov.item(fila, tags=("mejor_precio",))

    def _limpiar_busqueda_proveedor(self):
        self.entry_busqueda_prov.delete(0, "end")
        self._mostrar_tabla_proveedor()

    def _exportar_proveedor_txt(self):
        """Guarda la tabla del proveedor actualmente seleccionado como
        archivo de texto, en la misma carpeta que usa el menu de terminal."""
        nombre_proveedor = self.combo_proveedor.get()
        if not nombre_proveedor:
            messagebox.showwarning("Atencion", "Selecciona primero un proveedor.")
            return

        _asegurar_carpeta_archivos()
        # Reemplazamos espacios para que el nombre del archivo quede limpio
        nombre_archivo = f"proveedor_{nombre_proveedor}.txt"
        ruta = os.path.join(CARPETA_ARCHIVOS, nombre_archivo)

        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(f"TABLA DE PROVEEDOR: {nombre_proveedor}\n")
                archivo.write("ID | Producto | Precio Proveedor | Demanda\n")
                for item in proveedores.get(nombre_proveedor, []):
                    demanda = demanda_de_producto(item["producto"])
                    archivo.write(
                        f"{item['id']} | {item['producto']} | "
                        f"${item['precio_proveedor']:.2f} | {demanda}\n"
                    )
            messagebox.showinfo("Exportado", f"Tabla guardada en '{ruta}'")
        except OSError as error:
            messagebox.showerror("Error al exportar", f"No se pudo guardar el archivo: {error}")


if __name__ == "__main__":
    app = AppPapeleria()
    app.mainloop()