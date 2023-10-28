'''
Palabras reservadas

Claves
Registros
imprimir
imprimirln
conteo
promedio
contarsi
datos
sumar
max
min
exportarReporte

Tokens validos

Simbolos 
"=" (Signo igual): 61 
"[" (Corchete izquierdo): 91
"]" (Corchete derecho): 93
""" (Comillas dobles): 34
"," (Coma): 44
"{" (Llave izquierda o corchete): 123
"}" (Llave derecha o corchete): 125
";" (Punto y coma): 59
"(" (Paréntesis izquierdo): 40
")" (Paréntesis derecho): 41
"." (Punto): 46

Las cadenas de texto que no sean las palabras reservadas tienen que venir dentro de comillas
El punto puede venir solamente despues de un numero,


'''
from .CToken import Token
from .CError import Error

class Analizador():
    def __init__(self,texto) -> None:
        self.texto = texto
        self.tokens = []
        self.errores = []
    
    def getTokens(self):
        return self.tokens
        
    def getErrores(self):
        return self.errores
    
    def generahtml(self):
  
        html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Lista de Tokens</title>
    <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f2f2f2;
                    }
                    h1 {
                        text-align: center;
                        margin-top: 50px;
                    }
                    h2 {
                        margin-top: 30px;
                        margin-bottom: 20px;
                    }
                    table {
                        border-collapse: collapse;
                        margin: 0 auto;
                        background-color: white;
                        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                    }
                    th, td {
                        padding: 10px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                    }
                    th {
                        background-color: #4CAF50;
                        color: white;
                    }
                    tr:hover {
                        background-color: #f5f5f5;
                    }
                </style>
</head>
<body>
<h1>Token List</h1>
<table>
    <tr>
        <th>Nombre</th>
        <th>Lexema</th>
        <th>Fila</th>
        <th>Columna</th>
    </tr>
"""


        for token in self.tokens:
            html += """
    <tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
    </tr>
""".format(token.nombre, token.lexema, token.fila, token.columna)


        html += """
