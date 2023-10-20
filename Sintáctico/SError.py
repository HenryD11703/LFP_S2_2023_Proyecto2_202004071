class Error():
    def __init__(self, lexema,columna, fila) -> None:
        self.lexema = lexema
        
        self.columna = columna
        self.fila = fila
    
    def __str__(self):
        return f'Lexema: {self.lexema}, fila: {self.fila}, columna: {self.columna}'