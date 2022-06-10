from connection import Connection
from tkinter import *
from views.MainView import MainView

"""
Miembros del grupo
Grupo 3
6634178 - Carballo Benítez Richar Florentino
5218759 - Díaz Pérez Giuliano Darío Martín
5739116 - Mendieta Gonzalez Germán Antonio
6043735 - Perez Martinez Ever
5107448 - Kiss Benítez Leandro Fabián
"""


def main():
    # Se crea una conexión a la base de datos
    connection = Connection()
    
    # Ventana principal del proyecto
    ventana = Tk()
    MainView(ventana, connection)
    ventana.mainloop()
    
    # Cierra la conexión con la base de datos
    connection.close_connection()

# Checkquear si el archivo main.py no esta siendo importado
if __name__ == '__main__':
    main()
