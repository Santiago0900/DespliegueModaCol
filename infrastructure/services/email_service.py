from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings


# infrastructure/services/email_service.py

class EmailService:
    def enviar_recuperacion_password(self, destino: str, nombre: str, enlace: str):
        subject = "Restablecer tu contraseña - Modacol"

        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e1e1e1; border-radius: 10px; overflow: hidden;">
            <div style="background-color: #2d3748; padding: 20px; text-align: center;">
                <h2 style="color: white; margin: 0;">Modacol</h2>
            </div>
            <div style="padding: 30px;">
                <h3>Hola, {nombre}</h3>
                <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta. Si no hiciste esta solicitud, puedes ignorar este correo.</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{enlace}" style="background-color: #667eea; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        Restablecer Contraseña
                    </a>
                </div>
                <p style="color: #666; font-size: 12px;">Si tienes problemas con el botón, copia y pasa este enlace en tu navegador:</p>
                <p style="color: #667eea; font-size: 12px;">{enlace}</p>
            </div>
        </div>
        """

        email = EmailMultiAlternatives(
            subject,
            "Restablece tu contraseña en: " + enlace,
            settings.DEFAULT_FROM_EMAIL,
            [destino],
            )
        email.attach_alternative(html_content, "text/html")
        email.send()