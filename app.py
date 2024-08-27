from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
import pymysql
import smtplib
from dbdata import ConexionBaseDatos
from clase_producto import Producto
from clase_cliente import Cliente
from clase_venta import Venta
from correo_cliente import send_email
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image

#para las imagenes
import io
import base64


# Crea una instancia de la clase Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'

db_host = 'localhost'
db_user = 'root'
db_password = '123'
db_name = 'sportts'

# Define una ruta y la función asociada a esa ruta

@app.route('/')
def index():
    return render_template('index.html', Var0=True)

@app.route('/admin')
def admin():
      return render_template('index.html', Var1=True)

@app.route('/verificar_admin', methods=["POST", "GET"])
def verificar_admin():
    if request.method == "POST":
        nombre_admin = request.form.get("nombre_usuario")
        contrasena = request.form.get("contrasena")
        
        # Crear instancia de la clase ConexionBaseDatos
        conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
        conexion_db.conectar()
        
        # Consultar si las credenciales coinciden con algún registro en la tabla admin
        consulta = "SELECT nombre_admin FROM admin WHERE nombre_admin = %s AND contrasena = %s"
        valores = (nombre_admin, contrasena)
        
        resultado = conexion_db.consultar_datos(consulta, valores)
        
        if resultado:
            # Si hay resultados, las credenciales son válidas
            print("Credenciales válidas")
            conexion_db.cerrar_conexion()
            return redirect(url_for('inicio'))
        else:
            # Si no hay resultados, las credenciales son inválidas
            print("Credenciales inválidas")
            conexion_db.cerrar_conexion()
            return render_template('index.html', Var1=True, incorrect= True )
    
    # Si se accede por GET, renderizar el formulario de inicio de sesión
    return render_template('index.html', Var2=True)

@app.route('/inicio')
def inicio():
    return render_template('index.html', Var2=True)

@app.route('/productos')
def productos():
    producto = Producto(db_host, db_user, db_password, db_name)
    producto.conectar()
    productos = producto.mostrar_productos()

    # Codificar las imágenes en base64
    productos_codificados = []
    for prod in productos:
        id_producto, descripcion_producto, cantidad_producto, precio, imagen_producto = prod
        imagen_base64 = None
        if imagen_producto:
            imagen_base64 = base64.b64encode(imagen_producto).decode('utf-8')  # Codificar en base64 y decodificar a utf-8
        productos_codificados.append((id_producto, descripcion_producto, cantidad_producto, precio, imagen_base64))

    producto.cerrar_conexion()

    return render_template('index.html', Var3=True, productos=productos_codificados)



@app.route('/registrar_productos')
def registrar_productos():
     return render_template('index.html', Var4=True)

@app.route('/registro_producto', methods=["POST", "GET"])
def registro_producto():
    if request.method == "POST":
        producto = Producto(db_host, db_user, db_password, db_name)
        producto.conectar()
        
        precio = request.form.get("precio")
        cantidad = request.form.get("cantidad")
        descripcion = request.form.get("descripcion")
        
        imagen_producto = request.files.get("imagen_producto")
        imagen_data = None
        if imagen_producto:
            imagen_data = imagen_producto.read()  # Leer el contenido del archivo

        # Registra el producto
        producto.registrar_producto(descripcion, cantidad, precio, imagen_data)
        producto.cerrar_conexion()

        return redirect(url_for('registrar_productos'))

@app.route('/cargar_productos')
def cargar_productos():
    producto = Producto(db_host, db_user, db_password, db_name)
    producto.conectar()
    productos = producto.mostrar_productos()

    # Codificar las imágenes en base64
    productos_codificados = []
    for prod in productos:
        id_producto, descripcion_producto, cantidad_producto, precio, imagen_producto = prod
        imagen_base64 = None
        if imagen_producto:
            imagen_base64 = base64.b64encode(imagen_producto).decode('utf-8')  # Codificar en base64 y decodificar a utf-8
        productos_codificados.append((id_producto, descripcion_producto, cantidad_producto, precio, imagen_base64))

    producto.cerrar_conexion()

    return render_template('index.html', Var5=True, productos=productos_codificados)

@app.route('/eliminar_producto/<int:id>', methods=["GET"])
def eliminar_producto(id):
    producto = Producto(db_host, db_user, db_password, db_name)
    producto.conectar()
    producto.eliminar_producto(id)
    producto.cerrar_conexion()
    return redirect(url_for('cargar_productos'))

@app.route('/modificar_producto', methods=["POST"])
def modificar_producto_post():
    if request.method == "POST":
        id_producto = request.form.get("id_producto")
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        cantidad = request.form.get("cantidad")
        imagen_producto = request.files.get("imagen_producto")
        imagen_data = None
        if imagen_producto:
            imagen_data = imagen_producto.read()  # Leer el contenido del archivo

        producto = Producto(db_host, db_user, db_password, db_name)
        producto.conectar()
        producto.modificar_producto(id_producto, descripcion, precio, cantidad, imagen_data)
        producto.cerrar_conexion()

        flash('Producto modificado exitosamente')
        return redirect(url_for('cargar_productos'))



