import sys
import a1mod.extras


def main():
    # YOUR MAIN CODE GOES HERE

    # sample code to read from stdin.
    # make sure to remove all spurious print statements as required
    # by the assignment

    # Graph object
    StreetGraph = a1mod.extras.Graph()

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
        parsed_line = a1mod.extras.ParseInput(line)
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

    # print '[*]Exiting graph generator'
    # return exit code 0 on successful termination
    sys.exit(0)


if __name__ == '__main__':
    main()
