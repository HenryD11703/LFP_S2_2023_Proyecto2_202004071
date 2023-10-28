class Token():
    def __init__(self, nombre, lexema, fila, columna) -> None:
        self.nombre = nombre
        self.lexema = lexema
        self.fila = fila
        self.columna = columna

    def __str__(self):
        return f'Nombre: {self.nombre}      lexema: ({self.lexema})      fila: {self.fila}       columna: {self.columna}'
    
    def html(self):
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
<h1>Token Information</h1>
<table>
    <tr>
        <th>Nombre</th>
        <th>Lexema</th>
        <th>Fila</th>
        <th>Columna</th>
    </tr>
    <tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
    </tr>
</table>
</body>
</html>
""".format(self.nombre, self.nombre, self.lexema, self.fila, self.columna)

        return html