# Supongamos que tienes una clase Cliente definida con los métodos correspondientes

@app.route('/cargar_clientes')
def cargar_clientes():
    cliente = Cliente(db_host, db_user, db_password, db_name)
    cliente.conectar()
    clientes = cliente.mostrar_clientes()
    cliente.cerrar_conexion()
    return render_template('index.html', Var6=True, clientes=clientes)

@app.route('/eliminar_cliente/<int:cedula_cliente>', methods=["GET"])
def eliminar_cliente(cedula_cliente):
    cliente = Cliente(db_host, db_user, db_password, db_name)
    cliente.conectar()
    cliente.eliminar_cliente(cedula_cliente)
    cliente.cerrar_conexion()
    flash('Cliente eliminado exitosamente')
    return redirect(url_for('cargar_clientes'))

@app.route('/modificar_cliente', methods=["GET"])
def mostrar_lista_clientes():
    # Obtener la lista de clientes desde la base de datos
    cliente = Cliente(db_host, db_user, db_password, db_name)
    cliente.conectar()
    clientes = cliente.mostrar_clientes()
    cliente.cerrar_conexion()
    return render_template('index.html', clientes=clientes, Var6=True)

@app.route('/modificar_cliente', methods=["POST"])
def modificar_cliente_post():
    if request.method == "POST":
        cedula_cliente_original = request.form.get("cedula_cliente_original")
        cedula_cliente = request.form.get("cedula_cliente")
        nombre = request.form.get("nombre_cliente")
        apellido = request.form.get("apellido_cliente")
        telefono = request.form.get("telefono_cliente")
        email = request.form.get("email_cliente")
        contrasena = request.form.get("contrasena_cliente")

        cliente = Cliente(db_host, db_user, db_password, db_name)
        cliente.conectar()
        cliente.modificar_cliente(cedula_cliente_original, cedula_cliente, nombre, apellido, telefono, email, contrasena)
        cliente.cerrar_conexion()
        flash('Cliente modificado exitosamente')

    return redirect(url_for('mostrar_lista_clientes'))

    

    
@app.route('/verificar_cliente', methods=["POST", "GET"])
def verificar_cliente():
    if request.method == "POST":
        cedula_cliente = request.form.get("cedula_cliente")
        contrasena_cliente = request.form.get("contrasena_cliente")
        
        # Crear instancia de la clase ConexionBaseDatos
        conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
        conexion_db.conectar()

        # Consultar si las credenciales coinciden con algún registro en la tabla cliente
        consulta = "SELECT cedula_cliente, nombre_cliente FROM cliente WHERE cedula_cliente = %s AND contrasena_cliente = %s"
        valores = (cedula_cliente, contrasena_cliente)
        
        resultado = conexion_db.consultar_datos(consulta, valores)
        
        if resultado:
            # Si hay resultados, las credenciales son válidas
            session['cedula_cliente'] = resultado[0][0]
            session['nombre_cliente'] = resultado[0][1]   # Asumiendo que el nombre del cliente es el segundo valor en el resultado
            print (resultado[0][1])
            print ("hola")
            conexion_db.cerrar_conexion()
            return redirect(url_for('inicio_cliente'))
        else:
            # Si no hay resultados, las credenciales son inválidas
            conexion_db.cerrar_conexion()
            return render_template('index.html', Var7=True, incorrect=True)
    
    # Si se accede por GET, renderizar el formulario de inicio de sesión
    return render_template('index.html', Var2=True)


@app.route('/registrar_cliente')
def registrar_cliente():
     return render_template('index.html', Var8 = True)
    
@app.route('/pedidos')
def pedidos():
    venta = Venta(db_host, db_user, db_password, db_name)
    venta.conectar()
    pedidos = venta.mostrar_ventas()  # Asegúrate de que esta función existe
    venta.cerrar_conexion()
    return render_template('index.html', Var12=True, pedidos=pedidos)
    
@app.route('/registro_cliente', methods=["POST", "GET"])
def registro_cliente():
    if request.method == "POST":
        cliente = Cliente(db_host, db_user, db_password, db_name)
        cliente.conectar()
        
        # Obtener los datos del formulario
        cedula_cliente = request.form.get("cedula_cliente")
        nombre_cliente = request.form.get("nombre_cliente")
        apellido_cliente = request.form.get("apellido_cliente")
        telefono_cliente = request.form.get("telefono_cliente")
        email_cliente = request.form.get("email_cliente")
        contrasena_cliente = request.form.get("contrasena_cliente")
        confirmar_contrasena = request.form.get("confirmar_contrasena")

        # Registrar el cliente
        cliente.registrar_cliente(cedula_cliente, nombre_cliente, apellido_cliente, telefono_cliente, email_cliente, contrasena_cliente)
        cliente.cerrar_conexion()
        
    return render_template('index.html', Var7=True)
    
