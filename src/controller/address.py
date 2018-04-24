from src.model import AddressModel
from src.config import Settings
from src.validation import AddressValidation


class AddressController:

    def __init__(self):
        self.address_model = AddressModel()
        self.responseCode = Settings.error_codes()

    def hook(self, request):
        return request.Response(json=request.body)

    def get(self, request):
        user_input = request.query

        error, data = AddressValidation.is_valid(user_input, ['address', 'url_hook'])

        if not error:
            # self.redis.sadd(Settings.get("channel")['address']['default'], data['address'])
            result = self.address_model.store(data)
            if result:
                return request.success_response(
                    message="Successfully added address to watch",
                    status_code=201,
                    data={})
            return request.failed_response(
                status_code=400,
                code=20,
                message=self.responseCode['20'],
                error={})
        return request.failed_response(
            status_code=400,
            code=30,
            message=self.responseCode['30'],
            error=error)

    def delete(self, request):
        print('in delete')
        user_input = request.query

        error, data = AddressValidation.is_valid(user_input, ['address'])

        if not error:
            result = self.address_model.remove(data)
            if result:
                return request.success_response(
                    message="Successfully removed address from watch",
                    status_code=200,
                    data={})
            return request.failed_response(
                status_code=400,
                code=40,
                message=self.responseCode['40'],
                error={})
        return request.failed_response(
            status_code=400,
            code=30,
            message=self.responseCode['30'],
            error=error)
