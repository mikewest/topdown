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
    ### Setup JavaScriptTokenizer-specific regexen
        self.PREFIX             =   re.compile( "[%s]" % self.prefix )
        self.SUFFIX             =   re.compile( "[%s]" % self.suffix )
        self.BEGIN_IDENTIFIER   =   self.CHARACTER
        

    def token_generator( self ):
### "Constants"

        
### Begin processing the string, one character at a time.
        c = self.next_char()
        while ( c is not None ):
### 1) Whitespace
            if self.WHITESPACE.match( c ):
                pass
                
### 2) Identifier
            elif self.BEGIN_IDENTIFIER.match( c ):
                yield self.process_identifier()
                
### 3) Number
            elif self.NUMBER.match( c ):
                yield self.process_literal_number()

### 4) String
            elif self.BEGIN_STRING.match( c ):
                yield self.process_literal_string()

### 5) One-line Comments (not a token: just throw away)
            elif self.BEGIN_COMMENT.match( c ) and self.next_char_is( self.BEGIN_COMMENT ):
                while c is not None and not self.TERMINATOR.match( c ):
                    c = self.next_char()

### 6) Combining prefix/suffix
            elif self.PREFIX.match( c ):
                str_buffer = c
                while ( self.next_char_is( self.SUFFIX ) ):
                    str_buffer += self.next_char()
                yield Token( 'OPERATOR', str_buffer )

### Everything Else
            else:
                yield Token( 'OPERATOR', c )
                
            c = self.next_char()