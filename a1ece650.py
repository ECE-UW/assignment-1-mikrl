import sys
import re
import pdb  # debug


class Graph:

    streets_ = {}
    edges_ = {}
    vertices_ = {}

    def AddStreet(self, street_name, vertices):
        try:
            if street_name in self.streets_.keys():  # if street exists, do not add
                sys.stderr.write(error_codes[610]+'\n')
            else:
                self.streets_.update({street_name: vertices})
            print("Add street function")
        except:
            sys.stderr.write(error_codes[600]+'/n')

    def ChangeStreet(self, street_name, vertices):
        try:
            if street_name in self.streets_.keys():  # check if street actually exists
                self.streets_.update({street_name: vertices})
            else:
                sys.stderr.write(error_codes[620]+'\n')
            print("Change street function")
        except:
            sys.stderr.write(error_codes[700]+'\n')

    def RemoveStreet(self, street_name):
        try:
            if street_name in self.streets_.keys():
                self.streets_.pop(street_name, None)
            else:
                sys.stderr.write(error_codes[630]+'\n')
        except:
            sys.stderr.write(error_codes[800]+'\n')

    def BuildGraph(self):
        vertices = {}
        edges = {}
        """ for testing output
        vertices = {1:"(1,4)"}
        edges = [(1,4),(5,6)]
        Code goes here
        """
        for street in self.streets_:
            pass
        # Clear old graph
        self.vertices_.clear()
        self.edges_.clear()

        # Build new
        self.vertices_ = vertices
        self.edges_ = edges

    def OutputGraph(self):

        self.BuildGraph()

        output_string = "V = {\n"
        for vertex in self.vertices_.keys():
            output_string += "    %d:   %s\n" % (vertex,
                                                 str(self.vertices_[vertex].replace(" ", "")))
        output_string += "}\n"
        output_string += "E = {\n"
        for edge in self.edges_:
            output_string += "    <%d,%d>,\n" % edge
        output_string = output_string[:-2]+"\n}"
        print(output_string)


def errorHandler(command, arguments, street_name, vertices):

    error_code = 500  # uncaught error. bad

    if (command is 'a' or command is 'c'):  # input errors for a|c
        if not street_name and not vertices:  # if we don't find a street name or vertex set
            error_code = 521  # error 521: incorrect arg format
        elif not street_name:
            error_code = 522  # error 522: no street name
        elif not vertices:
            error_code = 523  # error 523: no vertices
        elif len(street_name) > 1:
            error_code = 511  # error 511: too many street names
    elif command is 'r':  # input errors for r
        if not street_name:
            error_code = 531  # error 531: no street name
        elif not not vertices:  # double negative! ack! but maybe pythonic?
            error_code = 532  # error 532: unnecessary vertices
        elif len(street_name) > 1:
            error_code = 511  # too many street names again
    elif command is 'g' and not not arguments:  # additional input for g
        error_code = 540  # error 540: additional args
    return error_code


