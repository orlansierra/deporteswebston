// Ejemplo usando fetch para enviar la solicitud al backend
fetch('/compra_finalizada', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        email_cliente: `${email_cliente}`  // Aquí el correo electrónico del cliente
    })
})
.then(response => response.json())
.then(data => {
    console.log('Respuesta del servidor:', data);
})
.catch(error => {
    console.error('Error:', error);
});