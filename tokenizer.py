# encoding: utf-8;
import re
from tokenexceptions import *

#
#   Token Class.  Now we're getting somewhere.
#
class Token( object ):
    """
        A Token is the smallest unit of a program that can be considered in
        abstraction.  It has a type, which should probably be an Enum of some
        sort, however those work in Python, and a value.
    """
    def __init__( self, token_type, token_value ):
        self.type           = token_type
        self.value          = token_value
        
    def __str__( self ):
        return "Token: '%s' of type %s" % ( self.value, self.type )

class Tokenizer( object ):
    """
        Given a string, Tokenizer provides an interface to iterate through
        it's tokens.  Tokenizer is more or less a straight port to Python of
        Douglas Crockman's [`tokens.js`][1].
        
        There's nothing new here.
        
        [1]: http://javascript.crockford.com/tdop/tokens.js
    """
    def __init__( self, string_to_tokenize = '', prefix_chars = '-=<>!+*&|/%^', suffix_chars = '=<>&|' ):
        self.original   =   string_to_tokenize
        self.prefix     =   prefix_chars
        self.suffix     =   suffix_chars
        
        self.length     =   len( string_to_tokenize )
        self.index      =   -1
        self.tokens     =   [ ]
#
#   Helper Methods (private)
#   
    def __next_char( self ):
        """Return the next character (or None), and advance the index."""
        self.index += 1
        if self.index < self.length:
            return self.original[ self.index ]
        else:
            return None
    
    def __next_x_chars( self, x = 1 ):
        """Return the next X characters (or None if there aren't enough), and advance the index."""
        first   = self.index + 1
        last    = first + x
        if last < self.length:
            return self.original[ first : last ]
        else:
            return None
    
    def __peek( self ):
        """Return the next character (or None), but don't advance the index."""
        newIndex = self.index + 1
        if newIndex < self.length:
            return self.original[ newIndex ]
        else:
            return None
            
    def __next_is( self, char_type ):
        """Returns true if the next character is of a certain type (e.g. matches a given regex)"""
        c = self.__peek()
        if c is not None:
            return char_type.match( c )
        else:
            return False
        
    def __new_token( self, token_type, token_value ):
        """Create a new token object, and append it to `self.tokens`"""
        self.tokens.append( Token( token_type, token_value ) )

#
#   Public Methods
#

    def tokenize( self ):
### "Constants"
        WHITESPACE          = re.compile("\s")
        SPACE               = re.compile("[ \t]")
        TERMINATOR          = re.compile("[\n\r]")
        
        CHARACTER           = re.compile("[a-zA-Z]")
        NUMBER              = re.compile("[0-9]")
        NUMBER_SIGN         = re.compile("[-+]")
        
        BEGIN_IDENTIFIER    = CHARACTER
        IDENTIFIER          = re.compile("[a-zA-Z0-9_]")
        
        NUMBER_SEPERATOR    = re.compile("[\.]")
        NUMBER_EXPONENT     = re.compile("[Ee]")
        
        BEGIN_STRING        = re.compile("['\"]")
        
        PREFIX              = re.compile( "[%s]" % self.prefix )
        SUFFIX              = re.compile( "[%s]" % self.suffix )
        
### Begin processing the string, one character at a time.
        c = self.__next_char()
        while ( c is not None ):
### 1) Whitespace
            if SPACE.match( c ):
                pass
                
### 2) Identifier
            elif BEGIN_IDENTIFIER.match( c ):
                str_buffer = c
                while ( self.__next_is( IDENTIFIER ) ):
                    str_buffer += self.__next_char()
                self.__new_token( 'IDENTIFIER', str_buffer )
                
### 3) Number
            elif NUMBER.match( c ):
                start_index = self.index
                str_buffer  = c
                
    ### Look for more digits
                while ( self.__next_is( NUMBER ) ):
                    str_buffer += self.__next_char()
                
    ### Look for a decimal fraction
                if ( self.__next_is( NUMBER_SEPERATOR ) ):
                    str_buffer += self.__next_char()
                    
        ### Look for more digits
                    while ( self.__next_is( NUMBER ) ):
                        str_buffer += self.__next_char()
                        
    ### Look for an exponent
                if ( self.__next_is( NUMBER_EXPONENT ) ):
                    str_buffer += self.__next_char()
        ### Look for a sign
                    if ( self.__next_is( NUMBER_SIGN ) ):
                        str_buffer += self.__next_char()
        ### If the next thing isn't a number, raise an error
                    if ( not self.__next_is( NUMBER ) ):
                        raise NumberBadExponent( str_buffer, start_index, self.index )
        ### Look for more digits
                    while ( self.__next_is( NUMBER ) ):
                        str_buffer += self.__next_char()
    ### We've got a number!  Unless the next character is a character, that is...
                if ( self.__next_is( CHARACTER ) ):
                    raise NumberFollowedByCharacter( str_buffer, start_index, self.index )
                else:
                    self.__new_token( 'NUMBER', str_buffer )

### 4) String
            elif BEGIN_STRING.match( c ):
                start_index = self.index
                quote_char  = c
                str_buffer  = ''
                ### Will exit this loop only via raising an error,
                ### or through a `break` when we find a closing quote.
                while True: 
                    c = self.__next_char()
            ### Raise an error?
                    if ( c is None or TERMINATOR.match( c ) ):
                        raise UnterminatedString( str_buffer, start_index, self.index )
                    # Need a test here for control characters
                    # elif [control characters].match( c ) ):
                    #   raise StringContainsControlCharacters( str_buffer, start_index, self.index )
                    
            ### Closing Quote?
                    if ( c == quote_char ):
                        self.__new_token( 'STRING', str_buffer )
                        break
                    
            ### Ok, then.
                    
                ### Escaped?
                    if ( c == '\\'):
                        escapee     = self.__next_char()
                        if ( escapee is None):
                            raise UnterminatedString( str_buffer, start_index, self.index )
                        
                        ### I wish Python had a `switch` statement.
                        if ( 'b' == escapee ):
                            c   = '\b'
                        elif ( 'f' == escapee ):
                            c   = '\f'
                        elif ( 'n' == escapee ):
                            c   = '\n'
                        elif ( 'r' == escapee ):
                            c   = '\r'
                        elif ( 't' == escapee ):
                            c   = '\t'
                        elif ( 'u' == escapee ):
                            base16 = self.__next_x_chars( 4 )
                            if ( base16 is None ):
                                raise UnterminatedString( str_buffer, start_index, self.index )
                            else:
                                try:
                                    c = chr( int( base16, 16 ) )
                                except ( ValueError, TypeError ):
                                    raise UnterminatedString( str_buffer, start_index, self.index )
                        else:
                            c   += escapee
                            
                ### Append, and move on
                    str_buffer += c
                    
### 5) Combining prefix/suffix
            elif PREFIX.match( c ):
                str_buffer = c
                while ( self.__next_is( SUFFIX ) ):
                    str_buffer += self.__next_char()
                self.__new_token( 'OPERATOR', str_buffer )

### Everything Else
            else:
                self.__new_token( 'OPERATOR', c )
                
            c = self.__next_char()

        return self.tokens