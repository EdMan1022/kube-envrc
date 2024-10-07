import base64

from kubernetes import config, client


def pull_secrets_from_kube_client(secrets_list: list[str], namespace: str):
    config.load_kube_config()
    api_client = client.ApiClient()
    v1_client = client.CoreV1Api(api_client)
    secret_result = v1_client.list_secret_for_all_namespaces()
    secret_return_data = {}
    namespace_secrets = [_ for _ in secret_result.items if _.metadata.namespace == namespace]
    for secret in namespace_secrets:
        secret_return_data[secret.metadata.name] = {

            key: base64.b64decode(value).decode()

            for key, value in secret.data.items()
        }

    return secret_return_data
