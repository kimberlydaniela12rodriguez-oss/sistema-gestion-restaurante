import tkinter as tk
from tkinter import ttk, messagebox
import base_dedatos  # Conectado con tu archivo base_dedatos.py

# Iniciamos la base de datos
base_dedatos.conectar()

# Menús y precios oficiales de la imagen del restaurante
MENUS = {
    "Lomo Saltado": 17900.0,
    "Pasta a la Panca": 14000.0,
    "Pollo Peruano": 15900.0,
    "Arroz Chaufa": 14900.0,
    "Chuleta en Salsa": 16900.0,
    "Ceviche Mixto": 17900.0
}

def limpiar_campos():
    entry_id.delete(0, tk.END)
    entry_comensal.delete(0, tk.END)
    combo_menu.set("")
    txt_reporte.config(state="normal")
    txt_reporte.delete("1.0", tk.END)
    txt_reporte.config(state="disabled")

def refrescar_tabla():
    for item in tabla.get_children():
        tabla.delete(item)
    for fila in base_dedatos.obtener_todos():
        tabla.insert("", tk.END, values=fila)

def calcular_valores(precio_original):
    iva = precio_original * 0.16
    servicio = precio_original * 0.10
    total = precio_original + iva + servicio
    return round(iva, 2), round(servicio, 2), round(total, 2)

def mostrar_reporte_pantalla(comensal, menu, precio, iva, servicio, total):
    txt_reporte.config(state="normal")
    txt_reporte.delete("1.0", tk.END)
    reporte = (
        f"*** REPORTE DE CUENTA ***\n\n"
        f"Comensal: {comensal}\n"
        f"Menú elegido: {menu}\n"
        f"Precio Base: {precio:,.2f}\n"
        f"IVA (16%): {iva:,.2f}\n"
        f"10% Servicio: {servicio:,.2f}\n"
        f"-------------------------\n"
        f"TOTAL A PAGAR: {total:,.2f}"
    )
    txt_reporte.insert(tk.END, reporte)
    txt_reporte.config(state="disabled")

def guardar_pedido():
    comensal = entry_comensal.get()
    menu_elegido = combo_menu.get()
    id_reg = entry_id.get()

    if not comensal or not menu_elegido:
        messagebox.showerror("Error", "Debe ingresar el comensal y elegir un menú")
        return

    precio_original = MENUS[menu_elegido]
    iva, servicio, total = calcular_valores(precio_original)

    if id_reg == "":
        base_dedatos.insertar(comensal, menu_elegido, precio_original, iva, servicio, total)
        messagebox.showinfo("Éxito", "Pedido registrado exitosamente")
    else:
        base_dedatos.actualizar(int(id_reg), comensal, menu_elegido, precio_original, iva, servicio, total)
        messagebox.showinfo("Éxito", "Pedido modificado exitosamente")

    mostrar_reporte_pantalla(comensal, menu_elegido, precio_original, iva, servicio, total)
    refrescar_tabla()
    limpiar_campos()

def eliminar_pedido():
    id_reg = entry_id.get()
    if id_reg == "":
        messagebox.showwarning("Advertencia", "Seleccione un registro de la tabla para eliminar")
        return
    
    base_dedatos.eliminar(int(id_reg))
    messagebox.showinfo("Éxito", "Pedido eliminado correctamente")
    limpiar_campos()
    refrescar_tabla()

def seleccionar_registro(event):
    seleccion = tabla.focus()
    valores = tabla.item(seleccion, 'values')
    if valores:
        limpiar_campos()
        entry_id.insert(0, valores[0])
        entry_comensal.insert(0, valores[1])
        combo_menu.set(valores[2])
        mostrar_reporte_pantalla(valores[1], valores[2], float(valores[3]), float(valores[4]), float(valores[5]), float(valores[6]))

# Crear la ventana gráfica
ventana = tk.Tk()
ventana.title("RESTAURANTE EL BUEN COMER - UNETI")
ventana.geometry("750x550")

# Formulario Izquierdo
frame_form = tk.LabelFrame(ventana, text=" Registro de Pedidos ", padx=10, pady=10)
frame_form.place(x=20, y=20, width=350, height=220)

tk.Label(frame_form, text="ID Registro (Auto):").grid(row=0, column=0, sticky="w", pady=5)
entry_id = tk.Entry(frame_form, width=10)
entry_id.grid(row=0, column=1, sticky="w", pady=5)

tk.Label(frame_form, text="Nombre del Comensal:").grid(row=1, column=0, sticky="w", pady=5)
entry_comensal = tk.Entry(frame_form, width=25)
entry_comensal.grid(row=1, column=1, pady=5)

tk.Label(frame_form, text="Seleccione Menú:").grid(row=2, column=0, sticky="w", pady=5)
combo_menu = ttk.Combobox(frame_form, values=list(MENUS.keys()), state="readonly", width=22)
combo_menu.grid(row=2, column=1, pady=5)

# Botones CRUD
btn_guardar = tk.Button(frame_form, text="Guardar / Modificar", command=guardar_pedido, bg="#c3e6cb")
btn_guardar.grid(row=3, column=0, pady=15)

btn_eliminar = tk.Button(frame_form, text="Eliminar", command=eliminar_pedido, bg="#f5c6cb", fg="red")
btn_eliminar.grid(row=3, column=1, pady=15)

btn_limpiar = tk.Button(frame_form, text="Nuevo", command=limpiar_campos)
btn_limpiar.grid(row=3, column=2, pady=15)

# Panel de Reporte Requerido (Derecha)
frame_reporte = tk.LabelFrame(ventana, text=" Reporte Final Requerido ", padx=10, pady=10)
frame_reporte.place(x=390, y=20, width=330, height=220)

txt_reporte = tk.Text(frame_reporte, font=("Courier", 10), state="disabled", bg="#f8f9fa")
txt_reporte.pack(fill="both", expand=True)

# Tabla Inferior (Historial SQL)
frame_tabla = tk.LabelFrame(ventana, text=" Registros en Base de Datos (Módulo de Carga SQL) ", padx=10, pady=10)
frame_tabla.place(x=20, y=260, width=700, height=260)

columnas = ("ID", "Comensal", "Menú", "Precio Base", "IVA", "Servicio", "Total")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings')

for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=95, anchor="center")
tabla.column("ID", width=40)

tabla.pack(fill="both", expand=True)
tabla.bind("<ButtonRelease-1>", seleccionar_registro)

refrescar_tabla()
ventana.mainloop()
 
 