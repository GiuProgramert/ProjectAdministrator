from tkinter import messagebox
from datetime import datetime

def validar_maximos_elementos(nombre_elemento, elementos, cantidad, ventana):
    """
        Valida la cantidad máxima si no se supera la cantidad máxima según el parametro cantidad
        nombre_elemento: nombre de lo que se va a validar
        elementos: lista de los elemento que se quieren validar
        cantidad: cantidad maxima de elementos que se quieren validar
        ventana: ventana padre para ubicar encima la ventana del mensaje
    """
    
    if len(elementos) >= cantidad:
        messagebox.showinfo(
            f"Cantidad {nombre_elemento}", 
            f"solo puede cargar {cantidad} {nombre_elemento}", 
            parent=ventana
        )
        return False
    
    return True

def validar_campos_vacios(campos, ventana):
    """
        Valida si la lista de los campos que se pasa como parametro no tiene campos vacios
        ventana: ventana padre para ubicar encima la ventana del mensaje
    """
    
    for campo in campos:
        if len(campo) == 0:
            messagebox.showinfo(
                f"Error al introducir", 
                f"Debes llenar todos los campos", 
                parent=ventana
            )
            return False

    return True

def validar_duracion_maxima(duracion, ventana):
    """
        Valida la cantidad máxima de duración y que esta no sea negativa
        ventana: ventana padre para ubicar encima la ventana del mensaje
    """
        
    if duracion > 99 or duracion <= 0:
        messagebox.showinfo(
            f"Error al introducir", 
            f"La máxima duración para una actividad es de 99 días", 
            parent=ventana
        )
        return False

    return True

# TODO
def validar_fech_inicio_proyecto(fecha, ventana):
    """
        Valida que la fecha insertada este en el formato correcto
    """
    
    # Si se introduce una fecha con menos longitud
    if len(fecha) < 10:
        return False

    try:
        # Valida el formato de la fecha
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except ValueError as ex:
        messagebox.showinfo(
            f"Error al introducir", 
            f"El formato de la fecha debe ser AAAA-MM-DD", 
            parent=ventana
        )
        print(ex)
        return False