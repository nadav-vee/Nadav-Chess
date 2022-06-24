import socket

ip_prot = socket.AF_INET
tcp_prot = socket.SOCK_STREAM
server_ip = '127.0.0.1'
server_port = 8820
client_port = 8821
MAX_MSG_LENGTH = 1024
server_name = "The Gfuel fan club"

disconnect_msg = "bye"
kill_server_msg = "bye and close"

# server functions:

def server_handle_pending_move(data):
    pass

def server_cont_handle():
    pass

def server_get_move():
    pass

def server_game_over():
    pass



server_functions_dict = {
    "CONT            " : server_cont_handle,
    "GET_MOVE        " : server_get_move,
    "GAME_OVER       " : server_game_over,
    "PENDING_MOVE    " : server_handle_pending_move
}

client_functions_dict = {

}

def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    # Implement code ...

    #return full_msg
    if(cmd == None or data == None):
        return None
    return "{:<16}".format(cmd) + "|{:0>4}".format(len(data))+ "|{}".format(data)



def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """

    # The function should return 2 values
    #return cmd, msg
    if(data.count("|") == 2):
        if(data[17:21].isdigit()):
            tmplen = data.rfind("|")
            if(int(data[17:21]) == len(data) - 22):
                msg = data.split("|")
                return msg[0].strip(), msg[2]
    return None, None


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """

    if(msg.count("#") != expected_fields-1):
        return None
    else:
        return msg.split("#", expected_fields-1)



def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    # Implement code ...
    return "#".join(msg_fields)


# general functions
'''
- - - protocol documentation - - -

Message structure:

    TTTTTTTTTTTTTTTT|SSSS|MMM
    
    T - a 16 character long field that represents the type of the message.
    
    S - a 4 character long string representing the size of the message (int between 0000 - 9999)
    
    M - an S sized string which is the actual data that is transferred

    The different message parts will be separated with "|" 
    which will then after get parsed using general parser
    
Message types from client to server:
    
    Request opponent:
        
        REQUEST_OPPONENT|0000|
        
        this message will be sent after client is ready for the game
        and is requesting an approval that server has connected to
    
    Continue:
    
        CONT            |0000|
        
        this message will be sent from a player to the server in order
        to tell the server to refresh the other player game after the player's
        finished all move logic.
    
    Get move:
        
        GET_MOVE        |0000|
        
        this message will be sent in order to inform the server
        that one's game is ready to accept a new move and that
        the server should ask the other player for a move
    
    Game over:
    
        GAME_OVER       |0000|
        
        this message will be sent from player a in order to inform the server
        that player b has won, the server will inform player b and after player b
        has confirmed finishing the game, the server will close both connections
    
    Pending move:
    
        PENDING_MOVE    |0006|IJYXGC
        I - move start row
        J - move start column
        Y - move end row
        X - move end column
        G - image index / piece enum value
        C - piece color
        
        this message will be communicated when a player
        is done making a move and another is waiting
        for a move.
    
Messages server to client:

    
'''