

class Utils:

    def __init__(self):
        pass

    @staticmethod
    def to_int(var):
        try:
            return int(var)
        except ValueError:
            return None
        except TypeError:
            return None