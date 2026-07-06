import time


class RequestLogMiddleware:
    """
    Middleware personalizado para registrar información básica
    de cada petición HTTP realizada al sistema.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Momento en que inicia la petición
        start_time = time.time()

        # Procesa la petición
        response = self.get_response(request)

        # Tiempo total de ejecución
        duration = round((time.time() - start_time) * 1000, 2)

        # Información registrada
        print(
            f"[REQUEST] "
            f"{request.method} "
            f"{request.path} | "
            f"Status: {response.status_code} | "
            f"Tiempo: {duration} ms"
        )

        return response