

class ProvisionException(Exception):
    pass


class UnitError(ProvisionException):
    pass

class DataError(ProvisionException):
    pass



class ConnectionException(Exception):
    pass