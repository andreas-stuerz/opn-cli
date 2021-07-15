import click
import textwrap

@click.command()
def completion():
    """
    Output Instructions for shell completion
    """
    instructions = '''
        Instructions for shell completion:
        
        See: https://click.palletsprojects.com/en/latest/shell-completion/
        
        Zsh:
        echo '# shell completion for opn-cli' >> ~/.zshrc
        echo 'eval "$(_OPN_CLI_COMPLETE=zsh_source opn-cli)"' >> ~/.zshrc
        
        Bash:
        echo '# shell completion for opn-cli' >> ~/.zshrc
        echo 'eval "$(_OPN_CLI_COMPLETE=bash_source opn-cli)"' >> ~/.zshrc
        
    '''
    click.echo(textwrap.dedent(instructions))






