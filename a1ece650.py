import sys
import re
import pdb #debug



def AddStreet(street_name, vertices):
    print "Add street function"

def ChangeStreet(street_name, vertices):
    print "Change street function"

def RemoveStreet(street_name):
    print "Remove street function"

def OutputGraph():
    print "Output graph function"

def errorHandler(command, arguments, street_name, vertices):

    error_code = 0 # default success

    if (command is 'a' or command is 'c'): #input errors for a|c
        if not street_name and not vertices: #if we don't find a street name or vertex set
            error_code = 521 #error 521: incorrect arg format
        elif not street_name:
            error_code = 522 #error 522: no street name
        elif not vertices:
            error_code = 523 #error 523: no vertices
        elif len(street_name)>1:
            error_code = 511 #error 511: too many street names

    elif command is 'r': #input errors for r
        if not street_name:
            error_code = 531 # error 531: no street name
        elif not not vertices: # double negative! ack! but maybe pythonic?
            error_code = 532 # error 532: unnecessary vertices
        elif len(street_name)>1:
            error_code = 511 # too many street names again

    elif command is 'g' and not not arguments: #additional input for g
        error_code = 540 # error 540: additional args

    return error_code

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

    parsed_output = {'output':[[],[],[]], 'error':0} #initialize return dict with empty command and OK code
    command = street_name = vertices = None #init our command structure  

    """LOOK AT TEST CASE WHERE INPUT IS a"blabla"  """
    if command_parser.search(line) is not None: # If there is a match, save into command variable
        command = command_parser.match(line).group().strip() #grab the parsed command and remove any whitespace
        #pdb.set_trace()
        arguments = arg_parser.findall(line)
        #check case : a "ababab" 
        street_name = street_name_parser.findall(''.join(arguments)) #split args into street name
        vertices = vertex_parser.findall(''.join(arguments)) #and vertices
        #pdb.set_trace()

        # handle the erroneous cases by setting an error code using our handler function
        parsed_output['error'] = errorHandler(command, arguments, street_name, vertices)
    
        if parsed_output['error']==0: #if we got here without any problems
            #process street name
            #process vertices
            command_sequence = [command, street_name, vertices] #build command sequence
            parsed_output['output'] = command_sequence    #put command sequence in output field

        else:
            pass #parsed output will be in the form {'output':[], 'error':x} anyway
            
        
        
    else:
        parsed_output['error'] = 510 # If no match, set error code 510
        
    #return the command sequence (set or not) and a success/error code
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
                   510:"Error: Command not found",
                   521:"Error: User chose a or c with incorrect input format. Please enter (a|c) \"<streetname\" (x1,y1) (x2,y2) (xi,yi)",
                   522:"",
                   523:"",
                   524:""}
                   

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
        elif command_sequence is 'r':
            menu_options[command](street_name)
        elif command_sequence is 'g':
            menu_options[command]()
        
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
