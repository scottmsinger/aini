#!/usr/bin/env python

import configparser
from optparse import OptionParser

#
#   aini
#   a class to encapsulate the aini wrapping of ini files for the purposes
#   abstracting location from project directories, processes, etc
#
#   It's a wrapping of ConfigParser that reads the .ini file, puts it in a
#   buffer. Walks up the '#include' directives doing each of those in turn,
#   Attaching a [aini] section to the head of each. Each is then handed to
#   ConfigParser, dictionaries are made, and these are merged down into a
#   a single dictionary.
#

class aini():

    s_ini_file = ""

    def __init__(self):
        self.s_ini_file = "./aini"

    


def add_section_header(properties_file, header_name):
    # configparser.ConfigParser requires at least one section header in a properties file.
    # Our properties file doesn't have one, so add a header to it on the fly.
    yield '[{}]\n'.format(header_name)
    for line in properties_file:
        yield line

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("--file", action="store", type="string", dest="s_file_name")
    parser.add_option("--var", action="store", type="string", dest="s_var_name")
    parser.add_option("--sec", action="store", type="string", dest="s_sec_name",default="aini")

    (options, args) = parser.parse_args()

    aini_my = configparser.SafeConfigParser();
    aini_my._interpolation = configparser.ExtendedInterpolation()

    print(options.s_file_name)
    file = open(options.s_file_name, 'r')
    aini_my.read_file(add_section_header(file, 'aini'), source=options.s_file_name)

    print(aini_my.get( options.s_sec_name, options.s_var_name))

if __name__ == "__main__":
    main()
