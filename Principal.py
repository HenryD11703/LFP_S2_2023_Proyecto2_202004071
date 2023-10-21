import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from Lexico.Analizador import Analizador
from Sintáctico.Gramatica import Sintactico

def abrir_archivo():
    archivo = filedialog.askopenfile(filetypes=[("Archivo Bizadata", "*.bizdata")])
    if archivo:
        contenido = archivo.read()
        cuadro_texto_grande.delete("1.0", "end")
        cuadro_texto_grande.insert("1.0", contenido)

def escribir():
    cuadro_texto_pequeño.config(state="normal")  
    cuadro_texto_pequeño.delete("1.0", "end")   
    # TODO: Hacer aca la impresion del codigo procesado
    cuadro_texto_pequeño.insert("1.0", "Hola")  # *Agregar el contenido aca 
    cuadro_texto_pequeño.config(state="disabled") 
    
def analizar():
    texto = cuadro_texto_grande.get("1.0","end")
    analizador = Analizador(texto)
    analizador.analizar()
    analizador.imprimirTokens()
    analizador.imprimirErrores()
    a = analizador.getTokens();
    
    
    s = Sintactico(a)
    s.analizar()
    s.ImprimirErrores()
    


ventana = tk.Tk()
ventana.title("Interfaz con Tkinter")
ventana.geometry("1000x900")

navbar_frame = tk.Frame(ventana, bg="lightgray")
navbar_frame.pack(fill="x")

titulo_label = tk.Label(navbar_frame, text="202004071", font=("Helvetica", 14), padx=150, bg="lightgray")
titulo_label.grid(row=0, column=0)

abrir_boton = tk.Button(navbar_frame, text="Abrir", padx=60, command=abrir_archivo)
abrir_boton.grid(row=0, column=1)

analizar_boton = tk.Button(navbar_frame, text="Analizar", padx=60, command=analizar)
analizar_boton.grid(row=0, column=2)

opcion = tk.StringVar()
opciones_combobox = ttk.Combobox(navbar_frame, textvariable=opcion, values=["Reporte de Errores", "Reporte de Tokens", "Arbol de Derivacion"])
opciones_combobox.grid(row=0, column=3)

cuadro_texto_grande = tk.Text(ventana, width=125, height=25, borderwidth=2, relief="solid")
cuadro_texto_grande.pack(pady=10, padx=10)

cuadro_texto_pequeño = tk.Text(ventana, width=125, height=25, borderwidth=2, relief="solid")
cuadro_texto_pequeño.pack(pady=10, padx=10)
cuadro_texto_pequeño.config(state="disabled")

ventana.mainloop()