def ParseInput(line):
    """ Generate the regexes to parse our input 

    added parsers for each function to enforce input restrictions

    command_parser parses the input command and ensures it is in (a|c|g|r)

    arg_parser parses the arguments and ensures it conforms to the guidelines given in the FAQ
    ie whitespace between each street arg and vertices, whitespace in vertices args don't matter
    note: this also matches the case where only one arg is passed in order to capture the case r

    street_name_parser parses the street names

    vertex_parser parses the vertices
    """

    add_change_parser = re.compile(
        r"(([ ]*(a|c)[ ]+)(\"[a-z A-Z]+\"[ ]+)((\([ ]*[0-9]+[ ]*\,[ ]*[0-9]+[ ]*\)[ ]*)+))$")
    remove_parser = re.compile(r"^([ ]*r)([ ]+\"[a-z A-Z]+\")$")
    graph_parser = re.compile(r"^[ ]*g[ ]*$")

    command_parser = re.compile(r"(^[ ]*(a|c|g|r)[ ]*)")
    arg_parser = re.compile(
        r"([ ]+[\"a-zA-Z]+[ ]*[a-zA-Z]*\"[ ]+(\([ ]*[0-9]+[ ]*[\,][ ]*[0-9]+[ ]*\)[ ]*)+)|([ ]+\"[a-zA-Z]+\"$)")
    street_name_parser = re.compile(r"([ ]*\")([a-z A-Z]+)(\"[ ]*)")
    vertex_parser = re.compile(r"\([ ]*[0-9]+[ ]*\,[ ]*[0-9]+[ ]*\)")

    # initialize return dict with empty command and OK code
    parsed_output = {'output': [[], [], []], 'error': 0}
    command = street_name = vertices = None  # init our command structure
    # pdb.set_trace()
    # If there is a match, save into command variable
    if (add_change_parser.match(line) or remove_parser.match(line) or graph_parser.match(line)):
        if add_change_parser.match(line):
            # grab the parsed command and remove any whitespace
            command = add_change_parser.match(line).group(2).strip()
            street_name = street_name_parser.match(
                add_change_parser.match(line).group(4)).group(2)
            vertices = add_change_parser.match(line).group(5)

        elif remove_parser.match(line):
            command = remove_parser.match(line).group(1)
            street_name = street_name_parser.match(
                remove_parser.match(line).group(2)).group(2)

        elif graph_parser.match(line):
            command = graph_parser.match(line).group(0).strip()

        # pdb.set_trace()

    else:
        try:
            if command_parser.match(line) is not None:
                pdb.set_trace()
                command = command_parser.match(line).group().strip()
                arguments = arg_parser.findall(line)
                # something dodgy going on here
                # split args into street name
                street_name = re.findall(r'\"[a-z A-Z]+\"', ''.join(arguments))
                vertices = vertex_parser.findall(
                    ''.join(arguments))  # and vertices
                # handle the erroneous cases by setting an error code using our handler function
                parsed_output['error'] = errorHandler(
                    command, arguments, street_name, vertices)

            else:
                # If no match, set error code 510 for erroneous input
                parsed_output['error'] = 510
        except:
            parsed_output['error'] = 500  # unhandled error

    if parsed_output['error'] == 0:  # if we got here without any problems
        # prepare street name and vertices for return

        # prepare output data in the right format
        if street_name:
            street_name = street_name.lower()
        if vertices:
            vertices = vertices.replace(" ", "")
            vertices = [(int(a.split(',')[0]), int(a.split(',')[1]))
                        for a in re.findall(r"[0-9]+,[0-9]+", vertices)]
        command_sequence = [command, street_name,
                            vertices]  # build command sequence
        # put command sequence in output field
        parsed_output['output'] = command_sequence

    # return the command sequence (set or not) and a success/error code
    # pdb.set_trace()
    return parsed_output


def main():
    # YOUR MAIN CODE GOES HERE

    # sample code to read from stdin.
    # make sure to remove all spurious print statements as required
    # by the assignment

    # Graph object
    StreetGraph = Graph()

    # Dict to hold references to functions
    menu_options = {'a': StreetGraph.AddStreet,
                    'c': StreetGraph.ChangeStreet,
                    'r': StreetGraph.RemoveStreet,
                    'g': StreetGraph.OutputGraph}

    # Dict to hold possible errors
    global error_codes
    error_codes = {01: "Error: Ruh roh!",
                   02: "Error: Invalid command",
                   500: "Error: Exception raised",
                   510: "Error: Command not found",
                   511: "Error: Too many street names for this argument",
                   521: "Error: Incorrect input format. (a|c) \"<street name>\" (x1,y1) (x2,y2) (xi,yi)",
                   522: "Error: Please enter a street name for (a|c)",
                   523: "Error: Please enter vertices for (a|c)",
                   531: "Error: No street name for (r). (r) \"<street name>\"",
                   532: "Error: Unnecessary vertices for (r). (r) \"<street name>\"",
                   540: "Error: Too many arguments for g. (g)",
                   600: "Error: Uncaught exception in Graph.AddStreet",
                   610: "Error: Street already in vertices. Use c to change or r to remove",
                   620: "Error: Street not in vertices. Please use a to add a street",
                   630: "Error: Street not in vertices. Cannot remove",
                   700: "Error: Uncaught exception in Graph.ChangeStreet",
                   800: "Error: Uncaught exception in Graph.RemoveStreet"}

    # wait for input
    while True:

        # Read a line of input
        line = sys.stdin.readline().strip()

        # If line is blank, exit program
        if line == '':
            break

        # Else parse the input line
        parsed_line = ParseInput(line)
        command_sequence = parsed_line['output']
        return_value = parsed_line['error']

        command = command_sequence[0]
        street_name = command_sequence[1]
        vertices = command_sequence[2]
        # Figure out if an error occurred within the function
        # If so, skip back to input
        if return_value is not 0:
            sys.stderr.write(error_codes[return_value]+'\n')
            continue

        if command in ['a', 'c']:
            menu_options[command](street_name, vertices)
        elif command is 'r':
            menu_options[command](street_name)
        elif command is 'g':
            menu_options[command]()

        else:
            sys.stderr.write(error_codes[02]+'\n')

    print '[*]Exiting graph generator'
    # return exit code 0 on successful termination
    sys.exit(0)


if __name__ == '__main__':
    main()
