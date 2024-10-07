import click

from kube_envrc.utils import yaml_utils, kubectl_utils, general_utils

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
    manifest_yaml = yaml_utils.load_manifest(kube_config)
    namespace = manifest_yaml['metadata']['namespace']

    # find all environment variables loaded from manifest,
    # append them to a dictionary to be filled out
    env_vars = yaml_utils.find_env_vars(manifest_yaml)
    print(env_vars)

    # figure out all secrets to be pulled from the namespace
    secrets_to_get = yaml_utils.secret_list(env_vars)
    print(secrets_to_get)

    # pull secrets from kubernetes
    secret_map = kubectl_utils.pull_secrets_from_kube_client(secrets_to_get, namespace=namespace)

    # fill out remaining values from secrets
    for env_var in env_vars:
        if env_var.secret:
            env_var.value = secret_map[env_var.secret.kube_secret][env_var.secret.secret_key]

    with open(envrc, 'w') as envrc_fo:
        general_utils.dump_to_envrc_file(env_vars, envrc_fo)

    click.echo("Finished")

