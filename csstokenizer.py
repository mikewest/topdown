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
### Throwing everything away after reading through the CSS spec.
### I ought be using the specified tokens, so I will.
# IDENT {ident}
# ATKEYWORD @{ident}
# STRING    {string}
# INVALID   {invalid}
# HASH  #{name}
# NUMBER    {num}
# PERCENTAGE    {num}%
# DIMENSION {num}{ident}
# URI   url\({w}{string}{w}\)
# |url\({w}([!#$%&*-~]|{nonascii}|{escape})*{w}\)
# UNICODE-RANGE U\+[0-9a-f?]{1,6}(-[0-9a-f]{1,6})?
# CDO   <!--
# CDC   -->
# ; ;
# { \{
# } \}
# ( \(
# ) \)
# [ \[
# ] \]
# S [ \t\r\n\f]+
# COMMENT   \/\*[^*]*\*+([^/*][^*]*\*+)*\/
# FUNCTION  {ident}\(
# INCLUDES  ~=
# DASHMATCH |=
# DELIM any other character not matched by the above rules, and neither a single nor a double quote
# 
# 
# ident [-]?{nmstart}{nmchar}*
# name  {nmchar}+
# nmstart   [_a-z]|{nonascii}|{escape}
# nonascii  [^\0-\177]
# unicode   \\[0-9a-f]{1,6}(\r\n|[ \n\r\t\f])?
# escape    {unicode}|\\[^\n\r\f0-9a-f]
# nmchar    [_a-z0-9-]|{nonascii}|{escape}
# num   [0-9]+|[0-9]*\.[0-9]+
# string    {string1}|{string2}
# string1   \"([^\n\r\f\\"]|\\{nl}|{escape})*\"
# string2   \'([^\n\r\f\\']|\\{nl}|{escape})*\'
# invalid   {invalid1}|{invalid2}
# invalid1  \"([^\n\r\f\\"]|\\{nl}|{escape})*
# invalid2  \'([^\n\r\f\\']|\\{nl}|{escape})*
# nl    \n|\r\n|\r|\f
# w [ \t\r\n\f]*