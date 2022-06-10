from cgitb import text
import imp
from tkinter import *
from tkinter import ttk
from datetime import datetime
from views.DiagramaGantt import DiagramaGantt

class VerDetalleProyecto():
    def __init__(self, id_proyecto, ventana_padre, connection,Fech):
        # Incializamos los objetos que emcapsulan nuestras herramientas
        self.connection = connection
        self.ventana_padre = ventana_padre
        self.id_proyecto = id_proyecto
        self.Fech = Fech
        # calculamos los datos a mostrar en pantalla
        self.fechas_tardias()
        self.caminio_Critico = self.caminio_Critico_Cadena()

        self.proyecto = self.get_proyecto()
        self.actividades = self.get_actividades()
        self.relaciones = self.get_relaciones()

        # configuramos el aspecto de LA VENTANA
        self.ventana = Toplevel(self.ventana_padre)
        
        self.ventana.title(self.proyecto[1])
        self.ventana.state("zoomed")

        self.frameIzquierdo = LabelFrame(self.ventana, text='Datos proyecto', height=50)
        self.frameDerecho = LabelFrame(self.ventana, text='Actividades y relaciones', height=50)

        # Frames
        self.frameIzquierdo.grid(row=0, column=0, rowspan=5)
        self.frameDerecho.grid(row=0, column=1, rowspan=5)

        # Datos proyecto
        self.nombreProyecto = Label(self.frameIzquierdo, text=f"Nombre: \n{self.proyecto[1]}")
        self.nombreProyecto.grid(row=1, column=0, pady=20)

        self.description = ""
        self.description_lista = self.proyecto[2].split(" ")
        # for elemento in self.proyecto[2].split(" "):
        #     if (self.description_lista.index(elemento) % 3 == 0):
        #         self.description += "\n" + elemento
            
        #     self.description += " " + elemento

        self.descripcionProyecto = Label(self.frameIzquierdo, text=f"Descripcion: \n{self.proyecto[2]}")
        self.descripcionProyecto.grid(row=2, column=0, pady=20)

        self.fechaInicioProyecto = Label(self.frameIzquierdo, text=f"Fecha inicio:\n {self.proyecto[3]}")
        self.fechaInicioProyecto.grid(row=3, column=0, pady=20)

        self.fechaInicioTardio = Label(self.frameIzquierdo, text=f"Fecha final:\n {self.proyecto[5]}")
        self.fechaInicioTardio.grid(row=4, column=0, pady=20)
        self.fechaInicioTardio = Label(self.frameIzquierdo, text=f"Camino Critico:\n {self.caminio_Critico}")
        self.fechaInicioTardio.grid(row=5, column=0, pady=20)

        self.verDiagramaDeGantt = Button(self.frameIzquierdo, text="Ver diagrama de Gantt", command=self.ver_diagrama_de_gantt)
        self.verDiagramaDeGantt.grid(row=6, column=0, pady=20)




        # Datos actividades
        self.tablaActividades = ttk.Treeview(self.frameDerecho, columns=('Nombre', 'Duración', 'Inicio temprano', 'Inicio tardío'))
        self.tablaActividades.heading("Nombre", text="Nombre", anchor=CENTER)
        self.tablaActividades.heading("Duración", text="Duración", anchor=CENTER)
        self.tablaActividades.heading("Inicio temprano", text="Inicio temprano", anchor=CENTER)
        self.tablaActividades.heading("Inicio tardío", text="Inicio tardío", anchor=CENTER)
        self.tablaActividades.grid(row=1, column=1, pady=10, padx=10)
        self.llenar_tabla(self.actividades, self.tablaActividades)

        # Separador
        self.separador = ttk.Separator(self.frameDerecho, orient='horizontal')
        self.separador.grid(row=2, column=1)

        # Tabla punto critico
        self.tablaRelacionesPuntoCritico = ttk.Treeview(self.frameDerecho, columns=('Nombre'))
        self.tablaRelacionesPuntoCritico.heading("Nombre", text="Punto Critico", anchor=CENTER)
        self.tablaRelacionesPuntoCritico.grid(row=4, column=1, pady=20)
        self.llenar_tabla(self.Lista_De_Puntos_Critico(), self.tablaRelacionesPuntoCritico) # Aqui



        # Datos Relaciones
        self.tablaRelaciones = ttk.Treeview(self.frameDerecho, columns=('Actividad', 'Actividad Siguiente'))
        self.tablaRelaciones.heading("Actividad", text="Actividad", anchor=CENTER)
        self.tablaRelaciones.heading("Actividad Siguiente", text="Actividad Siguiente", anchor=CENTER)
        # self.tablaRelaciones.heading("Actividad Critica", text="Actividad Critica", anchor=CENTER)
        self.tablaRelaciones.grid(row=3, column=1, pady=10)
        self.llenar_tabla(self.relaciones, self.tablaRelaciones)

    def ver_diagrama_de_gantt(self):
        DiagramaGantt(self.id_proyecto, self.connection)

    def get_proyecto(self):
        """Obtiene todos los datos del proyecto"""
        return self.connection.select(f"SELECT * FROM Proyecto WHERE id_proyecto = {self.id_proyecto}")[0]

    def get_actividades(self):
        """Öbtiene todas las actividades del proyecto"""
        return self.connection.select(f"SELECT id_actividad, nombre, duracion, fecha_inicio_temprano, fecha_inicio_tardio FROM Actividad WHERE id_proyecto = {self.id_proyecto}")
    
    def get_relaciones(self):
        """Obtiene todas las relaciones del proyecto"""
        relaciones = []
        # a b

        # b c
        # b d

        # c d

        # d e
        i = 0
        for actividad in self.actividades:
            id_actividades_sigs = self.connection.select(f"SELECT id_actividad_sig FROM Relacion WHERE id_actividad_ant = {actividad[0]}")
            for id_actividad_sig in id_actividades_sigs:
                relacion = self.connection.select(f"SELECT nombre FROM Actividad WHERE id_actividad = {id_actividad_sig[0]}")

                if len(relacion) > 0:
                    i += 1
                    relaciones.append([i, actividad[1], relacion[0][0]])

        return relaciones

    def llenar_tabla(self, datos, tabla):
        # cargamos en la tabla los datos que enviados
        for dato in datos:
            tabla.insert("", index=dato[0], text=dato[0], values=dato[1:])


    def fechas_tardias(self):
        # Calculamos las fechas de inicio tardio de cada actividad

        Actividades = self.connection.select(f"SELECT * FROM actividad WHERE id_proyecto = {self.id_proyecto}")
        Relaciones = self.connection.select(f"SELECT * FROM relacion WHERE id_proyect = {self.id_proyecto}")

        # por cada actividad se calcula y sus dependencias se calcula la fecha de inicio tardio y culminacion tardia
        for i in range(len(Actividades)):
            for actividad in Actividades :
                antecedente = self.connection.select(f"SELECT * FROM relacion WHERE id_actividad_ant = {actividad[0]}")
                # si la actividad no tiene relaciones
                if len(antecedente) == 0 :
                    fechFinal = self.connection.select(f"SELECT fecha_final FROM proyecto WHERE id_proyecto = {self.id_proyecto}")[0][0]
                    fechFinal = datetime.strptime(fechFinal.replace("/","-"),"%Y-%m-%d").date()
                    fecha_ini_tardio = self.Fech.restaFecha(fechFinal,int(actividad[3]))
                    # la actividad no esta relacionada y tendra fecha de inicio y culminacion dependiente de su fecha de inicio
                    self.connection.update("actividad",
                                           ["fecha_inicio_tardio","fecha_culminacion_tardio"],
                                           [fecha_ini_tardio,fechFinal],
                                           "id_actividad",
                                           actividad[0]
                                           )
                # si la actividad tiene otras actividades relacionadas
                else:
                    menor = self.connection.select(f"SELECT fecha_inicio_tardio FROM actividad WHERE id_actividad = {antecedente[0][2]}")[0][0]
                    menor = datetime.strptime(menor.replace("/","-"),"%Y-%m-%d").date()
                    # otras actividades dependen de esa actividad y se busca la menor de las fechas de inicio de las actividades dependientes
                    for ante in antecedente:
                        siguiente = self.connection.select(f"SELECT fecha_inicio_tardio FROM actividad WHERE id_actividad = {ante[2]}")[0][0]
                        fech2 =  datetime.strptime(siguiente.replace("/","-"),"%Y-%m-%d").date()
                        if menor > fech2:
                            menor = fech2

                    fecha_ini_tardio = self.Fech.restaFecha(menor, int(actividad[3]))
                    print(f"fech:{fecha_ini_tardio} \t duracion:{actividad[3]}\nmenor:{menor}")
                    self.connection.update("actividad",
                                           ["fecha_inicio_tardio", "fecha_culminacion_tardio"],
                                           [fecha_ini_tardio, menor],
                                           "id_actividad",
                                           actividad[0]
                                           )


    def  Lista_De_Puntos_Critico (self):
        # se consulta de la base de datos las actividades que son actividades CRITICAS
        actividades = self.connection.select(f"SELECT id_actividad, nombre FROM actividad WHERE id_proyecto = {self.id_proyecto} AND fecha_inicio_temprano = fecha_inicio_tardio")

        return actividades

    def caminio_Critico_Cadena(self):
        # para el camino critico se buscan las actividades que no tiene olgura en su inicio tardio

        actividades = self.connection.select(f"SELECT id_actividad FROM actividad WHERE actividad.id_proyecto = {self.id_proyecto} ")
        ban = 1
        i = 0
        siguiente = []
        id_critico = 0
        # buscamos las actividades que son actividades criticas y las que dependan de estas sera nuestro camino critico
        for critico in actividades:
            if ban == 1:
                id_critico = critico[0]
                print("El id critico:",id_critico)
                siguiente = self.connection.select(f"SELECT * FROM relacion WHERE id_proyect = {self.id_proyecto} AND id_actividad_sig = {id_critico}")
                print(siguiente)
                # con esta condicion decimos que encontramos la primera actividad del camino critico
                if len(siguiente) == 0:
                    ban = 0
            # una vez tenemos la primera actividad buscamos todas las actividades que dependen de esta y forman el camino critico
            if ban == 0 :
                siguiente = self.connection.select(
                    f"SELECT id_actividad,nombre FROM actividad,relacion WHERE relacion.id_proyect = {self.id_proyecto} AND actividad.id_proyecto = {self.id_proyecto} AND fecha_inicio_temprano = fecha_inicio_tardio "+
                    f"AND id_actividad_ant = {id_critico} ORDER BY id_actividad ")
                print(siguiente)
                ban = 2

        activis = []
        camino_critico = "Inicio"
        for nombre in siguiente:
            if nombre[1] not in activis:
                activis.append(nombre[1])
                camino_critico = camino_critico +"\n" + nombre[1]

        camino_critico = camino_critico +"\nFin"

        return camino_critico
