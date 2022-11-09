from .ProyectosView import ProyectosView
from tkinter import *
from tkinter import ttk

class MainView:
    """Ventana principal de la aplicacion"""
    def __init__(self, ventana, connection):
        """
            - Recibe la el objeto conexión que se usa para acceder en la base de datos
            - la ventana padre para poder ubicar la ventana encima de esta
        """
        self.connection = connection
        self.ventana = ventana

        # Configuración de la ventana
        self.ventana.title("Administrador de proyectos")
        self.ventana.geometry("250x150")

        # Cambia el tema de los elementos
        ttk.Style().theme_use('clam')

        # Configuración del frame
        self.frame = LabelFrame(self.ventana, text="Gestor de proyectos")
        self.frame.grid(row=0, column=0, columnspan=3, pady=35, padx=60)

        # Configuración botón
        self.proyectos_btn = Button(self.frame, text="Gestionar proyectos", command=self.open_proyectos_view)
        self.proyectos_btn.grid(row=1, column=1, padx=10, pady=10)

    def open_proyectos_view(self):
        """Muestra la tabla de los proyectos"""
        ProyectosView(self.ventana, self.connection)
