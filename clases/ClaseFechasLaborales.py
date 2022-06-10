from time import *  # libreria para tener fechas en formatos especificos
from datetime import *  # libreria para sumar y hacer calculos entre fechas


class fechasDeTrabajo:
    feriados = []
    diasLaborales = []
    fechaActual = date.today()

    def __init__(self, feriadosList, diaslaborales,
                 fechaActual):  # la fecha actual y los feriados se colocan en sus variables
        self.feriados = self.feriados + feriadosList
        self.diasLaborales = self.diasLaborales + diaslaborales
        self.fechaActual = fechaActual

    def __devolerFechaAct(self):
        return self.fechaActual

    def __DiasEntreFechas(self, fecha1, fecha2):  # dadas 2 fechas calcula los dias laborales que hay entre estas
        c = 0
        while fecha1 <= fecha2:
            if fecha1.strftime("%m%d") not in self.feriados and fecha1.isoweekday() in self.diasLaborales:
                c += 1
            fecha1 = fecha1 + timedelta(1)
        return c

    def __DiasEntreFechasSinDiasLaborales(self, fecha1, fecha2):  # dadas 2 fechas calcula los dias laborales que hay entre estas
        c = 0
        while fecha1 < fecha2:
            if fecha1.strftime("%m%d") not in self.feriados:
                c += 1
            fecha1 = fecha1 + timedelta(1)
        return c

    def __FechaSegunDias(self, fecha, dias):

        while dias != 0:
            if dias > 0:
                fecha = fecha + timedelta(1)
                if fecha.strftime("%m%d") not in self.feriados and fecha.isoweekday() in self.diasLaborales:
                    dias -= 1
            else:
                fecha = fecha - timedelta(1)
                if fecha.strftime("%m%d") not in self.feriados and fecha.isoweekday() in self.diasLaborales:
                    dias += 1
        return fecha

    def Fechahoy(self):
        return self.__devolerFechaAct();

    def DiasHastaUnaFechas(self, fechaFinal):
        # se calcula los dias laborales hasta una fechas desde la fecha Actual
        fechainicio = self.fechaActual
        return self.__DiasEntreFechas(fechainicio, fechaFinal)

    def DiasEntre2Fechas(self, fechainicio, fechaFinal):
        # se calcula los dias laborales entre las fechas
        return self.__DiasEntreFechas(fechainicio, fechaFinal)

    def FechaSegunDias(self, dias):
        # se calcula que fecha sera segun los dias datos
        fechaAct = datetime.strptime(self.fechaActual, "%Y-%m-%d")
        return self.__FechaSegunDias(fechaAct, dias)

    def restaFecha(self,fecha,dias):
        i = 0
        while i < dias:
            if fecha.isoweekday() in self.diasLaborales and fecha.strftime("%m%d") not in self.feriados:
                i += 1
            fecha = fecha - timedelta(1)

        while fecha.isoweekday() not in self.diasLaborales or fecha.strftime("%m%d") in self.feriados:
            fecha = fecha - timedelta(1)
        return fecha

    def FechaSegunFechaYDias(self, fechaInicial, dias):
        # se calcula que fecha sera segun la fecha inicial y los dias que deben transcurrir
        return self.__FechaSegunDias(fechaInicial, dias)

"""
GFech = fechasDeTrabajo(["0528","0529"], [1,2], date.today())
print(GFech.restaFecha(datetime.strptime("2022-06-10","%Y-%m-%d").date(),2))

        #instanciamos una clase dias de trabajo y como parametro le pasamos los dias feriados
GFech = fechasDeTrabajo(["0528","0529"], [1,2,3,4,5], date.today())
        #para usar los metodos se usa el objeto que instancia la clase
unaFechaFutura = date.today() + timedelta(4)
print("\tDias: {}".format(GFech.DiasHastaUnaFechas(unaFechaFutura)))
print("\tFecha dentro de {} dias es: {}".format(4 ,GFech.FechaSegunDias(4) ))
print("\tFecha de {} dias desde la decha {} es: {}".format(-3 ,GFech.FechaSegunDias(4),GFech.FechaSegunFechaYDias(GFech.FechaSegunDias(4),-3)) )

print("\tLa fecha con formato para guardar en la BD es:",GFech.FechaSegunDias(3).strftime("%Y%m%d"))

print("\tAño Actual: {}".format(GFech.Fechahoy().strftime("%Y")))
print("\tMes Actual: {}={}".format( GFech.Fechahoy().strftime("%B"), GFech.Fechahoy().strftime("%m")))
print("\tDia Actual: {}={}".format(GFech.Fechahoy().strftime("%A") , GFech.Fechahoy().isoweekday()))
print("\tDia Actual: {}".format(GFech.Fechahoy().strftime("%d")))

"""
