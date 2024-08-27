let mostrador = document.getElementById("mostrador");
let seleccion = document.getElementById("seleccion");
let imgSeleccionada = document.getElementById("img");
let modeloSeleccionado = document.getElementById("modelo");
let descripSeleccionada = document.getElementById("descripcion");
let precioSeleccionado = document.getElementById("precio");

let carrito = [];
let total = 0;

function cargar(item) {
    quitarBordes();
    mostrador.style.width = "60%";
    seleccion.style.width = "40%";
    seleccion.style.opacity = "1";
    item.style.border = "2px solid blue";
    item.style.height = "17rem";

    imgSeleccionada.src = item.getElementsByTagName("img")[0].src;
    modeloSeleccionado.innerHTML = item.getElementsByClassName("descripcion")[0].innerHTML;
    precioSeleccionado.innerHTML = item.getElementsByClassName("precio")[0].innerHTML;
    seleccion.dataset.producto = item.getElementsByClassName("descripcion")[0].innerHTML;
    seleccion.dataset.precio = item.getElementsByClassName("precio")[0].innerHTML.replace('$', '');
    seleccion.dataset.id = item.dataset.id;  // Establecer el id del producto
}

function cerrar() {
    mostrador.style.width = "100%";
    seleccion.style.width = "0%";
    seleccion.style.opacity = "0";
    quitarBordes();
}

function quitarBordes() {
    var items = document.getElementsByClassName("item");
    for (let i = 0; i < items.length; i++) {
        items[i].style.border = "none";
    }
}

function openNav() {
    document.getElementById("mySidebar").style.width = "350px";
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
}

function agregarAlCarrito() {
    const producto = seleccion.dataset.producto;
    const precio = parseFloat(seleccion.dataset.precio);
    const img = imgSeleccionada.src;
    const idProducto = seleccion.dataset.id;  // Obtener el id del producto desde el atributo data-id

    const productoExistente = carrito.find(item => item.id_producto === idProducto);
    if (productoExistente) {
        productoExistente.cantidad += 1;
    } else {
        carrito.push({ producto, precio, cantidad: 1, img, id_producto: idProducto });  // Incluir id_producto
    }

    // Imprimir el carrito en la consola
    console.log(carrito);  // Esto mostrará todos los productos en el carrito, incluyendo el id_producto

    actualizarContador();
    actualizarCarrito();
}

function eliminarDelCarrito(producto) {
    carrito = carrito.filter(item => item.producto !== producto);
    actualizarCarrito();
}
function vaciarCarrito() {
    carrito = [];
    actualizarCarrito();
}
function aumentarCantidad(producto) {
    const productoExistente = carrito.find(item => item.producto === producto);
    if (productoExistente) {
        productoExistente.cantidad += 1;
        actualizarCarrito();
    }
}

function disminuirCantidad(producto) {
    const productoExistente = carrito.find(item => item.producto === producto);
    if (productoExistente && productoExistente.cantidad > 1) {
        productoExistente.cantidad -= 1;
        actualizarCarrito();
    }
}

function actualizarContador() {
    const contadorProductos = document.getElementById('contador-productos');
    contadorProductos.innerText = carrito.reduce((acc, item) => acc + item.cantidad, 0);
}

