from helpers.calcularCulminacion import calcularFechaFinal
from views.CrearRelacionForm import CrearRelacionForm
from views.EditarActividadForm import EditarActividadForm
from .CrearActividadForm import CrearActividadForm
from tkinter import messagebox, ttk
from tkinter import *
from clases.ClaseFechasLaborales import fechasDeTrabajo

from helpers.LoadTableData import LoadTableData


class ActividadesView(LoadTableData):
    def __init__(self, id_proyecto, nombre_proyecto, ventana_padre, connection):
        self.id_proyecto = id_proyecto
        self.connection = connection
        self.ventana_padre = ventana_padre
        self.ventana = Toplevel(self.ventana_padre)

        self.ventana.title(f"Actividades del {nombre_proyecto}")
        self.ventana.geometry("1050x450")
        self.ListaAdyacencia = []
        self.ListaAdyacencia.append(0)

        self.crear_btn = Button(self.ventana, text="Agregar Actividad", command=self.open_create_actividad_form_view)
        self.crear_btn.grid(row=0, column=0, columnspan=3, pady=20)

        self.tabla = ttk.Treeview(self.ventana, height=14, columns = ('Nombre', 'Duracion', 'Fecha Inicio temprano', 'Fecha culminacion'))
        super().__init__(self.tabla, f"SELECT id_actividad, nombre, duracion, fecha_inicio_temprano, fecha_culminacion  FROM Actividad where id_proyecto = {self.id_proyecto}")
        for i in range(super().load_data()):
            self.ListaAdyacencia.append([])

        self.fechaProyecto = self.connection.select(f"SELECT fecha_inicio FROM proyecto WHERE proyecto.id_proyecto = {self.id_proyecto}")[0][0].replace("/", "-")



        self.tabla.heading("Nombre", text='Nombre', anchor=CENTER)
        self.tabla.heading("Duracion", text='Duracion', anchor=CENTER)
        self.tabla.heading("Fecha Inicio temprano", text='Fecha Inicio temprano', anchor=CENTER)
        self.tabla.heading("Fecha culminacion", text='Fecha culminacion', anchor=CENTER)
        self.tabla.grid(row=2, column=0, columnspan=3, pady=20, padx=25)

        self.borrar_btn = Button(self.ventana, text='Eliminar Actividad', command=self.borrar_seleccionado)
        self.borrar_btn.grid(row=3, column=0)

        self.editar_actividad = Button(self.ventana, text="Editar actividad", command=self.abrir_editar_actividades)
        self.editar_actividad.grid(row=3, column=1)

        self.actividades_btn = Button(self.ventana, text='Agregar relaciones', command=self.create_relacion_form_view)
        self.actividades_btn.grid(row=3, column=2)
        self.dias_laborales_proyecto = self.get_dias_laborales()
        # print(self.dias_laborales_proyecto)

        feriados = self.getFeriados()

        self.Fech = fechasDeTrabajo(feriados, self.dias_laborales_proyecto, self.fechaProyecto)

        calcularFechaFinal(self.connection,self.id_proyecto,self.Fech )

    
    def abrir_editar_actividades(self):
        elemt = self.tabla.selection()
        if len(elemt) != 1:
            messagebox.showinfo("Actividad", "Debe seleccionar solo una actividad", parent=self.ventana)
        else:
            item = elemt[0]
            id_actividad = self.table.item(item, "text")

            EditarActividadForm(self.id_proyecto, id_actividad, self.ventana, self.connection, self.tabla, self.Fech)


    def get_dias_laborales(self):
        dias_laborales_cadena = self.connection.select(f"SELECT dias_laborales FROM proyecto WHERE id_proyecto = {self.id_proyecto}")[0][0]
        dias_laborales_lista = list(dias_laborales_cadena)
        
        dias_laborales = []
        for dia_laboral in dias_laborales_lista:
            dias_laborales.append(int(dia_laboral))

        return dias_laborales

    def open_create_actividad_form_view(self):
        CrearActividadForm(self.id_proyecto, self.ventana, self.connection, self.tabla,self.Fech)
    
    def create_relacion_form_view(self):
        items = self.tabla.selection()
        
        # Si no se selecciono nada
        if len(items) != 1:
            messagebox.showinfo("Actividad", "Debe seleccionar solo una actividad", parent=self.ventana)
        else:
            item = items[0]
            id_actividad = self.table.item(item, "text")

            # calculamos la cantidad de actividades que no tienen relacion con la actividad
            if self.calcularActividades(id_actividad) > 0:
                CrearRelacionForm(id_actividad, self.id_proyecto, self.ventana, self.connection, self.ListaAdyacencia, self.Fech, super().load_data )

            else:
                messagebox.showinfo("Atencion", "No hay suficientes actividades para relacionar", parent=self.ventana)
    def calcularActividades(self,id_actividad):


        Actividades = self.connection.select(
            f"SELECT * FROM Actividad WHERE actividad.id_actividad != {id_actividad} AND actividad.id_proyecto = {self.id_proyecto}")
        canActividades = 0

        for actividad in Actividades:
            relaciones = self.connection.select(
                f"SELECT count(*) FROM relacion WHERE id_proyect = {self.id_proyecto} AND ( (relacion.id_actividad_ant = {id_actividad} AND relacion.id_actividad_sig = {actividad[0]}) OR ( relacion.id_actividad_ant = {actividad[0]} AND relacion.id_actividad_sig = {id_actividad}) )")[
                0][0]
            if relaciones == 0:
                canActividades += 1

        return canActividades

    def borrar_seleccionado(self):
        elemt = self.tabla.selection()
        if len(elemt) != 1:
            messagebox.showinfo("Actividad", "Debe seleccionar solo una actividad", parent=self.ventana)
        else:
            opcion = messagebox.askquestion("Atencion", "Esta seguro de quedesea eliminar la actividad?", parent=self.ventana)
            if opcion == "yes":
                id = self.table.item(elemt, "text")
                anteriores = self.connection.select(f"SELECT id_actividad_ant FROM relacion WHERE id_actividad_sig = {id}")
                relanciones = self.connection.select(f"SELECT id_actividad_sig FROM relacion WHERE id_actividad_ant = {id}")
                for anterior in anteriores:
                    for relacion in relanciones:
                        if len(self.connection.select(f"SELECT * FROM relacion WHERE id_actividad_ant = {anterior[0]} AND id_actividad_sig = {relacion[0]}") ) == 0:
                            self.connection.insert("Relacion",
                                                   ["id_actividad_ant","id_actividad_sig","id_proyect"],
                                                   [anterior[0], relacion[0],self.id_proyecto]
                                                   )
                #     delete * from relcion where id_actividad_sig = {id} or id_actividad_ant = {id}
                self.connection.delete_by_id("relacion","id_actividad_sig",id)
                self.connection.delete_by_id("relacion","id_actividad_ant",id)
                #     delete * from actividad where id_actividad = {id}
                self.connection.delete_by_id("actividad","id_actividad",id)
                print(self.Fech.Fechahoy())
                #     delete fecha_inicio,fecha_tardio_tardio,fehca_culminacion,fecha_culminacion_tardio from actividad where id_proyecto = {self.id_proyecto}
                self.connection.update("actividad",
                                       ["fecha_inicio_temprano","fecha_culminacion"],
                                       [self.Fech.Fechahoy(),''],
                                       "id_proyecto",
                                       self.id_proyecto
                                       )
                calcularFechaFinal(self.connection, self.id_proyecto, self.Fech)
                super().load_data()

    def getFeriados(self):
        feriadosMatriz = self.connection.select(f"SELECT * FROM Feriado")
        feriadoLista = []
        for feriado in feriadosMatriz:
            feriadoLista.append(feriado[0])
        return feriadoLista

    def abrir_relaciones_view(self):
        pass