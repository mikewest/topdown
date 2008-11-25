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
        self.BEGIN_CLASS        =   re.compile("[\.]")
        self.BEGIN_ID           =   re.compile("[#]")
        self.BEGIN_PSEUDOCLASS  =   re.compile("[:]")
        self.BEGIN_SELECTOR     =   re.compile("[*:\[\]\.#]")
        self.SELECTOR           =   re.compile("[*\[\]\"'~^$|():.#>+a-zA-Z]")
        self.BEGIN_RULEBLOCK    =   re.compile("[{]")
        self.END_RULEBLOCK      =   re.compile("[}]")
        

    def token_generator( self ):
### Begin processing the string, one character at a time.
        c = self.next_char()
        self.__state = 'BASE'
        while ( c is not None ):
### 1) Whitespace
            if self.cur_char_is( self.WHITESPACE ):
                yield self.process_whitespace()
            
### 2) Selector?
            if self.cur_char_is( self.BEGIN_SELECTOR ):
                state = 'INSIDE_SELECTOR'
                yield self.process_selector()

### Everything Else
            else:
                yield Token( 'OPERATOR', c )
            
            c = self.next_char()
            
#
#   Overrides for generic parsers
#
    def process_whitespace( self ):
        """Group a whitespace block together into either a 'WHITESPACE' Token, or 'DESCENDANT_SELECTOR' Token"""
        if self.__state == 'BASE':
            while self.next_char_is( self.WHITESPACE ):
                c = self.next_char()
        else:
            while self.next_char_is( self.WHITESPACE ):
                c = self.next_char()
            if not self.next_char_is( self.BEGIN_RULEBLOCK ):
                return Token( 'DESCENDANT_SELECTOR', None )
        return Token( 'WHITESPACE', None )

    def process_selector( self ):
        """Parses a single selector into a list of selector Tokens"""
        str_buffer = self.cur_char()
        while self.next_char_is( self.SELECTOR ):
            str_buffer += self.next_char()
            
        return Token( 'SELECTOR', str_buffer )
# if self.cur_char_is( self.BEGIN_CLASS ):
#     tokens.append( self.process_prefixed_identifier( 'CLASS' ) )
# elif self.cur_char_is( self.BEGIN_ID ):
#     yield self.process_prefixed_identifier( 'ID' )
# elif self.cur_char_is( self.BEGIN_PSEUDOCLASS ):
#     yield self.process_prefixed_identifier( 'PSEUDOCLASS' )
# elif self.cur_char_is( self.CHARACTER ):
#     yield self.process_identifier( )

    def process_prefixed_identifier( self, identifier_type ):
        # Skip first character; it'll be either '.' or '#', and irrelevant.
        str_buffer  = ''
        while self.next_char_is( self.IDENTIFIER ):
            str_buffer += self.next_char()
        if str_buffer is not '':
            return Token( identifier_type, str_buffer )
        else:
            raise MalformedIdentifier( str_buffer, start_index, self.index )