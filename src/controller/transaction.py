from src.model import TransactionModel
from src.config import Settings
from src.validation import TransactionValidation


class TransactionController:

    def __init__(self):
        self.txn_model = TransactionModel()
        self.responseCode = Settings.error_codes()

    def hook(self, request):
        return request.Response(json=request.body)

    """
        process transaction request
        @:return Json response
        @:argument Request
    """
    def get(self, request):
        user_input = request.query

        error, data = TransactionValidation.is_valid(user_input)

        if not error:
            result = self.txn_model.publish(data)
            print('result')
            print(result)
            if result:
                return request.success_response(
                    status_code=201,
                    data={})
            return request.failed_response(
                status_code=400,
                code=20,
                message=self.responseCode['20'],
                error={})

        return request.failed_response(
            code=30,
            message=self.responseCode['30'],
            status_code=400,
            error=data)




