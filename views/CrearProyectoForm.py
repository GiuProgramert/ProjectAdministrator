from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview

from datetime import datetime
from helpers.LoadTableData import LoadTableData
from helpers.validaciones import validar_campos_vacios, validar_fech_inicio_proyecto, validar_maximos_elementos

class CrearProyectoForm(LoadTableData):
    def __init__(self, ventana_padre, connection, tabla):
        """
            - Recibe la el objeto conexión que se usa para acceder en la base de datos
            - la ventana padre para poder ubicar la ventana encima de esta
            - y la tabla donde se muestran los datos del proyecto para poder actualizarla
        """
        self.ventana_padre = ventana_padre
        self.connection = connection
        self.tabla = tabla

        # Configuración ventana
        self.ventana = Toplevel(self.ventana_padre)
        self.ventana.title("Crear Proyecto")
        self.ventana.geometry("280x430")

        # Se instancia el padre LoadTableData que sirve para actualizar las tablas 
        # en la interfaz al momento de insetar un proyecto nuevo
        super().__init__(self.tabla, "SELECT * FROM Proyecto")

        # Configuración del frame
        self.frame = LabelFrame(self.ventana, text='Crear Proyecto', height=70)
        self.frame.grid(row=0, column=0, columnspan=5, pady=10, padx=65)

        # Configuración de las etiquetas del formulario
        self.name_label = Label(self.frame, text="Nombre: ").grid(row=1, column=0)
        self.desc_label = Label(self.frame, text="Descripcion: ").grid(row=3, column=0)
        self.fecha_init_label = Label(self.frame, text='Fecha Inicio').grid(row=5, column=0)

        # Configuración de los campos de texto del formulario
        self.name_entry = Entry(self.frame)
        self.name_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.desc_entry = Entry(self.frame)
        self.desc_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.fecha_init_entry = Entry(self.frame)
        self.fecha_init_entry.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Configuración de los campos de dias laborales del formulatio
        self.diasSemana = [0, IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
        self.lunesCheckBock = Checkbutton(self.frame, text="Lunes", variable=self.diasSemana[1], onvalue=1, offvalue=0)
        self.MartesCheckBock = Checkbutton(self.frame, text="Martes", variable=self.diasSemana[2], onvalue=1, offvalue=0)
        self.MiercolesCheckBock = Checkbutton(self.frame, text="Miércoles", variable=self.diasSemana[3], onvalue=1, offvalue=0)
        self.JuevesCheckBock = Checkbutton(self.frame, text="Jueves", variable=self.diasSemana[4], onvalue=1, offvalue=0)
        self.ViernesCheckBock = Checkbutton(self.frame, text="Viernes", variable=self.diasSemana[5], onvalue=1, offvalue=0)
        self.SabadoCheckBock = Checkbutton(self.frame, text="Sábado", variable=self.diasSemana[6], onvalue=1, offvalue=0)

        self.lunesCheckBock.grid(row=7, column=0)
        self.MartesCheckBock.grid(row=8, column=0)
        self.MiercolesCheckBock.grid(row=9, column=0)
        self.JuevesCheckBock.grid(row=10, column=0)
        self.ViernesCheckBock.grid(row=11, column=0)
        self.SabadoCheckBock.grid(row=12, column=0)

        # Botón de insertar
        self.insert_button = Button(self.ventana, text='Crear Proyecto', command=self.create_new_proyecto)
        self.insert_button.grid(row=7, column=0, columnspan=5)

    def create_new_proyecto(self):
        """Toma las nuevas entradas de los formularios y crea un nuevo proyecto"""
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        fecha_inicio = self.fecha_init_entry.get()

        # Validar entradas todos los datos
        if not self.validar_logitud_campos(name, desc):
            messagebox.showinfo(
                f"Error al introducir", 
                f"Nombre muy largo o descripción muy larga", 
                parent=self.ventana
            )
            return None
        if not validar_campos_vacios([name, desc, fecha_inicio], self.ventana):
            return None
        if not self.validar_cantidad_dias_semana():
            return None
        # TODO
        if not validar_fech_inicio_proyecto(fecha_inicio, self.ventana):
            return None
        if not self.validar_cantidad_proyectos():
            return None

        # Concatena el valor de los días seleccionados para guardar en la base de datos
        dias_semana_seleccionados = ""
        for i in range(1, len(self.diasSemana)):
            if self.diasSemana[i].get() == 1:
                dias_semana_seleccionados += str(i)
        
        # Cargamos en la base de datos
        proyecto_id = self.connection.insert(
            "Proyecto",
            ["nombre", "descripcion", "fecha_inicio", "dias_laborales", "fecha_final"],
            [name, desc, fecha_inicio, dias_semana_seleccionados, fecha_inicio]
        )

        # Si se inserto el proyecto sin problemas
        if proyecto_id is not None:
            messagebox.showinfo("Proyecto", "Insertado correctamente", parent=self.ventana)
            super().load_data()
            self.ventana_padre.focus()
            self.ventana.destroy()

    def validar_logitud_campos(self, nombre, desc):
        if len(nombre) > 30:
            return False
        
        if len(desc) > 60:
            return False

        return True

    def validar_cantidad_dias_semana(self):
        """Valida que se seleccione por lo menos un día laboral"""
        count = 0
        for i in range(1, len(self.diasSemana)):
            if self.diasSemana[i].get() == 1:
                count += 1

        if count == 0:
            messagebox.showinfo(
                f"Error al introducir", 
                f"Debe introducir al menos un día laboral", 
                parent=self.ventana
            )

            return False

        return True

    def validar_cantidad_proyectos(self):
        """valida que la cantidad de proyectos sea de 999"""
        proyectos = self.connection.select(f"SELECT * FROM Proyecto")

        return validar_maximos_elementos("proyectos", proyectos, 999, self.ventana)