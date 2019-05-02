class BaseResult:
    STATUS = 'base'

    def __init__(self, *args, **kwargs):
        self.failed = False
        self.args = list(args)
        self.kwargs = dict(kwargs)

    def _get_meta(self):
        return {
            'args': self.args,
            'kwargs': self.kwargs
        }

    def __dict__(self):
        return {
            'status': self.STATUS,
            'failed': self.failed,
            'meta': self._get_meta()
        }


class SuccessResult(BaseResult):
    STATUS = 'success'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed = False


class ErrorResult(BaseResult):
    STATUS = 'error'

    def __init__(self, error, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed = True
        self.error = error

    def _get_meta(self):
        super_meta = super()._get_meta()
        super_meta.update({'error_type': type(self.error)})
        super_meta.update({'error_message': str(self.error)})
        return super_meta
