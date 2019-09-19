import sys

# YOUR CODE GOES HERE

def AddStreet(street_name, vertices):
    pass

def ChangeStreet(street_name, vertices):
    pass

def RemoveStreet(street_name):
    pass

def OutputGraph():
    pass


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
        print 'read a line:', line

    print 'Finished reading input'
    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
