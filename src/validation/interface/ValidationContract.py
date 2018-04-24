import abc

class ValidationContract(object):
    @staticmethod
    def is_valid(user_input, **kwargs):
        pass

