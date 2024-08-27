import base64
import pymysql

class Venta:
    def __init__(self, host, usuario, contrasena, nombre_base_datos):
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre_base_datos = nombre_base_datos
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = pymysql.connect(
                host=self.host,
                user=self.usuario,
                password=self.contrasena,
                db=self.nombre_base_datos
            )
            print("Conexión a la base de datos establecida correctamente.")
        except pymysql.Error as error:
            print("Error al conectar a la base de datos:", error)

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión a la base de datos cerrada correctamente.")

    def registrar_venta(self, cedula_cliente, costo_total, metodo_pago, id_producto, cantidad):
        try:
            with self.conexion.cursor() as cursor:
                consulta = "INSERT INTO venta (cedula_cliente, costo_total, metodo_pago, id_producto, cantidad) VALUES (%s, %s, %s, %s, %s)"
                valores = (cedula_cliente, costo_total, metodo_pago, id_producto, cantidad)
                cursor.execute(consulta, valores)
                self.actualizar_stock(id_producto, cantidad)
            self.conexion.commit()
            print("Venta registrada correctamente.")
        except pymysql.Error as error:
            print("Error al registrar la venta:", error)

    def actualizar_stock(self, id_producto, cantidad):
        try:
            with self.conexion.cursor() as cursor:
                consulta_stock = "UPDATE producto SET cantidad_producto = cantidad_producto - %s WHERE id_producto = %s"
                cursor.execute(consulta_stock, (cantidad, id_producto))
            self.conexion.commit()
            print(f"Stock del producto {id_producto} actualizado correctamente.")
        except pymysql.Error as error:
            print(f"Error al actualizar el stock del producto {id_producto}: {error}")

    def mostrar_ventas(self):
        try:
            with self.conexion.cursor() as cursor:
                consulta = """
                SELECT v.id_venta, c.nombre_cliente, v.cedula_cliente, v.costo_total, m.descripcion, p.imagen_producto
                FROM venta v
                JOIN cliente c ON v.cedula_cliente = c.cedula_cliente
                JOIN metodo_de_pago m ON v.metodo_pago = m.metodo_pago
                JOIN producto p ON v.id_producto = p.id_producto
                """
                cursor.execute(consulta)
                ventas = cursor.fetchall()

                # Convertir las imágenes a base64
                ventas_base64 = []
                for venta in ventas:
                    imagen_base64 = base64.b64encode(venta[5]).decode('utf-8') if venta[5] else None
                    ventas_base64.append(venta[:5] + (imagen_base64,))
                
                return ventas_base64
        except pymysql.Error as error:
            print("Error al mostrar las ventas:", error)
            return []