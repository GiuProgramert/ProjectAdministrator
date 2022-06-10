from email import message
from views.VerDetalleProyecto import VerDetalleProyecto
from .ActividadesView import ActividadesView
from .CrearProyectoForm import CrearProyectoForm
from .EditarProyectoForm import EditarProyectoForm
from tkinter import messagebox, ttk
from tkinter import *
from datetime import datetime
from helpers.LoadTableData import LoadTableData
from clases.ClaseFechasLaborales import *

class ProyectosView(LoadTableData):
    def __init__(self, ventana_padre, connection):
        """
            Recibe la el objeto conexión que se usa para acceder en la base de datos
            y la ventana padre para poder ubicar la ventana encima de esta
        """
        self.connection = connection
        self.ventana_padre = ventana_padre

        # Confirguracion de la ventana
        self.ventana = Toplevel(self.ventana_padre)
        self.ventana.title("Proyectos")
        self.ventana.geometry("850x450")
        
        # Configuración de crear botón
        self.crear_btn = Button(self.ventana, text="Agregar proyecto", command=self.open_create_proyecto_form_view)
        self.crear_btn.grid(row=0, column=0, columnspan=3, pady=20)

        # Configuración de tabla
        self.tabla = ttk.Treeview(self.ventana, height=14, columns = ('Nombre', 'Descripcion', 'Fecha Inicio'))
        
        # Se instancia el padre LoadTableData que sirve para actualizar las tablas 
        # en la interfaz al momento de insetar un proyecto nuevo
        super().__init__(self.tabla, "SELECT * FROM Proyecto")
        super().load_data()
        
        # Configuración de columnas de la tabla
        self.tabla.heading("Nombre", text='Nombre', anchor=CENTER)
        self.tabla.heading("Descripcion", text='Descripcion', anchor=CENTER)
        self.tabla.heading("Fecha Inicio", text='Fecha Inicio', anchor=CENTER)
        self.table.bind('<Double-1>', self.ver_detalle_proyecto)
        self.tabla.grid(row=2, column=0, columnspan=3, pady=20, padx=25)

        # Configuración de eliminar proyecto
        self.borrar_btn = Button(self.ventana, text='Eliminar proyecto', command=self.borrar_seleccionado)
        self.borrar_btn.grid(row=3, column=0)
        
        self.ver_informe_btn = Button(self.ventana, text='Ver detalle proyecto', command=self.ver_detalle_proyecto)
        self.ver_informe_btn.grid(row=3, column=1)

        # Configuración de botón administrar actividad
        self.actividades_btn = Button(self.ventana, text='Administrar actividad', command=self.abrir_actividades_view)
        self.actividades_btn.grid(row=3, column=2)

    def open_create_proyecto_form_view(self):
        CrearProyectoForm(self.ventana, self.connection, self.tabla)

    def abrir_actividades_view(self):
        items = self.tabla.selection()
        
        # Si no se selecciono nada
        if len(items) != 1:
            messagebox.showinfo("Actividad", "Debe seleccionar solo un proyecto", parent=self.ventana)
        else:
            item = items[0]
            id_proyecto = self.table.item(item, "text")
            nombre_proyecto = self.connection.select(f"SELECT nombre FROM proyecto WHERE id_proyecto = {id_proyecto}")[0][0]
            ActividadesView(id_proyecto, nombre_proyecto, self.ventana, self.connection)

    def ver_detalle_proyecto(self, event = None):
        items = self.tabla.selection()

        # Si no se selecciona nada
        if len(items) != 1:
            messagebox.showinfo("Actividad", "Debe seleccionar solo un proyecto", parent=self.ventana)
        else:
            item = items[0]
            id_proyecto = self.table.item(item, "text")
            fechas = self.connection.select(f"SELECT fecha_inicio,fecha_final,dias_laborales FROM proyecto WHERE id_proyecto = {id_proyecto}")[0]

            dias_laborales_cadena = list(fechas[2])
            dias_laborales = []
            for dia_laboral in dias_laborales_cadena:
                dias_laborales.append(int(dia_laboral))

            print(dias_laborales)
            feriados = self.getFeriados()

            Fech = fechasDeTrabajo(feriados,dias_laborales ,(fechas[0].replace("/","-")))
            fech1 = datetime.strptime((fechas[0].replace("/","-")),"%Y-%m-%d").date()
            fech2 = datetime.strptime((fechas[1].replace("/","-")),"%Y-%m-%d").date()
            if Fech.DiasEntre2Fechas( fech1, fech2 ) < 365 :
                VerDetalleProyecto(id_proyecto, self.ventana, self.connection,Fech)
            else:
                messagebox.showinfo("Actividad", "La duracion de este proyecto es mayor que 365 dias\nModifique el mismo para que pueda ser representado", parent=self.ventana)
    def generar_mensaje_borrado(self, lista, mensaje):
        """Genera el mensaje a mostrar cuando se borra un proyecto"""
        lista_ids = ""
        
        # Se juntan los id de los elementos seleccionados en un string
        for elemento in lista:
            lista_ids += f"{elemento}, "
        lista_ids = lista_ids[: len(lista_ids) - 2]


        return mensaje % lista_ids

    def info_borrados(self, borrados, no_borrados):
        """Muestra en una ventana la información de los proyectos que fueron borrados"""
        
        if len(borrados) > 0:
            mensaje = self.generar_mensaje_borrado(borrados, "Los clientes con id %s fueron eliminados")

            messagebox.showinfo("Proyectos", mensaje, parent=self.ventana)
        
        if len(no_borrados) > 0:
            mensaje = self.generar_mensaje_borrado(no_borrados, "Los clientes con id %s no se pueden borrar")

            messagebox.showinfo("Proyectos", mensaje, parent=self.ventana)

    def borrar_seleccionado(self):
        """Borra los proyectos seleccionados en la tabla"""
        
        proyectos_seleccionados = self.tabla.selection() # Elementos seleccionados en la tabla
        
        #Se guardan los datos para luego mostrarlo al usuario
        borrados = []
        no_borrados = []

        # Si no se selecciono nada
        if len(proyectos_seleccionados) == 0:
            messagebox.showinfo("Proyectos", "No hay proyectos seleccionados", parent=self.ventana)

        confirmacion = messagebox.askyesno("Proyectos", "Esta seguro de borrar los siguientes proyectos?", parent=self.ventana)

        if not confirmacion:
            return None

        # Borrar los proyectos seleccionados
        for proyecto_seleccionado in proyectos_seleccionados:
            id = self.table.item(proyecto_seleccionado, "text")
            
            # TODO
            # borrar relaciones del proyecto
            self.connection.delete_by_id("relacion", "id_proyect", id)

            # borrar actividades del proyecto
            self.connection.delete_by_id("actividad", "id_proyecto", id)

            borrado = self.connection.delete_by_id("Proyecto", "id_proyecto", id)

            if borrado:
                borrados.append(id)
            else:
                no_borrados.append(id)
        
        self.info_borrados(borrados, no_borrados)
        super().load_data()

    def getFeriados(self):
        feriadosMatriz = self.connection.select(f"SELECT * FROM Feriado")
        feriadoLista = []
        for feriado in feriadosMatriz:
            feriadoLista.append(feriado[0])
        return feriadoLista
