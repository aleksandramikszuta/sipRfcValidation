#!/usr/bin/python3

from optparse import OptionParser
import re

def parseFile(fileName):
    result = {}
    input = open(fileName, "r").readlines()
    result["method"] = input[0].split(" ")[0]
    result["request-uri"] = input[0].split(" ")[1]
    for line in input[1:]:
        if line.find(":") != -1:
            result[line.split(":")[0].lower()] = line.split(": ")[1].strip()
        else:
            result["body"] = line.strip()
    return result

def printFile(parsedFile):
    result = """
The given SIP message is a request with:
request-uri: """
    result += parsedFile["to"]
    excluded_fields = ["to", "body", "method"]
    result += """
method: """
    result += parsedFile["method"]
    result += """
headers:"""
    for (key, value) in parsedFile.items():
        if key in excluded_fields:
            continue
        result += """
  """ + key + ": " + value
    result += """
and body: """ + parsedFile["body"]
    print(result)

def printHeaderExists(header, parsedFile):
    if header in parsedFile:
        print("Header " + header + " is present with value: " + parsedFile[header])
    else:
        print("Header " + header + " is not present in the file")

def validateMandatoryFields(parsedFile):
    result = ""
    mandatoryFields = ["to", "from", "cseq", "call-id", "max-forwards", "via"]
    for field in mandatoryFields:
        if field not in parsedFile:
            result += "Error: mandatory field as required by RFC section 8.1.1 is missing: " + field + "\n"
    return result

def validateRequestUri(parsedFile):
    if (parsedFile["method"] == "REGISTER"):
        return ""
    if (parsedFile["to"].find("<") == -1):
        return "" #pass-through for SIP format error that will be caught in a separate function
    if (parsedFile["request-uri"] == parsedFile["to"].split("<")[1][:-1]):
        return ""
    else:
        return "Error: request-uri does not match the to field despite the method not being REGISTER, as required by RFC section 8.1.1.1\n"
    
def validateToField(parsedFile):
    to_field_pattern = r'^(?:[^<]*\s*)?<sip:[a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+>(;tag=[a-zA-Z0-9-]+)?$'
    if re.match(to_field_pattern, parsedFile["to"]):
        return ""
    return "Error: to field is not a valid SIP value as required by RFC section 8.1.1.2\n"

def validateFromField(parsedFile):
    if parsedFile["from"].find(";tag=") != -1:
        return ""
    return "Error: from field does not contain required tag parameter as required by RFC section 8.1.1.3\n"

def validate(parsedFile):
    result = validateRequestUri(parsedFile) + validateMandatoryFields(parsedFile) + validateToField(parsedFile) + validateFromField(parsedFile)
    if result == "":
        print("The request has been verified and no issues were found.")
    else:
        print("The verification of the request failed due to the following reason(s):")
        print(result)


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", help="File to process")
    parser.add_option("-p", "--print", dest="print", action="store_true", default=False,
                    help="Print file contents (WIP)")
    parser.add_option("-e", "--exists",
                    action="store", dest="headerExists",
                    help="Check if given header exists in the file (WIP)")
    parser.add_option("-v", "--validate", dest="validate", action="store_true", default=False,
                       help="Validate RFC3261 conformity (WIP)")

    (options, args) = parser.parse_args()

    if (options.file is None):
        parser.print_help()
        exit()
    
    parsedFile = parseFile(options.file)

    if(options.print):
        printFile(parsedFile)
    
    if(options.headerExists is not None):
        printHeaderExists(options.headerExists, parsedFile)
    
    if(options.validate):
        validate(parsedFile)

if __name__ == "__main__":
    main()