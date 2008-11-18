# encoding: utf-8;

#
#   Token Exceptions
#
class TokenException( Exception ):
    """The base class for exceptions generated while tokenizing a string."""
    def __init__( self, partial_token = '', start_char = 0, end_char = 0):
        self.message = "Generic Tokenizer Exception!  OMG!"
        self.partial = partial_token
        self.start   = start_char
        self.end     = end_char
        
    def __str__( self ):
        return repr( '' ) + """
Friendly error:
    %s:
    - Partial Token: %s
    - Start Char:    %s
    - End Char:      %s
        """ % ( self.message, self.partial, self.start, self.end )
        
### There has to be a simpler way to do this.  Factories?  Something?
class NumberBadExponent( TokenException ):
    """Exception raised when a number has an invalid exponent."""
    def __init__( self, partial_token = '', start_char = 0, end_char = 0 ):
        TokenException.__init__( self, partial_token, start_char, end_char )
        self.message = "You've tried to create a number, but with a crap exponent"
        
class NumberFollowedByCharacter( TokenException ):
    """Exception raised when a number contains a character."""
    def __init__( self, partial_token = '', start_char = 0, end_char = 0 ):
        TokenException.__init__( self, partial_token, start_char, end_char )
        self.message = "You've tried to create a number, but with characters"
        
class StringContainsControlCharacters( TokenException ):
    """Exception raised when a string contains a control character."""
    def __init__( self, partial_token = '', start_char = 0, end_char = 0 ):
        TokenException.__init__( self, partial_token, start_char, end_char )
        self.message = "You've tried to create a string, but included control characters"
        
class UnterminatedString( TokenException ):
    """Exception raised when a string isn't terminated."""
    def __init__( self, partial_token = '', start_char = 0, end_char = 0 ):
        TokenException.__init__( self, partial_token, start_char, end_char )
        self.message = "You've tried to create a string, but didn't terminate it"
        


