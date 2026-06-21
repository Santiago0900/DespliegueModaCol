from django.shortcuts import redirect

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        rutas_publicas = [
            "/login",
            "/logout",
            "/forgot-password",
        ]

        if (
                request.session.get("usuario_id") or
                path.startswith("/static/") or
                path.startswith("/reset-password") or
                path.startswith("/usuarios/set-password/") or
                path in rutas_publicas
        ):
            return self.get_response(request)

        return redirect("login")