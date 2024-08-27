from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


# Ejemplo de datos de productos
productos = [
    [1, "Producto A", 10, 20.5, None],
    [2, "Producto B", 5, 30.0, "base64_encoded_image_data"]
    # Agrega más productos aquí
]

def generate_pdf(productos):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Título
    title = "LISTA DE PRODUCTOS"
    title_table = Table([[title]], colWidths=[540], rowHeights=[30])
    title_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(title_table)

    # Encabezados de la tabla
    data = [["ID", "Descripción", "Cantidad", "Precio", "Imagen", "Acciones"]]
    for producto in productos:
        imagen = "Con imagen" if producto[4] else "Sin imagen"
        data.append([
            producto[0],
            producto[1],
            producto[2],
            f"${producto[3]:.2f}",
            imagen,
            "Modificar"  # Puedes agregar más detalles si deseas
        ])

    table = Table(data, colWidths=[50, 200, 100, 100, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return buffer