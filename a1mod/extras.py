import re
import pdb
import sys


class Graph:

    streets_ = {}
    edges_ = {}
    vertices_ = {}
    intersections_ = {}

    def AddStreet(self, street_name, vertices):
        try:
            if street_name in self.streets_.keys():  # if street exists, do not add
                sys.stderr.write(error_codes[610]+'\n')
            else:
                self.streets_.update({street_name: vertices})
        except:
            sys.stderr.write(error_codes[600]+'/n')

    def ChangeStreet(self, street_name, vertices):
        try:
            if street_name in self.streets_.keys():  # check if street actually exists
                self.streets_.update({street_name: vertices})
            else:
                sys.stderr.write(error_codes[620]+'\n')
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

    def DetermineIntersections(self):
        # Look at all of this spaghetti!
        all_street_segments = []
        intersecting_segments = []
        intersections = []
        streets = []
        endpoint_names = []

        # Define determinant to determine intersections

        def Determinant(v0, v1):
            return float(v0[0]*v1[1]-v0[1]*v1[0])

        # Build list of paths
        for street in self.streets_.keys():
            streets.append(street)
            street_segments = []

            coordinates = self.streets_[street]
            for idx in range(1, len(coordinates)):
                street_segments.append((coordinates[idx-1], coordinates[idx]))

            all_street_segments.append(street_segments)

        # Horrible nested loops
        for idx1 in range(len(all_street_segments)):  # Compare street segments
            # With all other street segments
            for idx2 in range(idx1+1, len(all_street_segments)):
                # Compare all segments in segment1
                for segment_1 in all_street_segments[idx1]:
                    # With segment 2
                    for segment_2 in all_street_segments[idx2]:
                        p_i, p_f = segment_1  # generate p, q for p+tr = q + us equation
                        q_i, q_f = segment_2

                        r = (p_f[0]-p_i[0], p_f[1]-p_i[1])
                        s = (q_f[0]-q_i[0], q_f[1]-q_i[1])

                        if abs(Determinant(r, s)) > 1e-6:
                            t = Determinant(
                                (q_i[0]-p_i[0], q_i[1]-p_i[1]), s) / Determinant(r, s)
                            u = Determinant(
                                (q_i[0]-p_i[0], q_i[1]-p_i[1]), r) / Determinant(r, s)
                            if (0 <= t <= 1) and (0 <= u <= 1):
                                intersection = (p_i[0]+t*r[0], p_i[1]+t*r[1])
                                intersecting_segments.append(
                                    (segment_1, segment_2, intersection))
                        else:
                            continue
                    # end Inner segment for
                # end Outer segment for
            # end Inner street segment For
        # end Outer street segment For
        return intersecting_segments

    def DetermineVertices(self):
        pass

    def DetermineEdges(self):
        pass

    def BuildGraph(self):
        vertices = {}
        edges = {}

        intersecting_segments = self.DetermineIntersections()
        vertex_id = 1
        # now we have p1, p2, intersect
        # simply assign each (unique)  p1, p2, intersect an ID using dict and build edges from that
        pdb.set_trace()
        """
        for intersecting_segment in intersecting_segments:
            if intersecting_segment[0][0] not in vertices:
                vertices.update(str(i): intersecting_segment[0])
                intersecting_segment[0]
                i += 1
        """
        vertices = DetermineVertices()
        edges = DetermineEdges()
        """
        for street in self.streets_.keys():
            pass
        """
        # Clear old graph

        self.vertices_.clear()
        self.edges_.clear()

        # Build new
        self.vertices_.update(vertices)
        self.edges_.update(edges)

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
        r"(([ ]*(a|c)[ ]+)(\"[a-z A-Z]+\"[ ]+)((\([ ]*[\-]*[0-9]+[ ]*\,[ ]*[\-]*[0-9]+[ ]*\)[ ]*)+))$")
    remove_parser = re.compile(r"^([ ]*r)([ ]+\"[a-z A-Z]+\")$")
    graph_parser = re.compile(r"^[ ]*g[ ]*$")

    command_parser = re.compile(r"(^[ ]*(a|c|g|r)[ ]*)")
    arg_parser = re.compile(
        r"([ ]+[\"a-zA-Z]+[ ]*[a-zA-Z]*\"[ ]+(\([ ]*[\-]*[0-9]+[ ]*[\,][ ]*[\-]*[0-9]+[ ]*\)[ ]*)+)|([ ]+\"[a-zA-Z]+\"$)")
    street_name_parser = re.compile(r"([ ]*\")([a-z A-Z]+)(\"[ ]*)")
    vertex_parser = re.compile(r"\([ ]*[\-]*[0-9]+[ ]*\,[ ]*[\-]*[0-9]+[ ]*\)")

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
                        for a in re.findall(r"[\-]*[0-9]+,[\-]*[0-9]+", vertices)]
        command_sequence = [command, street_name,
                            vertices]  # build command sequence
        # put command sequence in output field
        parsed_output['output'] = command_sequence

    # return the command sequence (set or not) and a success/error code
    return parsed_output
