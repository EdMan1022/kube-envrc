class EnvVarSecret:

    def __init__(self, kube_secret, secret_key):
        self.kube_secret = kube_secret
        self.secret_key = secret_key


class ManifestEnvironmentVariable:

    def __init__(self, name, secret, value):
        self.name = name
        self.secret = secret
        self.value = value


def dump_to_envrc_file(envrc_vars: list[ManifestEnvironmentVariable], envrc_file_obj):
    
    for envrc_var in envrc_vars:
        envrc_file_obj.write(
            f'export {envrc_var.name}="{envrc_var.value}"\n'
        )
