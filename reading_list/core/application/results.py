class AResult:
    STATUS = 'base'


class SuccessResult(AResult):
    STATUS = 'success'


class ErrorResult(AResult):
    STATUS = 'error'
