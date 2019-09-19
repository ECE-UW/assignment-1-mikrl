import sys
import re

# YOUR CODE GOES HERE

def AddStreet(street_name, vertices):
    pass

def ChangeStreet(street_name, vertices):
    pass

def RemoveStreet(street_name, *extra):
    pass

def OutputGraph(*extra):
    pass

def ParseInput(line):
    """ Generate the regexes to parse our input 
    command_parser parses the input command and ensures it is in (a|c|g|r)

    arg_parser parses the arguments and ensures it conforms to the guidelines given in the FAQ
    ie whitespace between each street arg and vertices, whitespace in vertices args don't matter
    note: this also matches the case where only one arg is passed in order to capture the case r
    """
    command_parser = re.compile("(^[ ]*(a|c|g|r)[ ]*)")
    arg_parser = re.compile("([ ]+\"[a-z]+\"[ ]+(\([ ]*[0-9]+[ ]*[\,][ ]*[0-9]+[ ]*\)[ ]*)+)|([ ]+\"[a-z]+\"$)")


    
    # placeholder return statement
    return "a", "args", "more_args"

def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment

    # Dict to hold references to functions
    menu_options = {"a": AddStreet,
                    "c": ChangeStreet,
                    "r": RemoveStreet,
                    "g": OutputGraph}
    
    
    while True:
        line = sys.stdin.readline().strip()

        if line == '':
            break

        command, street_name, vertices = ParseInput(line)

        try:
            menu_options[command](street_name, vertices)
        except:
            pass
        
    print '[*]Exiting graph generator'
    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
