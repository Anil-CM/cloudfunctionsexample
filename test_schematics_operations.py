from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_schematics.schematics_v1 import SchematicsV1
import json
import copy



def func(api_key, workspace_id, count):
    authenticator = IAMAuthenticator(api_key)
    schematics_service = SchematicsV1(authenticator = authenticator)
    schematics_service.set_service_url('https://schematics.cloud.ibm.com')
    data = schematics_service.get_workspace(workspace_id)
    if data.get_status_code() in [200, 202, 201]:
        d = data.get_result()
        temp_data = d['template_data']
        t_data = copy.deepcopy(temp_data)
        t_data[0]['variablestore']=[]
        for variable in temp_data[0]['variablestore']:
            if variable['name'] == 'instance_count':
                variable['value'] += count
            t_data[0]['variablestore'].append(variable)    
        print(schematics_service.update_workspace(w_id=workspace_id, template_data=t_data))
        return d

def main(args):

    count = 0
    api_key = ""
    ws = ""
    if 'count' in args:
        count = args['count']
    if 'apikey' in args:
        api_key = args['apikey']
    if 'workspace_id' in args:
        ws = args['workspace_id']
    
    return func(api_key, ws, int(count))
    
    