function actualizarCarrito() {
    const listaCarrito = document.getElementById('lista-carrito');
    const totalCarrito = document.getElementById('total-carrito');
    
    listaCarrito.innerHTML = '';
    total = 0;
    
    carrito.forEach(item => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            <div>
                <img src="${item.img}" alt="Imagen del producto" style="width: 50px; height: 50px;">
                ${item.producto} - $${item.precio}

                
            </div>
            <div>
                 <span>${item.cantidad}</span>
                <button class="btn btn-sm btn-primary" onclick="disminuirCantidad('${item.producto}')">-</button>
                <button class="btn btn-sm btn-primary" onclick="aumentarCantidad('${item.producto}')">+</button>
                <button class="btn btn-danger btn-sm" onclick="eliminarDelCarrito('${item.producto}')">Eliminar</button>
            </div>`;
        listaCarrito.appendChild(li);
        total += item.precio * item.cantidad;
    });
    
    totalCarrito.innerText = `Total: $${total.toFixed(2)}`;
}

function confirmarCompra() {
    // Crear un objeto con los datos del carrito
    const datosCarrito = {
        carrito: carrito,
        total: total
    };

    // Convertir el objeto a formato JSON
    const carritoJSON = JSON.stringify(datosCarrito);

    // Almacenar los datos del carrito en el almacenamiento local (opcional)
    localStorage.setItem('carritoJSON', carritoJSON);

    // Redireccionar a la página de confirmación
    window.location.href = '/compra';
}

// compra de carrito

document.addEventListener('DOMContentLoaded', function() {
    // Recuperar los datos del carrito del almacenamiento local
    const carritoJSON = localStorage.getItem('carritoJSON');
    const datosCarrito = JSON.parse(carritoJSON);

    // Mostrar los productos seleccionados en la página
    mostrarProductosSeleccionados(datosCarrito);

    // Capturar el evento de envío del formulario
    const formulario = document.getElementById('confirmar-compra-form');
    formulario.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevenir el comportamiento por defecto

        // Obtener el método de pago seleccionado
        const metodoPago = document.getElementById('metodo_pago').value;

        // Crear un objeto con los datos a enviar
        const datosAEnviar = {
            carrito: datosCarrito.carrito,
            total: datosCarrito.total,
            metodo_pago: metodoPago,
            cedula_cliente: '{{ cedula_cliente }}' // Asegúrate de que esta variable esté disponible en el contexto del template
        };

        // Enviar los datos a la ruta de confirmación de compra
        fetch('/confirmar-compra', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosAEnviar)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Limpiar el carrito y redireccionar a la página de éxito
                localStorage.removeItem('carritoJSON');
                window.location.href = '/compra_finalizada';
            } else {
                // Mostrar un mensaje de error
                alert('Error al confirmar la compra');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al confirmar la compra');
        });
    });
});

function mostrarProductosSeleccionados(datosCarrito) {
    const contenedorProductos = document.getElementById('productos-seleccionados');

    datosCarrito.carrito.forEach(item => {
        const productoDiv = document.createElement('div');
        productoDiv.classList.add('producto-item');
        productoDiv.innerHTML = `
            <p>${item.producto} - $${item.precio} x ${item.cantidad}</p>
            <img src="${item.img}" alt="Imagen del producto" style="width: 50px; height: 50px;">
        `;
        contenedorProductos.appendChild(productoDiv);
    });

    const totalDiv = document.createElement('div');
    totalDiv.classList.add('total');
    totalDiv.innerHTML = `<p>Total: $${datosCarrito.total.toFixed(2)}</p>`;
    contenedorProductos.appendChild(totalDiv);
}
// lista de productos var 5
function cargarDatosProducto(id, descripcion, precio, cantidad) {
    document.getElementById('modificarProductoId').value = id;
    document.getElementById('modificarDescripcion').value = descripcion;
    document.getElementById('modificarPrecio').value = precio;
    document.getElementById('modificarCantidad').value = cantidad;
  }
  
  document.querySelectorAll('.btn-modificar').forEach(button => {
    button.addEventListener('click', (event) => {
      const id = event.target.dataset.id;
      const descripcion = event.target.dataset.descripcion;
      const precio = event.target.dataset.precio;
      const cantidad = event.target.dataset.cantidad;
      cargarDatosProducto(id, descripcion, precio, cantidad);
      var modificarModal = new bootstrap.Modal(document.getElementById('modificarModal'));
      modificarModal.show();
    });
  });
  
  document.querySelectorAll('.btn-eliminar').forEach(button => {
    button.addEventListener('click', (event) => {
      if (confirm('¿Está seguro de que desea eliminar este producto?')) {
        const id = event.target.dataset.id;
        window.location.href = `/eliminar_producto/${id}`;
        alert('Producto eliminado exitosamente');
      }
      return 
    });
  });

// lista de clientes var 6

document.addEventListener('DOMContentLoaded', function () {
    // Código para manejar el modal de modificar cliente
    var modificarClienteButtons = document.querySelectorAll('.btn-modificar-cliente');
    modificarClienteButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        var cedula_cliente = this.getAttribute('data-cedula_cliente');
        var nombre_cliente = this.getAttribute('data-nombre_cliente');
        var apellido_cliente = this.getAttribute('data-apellido_cliente');
        var telefono_cliente = this.getAttribute('data-telefono_cliente');
        var email_cliente = this.getAttribute('data-email_cliente');
        var contrasena_cliente = this.getAttribute('data-contrasena_cliente');

        document.getElementById('modificar_cliente_cedula_original').value = cedula_cliente;
        document.getElementById('modificar_cedula').value = cedula_cliente;
        document.getElementById('modificar_nombre').value = nombre_cliente;
        document.getElementById('modificar_apellido').value = apellido_cliente;
        document.getElementById('modificar_telefono').value = telefono_cliente;
        document.getElementById('modificar_email').value = email_cliente;

        var modificarClienteModal = new bootstrap.Modal(document.getElementById('modificarClienteModal'));
        modificarClienteModal.show();
      });
    });

    // Código para manejar la eliminación de clientes
    var eliminarClienteButtons = document.querySelectorAll('.btn-eliminar-cliente');
    eliminarClienteButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        var id = this.getAttribute('data-cedula_cliente');
        if (confirm('¿Estás seguro de que deseas eliminar este cliente?')) {
          window.location.href = '/eliminar_cliente/' + id;
        }
      });
    });
  });

  