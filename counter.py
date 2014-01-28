class NumberGenerator:
    def __init__(self, init=1, step=1):
        self._value = init
        self._step = step

    def next(self):
        value = self._value
        self._value += self._step
        return value

    def __call__(self):
        return self.next()
