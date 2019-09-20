import sys
import re
import pdb #debug



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

    street_name_parser parses the street names

    vertex_parser parses the vertices
    """
    command_parser = re.compile(r"(^[ ]*(a|c|g|r)[ ]*)")
    arg_parser = re.compile(r"([ ]+[\"a-zA-Z]+[ ]*[a-zA-Z]*\"[ ]+(\([ ]*[0-9]+[ ]*[\,][ ]*[0-9]+[ ]*\)[ ]*)+)|([ ]+\"[a-zA-Z]+\"$)")
    street_name_parser = re.compile(r"\"[a-zA-Z]+[ ]*[a-zA-Z]*\"")
    vertex_parser = re.compile(r"\([ ]*[0-9]+[ ]*\,[ ]*[0-9]+[ ]*\)")

    parsed_output = {'output':[], 'error':0}
    command = street_name = vertices = None

    """LOOK AT TEST CASE WHERE INPUT IS a"blabla"  """
    if command_parser.search(line) is not None: # If there is a match, save into command variable
        command = command_parser.match(line).group().strip() #grab the parsed command and remove any whitespace
        #pdb.set_trace()
        print command #DEBUG
        #arg_section = line[line.index(command)+1:]
        #print arg_section
        if (command is 'a' or command is 'c') and arg_parser.search(line) is not None:
            arguments = arg_parser.search(line).group()
            street_name = street_name_parser.search(arguments).group().strip("\"")
            vertices = vertex_parser.findall(arguments)

            # continue working on this
            
        elif command is 'r' and arg_parser.search(line) is not None:
            arg_parser.search(line)
            street_name = "hurr"
            vertices = ["durr"]
            
        elif command is 'g' and arg_parser.search(line) is None: #we want no args in this case
            street_name = None
            vertices = []
        else:
            #error cases go here
            if (command is 'a' or command is 'c'):
                parsed_output['error'] = 42
            elif command is 'r':
                parsed_output['error'] = 44
            elif command is 'g':
                parsed_output['error'] = 46
            else:
                parsed_output['error'] = 47
            
        
        command_sequence = [command, street_name, vertices] #placeholder command sequence
        parsed_output['output'] = command_sequence    #set command sequence as output
        
    else:
        parsed_output['error'] = 41 # If no match, set error code
    
    #return the command sequence (set or not) and a success code
    return parsed_output

def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment


    # Dict to hold references to functions
    menu_options = {'a': AddStreet,
                    'c': ChangeStreet,
                    'r': RemoveStreet,
                    'g': OutputGraph}
    
    # Dict to hold possible errors
    global error_codes
    error_codes = {01:"Error: Ruh roh!",
                   02:"Error: Invalid command",
                   41:"Error: Command not found"} 
        
    # wait for input
    while True:

        # Read a line of input
        line = sys.stdin.readline().strip()

        # If line is blank, exit program
        if line == '':
            break

        # Else parse the input line
        parsed_line=ParseInput(line)
        command_sequence = parsed_line['output']
        return_value = parsed_line['error']

        # Figure out if an error occurred within the function
        # If so, skip back to input
        if return_value is not 0:
            sys.stderr.write(error_codes[return_value]+'\n')
            continue
        
        if command_sequence[0] in ['a', 'c']:
            pass
        elif command_sequence[0] is 'r':
            pass
        elif command_sequence[0] is 'g':
            pass
        
        else:
            sys.stderr.write("Error: "+error_codes[02])
            
        street_name="Placeholder1"
        vertices = "Placeholder2"
        command=command_sequence[0]
        menu_options[command](street_name, vertices)
    
    print '[*]Exiting graph generator'
    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
