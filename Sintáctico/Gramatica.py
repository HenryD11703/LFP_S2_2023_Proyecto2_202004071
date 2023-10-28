'''
Lenguaje:

Claves = [
	"codigo","producto","precio_compra","precio_venta", "stock"
]

Registros = [
	{1, "Barbacoa", 10.50, 20.00, 6}
	{2, "Salsa", 13.00, 16.00,7}
	{3, "Mayonesa", 15.00,18.00,8}
	{4, "Mostaza", 14.00, 16.00,4}
]

imprimir("Reporte de");
imprimir("Abarroteria");

imprimirln("Reporte de");
imprimirln("Abarroteria");

conteo()

promedio("stock");

contarsi("stock",0);

datos();

sumar("stock");

max("precio_venta");

min("precio_compra");

exportarReporte("Reporte HTML de abarrotería");






Gramatica: 

Terminales: Claves, igual, corcheteA, string, coma, corcheteC
           Registros, llaveA, llaveC, entero, decimal
           imprimir, parentesisA, parentesisC, puntocoma
           imprimirln, conteo, promedio, contarsi, max, min, exportarReporte
           datos, sumar
           
No Terminales:
<Inicio> <Claves> <ListaStrings> <Registros> <registro> <valor> <otroValor> <otroRegistro> <Funciones>
<funcion> <otrafuncion> <imprimir> <imprimirln> <conteo> <promedio> <contarsi>
<datos> <sumar> <max> <min> <exportarReporte>

Inicio:<Inicio>
Producciones:  

    <Inicio> ::= <Claves> <Registros> <Funciones>
    
    <Claves> ::= Claves igual corcheteA string <ListaStrings> corcheteC
    <ListaStrings> ::= coma string <ListaStrings>
                    | lambda
                    
    <Registros> ::= Registros igual corcheteA <registro> <otroregistro> corcheteC
    <registro> ::= llaveA <valor> <otroValor> llaveC
    <valor> ::= string  
                | entero
                | decimal
    <otroValor> ::=  coma <valor> <otroValor>
                   | lambda
    <otroRegistro> ::= <registro> <otroRegistro>
                    | lambda
    
    <Funciones> ::= <funcion> <otrafuncion>
    <funcion>:: = <imprimir>                   
                 |<imprimirln>  
                 |<conteo> 
                 |<promedio>
                 |<contarsi>
                 |<datos>
                 |<sumar>
                 |<max>
                 |<min>
                 |<exportarReporte>

    <imprimir> ::= imprimir parentesisA string parentesisC puntocoma 
    <imprimirln> ::= imprimirln parentesisA string parentesisC puntocoma
    <conteo> ::= conteo parentesisA parentesisC puntocoma
    <promedio> ::= promedio parentesisA string parentesisC puntocoma
    <contarsi> ::= contarsi parentesisA string coma entero parentesisC puntocoma
    <datos> ::= datos parentesisA parentesisC puntocoma
    <sumar> ::= sumar parentesisA string parentesisC puntocoma
    <max> ::= max parentesisA string parentesisC puntocoma 
    <min> ::= min parentesisA string parentesisC puntocoma
    <exportarReporte> ::= exporterReporte parentesisA string parentesisC puntocoma

    <otrafuncion> ::= <funcion><otrafuncion>
                    | lambda
 
'''
from Sintáctico.SToken import Token
from Sintáctico.SError import Error
from graphviz import Digraph

