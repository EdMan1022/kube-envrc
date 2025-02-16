from unittest import TestCase
from kube_envrc.utils import yaml_utils


class TestFindEnvVars(TestCase):

    def test_load_yaml(self):
        manifest = yaml_utils.load_manifest('example.yaml')
        assert manifest is not None

    def test_find_env_vars(self):
        test_manifest = {'apiVersion': 'apps/v1', 'kind': 'Deployment', 'metadata': {'name': 'userlookup-service', 'namespace': 'userlookup'}, 'spec': {'selector': {'matchLabels': {'app': 'userlookup-service'}}, 'replicas': 1, 'template': {'metadata': {'labels': {'app': 'userlookup-service'}}, 'spec': {'containers': [{'name': 'userlookup-service', 'image': 'satregistry.ehps.ncsu.edu/user-lookup-tool/user-lookup-service:main', 'imagePullPolicy': 'IfNotPresent', 'ports': [{'name': 'service-port', 'containerPort': 8000}], 'env': [{'name': 'JWT_SECRET', 'valueFrom': {'secretKeyRef': {'key': 'JWT_SECRET', 'name': 'userlookup-service-secrets'}}}, {'name': 'FEED_DB_URL', 'valueFrom': {'secretKeyRef': {'key': 'FEED_DB_URL', 'name': 'userlookup-service-secrets'}}}, {'name': 'CCURE_USERNAME', 'valueFrom': {'secretKeyRef': {'key': 'CCURE_USERNAME', 'name': 'userlookup-service-secrets'}}}, {'name': 'CCURE_PASSWORD', 'valueFrom': {'secretKeyRef': {'key': 'CCURE_PASSWORD', 'name': 'userlookup-service-secrets'}}}, {'name': 'SERVICE_ACCOUNT_TOKEN', 'valueFrom': {'secretKeyRef': {'key': 'SERVICE_ACCOUNT_TOKEN', 'name': 'userlookup-service-secrets'}}}, {'name': 'ELASTIC_USERNAME', 'valueFrom': {'secretKeyRef': {'key': 'ELASTIC_USERNAME', 'name': 'userlookup-service-secrets'}}}, {'name': 'ELASTIC_PASSWORD', 'valueFrom': {'secretKeyRef': {'key': 'ELASTIC_PASSWORD', 'name': 'userlookup-service-secrets'}}}, {'name': 'ELASTIC_CA_CERTS', 'valueFrom': {'secretKeyRef': {'key': 'ELASTIC_CA_CERTS', 'name': 'userlookup-service-secrets'}}}, {'name': 'ELASTIC_URL', 'value': 'https://vrb-elk-01.ehps.ncsu.edu:9200'}, {'name': 'ELASTIC_LOG_INDEX', 'value': 'user_lookup_logs_staging'}, {'name': 'PEOPLESOFT_PROXY_URL', 'value': 'https://peoplesoft.services.staging.ehps.ncsu.edu'}, {'name': 'CCURE_BASE_URL', 'value': 'https://c9k.dev.ehps.ncsu.edu'}, {'name': 'CCURE_CLIENT_NAME', 'value': 'NCSU - Security Portal - Integration'}, {'name': 'CCURE_CLIENT_VERSION', 'value': '2.9'}, {'name': 'CCURE_CLIENT_ID', 'value': 'd2a1f285-2d28-4147-8652-ba5ea211f1c1'}]}]}}}}
        env_vars = yaml_utils.find_env_vars(test_manifest)

        assert env_vars[0].name == 'JWT_SECRET'
        assert env_vars[0].secret is not None
        assert env_vars[0].value is None

        assert env_vars[-2].secret is None
        assert env_vars[-2].value == '2.9'

    def test_get_secret_list_empty(self):
        test_env_vars = [yaml_utils.ManifestEnvironmentVariable(name='test-1', secret=None, value='lol')]

        secrets_to_get = yaml_utils.secret_list(test_env_vars)
        assert secrets_to_get == []

    def test_get_secret_list(self):
        test_env_vars = [
            yaml_utils.ManifestEnvironmentVariable(
                name='test-1',
                secret=yaml_utils.EnvVarSecret(kube_secret='test-secrets', secret_key='1'),
                value=None)]

        secrets_to_get = yaml_utils.secret_list(test_env_vars)
        assert secrets_to_get == ['test-secrets']
