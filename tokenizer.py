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
        
    def __eq__( self, other ):
        if isinstance( other, Token ):
            return self.type == other.type and self.value == other.value
        else:
            return NotImplemented
    
    def __ne__( self, other ):
        result = self.__eq__( other )
        if result is NotImplemented:
            return NotImplemented
        else:
            return not result

class TokenList( object ):
    def __init__( self, tokens = None ):
        self.__tokens   = tokens
        
        if self.__tokens is None:
            self.__tokens = []
        elif isinstance( self.__tokens, Token ):
            self.__tokens = [ self.__tokens ]
        
        self.__reset()
    
    def append( self, to_append ):
        """Appends a token to the TokenList, and resets the internal pointer"""
        if isinstance( to_append, Token ):
            self.__tokens.append( to_append )
            self.__reset()
        else:
            raise TypeError
    
    def next( self ):
        """Returns the next token in the list, and advances the pointer"""
        self.current += 1
        return self.__get_token( self.current )
    
    def peek( self ):
        """Returns the next token in the list, without advancing the pointer"""
        newIndex = self.current + 1
        return self.__get_token( newIndex )

    #
    #   Private Helpers
    #
    def __reset( self ):
        """Resets the internal pointer to the beginning of the list, and reevaluates the size"""
        self.current = -1
        self.length  = len( self.__tokens )
        
    def __get_token( self, x ):
        """Returns a specific token"""
        if x < self.length:
            return self.__tokens[ x ]
        else:
            return None
    #
    #   Equality
    #
    def __eq__( self, other ):
        if isinstance( other, TokenList ):
            if other.length == self.length:
                a = other.next()
                b = self.next()
                while a is not None or b is not None:
                    if a != b:
                        return False
                    a = other.next()
                    b = self.next()
                return True
            else:
                return False
        else:
            return NotImplemented
            
    def __ne__( self, other ):
        result = self.__eq__( other )
        if result is NotImplemented:
            return NotImplemented
        else:
            return not result
    
    #
    #   Conversion
    #
    def __str__( self ):
        str_buffer = ''
        cur        = 0
        for token in self.__tokens:
            str_buffer += "%d)  %s\n" % ( cur, token )
            cur        += 1
        return str_buffer

class Tokenizer( object ):
### Generic "Constants" to be overridden in subclasses
    WHITESPACE          = re.compile("\s")
    SPACE               = re.compile("[ \t]")
    TERMINATOR          = re.compile("[\n\r]")
    BEGIN_STRING        = re.compile("['\"]")
    CHARACTER           = re.compile("[a-zA-Z]")
    NUMBER              = re.compile("[0-9]")
    NUMBER_SIGN         = re.compile("[-+]")
    IDENTIFIER          = re.compile("[a-zA-Z0-9_]")
    NUMBER_SEPERATOR    = re.compile("[\.]")
    NUMBER_EXPONENT     = re.compile("[Ee]")
    BEGIN_COMMENT       = re.compile("[/]")
    
    def __init__( self, string_to_tokenize = ''):
        self.original   =   string_to_tokenize
        self.length     =   len( string_to_tokenize )
        self.index      =   -1
        self.tokens     =  TokenList()
        
#
#   Helper Methods (Private)
#
    def __peek( self ):
        """Return the next character (or None), but don't advance the index."""
        newIndex = self.index + 1
        return self.__get_char( newIndex )
    
    def __char_is( self, c, char_type ):
        """Returns true if the given character is not none, and matches the given type"""
        if c is not None:
            return char_type.match( c )
        else:
            return False

    def __get_char( self, x ):
        if x < self.length:
            return self.original[ x ]
        else:
            return None
#
#   Helper Methods (Not so private (used by subclasses))
#
    def cur_char( self ):
        """Return the current character (or None)."""
        return self.__get_char( self.index )
        
    def next_char( self ):
        """Return the next character (or None), and advance the index."""
        self.index += 1
        return self.__get_char( self.index )
    
    def next_x_chars( self, x = 1 ):
        """Return the next X characters (or None if there aren't enough), and advance the index."""
        first   = self.index + 1
        last    = first + x
        if last < self.length:
            return self.original[ first : last ]
        else:
            return None
    
    def cur_char_is( self, char_type ):
        """Returns true if the next character is of a certain type (e.g. matches a given regex)"""
        c = self.cur_char()
        return self.__char_is( c, char_type )
            
    def next_char_is( self, char_type ):
        """Returns true if the next character is of a certain type (e.g. matches a given regex)"""
        c = self.__peek()
        return self.__char_is( c, char_type )
    
    def token_generator( self ):
        pass

#
#   Public Methods
#

    def tokenize( self ):
        for token in self.token_generator():
            self.tokens.append( token )
        return self.tokens
        
#
#   Generic Tokens (can/should be overridden by subclasses)
#
    def process_literal_string( self ):
        """Process a 'generic' string, either raising an error or retuning a string Token"""
        c           = self.cur_char()
        start_index = self.index
        quote_char  = c
        str_buffer  = ''
        ### Will exit this loop only via raising an error,
        ### or through a `break` when we find a closing quote.
        while True: 
            c = self.next_char()
    ### Raise an error?
            if ( c is None or self.TERMINATOR.match( c ) ):
                raise UnterminatedString( str_buffer, start_index, self.index )
            # Need a test here for control characters
            # elif [control characters].match( c ) ):
            #   raise StringContainsControlCharacters( str_buffer, start_index, self.index )
            
    ### Closing Quote?
            if ( c == quote_char ):
                return Token( 'STRING', str_buffer )
                break
            
    ### Ok, then.
            
        ### Escaped?
            if ( c == '\\'):
                escapee     = self.next_char()
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
                    base16 = self.next_x_chars( 4 )
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
            
    def process_literal_number( self ):
        """Process a 'generic' number, either raising an error, or returning a number Token"""
        c           = self.cur_char()
        start_index = self.index
        str_buffer  = c

        while ( self.next_char_is( self.NUMBER ) ):
            str_buffer += self.next_char()
        
        if ( self.next_char_is( self.NUMBER_SEPERATOR ) ):
            str_buffer += self.next_char()
            
            while ( self.next_char_is( self.NUMBER ) ):
                str_buffer += self.next_char()
                
        if ( self.next_char_is( self.NUMBER_EXPONENT ) ):
            str_buffer += self.next_char()
            if ( self.next_char_is( self.NUMBER_SIGN ) ):
                str_buffer += self.next_char()

            if ( not self.next_char_is( self.NUMBER ) ):
                raise NumberBadExponent( str_buffer, start_index, self.index )

            while ( self.next_char_is( self.NUMBER ) ):
                str_buffer += self.next_char()

        if ( self.next_char_is( self.CHARACTER ) ):
            raise NumberFollowedByCharacter( str_buffer, start_index, self.index )
        else:
            return Token( 'NUMBER', str_buffer )
            
    def process_identifier( self ):
        """Process a 'generic' identifier, either raising an error, or returning an identifier Token"""
        c           = self.cur_char()
        str_buffer  = c
        while ( self.next_char_is( self.IDENTIFIER ) ):
            str_buffer += self.next_char()
        return Token( 'IDENTIFIER', str_buffer )