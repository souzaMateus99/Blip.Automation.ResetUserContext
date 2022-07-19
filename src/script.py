from uuid import uuid4
import requests

blip_commands_uri = 'https://msging.net/commands'
blip_commands_token = ''
blip_commands_method_get = 'get'
blip_commands_method_delete = 'delete'
blip_postmaster_domain = 'postmaster@msging.net'

def get_new_guid():
    return uuid4().hex

def blip_commands_request(command_endpoint, command_method, command_to = blip_postmaster_domain):
    # print('blip_commands_request')
    
    body_request = {
        'id': get_new_guid(),
        'to': command_to,
        'method': command_method,
        'uri': command_endpoint
    }

    # print(body_request)

    return requests.post(blip_commands_uri, headers={'Authorization': blip_commands_token}, json=body_request)

def is_blip_response_ok(response):
    status_code = response.status_code
    return status_code == 200 and response.json()['status'] != 'failure'

def get_blip_response_resource(response):
    return response.json()['resource']

def get_all_bot_contacts():
    bot_contacts_response = blip_commands_request('/contacts?$skip=0&$take=50', blip_commands_method_get)

    if is_blip_response_ok(bot_contacts_response):
        bot_contacts = get_blip_response_resource(bot_contacts_response)
        contacts = []

        for item in bot_contacts['items']:
            contacts.append(item['identity'])
        
        return contacts
    
    return []

def get_all_bot_user_variables(contact_identity):
    user_variables_response = blip_commands_request(f'/contexts/{contact_identity}', blip_commands_method_get)

    print(user_variables_response.status_code)

    if is_blip_response_ok(user_variables_response):
        user_variables = get_blip_response_resource(user_variables_response)
        variables = []

        for variable in user_variables['items']:
            variables.append(variable)

        return variables
    
    return []

def delete_all_bot_user_variables(contact_identity, user_variables):
    for variable in user_variables:
        user_variable_delete_response = blip_commands_request(f'/contexts/{contact_identity}/{variable}', blip_commands_method_delete)

        if is_blip_response_ok(user_variable_delete_response):
            print(f"deleted '{variable}' -> {contact_identity}")
        else:
            print(f"failed to delete '{variable}' -> {contact_identity}")

contacts_identity = get_all_bot_contacts()

for contact_identity in contacts_identity:
    print(f'run -> {contact_identity}')
    
    user_variables = get_all_bot_user_variables(contact_identity)

    if len(user_variables) > 0:
        print(f'total variables to delete -> {len(user_variables)}')

        delete_all_bot_user_variables(contact_identity, user_variables)