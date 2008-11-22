# encoding: utf-8;
import re
from tokenizer import Token, TokenList, Tokenizer
from tokenexceptions import *

class JavaScriptTokenizer( Tokenizer ):
    """
        Given a string, Tokenizer provides an interface to iterate through
        it's tokens.  Tokenizer is more or less a straight port to Python of
        Douglas Crockman's [`tokens.js`][1].
        
        There's nothing new here.
        
        [1]: http://javascript.crockford.com/tdop/tokens.js
    """
    def __init__( self, string_to_tokenize = '', prefix_chars = '-=<>!+*&|/%^', suffix_chars = '=<>&|' ):
        Tokenizer.__init__( self, string_to_tokenize )
        self.prefix     =   prefix_chars
        self.suffix     =   suffix_chars

    def token_generator( self ):
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
        
        BEGIN_COMMENT       = re.compile("[/]")
        
        BEGIN_STRING        = re.compile("['\"]")
        
        PREFIX              = re.compile( "[%s]" % self.prefix )
        SUFFIX              = re.compile( "[%s]" % self.suffix )
        
### Begin processing the string, one character at a time.
        c = self.next_char()
        while ( c is not None ):
### 1) Whitespace
            if WHITESPACE.match( c ):
                pass
                
### 2) Identifier
            elif BEGIN_IDENTIFIER.match( c ):
                str_buffer = c
                while ( self.next_char_is( IDENTIFIER ) ):
                    str_buffer += self.next_char()
                yield Token( 'IDENTIFIER', str_buffer )
                
### 3) Number
            elif NUMBER.match( c ):
                start_index = self.index
                str_buffer  = c
                
    ### Look for more digits
                while ( self.next_char_is( NUMBER ) ):
                    str_buffer += self.next_char()
                
    ### Look for a decimal fraction
                if ( self.next_char_is( NUMBER_SEPERATOR ) ):
                    str_buffer += self.next_char()
                    
        ### Look for more digits
                    while ( self.next_char_is( NUMBER ) ):
                        str_buffer += self.next_char()
                        
    ### Look for an exponent
                if ( self.next_char_is( NUMBER_EXPONENT ) ):
                    str_buffer += self.next_char()
        ### Look for a sign
                    if ( self.next_char_is( NUMBER_SIGN ) ):
                        str_buffer += self.next_char()
        ### If the next thing isn't a number, raise an error
                    if ( not self.next_char_is( NUMBER ) ):
                        raise NumberBadExponent( str_buffer, start_index, self.index )
        ### Look for more digits
                    while ( self.next_char_is( NUMBER ) ):
                        str_buffer += self.next_char()
    ### We've got a number!  Unless the next character is a character, that is...
                if ( self.next_char_is( CHARACTER ) ):
                    raise NumberFollowedByCharacter( str_buffer, start_index, self.index )
                else:
                    yield Token( 'NUMBER', str_buffer )

### 4) String
            elif BEGIN_STRING.match( c ):
                start_index = self.index
                quote_char  = c
                str_buffer  = ''
                ### Will exit this loop only via raising an error,
                ### or through a `break` when we find a closing quote.
                while True: 
                    c = self.next_char()
            ### Raise an error?
                    if ( c is None or TERMINATOR.match( c ) ):
                        raise UnterminatedString( str_buffer, start_index, self.index )
                    # Need a test here for control characters
                    # elif [control characters].match( c ) ):
                    #   raise StringContainsControlCharacters( str_buffer, start_index, self.index )
                    
            ### Closing Quote?
                    if ( c == quote_char ):
                        yield Token( 'STRING', str_buffer )
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

### 5) One-line Comments (not a token: just throw away)
            elif BEGIN_COMMENT.match( c ) and self.next_char_is( BEGIN_COMMENT ):
                while c is not None and not TERMINATOR.match( c ):
                    c = self.next_char()

### 6) Combining prefix/suffix
            elif PREFIX.match( c ):
                str_buffer = c
                while ( self.next_char_is( SUFFIX ) ):
                    str_buffer += self.next_char()
                yield Token( 'OPERATOR', str_buffer )

### Everything Else
            else:
                yield Token( 'OPERATOR', c )
                
            c = self.next_char()