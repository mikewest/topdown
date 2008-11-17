from tokenizer import Token, Tokenizer
from tokenexceptions import *
import unittest

if __name__ == "__main__":
    class KnownValues( unittest.TestCase ):
        KnownValues =   [
                            (
                                '1', Token( 'NUMBER', '1' )
                            ),
                            (
                                'identifier', Token( 'IDENTIFIER', 'identifier' )
                            ),
                            (
                                'identifier01', Token( 'IDENTIFIER', 'identifier01' )
                            ),
                            (
                                'ide_ntifi_er01', Token( 'IDENTIFIER', 'ide_ntifi_er01' )
                            ),
                            (
                                '1+1',
                                ( Token('NUMBER', '1'), Token( 'OPERATOR', '+' ), Token( 'NUMBER', '1' ) )
                            ),
                            (
                                ' 1 + 1 ',
                                ( Token('NUMBER', '1'), Token( 'OPERATOR', '+' ), Token( 'NUMBER', '1' ) )
                            ),
                            (
                                'identifier + 1E10', ( Token( 'IDENTIFIER', 'identifier' ), Token( 'OPERATOR', '+' ), Token('NUMBER', '1E10' ) )
                            ),
                        ]
        def to_str( self, the_tokens ):
            if isinstance( the_tokens, Token ):
                return '%s' % ( the_tokens )
            else:
                return ''.join( [ '%s' % ( token ) for token in the_tokens ] )
        
        def assertEqualTokens( self, a, b ):
            return self.assertEqual( self.to_str( a ), self.to_str( b ) )

        def testTokenizerKnownValues( self ):
            """Tokenizer.tokenize should give known result with known input"""
            for string, tokens in self.KnownValues:
                result = Tokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result ) 
    
    class KnownExceptions( unittest.TestCase ):
        def assertTokenizingRaises( self, exception, string ):
            tokenizer = Tokenizer( string )
            return self.assertRaises( exception, tokenizer.tokenize )
        
        def testNumberBadExponent( self ):
            """Tokenizer.tokenize should raise NumberBadExponent"""
            self.assertTokenizingRaises( NumberBadExponent, '1e')
            self.assertTokenizingRaises( NumberBadExponent, '1ex')
            self.assertTokenizingRaises( NumberBadExponent, '1E')
            self.assertTokenizingRaises( NumberBadExponent, '1EX')
            self.assertTokenizingRaises( NumberBadExponent, '1Ex')
            self.assertTokenizingRaises( NumberBadExponent, '1eX')
            self.assertTokenizingRaises( NumberBadExponent, '1.134eX')
            self.assertTokenizingRaises( NumberBadExponent, '1.0eX')
        
        def testNumberFollowedByCharacter( self ):
            """Tokenizer.tokenize should raise NumberFollowedByCharacter"""
            self.assertTokenizingRaises( NumberFollowedByCharacter, '1x')
            self.assertTokenizingRaises( NumberFollowedByCharacter, '9000x097')
            self.assertTokenizingRaises( NumberFollowedByCharacter, '12.34fs')
    
    unittest.main()