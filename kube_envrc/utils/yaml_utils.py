import yaml

def load_manifest(manifest_path: str):
    with open(manifest_path, 'r') as manifest_fo:
        manifest_data = yaml.safe_load(manifest_fo)

