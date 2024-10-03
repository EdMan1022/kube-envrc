import click

@click.group()
def cli():
    pass


@cli.command()
@click.argument('kube_config')
@click.option('--envrc', default='.envrc', help="Path to write envrc file to")
def update_envrc(kube_config, envrc):
    """Update local envrc file with secrets from current kube context using kube config file

    Parses kubernetes manifest located at kube_config argument,
    finds all of the referenced secrets,
    pulls them and parses them locally,
    and then puts those secrets as environment variables in a local .envrc file
    """

    # parse deployment yaml

    # find all environment variables loaded from secrets,
    # append them to a dictionary to be filled out

    # figure out all secrets to be pulled from the namespace

    # pull secrets from kubernetes

    click.echo("Finished")

