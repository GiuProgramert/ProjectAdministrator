class Actividad:
    fechatardio = 0
    def __init__(self, id, nom, desc, fecha):
        self.idactividad = id
        self.nombreactividad = nom
        self.duracion = desc
        self.fechainicio = fecha

    def __modificar_id(self, id):
        self.id = id
    def __modificar_nombre (self, nom):
        self.nombreactividad = nom
    def __modificar_duracion (self, duracion):
        self.duracion = duracion
    def __modificar_fechainicio (self, fecha):
        self.fechainicio = fecha
    def __modificar_fechatardio(self, fecha):
        self.fechatardio = fecha

    def __return_id(self):
        return self.id
    def __return_nombre(self):
        return self.nombreactividad
    def __return_fechaini(self):
        return self.fechainicio
    def __return_fechatar(self):
        return self.fechatardio
    def __return_duracion(self):
        return self.duracion
    def __return_id(self):
        return self.idactividad
    

    def set_id(self, id):
        self.__return_id()
    def set_fechainicio (self, fecha):
        self.__modificar_fechainicio(fecha)
    def set_fechatardio(self, fecha):
        self.__modificar_fechatardio(fecha)
    def set_nombre (self, nom):
        self.__modificar_nombre(nom)
    def set_duracion(self, duracion):
        self.__modificar_duracion(duracion)

    def get_id(self):
        self.__return_id()
    def get_fechainicio(self):
        return self.__return_fechaini()
    def get_fechatardio(self):
        return self.__return_fechatar()
    def get_nombre(self):
        return self.__return_nombre()
    def get_duracion(self):
        return self.__return_duracion()
    def get_id(self):
        return self.__return_id()
