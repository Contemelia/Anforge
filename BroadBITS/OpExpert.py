from base64 import b64decode
from hashlib import md5
from json import dumps, loads
from re import search
from requests import get, post
from urllib import parse, request





class OpExpert:
    
    def __init__(self, logPath, username, password, URL):
        
        self.opexpertUsername = username
        self.opexpertPassword = md5(password.encode('utf-8')).hexdigest()
        self.opexpertURL = URL
        self.logPath = logPath
    
    
    
    def initialLogin(self):
        data = {
            'user_auth': {
                'user_name': self.opexpertUsername, 
                'password': self.opexpertPassword
            }
        }
        self.opexpertSessionID = self.performRequest(['login', dumps(data)]).get('id')
    
    
    
    def performRequest(self, arguments, custom = None):
        
        # custom: any in [None, 'integration_login', 'integration_main']
        
        # This condition is for requests that apply on home
        if not custom:
            
            # arguments[0]: Method
            # arguments[1]: Data (In JSON format)
            
            payload = {
                'method': arguments[0], 
                'input_type': 'json', 
                'response_type': 'json', 
                'rest_data': arguments[1]
            }
            
            try:
                parameters = parse.urlencode(payload).encode('utf-8')
                response = request.urlopen(self.opexpertURL, parameters).read().strip()
                return loads(response.decode('utf-8'))
            except:
                return False
        
        
        # This condition is for requests associated with integrations
        elif custom in ['integration_login', 'integration_main']:
            
            # arguments[0]: API URL
            # arguments[1]: Parameters to pass as payload
            # arguments[2]: Header (can either be in base64 or JSON format)
            # arguments[3]: Response format
            # arguments[4]: SSL Verify [True/False]
            # arguments[5]: Main API [True/False]
            # arguments[6]: Login API [True/False]
            # arguments[7]: Custom API filter
            # arguments[8]: Data contents table
            # arguments[9]: Alias key
            # arguments[10]: Session ID
            # arguments[11]: Name of the integration
            
            payload = loads(arguments[1])
            if custom == 'integration_main':
                if arguments[10]:
                    payload['auth'] = str(arguments[9])
                else:
                    payload['auth'] = ''
            
            try:
                header = b64decode(arguments[2]).decode('utf-8')
                contentType = search(r'"(Content-Type:[^"]+)"', header).group(1)
                header = dict(header.split(":") for header in contentType.splitlines())
            except:
                header = loads(arguments[2].replace('\\/', '/'))[0]
                header = header.split(":")
                header = {header[0] : header[1]}
            
            try:
                if len(payload) > 1 or custom == 'integration_login':
                    response = post(arguments[0], json = payload, headers = header)
                    if response.status_code == 200:
                        return response.json().get('result') if custom == 'integration_login' else response.json()
                else:
                    response = get(arguments[0], headers = header)
                    if response.status_code == 200:
                        return response.json()
            except Exception as error:
                return False
    
    
    
    def getIntegrationList(self, arguments = ['', '', '', 0, [], {}, 1, False]):
        
        # arguments[0]: Name of the module
        # arguments[1]: Query ('' by default)
        # arguments[2]: Sort order ('' by default)
        # arguments[3]: Offset value (0 by default)
        # arguments[4]: Fields to select ([] by default)
        # arguments[5]: Link-name fields ({} by default)
        # arguments[6]: Maximum number of results to fetch (1 by default)
        # arguments[7]: Whether to include deleted record [True/False] (False by default)
        
        integrationsPayload = {
            'session': self.opexpertSessionID, 
            'module_name': arguments[0], 
            'query': arguments[1], 
            'order_by': arguments[2], 
            'offset': arguments[3], 
            'select_fields': arguments[4], 
            'link_name_to_fields_array': [arguments[5]],
            'max_results': arguments[6], 
            'deleted': arguments[7]
        }
        self.integrationList = self.performRequest(['get_entry_list', dumps(integrationsPayload)])
    
    
    
    def loginIntegration(self, integration):
        
        # integration: List that can have upto 3 API tasks
                
        if len(integration) in [2, 3]:
            
            # integration[0]: API URL
            # integration[1]: Parameters to pass as payload
            # integration[2]: Header (can either be in base64 or JSON format)
            # integration[3]: Response format
            # integration[4]: SSL Verify [True/False]
            # integration[5]: Main API [True/False]
            # integration[6]: Login API [True/False]
            # integration[7]: Custom API filter
            # integration[8]: Data contents table
            # integration[9]: Alias key
            # integration[10]: Name of the integration
            # integration[11]: Session ID
            
            try:
                for aPITask in integration:
                    if aPITask[6]:
                        sessionID = self.performRequest(aPITask, 'integration_login')
                    return sessionID if sessionID else None, integration[9]
            except Exception as error:
                pass
        
        else:
            return None, integration[9]
    
    
    
    def getDataIntegration(self, integration, sessionID):
        
        # integration[0]: API URL
        # integration[1]: Parameters to pass as payload
        # integration[2]: Header (can either be in base64 or JSON format)
        # integration[3]: Response format
        # integration[4]: SSL Verify [True/False]
        # integration[5]: Main API [True/False]
        # integration[6]: Login API [True/False]
        # integration[7]: Custom API filter
        # integration[8]: Data contents table
        # integration[9]: Alias key
        # integration[10]: Name of the integration
        
        try:
            for aPIList in integration:
                aPIList.append(sessionID)
                if aPIList[5]:
                    data = self.performRequest(aPIList, 'integration_main')
                    return data, aPIList[7], aPIList[8]
        except Exception as error:
            print(error)
            # print("getDataFromIntegration(): No input was given.")
        return None
