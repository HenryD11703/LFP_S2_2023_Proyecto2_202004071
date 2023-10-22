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
        self.listaClaves = []
        self.listaRegistros = []
        self.errores = []
        self.i=0
        self.v=0
        self.dot = Digraph()
        

        tokenN = Token('Fin','Fin',0,0)
        self.tokens.append(tokenN)
    
    def ImprimirErrores(self):
        print("Errores")
        for error in self.errores:
            print(f'{error}')
    
    def analizar(self):
        self.dot.node('A','Inicio')
        self.inicio()
        
        
    
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
                        self.tokens.pop(0)
                        
                        self.listaStrings()
                        
                        if self.tokens[0].nombre == "Simbolo" and self.tokens[0].lexema=="]":
                            self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
                            self.dot.edge('B',f'N{self.i}')
                            self.i+=1
                            self.tokens.pop(0)
                        else:
                            self.errores.append(Error('La lista de claves no ha sido cerrada',self.tokens[0].columna, self.tokens[0].fila))
                                                                               
                    else:
                        self.errores.append(Error('Se requiere al menos un elemento "String" en la lista',self.tokens[0].columna, self.tokens[0].fila))
                else:
                    self.errores.append(Error('Falta la apertura de corchete',self.tokens[0].columna, self.tokens[0].fila))
            else:
                self.errores.append(Error('Falto un signo =',self.tokens[0].columna, self.tokens[0].fila))
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
                self.tokens.pop(0)
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
                else:
                    self.errores.append(Error('Se esperaban registros [',self.tokens[0].columna, self.tokens[0].fila))
            else: 
                self.errores.append(Error('Se esperaba un simbolo igual',self.tokens[0].columna, self.tokens[0].fila))
        else:
            self.errores.append(Error('No se encontraron los registros',self.tokens[0].columna, self.tokens[0].fila))
            
  
            
       
    def registro(self):
        if self.tokens[0].nombre =="Simbolo" and self.tokens[0].lexema=="{":
            self.dot.node(f'N{self.i}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'Reg{self.i}',f'N{self.i}')
            reg=self.i
            self.i+=1
            self.tokens.pop(0)
            
            self.dot.node(f'V{self.i}','Valor')
            self.dot.edge(f'Reg{self.i-1}',f'V{self.i}')
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
                    self.errores.append(Error('La lista de registro no fue cerrada',self.tokens[0].columna, self.tokens[0].fila))           
        else: 
            self.errores.append(Error('Se esperaba al menos un registro',self.tokens[0].columna, self.tokens[0].fila))
            
    def valor(self):
        if self.tokens[0].nombre == "String" or self.tokens[0].nombre == "Entero" or self.tokens[0].nombre == "Decimal":
            print(f'{self.i} {self.tokens[0].lexema}')
            self.dot.node(f'vs{self.v}',f'{self.tokens[0].lexema}')
            self.dot.edge(f'V{self.i}',f'vs{self.v}')
            self.v+=1
            
            
            self.tokens.pop(0)
        else:
            self.errores.append(Error('Deberia haber un string o un numero',self.tokens[0].columna, self.tokens[0].fila))
    
    def otroValor(self):
        if self.tokens[0].nombre == "Simbolo" and self.tokens[0].lexema == ",":
            print(f'{self.tokens[0].lexema}')
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
            self.funcion()
            self.otrafuncion()
        else:
            self.errores.append(Error('No hay funciones :(',self.tokens[0].columna, self.tokens[0].fila))
            
        
    def funcion(self):
        if self.tokens[0].lexema =="imprimir" or self.tokens[0].lexema =="imprimirln" or self.tokens[0].lexema == "conteo" or self.tokens[0].lexema =="promedio" or self.tokens[0].lexema =="contarsi" or self.tokens[0].lexema =="datos" or self.tokens[0].lexema =="sumar" or self.tokens[0].lexema =="stock" or self.tokens[0].lexema =="max" or self.tokens[0].lexema =="min" or self.tokens[0].lexema =="exportarReporte":
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
             self.errores.append(Error('No hay funciones',self.tokens[0].columna, self.tokens[0].fila))
    
    def otrafuncion(self):
        if self.tokens[0].nombre !="Fin":
            self.funcion()
            self.otrafuncion()
        else:
            self.dot.render('Arbol.dot')
            print("Analisis completo xd")
            
    def imprimir(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="imprimir":
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.tokens.pop(0)
                            print("Imprimir correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;',self.tokens[0].columna, self.tokens[0].fila)) 
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
            else:
               self.errores.append(Error('Despues de imprimir se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))
        else:
            pass
              
        
            
    def imprimirln(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="imprimirln":
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.tokens.pop(0)
                            print("ImprimirLn correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;',self.tokens[0].columna, self.tokens[0].fila)) 
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
            else:
               self.errores.append(Error('Despues de imprimir se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))
        else:
            pass  
        
            
    def conteo(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="conteo":
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.tokens.pop(0)
                if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                        self.tokens.pop(0)
                        print("Conteo correcto")
                    else:
                        self.errores.append(Error('Se esperaba un ;',self.tokens[0].columna, self.tokens[0].fila)) 
                else:
                    self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
            else:
               self.errores.append(Error('Despues de imprimir se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))  
        else:
            pass
            
    def promedio(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="promedio":
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.tokens.pop(0)
                            print("Promedio correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;',self.tokens[0].columna, self.tokens[0].fila)) 
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
            else:
               self.errores.append(Error('Despues de imprimir se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))  

    
    def contarsi(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="contarsi":
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==",":
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Entero":
                            self.tokens.pop(0)
                            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                                self.tokens.pop(0)
                                if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                                    self.tokens.pop(0)
                                    print("Contar correcto")
                            else:
                                 self.errores.append(Error('Se esperaba cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                        else:
                            self.errores.append(Error('Se esperaba un numero entero',self.tokens[0].columna, self.tokens[0].fila)) 
                    else:
                        self.errores.append(Error('Se esperaba una separacion por coma',self.tokens[0].columna, self.tokens[0].fila)) 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
            else:
               self.errores.append(Error('Despues de imprimir se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))  

    
    def datos(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="datos":
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.tokens.pop(0)
                if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                        self.tokens.pop(0)
                        print("Datos correcto")
                    else:
                        self.errores.append(Error('Se esperaba un ;a',self.tokens[0].columna, self.tokens[0].fila)) 
                else:
                    self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
            else:
               self.errores.append(Error('Despues de imprimir se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))  
        
    
    def sumar(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="sumar":
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.tokens.pop(0)
                            print("Sumar correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;b',self.tokens[0].columna, self.tokens[0].fila)) 
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
            else:
               self.errores.append(Error('Despues de imprimir se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))  
        
        
    def fmax(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="max":
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.tokens.pop(0)
                            print("max correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;c',self.tokens[0].columna, self.tokens[0].fila)) 
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
            else:
               self.errores.append(Error('Despues de imprimir se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))  
        
    
    def fmin(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="min":
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.tokens.pop(0)
                            print("min correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;d',self.tokens[0].columna, self.tokens[0].fila)) 
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
            else:
               self.errores.append(Error('Despues de imprimir se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))  
        
        
    def exportarReporte(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema=="exportarReporte":
            self.tokens.pop(0)
            if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema=="(":
                self.tokens.pop(0)
                if self.tokens[0].nombre=="String":
                    self.tokens.pop(0)
                    if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==")":
                        self.tokens.pop(0)
                        if self.tokens[0].nombre=="Simbolo" and self.tokens[0].lexema==";":
                            self.tokens.pop(0)
                            print("Exportar correcto")
                        else:
                            self.errores.append(Error('Se esperaba un ;e',self.tokens[0].columna, self.tokens[0].fila)) 
                    else:
                        self.errores.append(Error('Se esperaba un cierre de )',self.tokens[0].columna, self.tokens[0].fila)) 
                else:
                    self.errores.append(Error('Se esperaba un string',self.tokens[0].columna, self.tokens[0].fila)) 
            else:
               self.errores.append(Error('Despues de imprimir se esperaba un (',self.tokens[0].columna, self.tokens[0].fila))  
      
    