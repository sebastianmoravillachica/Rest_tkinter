import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog 
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["restaurante"]
menu_collection = db["menu"]

def guardar_menu(menu):
    menu_collection.delete_many({})
    if menu:  # Verificar si hay elementos en el menú antes de insertarlos
        menu_collection.insert_many(menu)

def cargar_menu():
    menu = []
    for item in menu_collection.find():
        menu.append(item)
    return menu

def mostrar_menu_en_pantalla():
    texto_menu.delete("1.0", tk.END)
    for plato in menu:
        texto_menu.insert(tk.END, f"{plato['plato']}: ${plato['precio']}\n")

def agregar_plato():
    nombre = simpledialog.askstring("Nuevo Plato", "Ingrese el nombre del nuevo plato:")
    precio = simpledialog.askfloat("Nuevo Plato", "Ingrese el precio del nuevo plato:")
    if nombre and precio:
        menu.append({"plato": nombre, "precio": precio})
        combobox['values'] = [plato['plato'] for plato in menu]
        cargar_menu()
        guardar_menu(menu)
        mostrar_menu_en_pantalla()

def eliminar_plato():
    seleccion = combobox.get()
    menu[:] = [plato for plato in menu if plato['plato'] != seleccion]
    combobox['values'] = [plato['plato'] for plato in menu]
    cargar_menu()
    guardar_menu(menu)
    mostrar_menu_en_pantalla()

def modificar_plato():
    seleccion = combobox.get()
    nuevo_nombre = simpledialog.askstring("Modificar Plato", "Ingrese el nuevo nombre del plato:", initialvalue=seleccion)
    nuevo_precio = simpledialog.askfloat("Modificar Plato", "Ingrese el nuevo precio del plato:", initialvalue=[plato['precio'] for plato in menu if plato['plato'] == seleccion][0])
    if nuevo_nombre and nuevo_precio:
        for plato in menu:
            if plato['plato'] == seleccion:
                plato['plato'] = nuevo_nombre
                plato['precio'] = nuevo_precio
        combobox['values'] = [plato['plato'] for plato in menu]
        cargar_menu()
        guardar_menu(menu)
        mostrar_menu_en_pantalla()

def mostrar_precio():
    seleccion = combobox.get()
    precio = [plato['precio'] for plato in menu if plato['plato'] == seleccion][0]
    if seleccion not in alimentos_seleccionados:
        alimentos_seleccionados.append(seleccion)
        precio_seleccionado = f"{seleccion}: ${precio:.2f}\n"
        texto_desglose.insert(tk.END, precio_seleccionado)
    actualizar_precio_total()

def actualizar_precio_total():
    total = sum([plato['precio'] for plato in menu if plato['plato'] in alimentos_seleccionados])
    label_precio_total.config(text=f"Total: ${total:.2f}")

def finalizar_compra():
    total = sum([plato['precio'] for plato in menu if plato['plato'] in alimentos_seleccionados])
    tk.messagebox.showinfo("Total a Pagar", f"El total a pagar es: ${total:.2f}")

ventana = tk.Tk()
ventana.title("Menú de alimentos")

texto_menu = tk.Text(ventana, height=10, width=30)
texto_menu.pack()

menu = cargar_menu()
mostrar_menu_en_pantalla()

combobox = ttk.Combobox(ventana, values=[plato['plato'] for plato in menu])
combobox.pack()

boton_agregar = tk.Button(ventana, text="Agregar Plato", command=agregar_plato)
boton_agregar.pack()

boton_eliminar = tk.Button(ventana, text="Eliminar Plato", command=eliminar_plato)
boton_eliminar.pack()

boton_modificar = tk.Button(ventana, text="Modificar Plato", command=modificar_plato)
boton_modificar.pack()

boton_mostrar_precio = tk.Button(ventana, text="Agregar al Pedido", command=mostrar_precio)
boton_mostrar_precio.pack()

label_precio_total = tk.Label(ventana, text="")
label_precio_total.pack()

texto_desglose = tk.Text(ventana, height=10, width=30)
texto_desglose.pack()

boton_finalizar_compra = tk.Button(ventana, text="Finalizar Compra", command=finalizar_compra)
boton_finalizar_compra.pack()

alimentos_seleccionados = []

ventana.mainloop()
