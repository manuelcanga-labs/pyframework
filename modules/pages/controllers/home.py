from pyframework.http_foundation.responses import Response


class Home:
    def get(self, request):
        return Response("Hola mundo")