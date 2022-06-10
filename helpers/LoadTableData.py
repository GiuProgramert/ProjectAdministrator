from tkinter.ttk import Treeview
from connection import Connection

class LoadTableData:
    def __init__(self, table, query):
        self.table = table
        self.query = query

    def get_data_from_query(self):
        return self.connection.select(self.query)

    def clean_table(self):
        records = self.table.get_children()
        for element in records:
            self.table.delete(element)

    def fill_table(self):
        self.rows = self.get_data_from_query()
        for row in self.rows:
            self.table.insert("", index=row[0], text=row[0], values=row[1:])

        return len(self.rows)

    def load_data(self):
        self.clean_table()
        return self.fill_table()