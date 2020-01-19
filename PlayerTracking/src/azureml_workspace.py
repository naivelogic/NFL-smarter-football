
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

if __name__ == '__main__':
    
    # load configuraitons
    cfg = load_configs()['azureml']
    
    # init workspace from config parameters
    ws = get_workspace(cfg)
    
    # Get the workspace and write a workspace configuration file
    try:
        ws = Workspace(subscription_id = subscription_id, 
                       resource_group = resource_group, 
                       workspace_name = workspace_name)
        
        ws.write_config()
        print("Write Workspace configuration file succeeded.")
    except:
        print("Fail to write Workspace configuration file.")