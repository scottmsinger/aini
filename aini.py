
import configparser

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


    def __init__(self):
        self.s_file_name = "./AINI"
        self.s_section = "aini"
        self.aini_sum = configparser.RawConfigParser();
        self.aini_sum .optionxform = str

    #
    #   a function to create a aini section so that it doesn't need to be explicitly
    #   given. This mimics the old ani  structure in which there was simply an
    #   implicit section
    #
    def add_section_header(self, properties_file, header_name):
        # configparser.ConfigParser requires at least one section header in a properties file.
        # Our properties file doesn't have one, so add a header to it on the fly.
        yield '[{}]\n'.format(header_name)
        for line in properties_file:
            yield line

    #
    #   read the file and trace the includes
    #   build up an array of configparser objects which the merge via update()
    #   into the main aini of this module
    #
    def read(self):
        self.read_file(self.s_file_name, self.s_section)


    def read_file(self, s_in_file, s_in_section):

        self.s_file_name = s_in_file
        self.s_section = s_in_section

        aini_files = []
        #print(s_file_name)
        #
        #   gather up the #includes into a file list
        #   then append the local file and close it
        #
        file = open(self.s_file_name, 'r')

        for line in file:
            if("#include" in line):
                line = line.rstrip('\n')
                fields = line.split(" ")
                aini_files.append(fields[1])

        aini_files.append(self.s_file_name)
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
            aini_ptr[i_p].optionxform = str
            aini_ptr[i_p].read_file(self.add_section_header(file, self.s_section), source=name)
            i_p = i_p + 1


        #self.aini_sum = configparser.RawConfigParser();
        self.aini_sum.add_section(self.s_section)


        for aini_dict in aini_ptr:
            self.aini_sum[self.s_section].update(aini_dict[self.s_section])

        #if ("true" in options.s_expand.lower()) | ("1" in options.s_expand) :
        self.aini_sum._interpolation = configparser.ExtendedInterpolation()

        #for s_var in aini_sum.options("aini"):
        #    print(s_var+"="+aini_sum.get( "aini", s_var))

    def print_all(self):
        for s_var in self.aini_sum.options(self.s_section):
            print(s_var+"="+self.aini_sum.get( self.s_section, s_var))



#
#   END
#
