import pymysql

class ConexionBaseDatos:
    def __init__(self, host, usuario, contrasena, nombre_base_datos):
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre_base_datos = nombre_base_datos
        self.conexion = None
        self.cursor = None
#para conectar xD
    def conectar(self):
        try:
            self.conexion = pymysql.connect(host=self.host, user=self.usuario, password=self.contrasena, db=self.nombre_base_datos)
            self.cursor = self.conexion.cursor()
            print("Conexión a la base de datos establecida correctamente.")
        except pymysql.Error as error:
            print("Error al conectar a la base de datos:", error)
#para cerrar xD
    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión a la base de datos cerrada correctamente.")
#para ejecutar_consultas xD
    def ejecutar_consulta(self, consulta, valores=None):
        try:
            with self.conexion.cursor() as cursor:
                if valores:
                    cursor.execute(consulta, valores)
                else:
                    cursor.execute(consulta)
            self.conexion.commit()  
            print("Consulta ejecutada y transacción confirmada correctamente.")
            return cursor.fetchall()  # Devuelve los resultados de la consulta
        except pymysql.Error as error:
            print(f"Error al ejecutar la consulta: {error}")
            return None  # Devuelve None en caso de error
#para consultar_datos xD
    def consultar_datos(self, consulta, valores=None):
        try:
            if valores:
                self.cursor.execute(consulta, valores)
            else:
                self.cursor.execute(consulta)
            resultados = self.cursor.fetchall()
            return resultados
        except pymysql.Error as error:
            print("Error al consultar datos:", error)
            return None
# para eliminar_datos xD
    def eliminar_datos(self, consulta):
        self.ejecutar_consulta(consulta)
        print("Datos eliminados correctamente.")
# para modificar_datos   XD     
    def modificar_datos(self, consulta):
        self.ejecutar_consulta(consulta)
        print("Datos modificados correctamente.")
# para registrar datos XD
    def registrar_datos(self, consulta):
        self.ejecutar_consulta(consulta)
        print("Datos registrados correctamente.")
        
if __name__ == "__main__":
    host = 'localhost'
    usuario = 'root'
    contrasena = ''
    nombre_base_datos = 'productos_no_tangibles'

    conexion_db = ConexionBaseDatos(host, usuario, contrasena, nombre_base_datos)
    conexion_db.conectar()

    # Ejemplo de consultaXD
    consulta_select = "SELECT * FROM proveedor"
    resultados = conexion_db.consultar_datos(consulta_select)
    print("Resultados de la consulta SELECT:")
    print(resultados)

    # Ejemplo de eliminaciónXD
    consulta_delete = "DELETE FROM usuarios WHERE id = 1"
    conexion_db.eliminar_datos(consulta_delete)

    # Ejemplo de modificaciónXD
    consulta_update = "UPDATE usuarios SET nombre = 'Nuevo Nombre' WHERE id = 2"
    conexion_db.modificar_datos(consulta_update)

    # Ejemplo de registroXD
    consulta_insert = "INSERT INTO usuarios (nombre, email) VALUES ('Nuevo Usuario', 'nuevo_usuario@example.com')"
    conexion_db.registrar_datos(consulta_insert)

    # Cerrar la conexión cuando hayas terminadoXD
    conexion_db.cerrar_conexion()
    
    conexion_db = ConexionBaseDatos(host, usuario, contrasena, nombre_base_datos)
    conexion_db.conectar()
    consulta = "SELECT idproveedor, nombre FROM proveedor;"
    proveedores = conexion_db.consultar_datos(consulta)
    print (proveedores)
    conexion_db.cerrar_conexion()


