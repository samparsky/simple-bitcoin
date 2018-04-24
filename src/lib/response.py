"""
    Request library
    To process request
"""


class ApiResponse:
    """
    Success response
    """
    @staticmethod
    def success(response):
        def decorated(status_code=200, message="success", data={}):
            payload = {
                "status": True,
                "message": message,
                "data": data
            }
            return response(code=status_code, json=payload)
        return decorated

    @staticmethod
    def failed(response):
        """
        Failed response
        """
        def decorated(status_code=400, code=None, message="failed", error={}):
            payload = {
                "status": False,
                "code": code,
                "message": message,
                "error": error
            }
            return response(code=status_code, json=payload)
        return decorated
