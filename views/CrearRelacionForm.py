from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from clases.Relacion import *
from helpers.calcularCulminacion import calcularFechaFinal
from helpers.validaciones import *

class CrearRelacionForm():
    def __init__(self, id_actividad, id_proyecto, ventana_padre, connection, Lista_adyacencia, Fech, loadata):
        self.id_proyecto   = id_proyecto
        self.id_actividad  = id_actividad
        self.ventana_padre = ventana_padre
        self.connection    = connection
        self.ListaAdyacencia = Lista_adyacencia
        self.cant_Actividades = 0
        self.ventana = Toplevel(self.ventana_padre)
        self.ventana.title("Crear Relacion")
        self.ventana.geometry("280x190")
        self.Fech = Fech
        self.nombre_actividad = self.get_nombre_actividad()

        self.label_actividad = Label(self.ventana, text=f"Actividad: {self.nombre_actividad}")
        self.label_actividad.grid(row=0, column=0)

        self.frame = LabelFrame(self.ventana, text='Relacion', height=70)
        self.frame.grid(row=1, column=0, columnspan=5, pady=10, padx=65)

        self.actividad_actual = StringVar()

        self.label = Label(self.frame, text="Seleccionar relacion: ").grid(row=2, column=0)
        # TODO
        self.actividad_combobox = ttk.Combobox(self.frame, textvariable=self.actividad_actual, state='readonly')
        self.actividad_combobox.grid(row=3, column=0)
        self.actividad_combobox.state = 'readonly'

        self.llenar_combobox_actividades()
        self.load = loadata
        self.insert_button = Button(self.ventana, text='Relacionar Actividad', command=self.create_new_relacion)
        self.insert_button.grid(row=4, column=0, columnspan=5)

    def get_nombre_actividad(self):
        return self.connection.select(f"SELECT nombre from Actividad where id_actividad = {self.id_actividad}")[0][0]

    def llenar_combobox_actividades(self):

        actividades= self.connection.select(f"SELECT * FROM Actividad WHERE actividad.id_actividad != {self.id_actividad} AND actividad.id_proyecto = {self.id_proyecto}")

        actividades_combobox = []

        # print(relaciones,"\tC:",len(relaciones))
        # print(actividades,"\tC:",len(actividades))

        for actividad in actividades:
            relaciones = self.connection.select(f"SELECT count(*) FROM relacion WHERE id_proyect = {self.id_proyecto} AND ( (relacion.id_actividad_ant = {self.id_actividad} AND relacion.id_actividad_sig = {actividad[0]}) OR ( relacion.id_actividad_ant = {actividad[0]} AND relacion.id_actividad_sig = {self.id_actividad}) )")[0][0]
            if relaciones == 0:
                actividades_combobox.append(f"{actividad[0]}  {actividad[2]}")

            """
            actividades_combobox.append(f"{actividad[0]}  {actividad[2]}")
            self.cant_Actividades += 1
            """
        actis = []
        for element in actividades_combobox:
            if element not in actis:
                self.cant_Actividades += 1
                actis.append(element)

        self.actividad_combobox['values'] = actis


    def create_new_relacion(self):
        if not validar_campos_vacios([self.actividad_combobox.get()], self.ventana):
            return None
        cantRel = self.connection.select(f"SELECT count(*) FROM relacion WHERE id_proyect = {self.id_proyecto}")[0][0]

        if self.cant_Actividades > 0 and cantRel < 149:
            self.connection.insert("Relacion",
                                   ["id_actividad_ant","id_actividad_sig","id_proyect"],
                                   [self.id_actividad, self.actividad_actual.get().split(" ")[0],self.id_proyecto]
                                   )
            messagebox.showinfo("Atencion", "La Actividad fue relacionada correctamente", parent=self.ventana)
            calcularFechaFinal(self.connection,self.id_proyecto,self.Fech)
            self.load()
            self.ventana_padre.focus()
            self.ventana.destroy()

        else:
            messagebox.showinfo("Atencion", "No hay suficientes actividades para relacionar", parent=self.ventana)

    def cargarListaAdyacencia(self):
        id_actual = int(self.actividad_actual.get().split(" ")[0])
        id_actividad = int(self.id_actividad)
        idrelacion = self.connection.select(f"SELECT id_relacion FROM Relacion where id_actividad_ant = {id_actividad}")[0][0]
        indice = self.connection.select(f"SELECT nro_grafo FROM Actividad where id_actividad = {id_actividad}")[0][0]
        indice2 = self.connection.select(f"SELECT nro_grafo FROM Actividad where id_actividad = {id_actual}")[0][0]
        self.ListaAdyacencia[indice].append( Relacion(idrelacion,id_actividad, id_actual) )
        self.ListaAdyacencia[indice2].append( Relacion(idrelacion,id_actividad, id_actual) )

        print("Relacion:",(self.ListaAdyacencia[indice][0]).get_idrelacion())