from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# infrastructure/services/user_email_service.py

def enviar_correo_bienvenida_html(nombre, correo, rol, link):
    subject = "Bienvenido al equipo de Modacol"

    # Versión en texto plano para correos que no soportan HTML
    text_content = f"Hola {nombre}, bienvenido a Modacol. Crea tu cuenta aquí: {link}"

    html_content = f"""
    <div style="background-color: #f4f7f6; padding: 50px 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px; letter-spacing: 2px;">MODACOL</h1>
            </div>
            
            <div style="padding: 40px; line-height: 1.6; color: #333333;">
                <h2 style="color: #2d3748; margin-bottom: 20px;">¡Bienvenido, {nombre}!</h2>
                <p>Nos complace darte la bienvenida a nuestra plataforma de gestión. Se ha creado una cuenta para ti con el siguiente perfil:</p>
                
                <div style="background-color: #edf2f7; padding: 15px; border-radius: 6px; margin: 20px 0; text-align: center;">
                    <strong style="color: #4a5568; text-transform: uppercase; font-size: 14px;">Rol Asignado:</strong><br>
                    <span style="font-size: 18px; color: #667eea; font-weight: bold;">{rol}</span>
                </div>
                
                <p>Para comenzar a utilizar el sistema, es necesario que establezcas tu contraseña de acceso personal haciendo clic en el siguiente botón:</p>
                
                <div style="text-align: center; margin: 35px 0;">
                    <a href="{link}" style="background-color: #667eea; color: #ffffff; padding: 15px 35px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);">
                        Configurar mi Contraseña
                    </a>
                </div>
                
                <p style="font-size: 13px; color: #718096; text-align: center;">
                    Este enlace de seguridad es de un solo uso y expirará en 1 hora.
                </p>
            </div>
            
            <div style="background-color: #f8fafc; padding: 20px; text-align: center; border-top: 1px solid #e2e8f0;">
                <p style="margin: 0; font-size: 12px; color: #a0aec0;">&copy; 2026 Modacol - Software de Gestión. Todos los derechos reservados.</p>
            </div>
        </div>
    </div>
    """

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [correo],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()