class PybelugaxlException(Exception):
    """Base exception for Pybelugaxl."""
    pass

class InvalidICAOCodeError(PybelugaxlException):
    """Invalid ICAO code provided."""
    pass

class InvalidStatusError(PybelugaxlException):
    """Invalid status is provided."""
    pass

class InvalidGeoError(PybelugaxlException):
    """Invalid geographic bounds or zone name are provided."""
    pass

class InvalidRegistrationError(PybelugaxlException):
    """Provided registration is not a valid Beluga XL aircraft or the registration format is incorrect."""
    pass