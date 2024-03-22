from abc import ABC, abstractmethod
from bs4.element import Tag
from string import Template
import textwrap


class ClickOptionCodeFragment(ABC):
    def __init__(self, tag: Tag):
        self._tag_content = tag
        self._name = tag.name
        self._template = self.TEMPLATE_CREATE
        self.__help = "ToDo"

    @property
    @abstractmethod
    def TEMPLATE_CREATE(self):
        """This property should be implemented."""

    def get_code_for_create(self):
        self._template = self.TEMPLATE_CREATE
        return self._render_template()

    @property
    @abstractmethod
    def TEMPLATE_UPDATE(self):
        """This property should be implemented."""

    def get_code_for_update(self):
        self._template = self.TEMPLATE_UPDATE
        return self._render_template()

    @abstractmethod
    def _render_template(self):
        """This method should be implemented."""

    @property
    def _template(self):
        return self.__template

    @_template.setter
    def _template(self, template):
        self.__template = Template(textwrap.dedent(template))

    @property
    def _name(self):
        return self.__name

    @_name.setter
    def _name(self, name):
        self.__name = name

    @property
    def _required(self):
        if self._tag_content.find(name="Required", text="Y"):
            return "required=True,"
        return "required=False,"

    @property
    def _default(self):
        if self._tag_content.find(name="default"):
            return self._tag_content.find(name="default").string
        return None

    @property
    def _multiple(self):
        if self._tag_content.find(name="Multiple", text="Y") or self._tag_content.find(name="multiple", text="Y"):
            return True
        return False

    @property
    def _help(self):
        return self.__help

    @_help.setter
    def help(self, help):
        self.__help = help


class ClickBoolean(ClickOptionCodeFragment):
    TEMPLATE_CREATE = """
    @click.option(
        '--${name}/--no-${name}',
        help=('${help}'),
        show_default=True,
        is_flag=True,
        callback=bool_as_string,
        default=${default},
        ${required}
    )
    """
    TEMPLATE_UPDATE = """
    @click.option(
        '--${name}/--no-${name}',
        help=('${help}'),
        show_default=True,
        is_flag=True,
        callback=bool_as_string,
        default=None
    )
    """

    @property
    def _default(self):
        default = super()._default
        if default:
            return bool(default)

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            required=self._required,
            default=self._default,
            help=self._help,
        ).strip()


class ClickChoice(ClickOptionCodeFragment):
    TEMPLATE_CREATE = """
    @click.option(
        '--${name}',
        help=('${help}'),
        type=click.Choice(${choices}),
        multiple=${multiple},
        callback=tuple_to_csv,
        show_default=True,
        default=${default},
        ${required}
    )
    """
    TEMPLATE_UPDATE = """
    @click.option(
        '--${name}',
        help=('${help}'),
        type=click.Choice(${choices}),
        multiple=${multiple},
        callback=tuple_to_csv,
        show_default=True,
        default=None
    )
    """

    @property
    def _default(self):
        default_for_multiple = self._get_default_for_multiple()

        if default_for_multiple:
            return default_for_multiple

        if super()._default:
            return f"'{super()._default}'"
        else:
            return super()._default

    def _get_default_for_multiple(self):
        if self._multiple:
            if super()._default:
                return super()._default.split(",")
            else:
                return []
        return None

    @property
    def _choices(self):
        options = self._tag_content.find("OptionValues").findChildren(recursive=False)
        choices = [option.name for option in options]

        if "False" in self._required:
            choices.insert(0, "")

        return repr(choices)

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            choices=self._choices,
            multiple=self._multiple,
            required=self._required,
            default=self._default,
            help=self._help,
        ).strip()


class ClickInteger(ClickOptionCodeFragment):
    TEMPLATE_CREATE = """
    @click.option(
        '--${name}',
        help=('${help}'),
        show_default=True,
        type=INT_OR_EMPTY,
        callback=int_as_string,
        default=${default},
        ${required}
    )
    """
    TEMPLATE_UPDATE = """
    @click.option(
        '--${name}',
        help=('${help}'),
        show_default=True,
        type=INT_OR_EMPTY,
        callback=int_as_string,
        default=None
    )
    """

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            required=self._required,
            default=self._default,
            help=self._help,
        ).strip()


class ClickText(ClickOptionCodeFragment):
    TEMPLATE_CREATE = """
    @click.option(
        '--${name}',
        help=('${help}'),
        show_default=True,
        default=${default},
        ${required}
    )
    """
    TEMPLATE_UPDATE = """
    @click.option(
        '--${name}',
        help=('${help}'),
        show_default=True,
        default=None
    )
    """

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            required=self._required,
            default=f"'{self._default}'" if self._default else self._default,
            help=self._help,
        ).strip()


class ClickTextLinkedItem(ClickOptionCodeFragment):
    TEMPLATE_CREATE = """
    @click.option(
        '--${name}',
        help=('${help}'),
        callback=resolve_linked_names_to_uuids,
        type=CSV,
        show_default=True,
        default=${default},
        ${required}
    )
    """
    TEMPLATE_UPDATE = """
    @click.option(
        '--${name}',
        help=('${help}'),
        callback=resolve_linked_names_to_uuids,
        type=CSV,
        show_default=True,
        default=None
    )
    """

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            required=self._required,
            default=f"'{self._default}'" if self._default else self._default,
            help=self._help,
        ).strip()
