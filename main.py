#!/usr/bin/python3

from optparse import OptionParser

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

if __name__ == "__main__":
    main()