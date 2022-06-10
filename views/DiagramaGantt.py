from datetime import datetime
from clases.ClaseFechasLaborales import fechasDeTrabajo
import matplotlib.pyplot as plt

class DiagramaGantt():
    def __init__(self, id_proyecto, connection):
        self.connection = connection
        self.id_proyecto = id_proyecto
        
        self.proyecto = self.connection.select(f"SELECT * from proyecto where id_proyecto = {self.id_proyecto}")
        print(self.proyecto)
        self.actividades = self.connection.select(f"SELECT nombre, fecha_inicio_temprano, duracion fecha FROM actividad WHERE id_proyecto = {self.id_proyecto}")
        
        self.dias_laborales_proyecto = self.get_dias_laborales()
        self.nombres = self.get_nombres_actividades()
        self.dias_laborales_proyecto = self.get_dias_laborales()
        self.cantidad_actividades = len(self.nombres)
        print("dias laborales", self.dias_laborales_proyecto)
        self.Fech = fechasDeTrabajo(self.dias_laborales_proyecto, self.dias_laborales_proyecto, self.proyecto[0][5])

        fecha_inicio = datetime.strptime(self.proyecto[0][5], "%Y-%m-%d")
        fecha_inicio_proyecto = datetime.strptime(self.proyecto[0][3], "%Y-%m-%d")

        self.cantidad_dias_proyecto = self.Fech.DiasEntre2Fechas(fecha_inicio_proyecto, fecha_inicio)
        print(self.cantidad_dias_proyecto)
        self.fig, self.gnt = plt.subplots()

        # Limetes de x e y
        self.gnt.set_ylim(0, 120)
        self.gnt.set_xlim(0, self.cantidad_dias_proyecto + 10)
        # Nombres de los ejes
        self.gnt.set_xlabel('Tiempo')
        self.gnt.set_ylabel('Actividades')
    
        self.alturas = self.get_alturas()
        self.gnt.set_yticks(self.alturas)

        # self.nombres = nombres_actividades
        self.gnt.set_yticklabels(self.nombres)

        self.gnt.grid(True)

        self.a = self.calcular_fechas_desde_final()
        self.b = self.obtener_duraciones()
        print(self.a, self.b)

        self.generar_grafico()
        plt.show()
    
    def calcular_fechas_desde_final(self):
        diferencias = []
        for actividad in self.actividades:
            print(actividad)
            fecha_inicio = datetime.strptime(actividad[1], "%Y-%m-%d")
            fecha_inicio_proyecto = datetime.strptime(self.proyecto[0][3], "%Y-%m-%d")

            diferencias.append(self.Fech.DiasEntre2Fechas(fecha_inicio_proyecto, fecha_inicio))

        return diferencias

    def get_dias_laborales(self):
        dias_laborales_cadena = self.proyecto[0][4]
        dias_laborales_lista = list(dias_laborales_cadena)
        
        dias_laborales = []
        for dia_laboral in dias_laborales_lista:
            dias_laborales.append(int(dia_laboral))

        return dias_laborales

    def obtener_duraciones(self):
        duraciones_lista = []

        for actividad in self.actividades:
            duraciones_lista.append(actividad[2])

        return duraciones_lista

    def get_nombres_actividades(self):
        actividades_lista = []

        for actividad in self.actividades:
            actividades_lista.append(actividad[0])

        return actividades_lista

    def get_alturas(self):
        alturas = []
        for i in range(self.cantidad_actividades):
            alturas.append(i * 10 + 10)

        return alturas

    def generar_grafico(self):
        for i in range(self.cantidad_actividades):
            self.gnt.broken_barh([(self.a[i], (self.b[i]))], (10 + (10 * i), 9), facecolors=('tab:orange'))
            #gnt.broken_barh([(start_time, duration)],
            #                (lower_yaxis, height),
            #                facecolors=('tab:colors'))"
        