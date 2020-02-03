#Workspace.from_config()
import yaml

# Initialize a Workspace object 
from azureml.core import Workspace
from azureml.core.authentication import InteractiveLoginAuthentication


def load_configs():
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return(cfg)

def get_workspace(cfg):
    interactive_auth = InteractiveLoginAuthentication(tenant_id=cfg['tenant_id'])

    ws = Workspace(subscription_id=cfg['subscription_id'],
               resource_group=cfg['resource_group'],
               workspace_name=cfg['workspace_name'],
               auth=interactive_auth)

    return ws

# load configuraitons
cfg = load_configs()['azureml']

# may not need Docker Folder nw
from azureml.core.runconfig import AzureContainerRegistry, DockerEnvironment, EnvironmentDefinition, PythonEnvironment
registry = AzureContainerRegistry()
registry.address = cfg['address']
registry.username = cfg['username']
registry.password = cfg['password']

docker_config = DockerEnvironment()
docker_config.enabled = True
docker_config.base_image = 'nfl/base-gpu:0.2.1'
docker_config.base_image_registry = registry
docker_config.gpu_support = True

python_config = PythonEnvironment()
python_config.user_managed_dependencies = True
