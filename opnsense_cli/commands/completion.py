import click
import textwrap


@click.command()
def completion():
    """
    Output instructions for shell completion
    """
    instructions = '''
Instructions for shell completion:

See: https://click.palletsprojects.com/en/latest/shell-completion/

Bash (invoked every time a shell is started):
echo '# shell completion for opn-cli' >> ~/.bashrc
echo 'eval "$(_OPN_CLI_COMPLETE=bash_source opn-cli)"' >> ~/.bashrc

Bash (current shell):
_OPN_CLI_COMPLETE=bash_source opn-cli > ~/.opn-cli/opn-cli-complete.bash
source ~/.opn-cli/opn-cli-complete.bash

Zsh (invoked every time a shell is started):
echo '# shell completion for opn-cli' >> ~/.zshrc
echo 'eval "$(_OPN_CLI_COMPLETE=zsh_source opn-cli)"' >> ~/.zshrc

Zsh (current shell):
_OPN_CLI_COMPLETE=zsh_source opn-cli >! ~/.opn-cli/opn-cli-complete.zsh
source ~/.opn-cli/opn-cli-complete.zsh
'''
    click.echo(textwrap.dedent(instructions))
