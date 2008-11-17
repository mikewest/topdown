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
    def __init__( self, string_to_tokenize = '' ):
        self.original   =   string_to_tokenize
        self.length     =   len( string_to_tokenize )
        self.index      =   -1
        self.tokens     =   [ ]
#
#   Helper Methods (private)
#   
    def __next_char( self ):
        "Return the next character (or None), and advance the index."
        self.index += 1
        if self.index < self.length:
            return self.original[ self.index ]
        else:
            return None
        
    def __peek( self ):
        "Return the next character (or None), but don't advance the index."
        newIndex = self.index + 1
        if newIndex < self.length:
            return self.original[ newIndex ]
        else:
            return None
            
    def __next_is( self, char_type ):
        "Returns true if the next character is of a certain type (e.g. matches a given regex)"
        c = self.__peek()
        if c is not None:
            return char_type.match( c )
        else:
            return False
        
    def __new_token( self, token_type, token_value ):
        self.tokens.append( Token( token_type, token_value ) )

    def __error_token( self, token_type, token_value, error ):
        self.tokens.append( Token( token_type, token_value, error ) )
#
#   Public Methods
#

    def tokenize( self ):
### "Constants"
        WHITESPACE          = re.compile("\s")
        
        CHARACTER           = re.compile("[a-zA-Z]")
        NUMBER              = re.compile("[0-9]")
        NUMBER_SIGN         = re.compile("[-+]")
        
        BEGIN_IDENTIFIER    = CHARACTER
        IDENTIFIER          = re.compile("[a-zA-Z0-9_]")
        
        NUMBER_SEPERATOR    = re.compile("[\.]")
        NUMBER_EXPONENT     = re.compile("[Ee]")
        
        BEGIN_STRING        = re.compile("['\"]")
        
### Begin processing the string, one character at a time.
        c = self.__next_char()
        while ( c is not None ):
### 1) Whitespace
            if WHITESPACE.match( c ):
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

### 4) 

### Everything Else
            else:
                self.__new_token( 'OPERATOR', c )
                
            c = self.__next_char()

        return self.tokens