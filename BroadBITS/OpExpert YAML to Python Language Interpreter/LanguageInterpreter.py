# zabbixIntegration = getIntegrationWithData('5f38872e-08a5-22dd-720b-65c8c5084358')
# zabbixIntegrationOriginal = zabbixIntegration

# for zabbixIntegration in zabbixIntegrationOriginal:
#     if zabbixIntegration['Severity'] == 'Disaster':
#         emailID = moduleCall('Contacts', '22dd-720b-65c8c5084358', 'email_field')
#         sendEmail(emailID)





from yaml import safe_load as loadYAML





class YAMLLanguageInterpreter():
    
    def __init__(self, YAMLPayload):
        
        self.originalPayload = loadYAML(YAMLPayload)
        self.interpretedText = ''
        self.recordIterated = []
        
    
    
    def __processActions(self, payload):
        print("An action")
    
    
    
    def __processCodeSnippets(self, payload):
        print("A function")
    
    
    
    def __processConditions(self, payload):
        print("A condition")
        return ""
    
    
    
    def __processIntegrations(self, payload):
        
        interpretedText = ''
        interpretedText += payload.get('alias')
        interpretedText += " = getIntegrationWithID("
        interpretedText += ', '.join(payload.get('parameters'))
        interpretedText += ')'
        
        return interpretedText
    
        
        
    def __processModules(self, payload):
        print("A module")
    
    
    
    def processPayload(self):
        
        processes = {
            'action': self.__processActions, 
            'condition': self.__processConditions, 
            'function': self.__processCodeSnippets, 
            'integration': self.__processIntegrations, 
            'module': self.__processModules
        }
        
        for process in self.originalPayload:
            self.recordIterated = []
            action = processes[process['type']]
            result = action(process)
            self.interpretedText += result





def initialize():
    
    with open('languageSample.yaml') as stream:
        anObject = YAMLLanguageInterpreter(stream)
        stream.close()
        
    
    anObject.processPayload()
    print(anObject.interpretedText)





if __name__ == '__main__':
    
    try:
        initialize()
        
    except Exception as error:
        print(error)