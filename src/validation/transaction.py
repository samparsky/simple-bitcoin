from .interface import ValidationContract


class TransactionValidation(ValidationContract):
    @staticmethod
    def is_valid(user_input):
        error = {}
        data = {}

        if "target" in user_input:
            try:
                data['target'] = int(user_input['target'])
            except Exception as e:
                error['target'] = 'Please provide a valid integer target'

        if "transaction_id" in user_input:
            data['transaction_id'] = user_input['transaction_id']
        else:
            error['transaction_id'] = 'Please provide a transaction id'

        if "url_hook" in user_input:
            if "http://" in user_input['url_hook'] or "https://" in user_input['url_hook']:
                data['hook'] = user_input['url_hook']
            else:
                error['hook'] = 'Please provide a hook url that starts with https or http'
        else:
            error['hook'] = 'Please provide a hook url'

        if not error:
            return False, data
        return True, error


