import sys
sys.path.append('..')

from tokenizer import Token, TokenList
from csstokenizer import CSSTokenizer
from tokenexceptions import *
import unittest

if __name__ == "__main__":
    class KnownValues( unittest.TestCase ):
        WHITESPACE = Token( 'WHITESPACE', None )
        IdentifierKnownValues = [
                                    (
                                        '#id', Token( 'ID', 'id' )
                                    ),
                                    (
                                        '.class', Token( 'CLASS', 'class' )
                                    ),
                                    (
                                        '#id .class', ( Token( 'ID', 'id' ), WHITESPACE, Token( 'CLASS', 'class' ) )
                                    ),
                                    (
                                        '#id .class :focus', ( Token( 'ID', 'id' ), WHITESPACE, Token( 'CLASS', 'class' ), WHITESPACE, Token( 'PSEUDOCLASS', 'focus' ) )
                                    ),
                                    (
                                        '#id .class:visited', ( Token( 'ID', 'id' ), WHITESPACE, Token( 'CLASS', 'class' ), Token( 'PSEUDOCLASS', 'visited' ) )
                                    ),
                                ]

        ComplexKnownValues  =   [
                                    (
                                        '#id, .class', ( Token( 'ID', 'id' ), Token('OPERATOR', ','), WHITESPACE, Token( 'CLASS', 'class' ) )
                                    ),
                                    (
                                        '#id, .class { }', ( Token( 'ID', 'id' ), Token('OPERATOR', ','), WHITESPACE, Token( 'CLASS', 'class' ), WHITESPACE, Token('OPERATOR', '{'), WHITESPACE, Token('OPERATOR', '}') )
                                    ),
                                    (
                                        '#id, .class { xxx }', ( Token( 'ID', 'id' ), Token('OPERATOR', ','), WHITESPACE, Token( 'CLASS', 'class' ), WHITESPACE, Token('OPERATOR', '{'), WHITESPACE, Token('IDENTIFIER', 'xxx'), WHITESPACE, Token('OPERATOR', '}') )
                                    ),
                                    
                                ]
        def assertEqualTokens( self, a, b ):
            return self.assertEqual( TokenList( a ), b )
            
        def __loop_through_values( self, the_list ):
            for string, tokens in the_list:
                result = CSSTokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result )            
            
        def testCSSTokenizerKnownIdentifierValues( self ):
            """CSSTokenizer.tokenize should give known result with known Identifier input"""
            self.__loop_through_values( self.IdentifierKnownValues )
                
        def testCSSTokenizerKnownComplexValues( self ):
            """CSSTokenizer.tokenize should give known result with known Complex input"""
            self.__loop_through_values( self.ComplexKnownValues )
            
    unittest.main()