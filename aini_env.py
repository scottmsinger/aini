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
    parser.add_option("--file", action="store", type="string", dest="s_file_name",default="AINI")
    parser.add_option("--sec", action="store", type="string", dest="s_sec_name",default="aini")
    parser.add_option("--expand", action="store", type="string", dest="s_expand",default="True")

    (options, args) = parser.parse_args()

    aini_files = []

    #
    #   gather up the #includes into a file list
    #   then append the local file and close it
    #
    file = open(options.s_file_name, 'r')
    for line in file:
        if("#include" in line):
            line = line.rstrip('\n')
            fields = line.split(" ")
            aini_files.append(fields[1])
    aini_files.append(options.s_file_name)
    file.close()

    #
    #   loop over the list of files to process and create
    #   a list of ConfigParser objects.
    #
    aini_ptr = []
    i_p = 0
    for name in aini_files:
        file = open(name, 'r')
        aini_ptr.append(configparser.RawConfigParser());
        aini_ptr[i_p].read_file(add_section_header(file, 'aini'), source=name)
        i_p = i_p + 1


    aini_sum = configparser.RawConfigParser();
    aini_sum.add_section("aini")


    for aini_dict in aini_ptr:
        aini_sum['aini'].update(aini_dict['aini'])

    if ("true" in options.s_expand.lower()) | ("1" in options.s_expand) :
        aini_sum._interpolation = configparser.ExtendedInterpolation()

    for s_var in aini_sum.options("aini"):
        print(s_var+"="+aini_sum.get( "aini", s_var))


if __name__ == "__main__":
    main()
