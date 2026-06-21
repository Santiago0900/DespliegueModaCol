from django.core.signing import TimestampSigner

signer = TimestampSigner()


def generar_token_usuario(usuario_id):
    return signer.sign(usuario_id)


def validar_token_usuario(token, max_age=3600):
    try:
        usuario_id = signer.unsign(token, max_age=max_age)
        return int(usuario_id)
    except Exception:
        return None