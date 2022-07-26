from uuid import uuid4
import requests
import os
import json

blip_commands_uri = 'https://msging.net/commands'
blip_commands_method_get = 'get'
blip_commands_method_delete = 'delete'
blip_postmaster_domain = 'postmaster@msging.net'

def get_new_guid():
    return uuid4().hex

def blip_commands_request(command_endpoint, command_method, bot_authorization_key, command_to = blip_postmaster_domain):
    body_request = {
        'id': get_new_guid(),
        'to': command_to,
        'method': command_method,
        'uri': command_endpoint
    }

    return requests.post(blip_commands_uri, headers={'Authorization': bot_authorization_key}, json=body_request)

def is_blip_response_ok(response):
    status_code = response.status_code
    return status_code == 200 and response.json()['status'] != 'failure'

def get_blip_response_resource(response):
    return response.json()['resource']

def get_all_bot_contacts(bot_authorization_key, take = 50, skip = 0, contacts = []):    
    bot_contacts_response = blip_commands_request(f'/contacts?$skip={skip}&$take={take}', blip_commands_method_get, bot_authorization_key)

    if is_blip_response_ok(bot_contacts_response):
        bot_contacts = get_blip_response_resource(bot_contacts_response)

        for item in bot_contacts['items']:
            contacts.append(item['identity'])

        if bot_contacts["total"] > (take + skip):
            return get_all_bot_contacts(take, skip + take, contacts)
        
    return contacts

def get_all_bot_user_variables(bot_authorization_key, contact_identity):
    user_variables_response = blip_commands_request(f'/contexts/{contact_identity}', blip_commands_method_get, bot_authorization_key)

    if is_blip_response_ok(user_variables_response):
        user_variables = get_blip_response_resource(user_variables_response)
        variables = []

        for variable in user_variables['items']:
            variables.append(variable)

        return variables
    
    return []

def delete_all_bot_user_variables(bot_authorization_key, contact_identity, user_variables):
    for variable in user_variables:
        user_variable_delete_response = blip_commands_request(f'/contexts/{contact_identity}/{variable}', blip_commands_method_delete, bot_authorization_key)

        if is_blip_response_ok(user_variable_delete_response):
            print(f"deleted '{variable}' -> {contact_identity}")
        else:
            print(f"FAILED to delete '{variable}' -> {contact_identity}")
def get_config_json():
    script_path = os.path.realpath(__file__)
        
    file_split = __file__.split('/')

    if len(file_split) == 1:
        file_split = __file__.split('\\')

    config_filepath = script_path.replace('src', '').replace('\\\\', '').replace('//', '').replace(file_split[-1], '') + '/configuration/config.json'

    file = open(file=config_filepath, mode='r')

    return json.load(file)


config = get_config_json()

for bot_authorization_key in config['bot']['authorizationKeys']:
    contacts_identity = []

    if "isClearAll" in config['user'] and config['user']['isClearAll'] == True:
        contacts_identity = get_all_bot_contacts(bot_authorization_key)
    else:
        contacts_identity = config['user']['userIds']

    for contact_identity in contacts_identity:
        print(f'run -> {contact_identity}')
        
        user_variables = get_all_bot_user_variables(bot_authorization_key, contact_identity)

        if len(user_variables) > 0:
            print(f'total variables to delete -> {len(user_variables)}')

            delete_all_bot_user_variables(bot_authorization_key, contact_identity, user_variables)