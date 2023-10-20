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
<funcion> <otrafuncion>

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
    <funcion>:: = imprimir parentesisA string parentesisC puntocoma                    
                 |imprimirln parentesisA string parentesisC puntocoma  
                 |conteo parentesisA parentesisC puntocoma 
                 |promedio parentesisA string parentesisC puntocoma
                 |contarsi parentesisA string coma entero parentesisC puntocoma
                 |datos parentesisA parentesisC puntocoma
                 |sumar parentesisA string parentesisC puntocoma
                 |max parentesisA string parentesisC puntocoma
                 |min parentesisA string parentesisC puntocoma
                 |exporterReporte parentesisA string parentesisC puntocoma
    <otrafuncion> ::= <funcion><otrafuncion>
                    | lambda 
 
'''
from Sintáctico.SToken import Token
from Sintáctico.SError import Error

class Sintactico():
    def __init__(self,tokens) -> None:
        self.tokens = tokens
        self.listaClaves = []
        self.listaRegistros = []
        self.errores = []
        
        tokenN = Token('Fin','Fin',0,0)
        self.tokens.append(tokenN)
    
    def ImprimirErrores(self):
        print("Errores")
        for error in self.errores:
            print(f'{error}')
    
    def analizar(self):
        self.inicio()
    
    #<Inicio> ::= <Claves> <Registros> <Funciones>
    def inicio(self):
        self.claves()
        self.registros();
        #self.funciones();
    
    #<Claves> ::= Claves igual corcheteA string <ListaStrings> corcheteC
    def claves(self):
        if self.tokens[0].nombre == 'Texto' and self.tokens[0].lexema =="Claves":
            #print("Clave encontrada")
            self.tokens.pop(0)
            if self.tokens[0].nombre == 'Simbolo' and self.tokens[0].lexema == "=":
                #print("Simbolo encontrado")
                self.tokens.pop(0)
                if self.tokens[0].nombre == 'Simbolo' and self.tokens[0].lexema == "[":
                    #print("Corchete abierto")
                    self.tokens.pop(0)
                    if self.tokens[0].nombre == 'String':
                        #print("clave encontrada")
                        clave = self.tokens.pop(0)
                        self.listaClaves.append(clave.lexema)
                        self.listaStrings()
                        if self.tokens[0].nombre == "Simbolo" and self.tokens[0].lexema=="]":
                            self.tokens.pop(0)
                            print("Claves completas")
                        else:
                            self.errores.append(Error('La lista de claves no ha sido cerrada',self.tokens[0].columna, self.tokens[0].fila))                                                   
                    else:
                        self.errores.append(Error('Se requiere al menos un elemento en la lista',self.tokens[0].columna, self.tokens[0].fila))
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
            self.tokens.pop(0)
            if self.tokens[0].nombre == 'String':
                clave = self.tokens.pop(0)
                self.listaClaves.append(clave.lexema)
                self.listaStrings()
            else:
                self.errores.append(Error('Falto un string despues de la coma ,',self.tokens[0].columna, self.tokens[0].fila))
                
    #<Registros> ::= Registros igual corcheteA <registro> <otroregistro> corcheteC
    #<registro> ::= llaveA <valor> <otroValor> llaveC
    #<valor> ::= string  
    #            | entero
    #            | decimal
    #<otroValor> ::=  coma <valor> <otroValor>
    #               | lambda
    #<otroRegistro> ::= <registro> <otroRegistro>
    #                | lambda """
    
    def registros(self):
        if self.tokens[0].nombre == "Texto" and self.tokens[0].lexema =="Registros":
            self.tokens.pop(0)
            if self.tokens[0].nombre == 'Simbolo' and self.tokens[0].lexema == "=":
                self.tokens.pop(0)
                if self.tokens[0].nombre == 'Simbolo' and self.tokens[0].lexema == "[":
                    self.tokens.pop(0)
                    self.registro()#TODO: Seguir aca con otroregistro y corcheteC
                else:
                    self.errores.append(Error('Se esperaban registros [',self.tokens[0].columna, self.tokens[0].fila))
            else: 
                self.errores.append(Error('Se esperaba un simbolo igual',self.tokens[0].columna, self.tokens[0].fila))
        else:
            self.errores.append(Error('No se encontraron los registros',self.tokens[0].columna, self.tokens[0].fila))
            
       
    def registro(self):
        if self.tokens[0].nombre =="Simbolo" and self.tokens[0].lexema=="{":
            self.tokens.pop(0)
            self.valor() #TODO: Seguir aca con los valores dentro de registro
        else: 
            self.errores.append(Error('Se esperaba al menos un registro',self.tokens[0].columna, self.tokens[0].fila))