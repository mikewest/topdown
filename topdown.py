from tokenizer import Token, Tokenizer, TokenList
from tokenexceptions import *
import unittest

if __name__ == "__main__":
    class KnownValues( unittest.TestCase ):
        StringKnownValues = [
                                (
                                    '"xx\\\"x"', Token( 'STRING', 'xx\\"x' )
                                ),
                                (
                                    '"xx\\\"x"', Token( 'STRING', 'xx\\"x' )
                                ),
                                (
                                    '"xxx"', Token( 'STRING', 'xxx' )
                                )
                            ]
        NumberKnownValues = [
                                (
                                    '1', Token( 'NUMBER', '1' )
                                ),
                                (
                                    '1E10', Token( 'NUMBER', '1E10')
                                ),
                                (
                                    '1E+10', Token( 'NUMBER', '1E+10')
                                ),
                                (
                                    '1.32189E-10', Token( 'NUMBER', '1.32189E-10')
                                ),
                            ]
        OperatorKnownValues =   [
                                    ( '+', Token( 'OPERATOR', '+' ) ),
                                    ( '!', Token( 'OPERATOR', '!' ) ),
                                    ( '=', Token( 'OPERATOR', '=' ) ),
                                    ( '==', Token( 'OPERATOR', '==' ) ),
                                    ( '===', Token( 'OPERATOR', '===' ) ),
                                    ( '+&', Token( 'OPERATOR', '+&' ) )
                                ]
        
        
        IdentifierKnownValues = [
                                    (
                                        'identifier', Token( 'IDENTIFIER', 'identifier' )
                                    ),
                                    (
                                        'identifier01', Token( 'IDENTIFIER', 'identifier01' )
                                    ),
                                    (
                                        'ide_ntifi_er01', Token( 'IDENTIFIER', 'ide_ntifi_er01' )
                                    )
                                ]
        CommentKnownValues  =   [
                                    (
                                        '//xxx', None
                                    ),
                                    (
                                        '//xxx\n//xxx', None
                                    ),
                                    (
                                        '//xxx\n\n///xxx//xxx', None
                                    ),
                                ]
        ComplexKnownValues  =   [
                                    (
                                        '1+1',
                                        ( Token('NUMBER', '1'), Token( 'OPERATOR', '+' ), Token( 'NUMBER', '1' ) )
                                    ),
                                    (
                                        ' 1 + 1 ',
                                        ( Token('NUMBER', '1'), Token( 'OPERATOR', '+' ), Token( 'NUMBER', '1' ) )
                                    ),
                                    (
                                        'identifier + 1E10',
                                        ( Token( 'IDENTIFIER', 'identifier' ), Token( 'OPERATOR', '+' ), Token('NUMBER', '1E10' ) )
                                    ),
                                    (
                                        'identifier +// \n 1E10',
                                        ( Token( 'IDENTIFIER', 'identifier' ), Token( 'OPERATOR', '+' ), Token('NUMBER', '1E10' ) )
                                    ),
                                    (
                                        'identifier +//\r\n 1E10',
                                        ( Token( 'IDENTIFIER', 'identifier' ), Token( 'OPERATOR', '+' ), Token('NUMBER', '1E10' ) )
                                    ),
                                    (
                                        '1// this is a comment', Token( 'NUMBER', '1')
                                    ),
                                    (
                                        '1// this is a comment\n1', ( Token( 'NUMBER', '1'), Token( 'NUMBER', '1'), )
                                    ),
                                ]
                                
        def assertEqualTokens( self, a, b ):
            return self.assertEqual( TokenList( a ), b )
            
        def testTokenizerKnownStringValues( self ):
            """Tokenizer.tokenize should give known result with known input"""
            for string, tokens in self.StringKnownValues:
                result = Tokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result )
                
        def testTokenizerKnownNumberValues( self ):
            """Tokenizer.tokenize should give known result with known input"""
            for string, tokens in self.NumberKnownValues:
                result = Tokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result ) 
                
        def testTokenizerKnownOperatorValues( self ):
            """Tokenizer.tokenize should give known result with known input"""
            for string, tokens in self.OperatorKnownValues:
                result = Tokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result ) 
                
        def testTokenizerKnownIdentifierValues( self ):
            """Tokenizer.tokenize should give known result with known input"""
            for string, tokens in self.IdentifierKnownValues:
                result = Tokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result ) 
                
        def testTokenizerKnownComplexValues( self ):
            """Tokenizer.tokenize should give known result with known input"""
            for string, tokens in self.ComplexKnownValues:
                result = Tokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result ) 
        
        def testTokenizerKnownCommentValues( self ):
            """Tokenizer.tokenize should give known result with known input"""
            for string, tokens in self.CommentKnownValues:
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
    
        def testUnterminatedString( self ):
            """Tokenizer.tokenize should raise UnterminatedString"""
            self.assertTokenizingRaises( UnterminatedString, '"xxx')
            self.assertTokenizingRaises( UnterminatedString, '\'xxx')
            self.assertTokenizingRaises( UnterminatedString, '\'xxx\n')
            self.assertTokenizingRaises( UnterminatedString, '\'xxx\r\n')
    
    unittest.main()