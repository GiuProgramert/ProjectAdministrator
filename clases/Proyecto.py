class Proyecto:
    def __init__(self, id, nom, desc, fecha):
        self.idproyecto = id
        self.nombreproyecto = nom
        self.descripcion = desc
        self.fechainicio = fecha

    def __modifcar_id(self, id):
        self.id = id
    def __modificar_nombre(self, nom):
        self.nombreproyecto = nom
    def __modificar_descripcion(self, desc):
        self.descripcion = desc
    def __modificar_fechainicio(self, fech):
        self.fechainicio = fech


    def __return_id(self):
        return self.id
    def __return_nombre(self):
        return self.nombreproyecto
    def __return_descripcion(self):
        return self.descripcion
    def __return_fechainicio(self):
        return self.fechainicio



    def set_id(self, id):
        self.__modifcar_id(id)
    def set_nombre(self, nombre):
        self.__modificar_nombre()
    def set_descripcion(self, descripcion):
        self.__modificar_descripcion(descripcion)
    def set_fechainicio(self, fecha):
        self.__modificar_fechainicio(fecha)


    def get_id (self):
        return self.__return_id()
    def get_nombre(self):
        return self.__return_nombre()
    def get_descripcion(self):
        return self.__return_descripcion()
    def get_fechainicio(self):
        return self.__return_fechainicio()
