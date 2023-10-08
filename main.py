#!/usr/bin/python3

from optparse import OptionParser

def parseFile(fileName):
    result = {}
    input = open(fileName, "r").readlines()
    result["method"] = input[0].split(" ")[0]
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

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", help="File to process")
    parser.add_option("-p", "--print", dest="print", action="store_true", default=False,
                    help="Print file contents (WIP)")
    parser.add_option("-e", "--exists",
                    action="store", dest="headerExists",
                    help="Check if given header exists in the file (WIP)")
    parser.add_option("-v", "--validate", action="store_true", default=False,
                       help="Validate RFC3261 conformity (WIP)")

    (options, args) = parser.parse_args()

    if (options.file is None):
        parser.print_help()
        exit()
    
    parsedFile = parseFile(options.file)

    if(options.print):
        printFile(parsedFile)

if __name__ == "__main__":
    main()