import pyodbc


class Conexion:
    """
    Permite conectar con la bd y realizar consultas basicas para actualizar los datos
    """

    def __init__(self, conector):
        """
        Llama al metodo para iniciar la conexión con la bd y guarda los atributos
        """
        self.conexion = None
        self.cursor = None
        self.iniciar_conexion(conector)

    def iniciar_conexion(self, conector):
        """
        Inicia la conexion, recibiendo como unico parametro el enlace a la bd
        """
        try:
            self.conexion = pyodbc.connect(conector)
            self.cursor = self.conexion.cursor()
            print("Conexion exitosa")

        except pyodbc.Error as e:
            raise ValueError("Error: Fallo la conexion")

    def cerrar_conexion(self):
        """
        Detiene la conexion cuando el proceso se cumple y los datos ya se encuentran cargados
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.conexion:
                self.conexion.close()

        except pyodbc.Error as e:
            raise ValueError(f"Error: Fallo al cerrar la conexion -> {e}")

    def ejecutar_consulta(self, query, parametros=()):
        """
        Recibe el string de la consulta y la ejecuta un SELECT sobre la bd
        """
        try:
            self.cursor.execute(query, parametros)
            return [tuple(fila) for fila in self.cursor.fetchall()]

        except pyodbc.Error as e:
            raise ValueError(f"Error: Fallo la consulta -> {e}")

    def insertar_datos(self, query, *args):
        try:
            self.cursor.execute(query, args)
            self.conexion.commit()
        except pyodbc.Error as e:
            self.conexion.rollback()
            raise ValueError(f"Error: Fallo el comando -> {e}")
