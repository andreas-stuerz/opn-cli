import click


class CsvParamType(click.types.StringParamType):
    name = "csv"

    def __repr__(self) -> str:
        return "CSV"


CSV = CsvParamType()
