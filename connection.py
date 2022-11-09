import sqlite3


class Connection:
    """Clase encargada de gestionar la base de datos"""
    def __init__(self, db_name='database.db'):
        """Recibe el nombre del archivo que 
        hace referencia a la base de datos"""
        try:
            self.connection = sqlite3.connect(db_name)  # Crea la conexión con la base de datos
            self.cursor = self.connection.cursor() # El cursor sirve para hacer las consultas en la base de datos
        except Exception as ex:
            print("Error to search the DB: ", ex)

    def update(self, table, columns, values, columna_id, id):
        """
            realiza la operación de actualizar dependiendo de los parametros
            - table: nombre de la tabla a actualizar 
            - columns: lista de nombre de las columnas a actualizar
            - values: lista de los valores a actualizar
            - columna_id: nombre de la clave primaría a actualizar
            - id: valor de la id de la columna de la clave primaría
        """
        
        try:
            # crea la query para actualizar
            query = self.create_update_query(table, columns, columna_id)

            # ejecuta la query
            self.cursor.execute(query, (*values, id))
            self.connection.commit()
                        
            print(f"Actualizado correctamente en la tabla {table}")
            return True
        except Exception as ex:
            print(f"Error al tratar de eliminar el objeto de la tabla {table} con el id {id}")
            print(ex)
            return False

    def create_update_query(self, table, columns, columna_id):
        """Crea la query para actualizar los datos según los parametros"""
        
        # Tabla a modificar
        query = f"UPDATE {table}\n SET "

        # Columnas a modificar de la tabla
        for column in columns:
            query += f"{column} = ?, "
        
        # Condición para actualizar dependiente del nombre de la clave primaría
        query = query[:-2] + f"\nWhere {columna_id} = ?"

        return query

    def create_insert_query(self, table, columns):
        """Crea la query para insertar los datos según los parametros"""
        
        # Tabla a modificar
        query = f"INSERT INTO {table} \n"
        
        columns_query = "("
        values_query = "VALUES ("

        # Columnas a modificar de la tabla
        for column in columns:
            columns_query += f"{column}, "
            values_query += "?, "

        # Terminando la cadena correctamente    
        columns_query = columns_query[:-2] + ")\n"         
        values_query = values_query[:-2] + ")"

        query += columns_query + values_query

        return query

    def insert(self, table, columns, values):
        """
            realiza la operación de insertar dependiendo de los parametros
            - table: nombre de la tabla a insertar 
            - columns: lista de nombres de las columnas a insertar
            - values: lista de los valores a insertar
        """

        # Crea la query
        query = self.create_insert_query(table, columns)
        
        # Ejecuta la query
        self.cursor.execute(query, values)
        self.connection.commit()

        # ID del último elemento insertado
        element_id = self.cursor.lastrowid

        return element_id

    def select(self, query):
        """Solamente usada para crear una consulta de tipo select con la query especificada"""

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_by_id(self, table, columna, id):
        """
            Eliminar un registro de la base de datos teniendo en cuenta el id del elemento
            realiza la operación de actualizar dependiendo de los parametros
            - table: nombre de la tabla a borrar
            - columna: nombre de la columna identificadora
            - id: valor de la id de la columna de la clave primaría
        """
        try:
            query = f"DELETE FROM {table} WHERE {columna} = {id}"

            # Ejecuta la query
            self.cursor.execute(query)
            self.connection.commit()

            print(f"Eliminado correctamente de la tabla {table}")
            return True
        except Exception as ex:
            print(ex)
            print(f"Error al tratar de eliminar el objeto de la tabla {table} con id {id}")
            return False

    def close_connection(self):
        """Cierra la conexión con la base de datos"""

        self.cursor.close()
        self.connection.close()
        print("Conexion finalizada")


