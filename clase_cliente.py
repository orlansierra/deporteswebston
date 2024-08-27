import pymysql

class Cliente:
    def __init__(self, host, usuario, contrasena, nombre_base_datos):
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre_base_datos = nombre_base_datos
        self.conexion = None
        self.cursor = None

    def conectar(self):
        try:
            self.conexion = pymysql.connect(
                host=self.host,
                user=self.usuario,
                password=self.contrasena,
                db=self.nombre_base_datos
            )
            self.cursor = self.conexion.cursor()
            print("Conexión a la base de datos establecida correctamente.")
        except pymysql.Error as error:
            print("Error al conectar a la base de datos:", error)

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión a la base de datos cerrada correctamente.")
            
    def mostrar_clientes(self):
        try:
            consulta = "SELECT * FROM cliente"
            self.cursor.execute(consulta)
            clientes = self.cursor.fetchall()
            return clientes
        except pymysql.Error as error:
            print("Error al mostrar los clientes:", error)
            return []

    def registrar_cliente(self, cedula_cliente, nombre_cliente, apellido_cliente, telefono_cliente, email_cliente, contrasena_cliente):
        try:
            consulta = "INSERT INTO cliente (cedula_cliente, nombre_cliente, apellido_cliente, telefono_cliente, email_cliente, contrasena_cliente) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (cedula_cliente, nombre_cliente, apellido_cliente, telefono_cliente, email_cliente, contrasena_cliente)
            self.cursor.execute(consulta, valores)
            self.conexion.commit()
            print("Cliente registrado correctamente.")
        except pymysql.Error as error:
            print("Error al registrar el cliente:", error)

            
    def eliminar_cliente(self, cedula_cliente):
        try:
            consulta = "DELETE FROM cliente WHERE cedula_cliente = %s"
            valores = (cedula_cliente,)
            self.cursor.execute(consulta, valores)
            self.conexion.commit()
            print("cliente eliminado correctamente.")
        except pymysql.Error as error:
            print("Error al eliminar el cliente:", error)

    def modificar_cliente(self, cedula_cliente_original, cedula_cliente, nombre=None, apellido=None, telefono=None, email=None, contrasena=None):
        try:
            consulta = "UPDATE cliente SET "
            valores = []
        
            if cedula_cliente != cedula_cliente_original:
                consulta += "cedula_cliente = %s, "
                valores.append(cedula_cliente)
        
            if nombre:
                consulta += "nombre_cliente = %s, "
                valores.append(nombre)
            if apellido:
                consulta += "apellido_cliente = %s, "
                valores.append(apellido)
            if telefono:
                consulta += "telefono_cliente = %s, "
                valores.append(telefono)
            if email:
                consulta += "email_cliente = %s, "
                valores.append(email)
            if contrasena:
                consulta += "contrasena_cliente = %s, "
                valores.append(contrasena)

            # Eliminar la última coma y espacio
            consulta = consulta.rstrip(", ")
            consulta += " WHERE cedula_cliente = %s"
            valores.append(cedula_cliente_original)

            self.cursor.execute(consulta, tuple(valores))
            self.conexion.commit()
            print("Cliente modificado correctamente.")
        except pymysql.Error as error:
            print("Error al modificar el cliente:", error)