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
    
    
    
    def performRequest(self, arguments, custom = None):
        
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
                response = request.urlopen(self.opexpertCRMURL, parameters).read().strip()
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
            # arguments[9]: Session ID (Provisional)
            # arguments[10]: Session ID
            
            ...