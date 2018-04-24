from .interface import ValidationContract


class AddressValidation(ValidationContract):

    @staticmethod
    def is_valid(user_input, fields):
        data = {}
        error = {}

        if "address" in fields:
            if "address" in user_input:
                data['address'] = user_input['address']
            else:
                error['address'] = 'Please provide a valid address'

        if "url_hook" in fields:
            if "url_hook" in user_input:
                if "http://" in user_input['url_hook'] or "https://" in user_input['url_hook']:
                    data['hook'] = user_input['url_hook']
                else:
                    error['hook'] = 'Please provide a hook url that starts with https or http'
            else:
                error['hook'] = 'Please provide a hook url'

        return error, data

