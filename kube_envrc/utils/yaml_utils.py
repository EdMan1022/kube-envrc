import yaml

from kube_envrc.utils.general_utils import EnvVarSecret, ManifestEnvironmentVariable

def load_manifest(manifest_path: str):
    with open(manifest_path, 'r') as manifest_fo:
        manifest_data = yaml.safe_load(manifest_fo)
    return manifest_data


def find_env_vars(manifest_data: dict) -> list[ManifestEnvironmentVariable]:
    containers = manifest_data['spec']['template']['spec']['containers']
    env_vars = []
    for container in containers:
        for env_var in container['env']:
            if 'value' in env_var.keys():
                env_vars.append(ManifestEnvironmentVariable(
                    name=env_var['name'],
                    value=env_var['value'],
                    secret=None
                ))
            else:
                env_vars.append(
                    ManifestEnvironmentVariable(
                        name=env_var['name'],
                        value=None,
                        secret=EnvVarSecret(
                            kube_secret=env_var['valueFrom']['secretKeyRef']['name'],
                            secret_key=env_var['valueFrom']['secretKeyRef']['key']
                        )
                    )
                )

    return env_vars


def secret_list(manifest_env_variables: list[ManifestEnvironmentVariable]):
    secret_set = set()
    for env_var in manifest_env_variables:
        if env_var.secret is not None:
            secret_set.add(env_var.secret.kube_secret)

    return list(secret_set)
