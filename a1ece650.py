import sys
import a1mod.extras


def main():
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
            sys.stderr.write(a1mod.extras.error_codes(return_value)+'\n')
            continue

        elif command in ['a', 'c']:
            menu_options[command](street_name, vertices)
        elif command is 'r':
            menu_options[command](street_name)
        elif command is 'g':
            menu_options[command]()

        else:
            sys.stderr.write(a1mod.extras.error_codes(02)+'\n')

    # return exit code 0 on successful termination
    del(StreetGraph)
    sys.exit(0)


if __name__ == '__main__':
    main()