@app.route('/inicio_cliente')
def inicio_cliente():
    #cedula_cliente = session.get('cedula_cliente')  # Obtener la cédula del cliente desde la sesión
    #nombre_cliente = session.get('nombre_cliente')  # Obtener el nombre del cliente desde la sesión
    return render_template('index.html', Var9=True)#, cedula_cliente=cedula_cliente, nombre_cliente=nombre_cliente)
    
@app.route('/compra')
def compra():
    datos_carrito = session.get('carrito', {})
    carrito = datos_carrito.get('carrito', [])
    total = datos_carrito.get('total', 0)

    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()

    consulta_metodos_pago = "SELECT metodo_pago, descripcion FROM metodo_de_pago"
    metodos_de_pago = conexion_db.consultar_datos(consulta_metodos_pago)

    print(metodos_de_pago)  # Esto para asegurarte de que los datos son correctos

    conexion_db.cerrar_conexion()

    return render_template('index.html', Var10=True, metodos_de_pago=metodos_de_pago, datos_carrito=carrito, total=total)

@app.route('/confirmar-compra', methods=['POST'])
def confirmar_compra():  
    datos = request.json
    cedula_cliente = session.get('cedula_cliente')
    costo_total = datos.get('total')
    metodo_pago = datos.get('metodo_pago')
    carrito = datos.get('carrito')
    print("cedula: ", cedula_cliente, "costo total: ", costo_total, "metodo pago: ", metodo_pago)


    venta = Venta(db_host, db_user, db_password, db_name)
    venta.conectar()

    try:
        for item in carrito:
            id_producto = item['id_producto']
            cantidad = item['cantidad']
            print("ID Producto: ", id_producto, "Cantidad: ", cantidad)  # Agregar print para verificar el id_producto y cantidad
            venta.registrar_venta(cedula_cliente, costo_total, metodo_pago, id_producto, cantidad)

        venta.cerrar_conexion()
        return jsonify({'success': True})

    except Exception as e:
        print(f"Error al procesar la compra: {e}")
        venta.cerrar_conexion()
        return jsonify({'success': False, 'error': str(e)})


@app.route('/compra_finalizada')
def compra_finalizada():
    subject = "Confirmación de Compra"
    message = "¡Gracias por tu compra! Esperamos que disfrutes de tus productos."
    recipient_email = "sierraorlan25@gmail.com"  # Cambia esto por el correo electrónico real del cliente

    send_email(subject, message, recipient_email)
    return render_template('index.html', Var11=True)

def generate_pdf(productos_codificados):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []
    

    # Add a title
    styles = getSampleStyleSheet()
    title = Paragraph("Deportes Webston", styles['Title'])
    elements.append(title)

    # Define the table data
    data = [['ID', 'Descripción', 'Cantidad', 'Precio']]
    for prod in productos_codificados:
        id_producto, descripcion, cantidad, precio, imagen_base64 = prod
        imagen_path = None
        if imagen_base64:
            try:
                # Decodificar imagen de base64
                imagen = Image.open(io.BytesIO(base64.b64decode(imagen_base64)))
                
                imagen.save(imagen_path)
            except Exception as e:
                imagen_path = None

        row = [id_producto, descripcion, cantidad, f"${precio:.2f}"]
        data.append(row)

    # Create table and set style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Azul pastel para la cabecera
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texto blanco en la cabecera
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),  # Azul pastel claro para el fondo de las filas
        ('GRID', (0, 0), (-1, -1), 1, colors.lightblue),  # Rejilla azul pastel
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return buffer

@app.route('/reporte')
def reporte():
    producto = Producto(db_host, db_user, db_password, db_name)
    producto.conectar()
    productos = producto.mostrar_productos()

    # Codificar las imágenes en base64
    productos_codificados = []
    for prod in productos:
        id_producto, descripcion_producto, cantidad_producto, precio, imagen_producto = prod
        imagen_base64 = None
        if imagen_producto:
            imagen_base64 = base64.b64encode(imagen_producto).decode('utf-8')  # Codificar en base64 y decodificar a utf-8
        productos_codificados.append((id_producto, descripcion_producto, cantidad_producto, precio, imagen_base64))

    producto.cerrar_conexion()

    # Generar el PDF
    buffer = generate_pdf(productos_codificados)


    return send_file(buffer, as_attachment=True, download_name='reporte_productos.pdf', mimetype='application/pdf')


