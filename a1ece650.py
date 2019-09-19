import sys
import re

# YOUR CODE GOES HERE

def AddStreet(street_name, vertices):
    pass

def ChangeStreet(street_name, vertices):
    pass

def RemoveStreet(street_name):
    pass

def OutputGraph():
    pass

def ParseInput(line):
    input_parser = re.compile("[a-z]")

    # placeholder return statement
    return "a", "args"

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

        command, args = ParseInput(line)

        try:
            menu_options[command](args)
        except:
            pass
        
    print '[*]Exiting graph generator'
    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
