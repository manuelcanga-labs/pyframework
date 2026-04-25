from pyframework.responses import Response


class Home:
    def get(self, environ):
        return Response("Hola mundo")