</table>
</body>
</html>
"""

        return html
    
    def imprimirTokens(self):
        print("Tokens Reconocidos: ")
        for token in self.tokens:
            print(f'{token}')
            
    def imprimirErrores(self):
        print("Errores Reconocidos")
        for error in self.errores:
            print(f'{error}')
    
    def SimboloValido(self,ascii):
        if ascii == 61 or ascii == 91 or ascii == 93 or ascii ==44 or ascii == 123 or ascii == 125 or ascii == 59 or ascii == 40 or ascii == 41 or ascii == 46:
            return True
        return False 
    
    def analizar(self):
        #Condiciones Iniciales
        fila = 1
        columna = 1
        estado = "A"
        lexema=""
        self.tokens = []
        self.errores = []
        
        for caracter in self.texto:
            ascii = ord(caracter)
            
            #Estado Incial A
            if estado == "A":
                #configurar estado a
                if ascii==35:
                    lexema+=caracter
                    estado="G"
                elif caracter.isalpha():
                    lexema+=caracter
                    estado="B"
                elif caracter.isdigit():
                    lexema+=caracter
                    estado="E"
                elif ascii==34:
                    lexema+=caracter
                    estado="C"
                elif self.SimboloValido(ascii):
                    lexema+=caracter
                    estado="F"
                elif ascii==43 or ascii==45:
                    lexema+=caracter
                    estado="D"
                elif ascii==39:
                    lexema+=caracter
                    estado="H1"
                elif ascii == 32 or ascii == 9 or ascii == 10:
                    pass
                else:
                    self.errores.append(Error(caracter,'lexico 18',columna-len(lexema),fila))
                    lexema=""#reset
                    estado="A"#Volver a empezar con el siguiente lexema
                
            #Estado B (se llego acá con al ingresar una letra)
            elif estado=="B":
                if caracter.isalpha():
                    lexema+=caracter
                    estado="B"
                elif ascii==32 or ascii==9 or ascii==10 or self.SimboloValido(ascii) or ascii==35:#ya que si lo que viene es un espacio o salto de linea significa que se termino el string ó como es una palabra reservada tambien puede haber algun simbolo valido
                    self.tokens.append(Token('Texto',lexema,fila,columna-len(lexema)))# Y se acepta el texto
                    lexema=""
                    estado="A"
                    if ascii==35:
                        lexema+=caracter
                        estado="G"
                    elif caracter.isalpha():
                        lexema+=caracter
                        estado="B"
                    elif caracter.isdigit():
                        lexema+=caracter
                        estado="E"
                    elif ascii==34:
                        lexema+=caracter
                        estado="C"
                    elif self.SimboloValido(ascii):
                        lexema+=caracter
                        estado="F"
                    elif ascii==43 or ascii==45:
                        lexema+=caracter
                        estado="D"
                    elif ascii==39:
                        lexema+=caracter
                        estado="H1"
                    elif ascii == 32 or ascii == 9 or ascii == 10:
                        pass
                    else:
                        self.errores.append(Error(caracter,'lexico 17',columna-len(lexema),fila))
                        lexema=""#reset
                        estado="A"#Volver a empezar con el siguiente lexema
                else:
                    self.errores.append(Error(caracter,'lexico 16',columna-len(lexema),fila))
                    lexema=""
                    estado="A"
                    
            
            #Estado C (Cadenas de texto dentro de "")
            elif estado=="C":
                if ascii==34:
                    lexema+=caracter
                    estado="I"
                elif ascii!=10:
                    lexema+=caracter
                    estado="C"
                elif ascii== 10:
                    self.errores.append(Error(caracter,'lexico 15',columna-len(lexema),fila))
                    lexema = ""
                    estado = "A"
            
            #Ingresar un numero despues de un signo (+/-)
            elif estado=="D":
                if caracter.isdigit():
                    lexema+=caracter
                    estado="E"
                else:
                    self.errores.append(Error(caracter,'lexico 14',columna-len(lexema),fila))
                    lexema = ""
                    estado = "A"
                    
            #Estado E que maneja numeros enteros, positivos y negativos
            elif estado=="E":
                #este estado puede aceptar en la entrada
                if caracter.isdigit():
                    lexema+=str(caracter)
                    estado="E"
                elif ascii==46:
                    lexema+=caracter
                    estado="J"
                elif self.SimboloValido(ascii) or ascii== 10 or ascii==9 or ascii==32 or ascii==35:
                    self.tokens.append(Token('Entero',lexema,fila,columna-len(lexema)))
                    lexema=""
                    estado="A"
                    if ascii==35:
                        lexema+=caracter
                        estado="G"
                    elif caracter.isalpha():
                        lexema+=caracter
                        estado="B"
                    elif caracter.isdigit():
                        lexema+=caracter
                        estado="E"
                    elif ascii==34:
                        lexema+=caracter
                        estado="C"
                    elif self.SimboloValido(ascii):
                        lexema+=caracter
                        estado="F"
                    elif ascii==43 or ascii==45:
                        lexema+=caracter
                        estado="D"
                    elif ascii==39:
                        lexema+=caracter
                        estado="H1"
                    elif ascii == 32 or ascii == 9 or ascii == 10:
                        pass
                    else:
                        self.errores.append(Error(caracter,'lexico 13',columna-len(lexema),fila))
                        lexema=""#reset
                        estado="A"#Volver a empezar con el siguiente lexema
                else:
                    self.errores.append(Error(caracter,'lexico 12',columna-len(lexema),fila))
                    lexema = ""
                    estado = "A"
                    
            #Estado F (Simbolos validos)
            elif estado=="F":
                self.tokens.append(Token('Simbolo',lexema,fila,columna-len(lexema)))
                lexema=""
                estado="A"
                if ascii==35:
                    lexema+=caracter
                    estado="G"
                elif caracter.isalpha():
                    lexema+=caracter
                    estado="B"
                elif caracter.isdigit():
                    lexema+=caracter
                    estado="E"
                elif ascii==34:
                    lexema+=caracter
                    estado="C"
                elif self.SimboloValido(ascii):
                    lexema+=caracter
                    estado="F"
                elif ascii==43 or ascii==45:
                    lexema+=caracter
                    estado="D"
                elif ascii==39:
                    lexema+=caracter
                    estado="H1"
                elif ascii == 32 or ascii == 9 or ascii == 10:
                    pass
                else:
                    self.errores.append(Error(caracter,'lexico 11',columna-len(lexema),fila))
                    lexema=""#reset
                    estado="A"#Volver a empezar con el siguiente lexema
                
            #Estado G (Simbolo # y luego cualquier cosa, el salto de linea lo termina y aceptarlo)
            elif estado=="G":
                if ascii != 10:
                    lexema+=caracter
                    estado="G"
                elif ascii==10:
                    #self.tokens.append(Token('Comentario',lexema,fila,columna-len(lexema)))
                    lexema=""
                    estado="A"
                    if ascii==35:
                        lexema+=caracter
                        estado="G"
                    elif caracter.isalpha():
                        lexema+=caracter
                        estado="B"
                    elif caracter.isdigit():
                        lexema+=caracter
                        estado="E"
                    elif ascii==34:
                        lexema+=caracter
                        estado="C"
                    elif self.SimboloValido(ascii):
                        lexema+=caracter
                        estado="F"
                    elif ascii==43 or ascii==45:
                        lexema+=caracter
                        estado="D"
                    elif ascii==39:
                        lexema+=caracter
                        estado="H1"
                    elif ascii == 32 or ascii == 9 or ascii == 10:
                        pass
                    else:
                        self.errores.append(Error(caracter,'lexico 10',columna-len(lexema),fila))
                        lexema=""#reset
                        estado="A"#Volver a empezar con el siguiente lexema
                    
            #Estados H que son para las comillas:
            elif estado=="H1":
                if ascii==39:
                    lexema+=caracter#segunda comilla
                    estado="H2"
                else:
                    self.errores.append(Error(caracter,'lexico 9',columna-len(lexema),fila))
                    lexema = ""
                    estado = "A"
            
            elif estado=="H2":
                if ascii==39:
                    lexema+=caracter#tercera comilla
                    estado="H3"
                else:
                    self.errores.append(Error(caracter,'lexico 8',columna-len(lexema),fila))
                    lexema = ""
                    estado = "A"
            
            elif estado=="H3":
                if ascii!=39:
                    lexema+=caracter
                    estado="H3"
                elif ascii==39:
                    lexema+=caracter
                    estado="H4"
            
            elif estado=="H4":
                if ascii==39:
                    lexema+=caracter#segunda comilla
                    estado="H5"
                else:
                    self.errores.append(Error(caracter,'lexico 7',columna-len(lexema),fila))
                    lexema = ""
                    estado = "A"
            
            elif estado=="H5":
                if ascii==39:
                    lexema+=caracter#tercera comilla
                    estado="K"
                else:
                    self.errores.append(Error(caracter,'lexico 6',columna-len(lexema),fila))
                    lexema = ""
                    estado = "A"
                    
            
            #Estado I (acepta las cadenas dentro de "")
            elif estado=="I":
                self.tokens.append(Token('String',lexema,fila,columna-len(lexema)))
                lexema=""
                estado="A"
                if ascii==35:
                        lexema+=caracter
                        estado="G"
                elif caracter.isalpha():
                        lexema+=caracter
                        estado="B"
                elif caracter.isdigit():
                        lexema+=caracter
                        estado="E"
                elif ascii==34:
                        lexema+=caracter
                        estado="C"
                elif self.SimboloValido(ascii):
                        lexema+=caracter
                        estado="F"
                elif ascii==43 or ascii==45:
                        lexema+=caracter
                        estado="D"
                elif ascii==39:
                        lexema+=caracter
                        estado="H1"
                elif ascii == 32 or ascii == 9 or ascii == 10:
                    pass
                else:
                        self.errores.append(Error(caracter,'lexico 5',columna-len(lexema),fila))
                        lexema=""#reset
                        estado="A"#Volver a empezar con el siguiente lexema
                
                
            #Estado J (El estado E pasa aca cuando hay un punto)
            elif estado=="J":
                if caracter.isdigit():
                    lexema+=str(caracter)
                    estado="L"
                else:
                    self.errores.append(Error(caracter,'lexico 4',columna-len(lexema),fila))
                    lexema = ""
                    estado = "A"
            
            
            
            #estado K que acepta las cadenas de comentarios multilinea
            elif estado=="K":
                #self.tokens.append(Token('Comentario Multilinea',lexema,fila,columna-len(lexema)))
                lexema=""
                estado="A"
                if ascii==35:
                        lexema+=caracter
                        estado="G"
                elif caracter.isalpha():
                        lexema+=caracter
                        estado="B"
                elif caracter.isdigit():
                        lexema+=caracter
                        estado="E"
                elif ascii==34:
                        lexema+=caracter
                        estado="C"
                elif self.SimboloValido(ascii):
                        lexema+=caracter
                        estado="F"
                elif ascii==43 or ascii==45:
                        lexema+=caracter
                        estado="D"
                elif ascii==39:
                        lexema+=caracter
                        estado="H1"
                elif ascii == 32 or ascii == 9 or ascii == 10:
                    pass
                else:
                        self.errores.append(Error(caracter,'lexico 3',columna-len(lexema),fila))
                        lexema=""#reset
                        estado="A"#Volver a empezar con el siguiente lexema
                
            
            #Estado L acepta decimales
            elif estado =="L":
                if caracter.isdigit():
                    lexema+=caracter
                    estado="L"
                elif self.SimboloValido(ascii)  or ascii== 10 or ascii==9 or ascii==32:
                    self.tokens.append(Token('Decimal',lexema,fila,columna-len(lexema)))
                    lexema=""
                    estado="A"
                    if ascii==35:
                        lexema+=caracter
                        estado="G"
                    elif caracter.isalpha():
                            lexema+=caracter
                            estado="B"
                    elif caracter.isdigit():
                            lexema+=caracter
                            estado="E"
                    elif ascii==34:
                            lexema+=caracter
                            estado="C"
                    elif self.SimboloValido(ascii):
                            lexema+=caracter
                            estado="F"
                    elif ascii==43 or ascii==45:
                            lexema+=caracter
                            estado="D"
                    elif ascii==39:
                            lexema+=caracter
                            estado="H1"
                    elif ascii == 32 or ascii == 9 or ascii == 10:
                        pass
                    else:
                            self.errores.append(Error(caracter,'lexico 2',columna-len(lexema),fila))
                            lexema=""#reset
                            estado="A"#Volver a empezar con el siguiente lexema
                else:
                    self.errores.append(Error(caracter,'lexico 1',columna-len(lexema),fila))
                    lexema = ""
                    estado = "A"
                
            if ascii == 10:
                fila += 1
                columna = 1
                continue
            #Tabulación
            elif ascii == 9:
                columna += 4
                continue
            #Espacio
            elif ascii == 32:
                columna += 1
                continue
            

            columna += 1
                    
            
            
            
            
                
                    
        