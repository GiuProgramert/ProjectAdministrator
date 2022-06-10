from tkinter import *
from tkinter import messagebox
from clases.ClaseFechasLaborales import fechasDeTrabajo

from helpers.LoadTableData import LoadTableData
from helpers.validaciones import validar_campos_vacios, validar_duracion_maxima, validar_maximos_elementos
from helpers.calcularCulminacion import calcularFechaFinal


class EditarActividadForm(LoadTableData):
    def __init__(self, id_proyecto, id_actividad, ventana_padre, connection, tabla, Fech):
        self.connection    = connection
        self.id_proyecto   = id_proyecto
        self.id_actividad  = id_actividad
        self.actividad = self.connection.select(f"SELECT * FROM actividad WHERE id_actividad = {self.id_actividad}")
        self.ventana_padre = ventana_padre
        self.tabla         = tabla
        self.Fech = Fech
        self.ventana = Toplevel(self.ventana_padre)
        self.ventana.title("Modificar Actividad")
        self.ventana.geometry("280x320")

        super().__init__(self.tabla, f"SELECT id_actividad, nombre, duracion, fecha_inicio_temprano, fecha_culminacion  FROM Actividad where id_proyecto = {self.id_proyecto}")

        self.frame = LabelFrame(self.ventana, text='Actualizar Actividad', height=70)
        self.frame.grid(row=0, column=0, columnspan=5, pady=10, padx=65)
        # self.fechaProyecto = self.connection.select(f"SELECT fecha_inicio FROM proyecto WHERE proyecto.id_proyecto = {self.id_proyecto}")[0][0]

        self.name_label = Label(self.frame, text="Nombre: ").grid(row=1, column=0)
        self.duracion_label = Label(self.frame, text="Duración: ").grid(row=3, column=0)

        self.nombre = StringVar()
        self.duracion = StringVar()

        self.name_entry = Entry(self.frame, textvariable=self.nombre)
        self.name_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.duracion_entry = Entry(self.frame, textvariable=self.duracion)
        self.duracion_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.llenar_campos()

        self.insert_button = Button(self.ventana, text='Actualizar Actividad', command=self.update_new_actividad)
        self.insert_button.grid(row=9, column=0, columnspan=5)
    

    def llenar_campos(self):
        self.nombre.set(self.actividad[0][2])
        self.duracion.set(self.actividad[0][3])


    def update_new_actividad(self):
        name     = self.name_entry.get()
        duracion = self.duracion_entry.get()

        # Validar entradas

        if not self.validar_logitud_campos(name):
            messagebox.showinfo(
                f"Error al introducir", 
                f"Nombre muy largo", 
                parent=self.ventana
            )
            return None
        if not validar_campos_vacios([name, duracion], self.ventana):
            return None

        try:
            int(duracion)
        except Exception:
            messagebox.showinfo(
                f"Error al introducir", 
                f"Debes introducir una duración valida", 
                parent=self.ventana
            )
            return None

        if not validar_duracion_maxima(int(duracion), self.ventana):
            return None 
        if not self.validar_cantidad_actividades():
            return None

        nro_grafo = self.calcular_nro_grafo()

        fecha_inicio = self.connection.select(f"SELECT fecha_inicio FROM Proyecto WHERE id_proyecto = {self.id_proyecto}")[0][0]

        confirmacion = self.connection.update(
            "actividad",
            ["nombre", "duracion"],
            [self.nombre.get(), self.duracion.get()],
            "id_actividad",
            self.id_actividad
        )

        if confirmacion:
            self.connection.update("Proyecto",["fecha_final"],[fecha_inicio],"id_proyecto",self.id_proyecto)
            messagebox.showinfo("Actividad", "Actualizada correctamente", parent=self.ventana)
            calcularFechaFinal(self.connection,self.id_proyecto,self.Fech)
            super().load_data()
            self.ventana_padre.focus()
            self.ventana.destroy()

    def validar_logitud_campos(self, nombre):
        if len(nombre) > 20:
            return False

        return True

    def calcular_nro_grafo(self):
        numeros_grafo = self.connection.select(f"SELECT nro_grafo FROM Actividad WHERE id_proyecto = {self.id_proyecto} ORDER BY nro_grafo DESC LIMIT 1")

        if len(numeros_grafo) > 0:
            return numeros_grafo[0][0] + 1
        else:
            return 1

    # def calcular_fechas_inicio(self, duracion, fecha_inicio_proyecto):
    #     cantidad_actividades_proyecto = self.connection.select(f"SELECT count(*) FROM Actividad WHERE id_proyecto = {self.id_proyecto}")[0][0]
        
    #     if cantidad_actividades_proyecto == 0:
    #         return fecha_inicio_proyecto
        
    #     return self.calcular_fechas_inicio(duracion, fecha_inicio_proyecto)

    # def calcular_fechas_inicio(self, duracion, fecha_inicio_proyecto):        
    #     fechaTrabajo = fechasDeTrabajo([], [1, 2, 3, 4, 5], fecha_inicio_proyecto)
    #     return fechaTrabajo.FechaSegunDias(duracion).strftime("%Y/%m/%d")

    def validar_cantidad_actividades(self):
        actividades = self.connection.select(f"SELECT * FROM Actividad WHERE id_proyecto = {self.id_proyecto}")

        return validar_maximos_elementos("actividades", actividades, 99 , self.ventana)