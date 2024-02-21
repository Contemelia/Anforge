from re import findall





class Interpreter:
    
    def __init__(self, text):
        
        self.inputText = text
        self.interpretedText = text
    
    
    
    def interpretToPython(self):
        
        newText = ''
        tabsToInclude = 0
        loopIndent = 0
        
        for line in self.interpretedText.splitlines():
            
            line = line.strip()
            line = line.replace('=', '==')
            includeColon = False
            
            # Removes tabs accordingly
            if '}' in line:
                tabsToInclude -= line.count('}')
                tabsToInclude -= loopIndent
                loopIndent = 0
            
            # Includes parameters if necessary and assigns it to a variable
            if ' AS ' in line:
                line = line.split(' AS ')
                if ' WITH ' in line[-1]:
                    text = line[-1].split(' WITH ')
                    newLine = text[0] + " = "
                    newLine += line[0].replace('()', '(' + ', '.join(text[-1].split(' ')) + ')') + "\n"
                    newLine += "\nif type(" + text[0] + ") in [list, tuple, dict]:"
                    newLine += "\n\t" + text[0] + "Original = " + text[0] + "[:]"
                else:
                    line = line[-1] + " = " + line[0] + "\n" + line[-1] + "Original = " + line[0]
                    newLine = line[-1] + " = " + line[0]
                    newLine += "\nif type(" + line[-1] + ") in [list, tuple, dict]:"
                    newLine += "\n\t" + line[-1] + "Original = " + line[-1] + "[:]"
                line = newLine
            
            # Refering to values within a record as a dictionary
            addedDictionaries = []
            pattern = r'\b(\w+)\[\'(\w+)\'\]'
            matches = findall(pattern, line)
            for match in matches:
                # You might wanna remove " and ('if' in line or 'elif' in line)"
                if match[0] not in addedDictionaries and ('IF' in line or 'ELIF' in line):
                    newText += '\t' * tabsToInclude + f"{match[0]}OriginalCopy = {match[0]}Original\n"
                    newText += '\t' * tabsToInclude + f"for {match[0]}Index, {match[0]} in enumerate({match[0]}OriginalCopy):\n"
                    tabsToInclude += 1
                    loopIndent += 1
                    # newText += '\t' * tabsToInclude + f"{match[0]}OriginalCopy[" + f"{match[0]}Index" + "].update(" + "key: None for key in " + f"{match[0]}OriginalCopy[" + f"{match[0]}Index" + "])\n" + "}"
                    newText += '\t' * tabsToInclude + f"for {match[0]}Key in {match[0]}:\n"
                    newText += '\t' * (tabsToInclude + 1) + f"{match[0]}[{match[0]}Key] = ''\n"
                    addedDictionaries.append(match[0])
            
            # Includeing a line in Python format
            newText += '\t' * tabsToInclude + line
            
            # Introducing a colon at the end of statements
            if '{' in line:
                tabsToInclude += line.count("{")
                includeColon = True
            if includeColon:
                newText += ':'
                
            newText += '\n'
        
        # Replaces a fex characters into Python-readable format
        newText = newText.replace(r'{', '')
        newText = newText.replace(r'}', '')
        newText = newText.replace(r' :', ':')
        newText = newText.replace(r' AND ', ' and ')
        newText = newText.replace(r' OR ', ' or ')
        newText = newText.replace(r' NOT ', ' not ')
        newText = newText.replace(r'ELIF', 'elif')
        newText = newText.replace(r'IF', 'if')
        newText = newText.replace(r'ELSE', 'else')
        self.interpretedText = newText






def executeText():
    
    text = """ACTION getHostList()
    CONDITION IF 'hosts' = 'Babtain' AND 'Severity' = 'Disaster' {
    ACTION sendReport(); ACTION sendEmail()
    }
    CONDITION IF ('hosts' = 'Zabbix' OR 'Severity' = 'Normal') AND 'id' = '123' {
    ACTION doNothing()
    }
    CONDITION IF 'hosts' = 'Zabbix' {
    CONDITION IF 'id' = '123' {
    ACTION getOtherList(); ACTION doNothing()
    }
    }"""
    text = """getHostList() AS ASpier
    IF 'hosts' = 'Babtain' AND 'Severity' = 'Disaster' {
    sendReport()
    sendEmail() AS potato
    }
    IF ('hosts' = 'Zabbix' OR 'Severity' = 'Normal') AND 'id' = '123' {
    doNothing()
    }
    IF 'hosts' = 'Zabbix' {
    IF 'id' = '123' {
    getOtherList()
    doNothing()
    }
    ELIF result['hosts'] = 'POT' {
        getIt() AS rev
        IF 'POT' > 'ANT' {
            beep_boop()
        }
        ELSE {
            nothing()
        }
    }
    }"""
    
    anObject = Interpreter(text)
    anObject.interpretToPython()
    print(anObject.interpretedText)



# executeText()
if __name__ == '__main__':
    
    try:
        executeText()
    
    except:
        pass