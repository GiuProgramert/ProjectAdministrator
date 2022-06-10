from tkinter import *
from tkinter import ttk
from helpers.LoadTableData import LoadTableData

class RelacionesView(LoadTableData):
    def __init__(self, id_actividad, ventana_padre, connection):
        self.connection = connection
        self.ventana_padre = ventana_padre
        self.id_actividad = id_actividad

        # Confirguracion de la ventana
        self.ventana = Toplevel(self.ventana_padre)
        self.ventana.title("Relaciones")
        self.ventana.geometry("850x450")

        # Configuración de crear botón
        self.crear_btn = Button(self.ventana, text="Agregar Relacion", command=self.open_create_relacion_form_view)
        self.crear_btn.grid(row=0, column=0, columnspan=3, pady=20)
        
        # Configuración de tabla
        self.tabla = ttk.Treeview(self.ventana, height=14, columns = ('Actividad Precedente', 'Actividad Siguiente'))

        super().__init__(self.tabla, "SELECT * FROM Relacion where ")