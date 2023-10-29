import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from Lexico.Analizador import Analizador
from Lexico.CToken import Token
from Sintáctico.Gramatica import Sintactico


def abrir_archivo():
    archivo = filedialog.askopenfile(
        filetypes=[("Archivo Bizadata", "*.bizdata")])
    if archivo:
        contenido = archivo.read()
        cuadro_texto_grande.delete("1.0", "end")
        cuadro_texto_grande.insert("1.0", contenido)


erroresl = ""
tokens = ""


def analizar():
    global erroresd
    global tokens
    texto = cuadro_texto_grande.get("1.0", "end")
    analizador = Analizador(texto)
    analizador.analizar()
    # analizador.imprimirTokens()
    # analizador.imprimirErrores()
    a = analizador.getTokens()
    tokens = analizador.generahtml()
    erroresl = analizador.generahtmlerrores()

    s = Sintactico(a)
    s.analizar()
    s.ImprimirErrores()
    erroress = s.reghtml()
    claves = s.mostrarclaves()
    erroresd = erroresl + '\n' + erroress

    regsd = s.mostrarRegistros()
    regs = eliminar_registros_duplicados(regsd)

    cuadro = []
    cuadro.append(claves)
    cuadro.append(regs)
    # meter este cuadro en un html que se vea bonito y para crear el archivo html con la tabla de registros

    tabla = s.datosimp(claves, regs)

    proms = s.promediosimp()
    sumas = s.sumasimp()
    contados = s.contarsiimp()
    conteo = s.conteoimp(regs)

    maximo = s.maximoimp()
    minimo = s.minimoimp()
    if conteo == 0:
        conteo = " "

    tabladd = s.generar_tabla_html(claves, regs)
    if tabladd is not None:
        with open('tabla.html', 'w') as f:
            f.write(tabladd)
    else:
        # vaciar el archivo
        with open('tabla.html', 'w') as f:
            f.write('')

    print(conteo)

    print(tabla)  # filas para mostrarlo en consola bonito

    imprimir = s.imprimirtxt() + "\n"
    imprimirln = s.imprimirtxtln() + "\n"
    res = imprimir + '\n' + imprimirln + \
        str(conteo) + '\n'+'\n' + tabla + '\n' + proms + '\n' + \
        sumas + '\n' + contados + '\n' + maximo + '\n' + minimo

    escribir(res)


def eliminar_registros_duplicados(lista):
    lista_sin_duplicados = []
    registro_anterior = None

    for registro in lista:
        if registro != registro_anterior:
            lista_sin_duplicados.append(registro)
        registro_anterior = registro

    return lista_sin_duplicados


def escribir(textoimp):
    cuadro_texto_pequeño.config(state="normal")
    cuadro_texto_pequeño.delete("1.0", "end")

    cuadro_texto_pequeño.insert("1.0", textoimp)  # *Agregar el contenido aca
    cuadro_texto_pequeño.config(state="disabled")


ventana = tk.Tk()
ventana.title("Interfaz con Tkinter")
ventana.geometry("1000x900")


navbar_frame = tk.Frame(ventana, bg="lightgray")
navbar_frame.pack(fill="x")

titulo_label = tk.Label(navbar_frame, text="202004071", font=(
    "Helvetica", 14), padx=150, bg="lightgray")
titulo_label.grid(row=0, column=0)

abrir_boton = tk.Button(navbar_frame, text="Abrir",
                        padx=60, command=abrir_archivo)
abrir_boton.grid(row=0, column=1)

analizar_boton = tk.Button(
    navbar_frame, text="Analizar", padx=60, command=analizar)
analizar_boton.grid(row=0, column=2)

opcion = tk.StringVar()
opciones_combobox = ttk.Combobox(navbar_frame, textvariable=opcion, values=[
                                 "Reporte de Errores", "Reporte de Tokens", "Arbol de Derivacion"])
opciones_combobox.grid(row=0, column=3)
opciones_combobox.state(["readonly"])


def reporte_errores():
    print("Reporte de Errores")
    with open('errores.html', 'w') as f:
        f.write(erroresd)


def reporte_tokens():
    print("Reporte de Tokens")
    with open('tokens.html', 'w') as f:
        f.write(tokens)


def arbol_derivacion():
    print("Arbol de Derivacion")
    htmlt = f'<!DOCTYPE html>\n<html>\n<head>\n'
    htmlt += '<meta charset="UTF-8">\n'
    htmlt += '<title>Arbol de Derivacion</title>\n'
    htmlt += '<style>\n'
    htmlt += 'body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }\n'
    htmlt += 'header { background-color: #333; color: #fff; padding: 20px; text-align: center; }\n'
    htmlt += '.container { max-width: 960px; margin: 20px auto; padding: 20px; background-color: #fff; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); }\n'
    htmlt += '</style>\n'
    htmlt += '</head>\n'
    htmlt += '<body>\n'
    htmlt += '<header>\n<h1>Arbol de Derivacion</h1>\n</header>\n'
    htmlt += '<div class="container">\n'
    htmlt += f'<embed src="Arbol.dot.pdf" type="application/pdf" width="100%" height="600px" />'
    htmlt += '</div>\n'
    htmlt += '</body>\n'
    htmlt += '</html>'

    # Escribir el contenido HTML en un archivo
    with open("arbolS.html", "w") as html:
        html.write(htmlt)


def seleccionar_opcion(event):
    opcion = opciones_combobox.get()
    if opcion == "Reporte de Errores":
        reporte_errores()
    elif opcion == "Reporte de Tokens":
        reporte_tokens()
    elif opcion == "Arbol de Derivacion":
        arbol_derivacion()


opciones_combobox.bind("<<ComboboxSelected>>", seleccionar_opcion)


cuadro_texto_grande = tk.Text(
    ventana, width=125, height=25, borderwidth=2, relief="solid")
cuadro_texto_grande.pack(pady=10, padx=10)

cuadro_texto_pequeño = tk.Text(
    ventana, width=125, height=25, borderwidth=2, relief="solid")
cuadro_texto_pequeño.pack(pady=10, padx=10)
cuadro_texto_pequeño.config(state="disabled")

ventana.mainloop()
