import sys
sys.path.append('..')

from tokenizer import Token, TokenList
from csstokenizer import CSSTokenizer
from tokenexceptions import *
import unittest

if __name__ == "__main__":
    class KnownValues( unittest.TestCase ):
        IdentifierKnownValues = [
                                    (
                                        '#id', Token( 'ID', 'id' )
                                    ),
                                    (
                                        '.class', Token( 'CLASS', 'class' )
                                    ),
                                    (
                                        '#id .class', ( Token( 'ID', 'id' ), Token( 'CLASS', 'class' ) )
                                    ),
                                    (
                                        '#id .class :focus', ( Token( 'ID', 'id' ), Token( 'CLASS', 'class' ), Token( 'PSEUDOCLASS', 'focus' ) )
                                    ),
                                    (
                                        '#id .class:visited', ( Token( 'ID', 'id' ), Token( 'CLASS', 'class' ), Token( 'PSEUDOCLASS', 'visited' ) )
                                    ),
                                ]

        ComplexKnownValues  =   [
                                    (
                                        '#id, .class', ( Token( 'ID', 'id' ), Token('OPERATOR', ','), Token( 'CLASS', 'class' ) )
                                    ),
                                    (
                                        '#id, .class { }', ( Token( 'ID', 'id' ), Token('OPERATOR', ','), Token( 'CLASS', 'class' ), Token('OPERATOR', '{'), Token('OPERATOR', '}') )
                                    ),
                                    
                                ]
        def assertEqualTokens( self, a, b ):
            return self.assertEqual( TokenList( a ), b )
            
        def __loop_through_values( self, the_list ):
            for string, tokens in the_list:
                result = CSSTokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result )            
            
        def testCSSTokenizerKnownIdentifierValues( self ):
            """CSSTokenizer.tokenize should give known result with known input"""
            self.__loop_through_values( self.IdentifierKnownValues )
                
        def testCSSTokenizerKnownComplexValues( self ):
            """CSSTokenizer.tokenize should give known result with known input"""
            self.__loop_through_values( self.ComplexKnownValues )
            
    unittest.main()