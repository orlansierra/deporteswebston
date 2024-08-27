import pymysql




class Producto:
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

    def registrar_producto(self, descripcion, cantidad, precio, imagen_producto):
        try:
            consulta = "INSERT INTO producto (descripcion_producto, cantidad_producto, precio, imagen_producto) VALUES (%s, %s, %s, %s)"
            valores = (descripcion, cantidad, precio, imagen_producto)
            self.cursor.execute(consulta, valores)
            self.conexion.commit()
            print("Producto registrado correctamente.")
        except pymysql.Error as error:
            print("Error al registrar el producto:", error)

    def mostrar_productos(self):
        try:
            consulta = "SELECT * FROM producto"
            self.cursor.execute(consulta)
            productos = self.cursor.fetchall()
            return productos
        except pymysql.Error as error:
            print("Error al mostrar los productos:", error)
            return []

    def eliminar_producto(self, id_producto):
        try:
            consulta = "DELETE FROM producto WHERE id_producto = %s"
            valores = (id_producto,)
            self.cursor.execute(consulta, valores)
            self.conexion.commit()
            print("Producto eliminado correctamente.")
        except pymysql.Error as error:
            print("Error al eliminar el producto:", error)


    def modificar_producto(self, id_producto, descripcion=None, precio=None, cantidad=None, imagen=None):
        try:
            consulta = "UPDATE producto SET "
            valores = []
            if descripcion:
                consulta += "descripcion_producto = %s, "
                valores.append(descripcion)
            if precio:
                consulta += "precio = %s, "
                valores.append(precio)
            if cantidad:
                consulta += "cantidad_producto = %s, "
                valores.append(cantidad)
            if imagen:
                consulta += "imagen_producto = %s, "
                valores.append(imagen)

            # Eliminar la última coma y espacio
            consulta = consulta.rstrip(", ")
            consulta += " WHERE id_producto = %s"
            valores.append(id_producto)

            self.cursor.execute(consulta, tuple(valores))
            self.conexion.commit()
            print("Producto modificado correctamente.")
        except pymysql.Error as error:
            print("Error al modificar el producto:", error)

    def obtener_producto(self, id_producto):
        try:
            consulta = "SELECT * FROM producto WHERE id_producto = %s"
            self.cursor.execute(consulta, (id_producto,))
            producto = self.cursor.fetchone()
            return producto
        except pymysql.Error as error:
            print("Error al obtener el producto:", error)
            return None
 
