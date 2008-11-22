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
                                        '#id, .class', ( Token( 'ID', 'id' ), Token('OPERATOR', ','), Token( 'CLASS', 'class' ) )
                                    ),
                                    (
                                        '#id, .class { }', ( Token( 'ID', 'id' ), Token('OPERATOR', ','), Token( 'CLASS', 'class' ), Token('OPERATOR', '{'), Token('OPERATOR', '}') )
                                    )
                                ]
        def assertEqualTokens( self, a, b ):
            return self.assertEqual( TokenList( a ), b )
            
        def testCSSTokenizerKnownIdentifierValues( self ):
            """CSSTokenizer.tokenize should give known result with known input"""
            for string, tokens in self.IdentifierKnownValues:
                result = CSSTokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result )
                
    unittest.main()