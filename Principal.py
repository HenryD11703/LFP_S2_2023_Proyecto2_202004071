import tkinter as tk
from tkinter import ttk


def escribir():
    cuadro_texto_pequeño.config(state="normal")  
    cuadro_texto_pequeño.delete("1.0", "end")   
    # TODO: Hacer aca la impresion del codigo procesado
    cuadro_texto_pequeño.insert("1.0", "Hola")  #Agregar el contenido aca 
    cuadro_texto_pequeño.config(state="disabled") 

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz con Tkinter")
ventana.geometry("1000x900")

# Crear el navbar
navbar_frame = tk.Frame(ventana, bg="lightgray")
navbar_frame.pack(fill="x")

titulo_label = tk.Label(navbar_frame, text="202004071", font=("Helvetica", 14), padx=150, bg="lightgray")
titulo_label.grid(row=0, column=0)

abrir_boton = tk.Button(navbar_frame, text="Abrir", padx=60, command=escribir)
abrir_boton.grid(row=0, column=1)

analizar_boton = tk.Button(navbar_frame, text="Analizar", padx=60)
analizar_boton.grid(row=0, column=2)

opcion = tk.StringVar()
opciones_combobox = ttk.Combobox(navbar_frame, textvariable=opcion, values=["Reporte de Errores", "Reporte de Tokens", "Arbol de Derivacion"])
opciones_combobox.grid(row=0, column=3)

cuadro_texto_grande = tk.Text(ventana, width=125, height=25, borderwidth=2, relief="solid")
cuadro_texto_grande.pack(pady=10, padx=10)

cuadro_texto_pequeño = tk.Text(ventana, width=125, height=25, borderwidth=2, relief="solid")
cuadro_texto_pequeño.pack(pady=10, padx=10)
cuadro_texto_pequeño.config(state="disabled")

# Iniciar la aplicación
ventana.mainloop()
