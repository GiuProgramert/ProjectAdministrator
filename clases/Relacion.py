
class Relacion:

    def __init__(self, idrelacion, idprecedente, idsiguiente):
        self.id_relacion = idrelacion
        self.id_precedente = idprecedente
        self.id_siguiente = idsiguiente

    def __modificar_idrelacion(self, id):
        self.id_relacion = id
    def __modificar_idprecedente(self, id):
        self.id_precedente = id
    def __modificar_idsiguiente(self, id):
        self.id_siguiente = id

    def __return_idrelacion(self):
        return self.id_relacion
    def __return_idprecedente(self):
        return self.id_precedente
    def __return_idsiguiente(self):
        return self.id_siguiente


    def set_idrelacion(self, id):
        self.__modificar_idrelacion(id)
    def set_idprecedentes(self, id):
        self.__modificar_idprecedente(id)
    def set_idsiguiente(self, id):
        self.__modificar_idsiguiente(id)

    def get_idrelacion(self):
        self.__return_idrelacion()
    def get_idprecedente(self):
        self.__return_idprecedente()
    def get_idsiguiente(self):
        self.__return_idsiguiente()
