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
        self.MULTILINE_COMMENT  =   re.compile("[\*]")
        self.END_COMMENT        =   re.compile("[/]")
        self.ESCAPE             =   re.compile("[\\\\]")
        
    def token_generator( self ):
### Begin processing the string, one character at a time.
        c = self.next_char()
        while ( c is not None ):
### 1) Whitespace
            if self.cur_char_is( self.WHITESPACE ):
                pass
                
### 2) Identifier
            elif self.cur_char_is( self.BEGIN_IDENTIFIER ):
                yield self.process_identifier()
                
### 3) Number
            elif self.cur_char_is( self.NUMBER ):
                yield self.process_literal_number()

### 4) String
            elif self.cur_char_is( self.BEGIN_STRING ):
                yield self.process_literal_string()

### 5) One-line Comments (not a token: just throw away)
            elif not self.prev_char_is( self.ESCAPE ) and self.cur_char_is( self.BEGIN_COMMENT ) and self.next_char_is( self.BEGIN_COMMENT ):
                while c is not None and not self.cur_char_is( self.TERMINATOR ):
                    c = self.next_char()

### 5a) Multi-line Comments (not a token, throw these away too)
            elif not self.prev_char_is( self.ESCAPE ) and self.cur_char_is( self.BEGIN_COMMENT ) and self.next_char_is( self.MULTILINE_COMMENT ):
                self.next_char()
                while c is not None and not ( self.cur_char_is( self.MULTILINE_COMMENT) and self.next_char_is( self.END_COMMENT ) ):
                    c = self.next_char()
                if self.cur_char_is( self.MULTILINE_COMMENT) and self.next_char_is( self.END_COMMENT ):
                    c = self.next_char();
                    
### 6) Combining prefix/suffix
            elif self.cur_char_is( self.PREFIX ):
                str_buffer = c
                while ( self.next_char_is( self.SUFFIX ) ):
                    str_buffer += self.next_char()
                yield Token( 'OPERATOR', str_buffer )

### Everything Else
            else:
                yield Token( 'OPERATOR', c )
                
            c = self.next_char()