class Sintactico():
    def __init__(self,tokens) -> None:
        self.tokens = tokens
        self.listaClaves=[]
        self.listaRegistros=[]
        self.errores = []
        self.i=0
        self.v=0
        self.cf=0
        self.funcionc=0
        self.dot = Digraph()
        self.textoimp=""
        self.textoimpln=""
        self.datosd=False
        self.tabla=""
        self.conteos=False
        self.conteop=0
        self.generarTabla=False
        self.tituloTabla=""
        tokenN = Token('Fin','Fin',0,0)
        self.tokens.append(tokenN)
        
        
    def generar_tabla_html(self, headers, rows):
        if self.generarTabla is True:
            if not headers or not rows:
                return "<p>No hay datos para mostrar</p>"
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f2f2f2;
                    }}
                    h1 {{
                        text-align: center;
                        margin-top: 50px;
                    }}
                    h2 {{
                        margin-top: 30px;
                        margin-bottom: 20px;
                    }}
                    table {{
                        border-collapse: collapse;
                        margin: 0 auto;
                        background-color: white;
                        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                    }}
                    th, td {{
                        padding: 10px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                    }}
                    th {{
                        background-color: #4CAF50;
                        color: white;
                    }}
                    tr:hover {{
                        background-color: #f5f5f5;
                    }}
                </style>
            </head>
            <body>
            """.format(self.tituloTabla)
            
            
            html += "<h1>{}</h1>".format(self.tituloTabla) 
            html += "<table>"
            html += "<tr>"
            for header in headers:
                html += "<th>{}</th>".format(header)
            html += "</tr>"
            for row in rows:
                html += "<tr>"
                for cell in row:
                    html += "<td>{}</td>".format(cell)
                html += "</tr>"
            html += "</table>"
            html += "</body></html>"

            return html
    
    
    def conteoimp(self,reg):
        if self.conteos is True:
            self.conteop=len(reg)
        return self.conteop
            

    def datosimp(self,claves,regs):
        if self.datosd is True: 
            self.tabla = " | ".join(claves) + "\n"  #Encabezados para mostrarlo en consola bonito nada mas
            #join para concatenar
            for fila in regs:
                self.tabla += " | ".join(fila) + "\n"
        return self.tabla
    
    #funcion imprimir
    def imprimirtxt(self):
        return self.textoimp
    #funcion imprimirln
    def imprimirtxtln(self):
        return self.textoimpln
    #mostrar las lista de claves        
    def mostrarclaves(self):
        return self.listaClaves
    #mostrar la lista de registros datos
    def mostrarRegistros(self):
        return self.listaRegistros
    
 

    
    def ImprimirErrores(self):
        print("Errores")
        for error in self.errores:
            print(f'{error}')
    
    def analizar(self):
        self.dot.node('A','Inicio')
        self.inicio()
    
    #if self.tokens[0].lexema =="imprimir" or self.tokens[0].lexema =="imprimirln" or self.tokens[0].lexema == "conteo" or self.tokens[0].lexema =="promedio" or self.tokens[0].lexema =="contarsi" or self.tokens[0].lexema =="datos" or self.tokens[0].lexema =="sumar" or self.tokens[0].lexema =="stock" or self.tokens[0].lexema =="max" or self.tokens[0].lexema =="min" or self.tokens[0].lexema =="exportarReporte":
    #metodo para recuperar errores de las funciones
    def recuperarfunc(self, f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11):
        while self.tokens and self.tokens[0].lexema != f1 and self.tokens[0].lexema != f2 and self.tokens[0].lexema != f3 and self.tokens[0].lexema != f4 and self.tokens[0].lexema != f5 and self.tokens[0].lexema != f6 and self.tokens[0].lexema != f7 and self.tokens[0].lexema != f8 and self.tokens[0].lexema != f9 and self.tokens[0].lexema != f10 and self.tokens[0].lexema != f11 and self.tokens[0].lexema != 'Fin':
            self.tokens.pop(0) 
        
    def recuperar(self, token):
        while self.tokens and self.tokens[0].lexema != token and self.tokens[0].lexema != 'Fin':
            self.tokens.pop(0)
    
    def recuperarn(self, token):
        while self.tokens and self.tokens[0].nombre != token and self.tokens[0].lexema != 'Fin':
            self.tokens.pop(0)
  
    
    #<Inicio> ::= <Claves> <Registros> <Funciones>
    def inicio(self):
        self.dot.node('B','Claves')
        self.dot.node('C','Registros')
        self.dot.node('D','Funciones')
        self.dot.edge('A','B')
        self.claves()
        self.dot.edge('A','C')
        self.registros();
        self.dot.edge('A','D')
        self.funciones();
    
    #<Claves> ::= Claves igual corcheteA string <ListaStrings> corcheteC
    def claves(self):
        self.recuperar('Claves')
        if self.tokens[0].nombre == 'Texto' and self.tokens[0].lexema =="Claves":
            self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
            self.dot.edge('B',f'N{self.i}')
            self.i+=1
            self.tokens.pop(0)
            
            if self.tokens[0].nombre == 'Simbolo' and self.tokens[0].lexema == "=":
                self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
                self.dot.edge('B',f'N{self.i}')
                self.i+=1
                self.tokens.pop(0)
              
                if self.tokens[0].nombre == 'Simbolo' and self.tokens[0].lexema == "[":
                    self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
                    self.dot.edge('B',f'N{self.i}')
                    self.i+=1
                    self.tokens.pop(0)
                 
                    if self.tokens[0].nombre == 'String':
                        
                        self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
                        self.dot.edge('B',f'N{self.i}')                        
                        self.i+=1
                        self.dot.node(f'L{self.i}',f'Lista Strings')
                        self.dot.edge('B',f'L{self.i}')
                        clave = self.tokens.pop(0)
                        self.listaClaves.append(clave.lexema)
                         
                        self.listaStrings()
                        
                        if self.tokens[0].nombre == "Simbolo" and self.tokens[0].lexema=="]":
                            self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
                            self.dot.edge('B',f'N{self.i}')
                            self.i+=1
                            self.tokens.pop(0)
                        else:
                            self.errores.append(Error('La lista de claves no ha sido cerrada',self.tokens[0].columna, self.tokens[0].fila))
                            self.recuperar(']')
                                                                               
                    else:
                        self.errores.append(Error('Se requiere al menos un elemento "String" en la lista',self.tokens[0].columna, self.tokens[0].fila))
                        self.recuperarn('String')
                else:
                    self.errores.append(Error('Falta la apertura de corchete',self.tokens[0].columna, self.tokens[0].fila))
                    self.recuperar('[')
            else:
                self.errores.append(Error('Falto un signo =',self.tokens[0].columna, self.tokens[0].fila))
                self.recuperar('=')
        else:
           
            self.errores.append(Error('No se encontraron las claves',self.tokens[0].columna, self.tokens[0].fila))
            
     
    #<ListaStrings> ::= coma string <ListaStrings>
     #               | lambda       
    def listaStrings(self):
        if self.tokens[0].nombre == "Simbolo" and self.tokens[0].lexema == ",":
            self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'L{self.i}',f'N{self.i}')
            self.i+=1
            self.tokens.pop(0)
            if self.tokens[0].nombre == 'String':
                self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'L{self.i-1}',f'N{self.i}')
                self.i+=1
                clave = self.tokens.pop(0)
                self.listaClaves.append(clave.lexema)
                self.dot.node(f'L{self.i}',f'Lista Strings')
                self.dot.edge(f'L{self.i-2}',f'L{self.i}')    
                self.listaStrings()
            else:
                self.errores.append(Error('Falto un string despues de la coma ,',self.tokens[0].columna, self.tokens[0].fila))
        else:
            self.dot.edge(f'L{self.i}','ε')
                
    #<Registros> ::= Registros igual corcheteA <registro> <otroregistro> corcheteC
    #<registro> ::= llaveA <valor> <otroValor> llaveC
    #<valor> ::= string  
    #            | entero
    #            | decimal
    #<otroValor> ::=  coma <valor> <otroValor>
    #               | lambda
    #<otroRegistro> ::= <registro> <otroRegistro>
    #                | lambda 
    
    def registros(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema =="Registros":
            self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
            self.dot.edge('C',f'N{self.i}')
            self.i+=1
            self.tokens.pop(0)
            if self.tokens[0].nombre == 'Simbolo' and self.tokens[0].lexema == "=":
                self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
                self.dot.edge('C',f'N{self.i}')
                self.i+=1
                self.tokens.pop(0)
                if self.tokens[0].nombre == 'Simbolo' and self.tokens[0].lexema == "[":
                    self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
                    self.dot.edge('C',f'N{self.i}')
                    self.i+=1
                    self.tokens.pop(0)
                    
                    self.dot.node(f'Reg{self.i}','Registro')
                    self.dot.edge('C',f'Reg{self.i}')
                    self.registro()
                    
                    
                    self.dot.node(f'oR{self.i}','OtroRegistro')
                    self.dot.edge('C',f'oR{self.i}')
                    self.otroregistro()
                    
                    
                    if self.tokens[0].nombre == 'Simbolo' and self.tokens[0].lexema == "]":
                        self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
                        self.dot.edge('C',f'N{self.i}')
                        self.i+=1
                        self.tokens.pop(0)
                    else:
                       self.errores.append(Error('Se esperaba ]',self.tokens[0].columna, self.tokens[0].fila)) # 
                       self.recuperar(']')
                else:
                    self.errores.append(Error('Se esperaban un simbolo [',self.tokens[0].columna, self.tokens[0].fila))
                    self.recuperar('[')
                    
            else: 
                self.errores.append(Error('Se esperaba un simbolo igual',self.tokens[0].columna, self.tokens[0].fila))
                self.recuperar('=')
        else:
            self.errores.append(Error('No se encontraron los registros',self.tokens[0].columna, self.tokens[0].fila))
            self.recuperar('Registros')
            
  
            
       
    def registro(self):
        if self.tokens[0].nombre =="Simbolo" and self.tokens[0].lexema=="{":
            self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Reg{self.i}',f'N{self.i}')
            reg=self.i
            self.i+=1
            
            
            self.tokens.pop(0)
            
            self.dot.node(f'V{self.i}','Valor')
            self.dot.edge(f'Reg{self.i-1}',f'V{self.i}')
            self.listaV = []
            self.valor() 
            self.dot.node(f'OV{self.i}','Otro Valor')
            self.dot.edge(f'Reg{self.i-1}',f'OV{self.i}')
            self.otroValor()
            
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="}":
                self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'Reg{reg}',f'N{self.i}')
                reg+=1
                self.i+=1
                self.tokens.pop(0)
            else:
                    self.errores.append(Error('Error en lista de registros',self.tokens[0].columna, self.tokens[0].fila))
                    self.recuperar('}')           
        else: 
            self.errores.append(Error('Se esperaba un registro en {',self.tokens[0].columna, self.tokens[0].fila))
            self.recuperar('{')
            
    def valor(self):
        if self.tokens[0].nombre == "String" or self.tokens[0].nombre == "Entero" or self.tokens[0].nombre == "Decimal":
            
            print(f'{self.i} {self.tokens[0].lexema}')
            self.dot.node(f'vs{self.v}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'V{self.i}',f'vs{self.v}')
            self.listaV.append(self.tokens[0].lexema)
            self.v+=1
            
            
            self.tokens.pop(0)
        else:
            self.errores.append(Error('Deberia haber un string o un numero',self.tokens[0].columna, self.tokens[0].fila))
    
    def otroValor(self):
        if self.tokens[0].nombre == "Simbolo" and self.tokens[0].lexema == ",":
            self.listaRegistros.append(self.listaV)
            self.tokens.pop(0)
            self.valor()
            self.otroValor()
        else:
            print("registro completo")
            
                
    
    def otroregistro(self):
        if self.tokens[0].nombre == "Simbolo" and self.tokens[0].lexema=="{":
            self.dot.node(f'oR{self.i}','OtroRegistro')
            self.dot.node(f'Reg{self.i}','Registro')
            self.dot.edge(f'oR{self.i}',f'Reg{self.i}')   
            self.registro()
            self.dot.edge(f'oR{self.i-2}',f'oR{self.i}')
            self.otroregistro()
        else:
            self.dot.node(f'oR{self.i}','OtroRegistro')
            self.dot.node(f'va{self.i}','ε')
            self.dot.edge(f'oR{self.i}',f'va{self.i}')
            
    def funciones(self):
        if self.tokens[0].lexema =="imprimir" or self.tokens[0].lexema =="imprimirln" or self.tokens[0].lexema == "conteo" or self.tokens[0].lexema =="promedio" or self.tokens[0].lexema =="contarsi" or self.tokens[0].lexema =="datos" or self.tokens[0].lexema =="sumar" or self.tokens[0].lexema =="stock" or self.tokens[0].lexema =="max" or self.tokens[0].lexema =="min" or self.tokens[0].lexema =="exportarReporte":
            self.dot.node(f'F{self.cf}','Funcion')
            self.dot.edge('D',f'F{self.cf}') 
            
            self.funcion()
            
            self.dot.node(f'oF{self.cf-1}','OtraFuncion')
            self.dot.edge('D',f'oF{self.cf-1}')
            self.otrafuncion()
        else:
            self.errores.append(Error('Funcion incorrecta',self.tokens[0].columna, self.tokens[0].fila))
            self.recuperarfunc('imprimir','imprimirln','conteo','promedio','contarsi','datos','sumar','stock','max','min','exportarReporte')
            
            
        
    def funcion(self):
        if self.tokens[0].lexema =="imprimir" or self.tokens[0].lexema =="imprimirln" or self.tokens[0].lexema == "conteo" or self.tokens[0].lexema =="promedio" or self.tokens[0].lexema =="contarsi" or self.tokens[0].lexema =="datos" or self.tokens[0].lexema =="sumar" or self.tokens[0].lexema =="max" or self.tokens[0].lexema =="min" or self.tokens[0].lexema =="exportarReporte":
            
            
            self.imprimir()
            self.imprimirln()
            self.conteo()
            self.promedio()
            self.contarsi()
            self.datos()
            self.sumar()
            self.fmax()
            self.fmin()
            self.exportarReporte()
        else:
            
            self.errores.append(Error('Funcion incorrecta',self.tokens[0].columna, self.tokens[0].fila))
            self.recuperarfunc('imprimir','imprimirln','conteo','promedio','contarsi','datos','sumar','stock','max','min','exportarReporte')
    
    def otrafuncion(self):
        if self.tokens[0].nombre !="Fin":
            self.funcion()  
            self.otrafuncion()
        else:
            
            self.dot.render('Arbol.dot')
            print("Analisis completo xd")
            
    def imprimir(self):# *Funcion completada
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="imprimir":
            self.cf+=1
            self.dot.node(f'F{self.cf}','Funcion')
            self.dot.node(f'oF{self.cf-1}',f'OtraFuncion')
            self.dot.edge(f'oF{self.cf-2}',f'oF{self.cf-1}')
            self.dot.edge(f'oF{self.cf-1}',f'F{self.cf}')
            
            self.dot.node(f'Fu{self.cf}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'F{self.cf-1}',f'Fu{self.cf}')
            
            self.dot.node(f't{self.funcionc}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Fu{self.cf}',f't{self.funcionc}')
            
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.dot.node(f'S{self.funcionc}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'Fu{self.cf}',f'S{self.funcionc}')
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.textoimp+=self.tokens[0].lexema
                    self.dot.node(f'St{self.funcionc}',f'{self.tokens[0].lexema}')
                    self.dot.edge(f'Fu{self.cf}',f'St{self.funcionc}')
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.dot.node(f'S2{self.funcionc}',f'{self.tokens[0].lexema}')
                        self.dot.edge(f'Fu{self.cf}',f'S2{self.funcionc}')
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.dot.node(f'S3{self.funcionc}',f'{self.tokens[0].lexema}')
                            self.dot.edge(f'Fu{self.cf}',f'S3{self.funcionc}')
                            self.funcionc+=1
                            self.tokens.pop(0)
                        else:
                            self.errores.append(Error('Se esperaba un ;',self.tokens[0].columna, self.tokens[0].fila)) 
                            self.recuperarn(';')
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila))
                         
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
                    self.recuperar('String')
            else:
               self.errores.append(Error('Despues de imprimir se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))
               self.recuperarn('(')
        else:
            pass
              
        
            
    def imprimirln(self):#* funcion completada
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="imprimirln":
            self.cf+=1
            self.dot.node(f'F{self.cf}','Funcion')
            self.dot.node(f'oF{self.cf-1}',f'OtraFuncion')
            self.dot.edge(f'oF{self.cf-2}',f'oF{self.cf-1}')
            self.dot.edge(f'oF{self.cf-1}',f'F{self.cf}')
            
            self.dot.node(f'Fu{self.cf}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'F{self.cf-1}',f'Fu{self.cf}')
            
            self.dot.node(f't{self.funcionc}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Fu{self.cf}',f't{self.funcionc}')
            
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.dot.node(f'S{self.funcionc}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'Fu{self.cf}',f'S{self.funcionc}')
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.dot.node(f'St{self.funcionc}',f'{self.tokens[0].lexema}')
                    self.dot.edge(f'Fu{self.cf}',f'St{self.funcionc}')
                    self.textoimpln+=self.tokens[0].lexema+'\n'
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.dot.node(f'S2{self.funcionc}',f'{self.tokens[0].lexema}')
                        self.dot.edge(f'Fu{self.cf}',f'S2{self.funcionc}')
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.dot.node(f'S3{self.funcionc}',f'{self.tokens[0].lexema}')
                            self.dot.edge(f'Fu{self.cf}',f'S3{self.funcionc}')
                            self.funcionc+=1
                            self.tokens.pop(0)
                            print("ImprimirLn correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;',self.tokens[0].columna, self.tokens[0].fila)) 
                            self.recuperarn(';')
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                        self.recuperarn(')')
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
                    self.recuperarn('String')
            else:
               self.errores.append(Error('Despues de la imprimirln se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))
               self.recuperarn('(')
        else:
            pass  
        
            
    def conteo(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="conteo":
            self.cf+=1
            self.dot.node(f'F{self.cf}','Funcion')
            self.dot.node(f'oF{self.cf-1}',f'OtraFuncion')
            self.dot.edge(f'oF{self.cf-2}',f'oF{self.cf-1}')
            self.dot.edge(f'oF{self.cf-1}',f'F{self.cf}')
            
            self.dot.node(f'Fu{self.cf}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'F{self.cf-1}',f'Fu{self.cf}')
            
            self.dot.node(f't{self.funcionc}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Fu{self.cf}',f't{self.funcionc}')
            
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.dot.node(f'S{self.funcionc}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'Fu{self.cf}',f'S{self.funcionc}')
                self.tokens.pop(0)
                if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                    self.dot.node(f'S2{self.funcionc}',f'{self.tokens[0].lexema}')
                    self.dot.edge(f'Fu{self.cf}',f'S2{self.funcionc}')
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                        self.dot.node(f'S3{self.funcionc}',f'{self.tokens[0].lexema}')
                        self.dot.edge(f'Fu{self.cf}',f'S3{self.funcionc}')
                        self.funcionc+=1
                        self.tokens.pop(0)
                        self.conteos=True
                        print("Conteo correcto")
                    else:
                        self.errores.append(Error('Se esperaba un ;',self.tokens[0].columna, self.tokens[0].fila))
                        self.recuperarn(';') 
                else:
                    self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                    self.recuperarn(')')
            else:
               self.errores.append(Error('Despues de conteo se esperaba un (',self.tokens[0].columna, self.tokens[0].fila)) 
               self.recuperarn('(') 
        else:
            pass
            
    def promedio(self):
        
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="promedio":
            self.cf+=1
            self.dot.node(f'F{self.cf}','Funcion')
            self.dot.node(f'oF{self.cf-1}',f'OtraFuncion')
            self.dot.edge(f'oF{self.cf-2}',f'oF{self.cf-1}')
            self.dot.edge(f'oF{self.cf-1}',f'F{self.cf}')
            
            self.dot.node(f'Fu{self.cf}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'F{self.cf-1}',f'Fu{self.cf}')
            
            self.dot.node(f't{self.funcionc}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Fu{self.cf}',f't{self.funcionc}')
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.dot.node(f'S{self.funcionc}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'Fu{self.cf}',f'S{self.funcionc}')
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.dot.node(f'St{self.funcionc}',f'{self.tokens[0].lexema}')
                    self.dot.edge(f'Fu{self.cf}',f'St{self.funcionc}')
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.dot.node(f'Sss{self.funcionc}',f'{self.tokens[0].lexema}')
                        self.dot.edge(f'Fu{self.cf}',f'Sss{self.funcionc}')
                        self.funcionc+=1
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.tokens.pop(0)
                            print("Promedio correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;',self.tokens[0].columna, self.tokens[0].fila)) 
                            self.recuperarn(';')
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila))
                        self.recuperarn(')') 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
                    self.recuperar('String')
            else:
               self.errores.append(Error('Despues de promedio se esperaba un (',self.tokens[0].columna, self.tokens[0].fila)) 
               self.recuperarn('(') 

    
    def contarsi(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="contarsi":
            self.cf+=1
            self.dot.node(f'F{self.cf}','Funcion')
            self.dot.node(f'oF{self.cf-1}',f'OtraFuncion')
            self.dot.edge(f'oF{self.cf-2}',f'oF{self.cf-1}')
            self.dot.edge(f'oF{self.cf-1}',f'F{self.cf}')
            
            self.dot.node(f'Fu{self.cf}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'F{self.cf-1}',f'Fu{self.cf}')
            
            self.dot.node(f't{self.funcionc}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Fu{self.cf}',f't{self.funcionc}')
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.dot.node(f'S{self.funcionc}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'Fu{self.cf}',f'S{self.funcionc}')
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    
                    #usar este string para la funcion stringcontarsi

                    self.dot.node(f'Sr{self.funcionc}',f'{self.tokens[0].lexema}')
                    self.dot.edge(f'Fu{self.cf}',f'Sr{self.funcionc}')
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==",":
                        self.dot.node(f'S2{self.funcionc}',f'{self.tokens[0].lexema}')
                        self.dot.edge(f'Fu{self.cf}',f'S2{self.funcionc}')
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Entero":
                            self.dot.node(f'nn{self.funcionc}',f'{self.tokens[0].lexema}')
                            self.dot.edge(f'Fu{self.cf}',f'nn{self.funcionc}')
                            self.tokens.pop(0)
                            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                                self.dot.node(f'S5{self.funcionc}',f'{self.tokens[0].lexema}')
                                self.dot.edge(f'Fu{self.cf}',f'S5{self.funcionc}')
                                self.tokens.pop(0)
                                if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                                    self.dot.node(f'Smm{self.funcionc}',f'{self.tokens[0].lexema}')
                                    self.dot.edge(f'Fu{self.cf}',f'Smm{self.funcionc}')
                                    self.funcionc+=1
                                    self.tokens.pop(0)
                                    print("Contar correcto")
                            else:
                                 self.errores.append(Error('Se esperaba cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                                 self.recuperar(')')
                        else:
                            self.errores.append(Error('Se esperaba un numero entero',self.tokens[0].columna, self.tokens[0].fila)) 
                            self.recuperar('String')
                    else:
                        self.errores.append(Error('Se esperaba una separacion por coma',self.tokens[0].columna, self.tokens[0].fila)) 
                        self.recuperar('String')
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
                    self.recuperar('String')
            else:
               self.errores.append(Error('Despues de contarsi se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))
               self.recuperar('(')  

    
    def datos(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="datos":   
            self.cf+=1
            self.dot.node(f'F{self.cf}','Funcion')
            self.dot.node(f'oF{self.cf-1}',f'OtraFuncion')
            self.dot.edge(f'oF{self.cf-2}',f'oF{self.cf-1}')
            self.dot.edge(f'oF{self.cf-1}',f'F{self.cf}')
            
            self.dot.node(f'Fu{self.cf}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'F{self.cf-1}',f'Fu{self.cf}')
            
            self.dot.node(f't{self.funcionc}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Fu{self.cf}',f't{self.funcionc}')
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.dot.node(f'S2{self.funcionc}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'Fu{self.cf}',f'S2{self.funcionc}')
                self.tokens.pop(0)
                if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                    self.dot.node(f'S3{self.funcionc}',f'{self.tokens[0].lexema}')
                    self.dot.edge(f'Fu{self.cf}',f'S3{self.funcionc}')
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                        self.dot.node(f'S22{self.funcionc}',f'{self.tokens[0].lexema}')
                        self.dot.edge(f'Fu{self.cf}',f'S22{self.funcionc}')
                        self.funcionc+=1
                        self.tokens.pop(0)
                        self.datosd=True
                        print("Datos correcto")
                    else:
                        self.errores.append(Error('Se esperaba un ;a',self.tokens[0].columna, self.tokens[0].fila))
                        self.recuperarn(';')
                else:
                    self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila))
                    self.recuperarn(')') 
            else:
               self.errores.append(Error('Despues de datos se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))
               self.recuperarn('(')  
        
    
    def sumar(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="sumar": 
            self.cf+=1
            self.dot.node(f'F{self.cf}','Funcion')
            self.dot.node(f'oF{self.cf-1}',f'OtraFuncion')
            self.dot.edge(f'oF{self.cf-2}',f'oF{self.cf-1}')
            self.dot.edge(f'oF{self.cf-1}',f'F{self.cf}')
            
            self.dot.node(f'Fu{self.cf}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'F{self.cf-1}',f'Fu{self.cf}')
            
            self.dot.node(f't{self.funcionc}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Fu{self.cf}',f't{self.funcionc}')
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.dot.node(f'Ss2{self.funcionc}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'Fu{self.cf}',f'Ss2{self.funcionc}')
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.dot.node(f'Ss3{self.funcionc}',f'{self.tokens[0].lexema}')
                    self.dot.edge(f'Fu{self.cf}',f'Ss3{self.funcionc}')
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.dot.node(f'Ssd2{self.funcionc}',f'{self.tokens[0].lexema}')
                        self.dot.edge(f'Fu{self.cf}',f'Ssd2{self.funcionc}')
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.dot.node(f'Ssdd2{self.funcionc}',f'{self.tokens[0].lexema}')
                            self.dot.edge(f'Fu{self.cf}',f'Ssdd2{self.funcionc}')
                            self.funcionc+=1
                            self.tokens.pop(0)
                            print("Sumar correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;b',self.tokens[0].columna, self.tokens[0].fila))
                            self.recuperarn(';') 
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila))
                        self.recuperarn(')') 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila))
                    self.recuperar('String') 
            else:
               self.errores.append(Error('Despues de sumar se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))
               self.recuperarn('(')  
        
        
    def fmax(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="max":
            self.cf+=1
            self.dot.node(f'F{self.cf}','Funcion')
            self.dot.node(f'oF{self.cf-1}',f'OtraFuncion')
            self.dot.edge(f'oF{self.cf-2}',f'oF{self.cf-1}')
            self.dot.edge(f'oF{self.cf-1}',f'F{self.cf}')
            
            self.dot.node(f'Fu{self.cf}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'F{self.cf-1}',f'Fu{self.cf}')
            
            self.dot.node(f't{self.funcionc}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Fu{self.cf}',f't{self.funcionc}')
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.dot.node(f'Ss2{self.funcionc}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'Fu{self.cf}',f'Ss2{self.funcionc}')
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.dot.node(f'Ssss2{self.funcionc}',f'{self.tokens[0].lexema}')
                    self.dot.edge(f'Fu{self.cf}',f'Ssss2{self.funcionc}')
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.dot.node(f'ddSs2{self.funcionc}',f'{self.tokens[0].lexema}')
                        self.dot.edge(f'Fu{self.cf}',f'ddSs2{self.funcionc}')
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.dot.node(f'Ssddddd2{self.funcionc}',f'{self.tokens[0].lexema}')
                            self.dot.edge(f'Fu{self.cf}',f'Ssddddd2{self.funcionc}')
                            self.funcionc += 1
                            self.tokens.pop(0)
                            print("max correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;c',self.tokens[0].columna, self.tokens[0].fila)) 
                            self.recuperarn(';')
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                        self.recuperarn(')')
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
                    self.recuperar('String')
            else:
                self.errores.append(Error('Despues de fmax se esperaba un (',self.tokens[0].columna, self.tokens[0].fila)) 
                self.recuperarn('(') 
        
    
    def fmin(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="min": 
            self.cf+=1
            self.dot.node(f'F{self.cf}','Funcion')
            self.dot.node(f'oF{self.cf-1}',f'OtraFuncion')
            self.dot.edge(f'oF{self.cf-2}',f'oF{self.cf-1}')
            self.dot.edge(f'oF{self.cf-1}',f'F{self.cf}')
            
            self.dot.node(f'Fu{self.cf}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'F{self.cf-1}',f'Fu{self.cf}')
            
            self.dot.node(f't{self.funcionc}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Fu{self.cf}',f't{self.funcionc}')
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.dot.node(f'Ss2{self.funcionc}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'Fu{self.cf}',f'Ss2{self.funcionc}')
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.dot.node(f'Stt2{self.funcionc}',f'{self.tokens[0].lexema}')
                    self.dot.edge(f'Fu{self.cf}',f'Stt2{self.funcionc}')
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.dot.node(f'Ss2ddd{self.funcionc}',f'{self.tokens[0].lexema}')
                        self.dot.edge(f'Fu{self.cf}',f'Ss2ddd{self.funcionc}')
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.dot.node(f'Ssssssss2{self.funcionc}',f'{self.tokens[0].lexema}')
                            self.dot.edge(f'Fu{self.cf}',f'Ssssssss2{self.funcionc}')
                            self.funcionc += 1
                            self.tokens.pop(0)
                            print("min correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;d',self.tokens[0].columna, self.tokens[0].fila))
                            self.recuperarn(';') 
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila))
                        self.recuperarn(')') 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila))
                    self.recuperar('String') 
            else:
               self.errores.append(Error('Despues de fmin se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))
               self.recuperarn('(')  
        
        
    def exportarReporte(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="exportarReporte":
            self.cf+=1
            self.dot.node(f'F{self.cf}','Funcion')
            self.dot.node(f'oF{self.cf-1}',f'OtraFuncion')
            self.dot.edge(f'oF{self.cf-2}',f'oF{self.cf-1}')
            self.dot.edge(f'oF{self.cf-1}',f'F{self.cf}')
            
            self.dot.node(f'Fu{self.cf}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'F{self.cf-1}',f'Fu{self.cf}')
            
            self.dot.node(f't{self.funcionc}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Fu{self.cf}',f't{self.funcionc}')
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.dot.node(f'S2s2{self.funcionc}',f'{self.tokens[0].lexema}')
                self.dot.edge(f'Fu{self.cf}',f'S2s2{self.funcionc}')
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.dot.node(f'S3s2{self.funcionc}',f'{self.tokens[0].lexema}')
                    self.dot.edge(f'Fu{self.cf}',f'S3s2{self.funcionc}')
                    self.tituloTabla=self.tokens[0].lexema
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.dot.node(f'S4s2{self.funcionc}',f'{self.tokens[0].lexema}')
                        self.dot.edge(f'Fu{self.cf}',f'S4s2{self.funcionc}')
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.dot.node(f'S5s2{self.funcionc}',f'{self.tokens[0].lexema}')
                            self.dot.edge(f'Fu{self.cf}',f'S5s2{self.funcionc}')
                            self.funcionc += 1
                            self.tokens.pop(0)
                            self.generarTabla=True
                            print("Exportar correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;e',self.tokens[0].columna, self.tokens[0].fila))
                            self.recuperarn(';') 
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila))
                        self.recuperarn(')') 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
                    self.recuperar('String')
            else:
               self.errores.append(Error('Despues de exportarReporte se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))
               self.recuperarn('(')  
        else:
            pass
    
    
      
    