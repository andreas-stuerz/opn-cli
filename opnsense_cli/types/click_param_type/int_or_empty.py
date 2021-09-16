import click


class IntOrEmptyClickParamType(click.ParamType):
    name = 'int_or_empty'

    def convert(self, value, param, ctx):
        if value == '':
            return value
        try:
            return int(value)
        except ValueError:
            self.fail('%s is not a valid integer' % value, param, ctx)


INT_OR_EMPTY = IntOrEmptyClickParamType()
