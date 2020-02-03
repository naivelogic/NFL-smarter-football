# may not need Docker Folder nw
from azureml.core.runconfig import AzureContainerRegistry, DockerEnvironment, EnvironmentDefinition, PythonEnvironment
registry = AzureContainerRegistry()
registry.address = 'skywalker61cafcd0.azurecr.io'
registry.username = 'skywalker61cafcd0'
registry.password = '1UT6Ndugwrk/j0JcFQKg8V5++f7Yl1nV'

docker_config = DockerEnvironment()
docker_config.enabled = True
docker_config.base_image = 'zerowaste/base-gpu:0.2.1'
docker_config.base_image_registry = registry
docker_config.gpu_support = True

python_config = PythonEnvironment()
python_config.user_managed_dependencies = True
