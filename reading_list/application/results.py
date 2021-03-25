class BaseResult:
    STATUS = 'base'


class SuccessResult(BaseResult):
    STATUS = 'success'


class ErrorResult(BaseResult):
    STATUS = 'error'
