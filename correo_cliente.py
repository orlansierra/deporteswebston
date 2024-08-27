import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, message, recipient_email):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "deporteswebston@gmail.com"
    password = "syvmtjdytgzeaerm"  # Reemplaza con tu contraseña de aplicación

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    # Try to log in to server and send email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Correo enviado exitosamente")
    except Exception as e:
        # Print any error messages to stdout
        print(f"Error al enviar el correo: {e}")
