# encoding: utf-8;
import re
from tokenizer import Token, TokenList, Tokenizer
from tokenexceptions import *

class MalformedIdentifier( TokenException ):
    """Exception raised when an identifier is malformed."""
    def __init__( self, partial_token = '', start_char = 0, end_char = 0 ):
        TokenException.__init__( self, partial_token, start_char, end_char )
        self.message = "You've tried to create a identifier, but with a crap name"

class CSSTokenizer( Tokenizer ):
    """
        Given a string, Tokenizer breaks it into strings according to the
        rules specified in the CSS standard.
        
        There's nothing new here.
    """
    def __init__( self, string_to_tokenize = '' ):
        Tokenizer.__init__( self, string_to_tokenize )

    ### Setup CSSTokenizer-specific regexen
        self.BEGIN_CLASS        =    re.compile("[\.]")
        self.BEGIN_ID           =    re.compile("[#]")
        self.BEGIN_PSEUDOCLASS  =    re.compile("[:]")
        

    def token_generator( self ):
### Begin processing the string, one character at a time.
        c = self.next_char()
        while ( c is not None ):
### 1) Whitespace
            if self.cur_char_is( self.WHITESPACE ):
                pass
                
### 2) Identifier
            elif self.cur_char_is( self.BEGIN_CLASS ):
                yield self.process_identifier( 'CLASS' )
            elif self.cur_char_is( self.BEGIN_ID ):
                yield self.process_identifier( 'ID' )
            elif self.cur_char_is( self.BEGIN_PSEUDOCLASS ):
                yield self.process_identifier( 'PSEUDOCLASS' )

### Everything Else
            else:
                yield Token( 'OPERATOR', c )
                
            c = self.next_char()
            
#
#   Overrides for generic parsers
#
    def process_identifier( self, identifier_type ):
        # Skip first character; it'll be either '.' or '#', and irrelevant.
        str_buffer  = ''
        while self.next_char_is( self.IDENTIFIER ):
            str_buffer += self.next_char()
        if str_buffer is not '':
            return Token( identifier_type, str_buffer )
        else:
            raise MalformedIdentifier( str_buffer, start_index, self.index )