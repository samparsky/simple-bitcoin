from src.lib import ApiResponse
from src.routes import app
from japronto import RouteNotFoundException


def success_response(request):
    return ApiResponse.success(request.Response)


def failed_response(request):
    return ApiResponse.failed(request.Response)


def error_handler(request, exception):
    return request.Response(code=404, json={"message": "invalid route"})

app.extend_request(success_response, property=True)
app.extend_request(failed_response, property=True)
app.add_error_handler(RouteNotFoundException, error_handler)
