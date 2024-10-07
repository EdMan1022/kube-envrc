from unittest import TestCase

from kube_envrc.utils import kubectl_utils


class TestKubeUtils(TestCase):

    def test_load_secret(self):
        secret_list = ['ads-secrets']
        namespace_secrets = kubectl_utils.pull_secrets_from_kube_client(secret_list, 'asset-data-service')
        pass

