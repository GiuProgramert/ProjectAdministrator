from tkinter import Toplevel, LabelFrame, Label, StringVar, Entry, ttk, Button, messagebox, Tk
from tokenize import String
from connection import Connection

from helpers.LoadTableData import LoadTableData

class EditarProyectoForm(LoadTableData):
    def __init__(self, id, ventana_padre, connection, tabla):
        self.id = id
        self.ventana_padre = ventana_padre
        self.connection = connection
        self.tabla = tabla

        self.ventana = Toplevel(self.ventana_padre)
        self.ventana.title("Actualizar Proyecto")
        self.ventana.geometry("300x230")

        self.name_text = StringVar()
        self.desc_text = StringVar()
        self.fecha_init_text = StringVar()

        super().__init__(self.table, f"SELECT * FROM Acticidad where proyecto_id = {self.id}")

        self.frame = LabelFrame(self.ventana, text='Actualizar Proyecto', height=70)
        self.frame.grid(row=0, column=0, columnspan=5, pady=10, padx=55)

        self.name_label = Label(self.frame, text="Nombre: ").grid(row=1, column=0)
        self.desc_label = Label(self.frame, text="Descripción: ").grid(row=3, column=0)
        self.fecha_init_label = Label(self.frame, text="Fecha inicial: ").grid(row=5, column=0)

        self.name_entry = Entry(self.frame, textvariable=self.name_text)
        self.name_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.desc_entry = Entry(self.frame, textvariable=self.desc_text)
        self.desc_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.fecha_init_entry = Entry(self.frame)

        self.insert_button = Button(self.ventana, text='Actualizar cliente', command=self.update_cliente)
        self.insert_button.grid(row=6, column=0, columnspan=5)

        self.set_entries()

    def get_cliente_by_id(self, id: int) -> list:
        return self.connection.select(f"select * from clientes where id = {id}")[0]

    def set_entries(self) -> None:
        self.cliente = self.get_cliente_by_id(self.id)
        self.name_text.set(self.cliente[1])
        self.email_text.set(self.cliente[2])

    def update_cliente(self) -> None:
        name_value = self.name_entry.get()
        email_value = self.email_entry.get()

        self.connection.update(
            "clientes",
            ("nombre", "correo"),
            (name_value, email_value),
            self.id
        )

        messagebox.showinfo("Clientes", "Actualizado correctamente", parent=self.ventana)
        super().load_data()
        self.ventana_padre.focus()
        self.ventana.destroy()