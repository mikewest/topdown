import sys
sys.path.append('..')

from tokenizer import Token, TokenList
from javascripttokenizer import JavaScriptTokenizer
from tokenexceptions import *
import unittest

if __name__ == "__main__":
    class KnownValues( unittest.TestCase ):
        StringKnownValues = [
                                (
                                    '"xx\\\"x"', Token( '(STRING)', 'xx\\"x' )
                                ),
                                (
                                    '"xx\\\"x"', Token( '(STRING)', 'xx\\"x' )
                                ),
                                (
                                    '"xxx"', Token( '(STRING)', 'xxx' )
                                )
                            ]
        NumberKnownValues = [
                                (
                                    '1', Token( '(NUMBER)', '1' )
                                ),
                                (
                                    '1E10', Token( '(NUMBER)', '1E10')
                                ),
                                (
                                    '1E+10', Token( '(NUMBER)', '1E+10')
                                ),
                                (
                                    '1.32189E-10', Token( '(NUMBER)', '1.32189E-10')
                                ),
                            ]
        OperatorKnownValues =   [
                                    ( '+', Token( '(OPERATOR)', '+' ) ),
                                    ( '!', Token( '(OPERATOR)', '!' ) ),
                                    ( '=', Token( '(OPERATOR)', '=' ) ),
                                    ( '==', Token( '(OPERATOR)', '==' ) ),
                                    ( '===', Token( '(OPERATOR)', '===' ) ),
                                    ( '+&', Token( '(OPERATOR)', '+&' ) )
                                ]
        
        
        IdentifierKnownValues = [
                                    (
                                        'identifier', Token( '(IDENTIFIER)', 'identifier' )
                                    ),
                                    (
                                        'identifier01', Token( '(IDENTIFIER)', 'identifier01' )
                                    ),
                                    (
                                        'ide_ntifi_er01', Token( '(IDENTIFIER)', 'ide_ntifi_er01' )
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
                                        ( Token('(NUMBER)', '1'), Token( '(OPERATOR)', '+' ), Token( '(NUMBER)', '1' ) )
                                    ),
                                    (
                                        ' 1 + 1 ',
                                        ( Token('(NUMBER)', '1'), Token( '(OPERATOR)', '+' ), Token( '(NUMBER)', '1' ) )
                                    ),
                                    (
                                        'identifier + 1E10',
                                        ( Token( '(IDENTIFIER)', 'identifier' ), Token( '(OPERATOR)', '+' ), Token('(NUMBER)', '1E10' ) )
                                    ),
                                    (
                                        'identifier +// \n 1E10',
                                        ( Token( '(IDENTIFIER)', 'identifier' ), Token( '(OPERATOR)', '+' ), Token('(NUMBER)', '1E10' ) )
                                    ),
                                    (
                                        'identifier +//\r\n 1E10',
                                        ( Token( '(IDENTIFIER)', 'identifier' ), Token( '(OPERATOR)', '+' ), Token('(NUMBER)', '1E10' ) )
                                    ),
                                    (
                                        '1// this is a comment', Token( '(NUMBER)', '1')
                                    ),
                                    (
                                        '1// this is a comment\n1', ( Token( '(NUMBER)', '1'), Token( '(NUMBER)', '1'), )
                                    ),
                                ]
                                
        def assertEqualTokens( self, a, b ):
            return self.assertEqual( TokenList( a ), b )
            
        def testJavaScriptTokenizerKnownStringValues( self ):
            """JavaScriptTokenizer.tokenize should give known result with known input"""
            for string, tokens in self.StringKnownValues:
                result = JavaScriptTokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result )
                
        def testJavaScriptTokenizerKnownNumberValues( self ):
            """JavaScriptTokenizer.tokenize should give known result with known input"""
            for string, tokens in self.NumberKnownValues:
                result = JavaScriptTokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result ) 
                
        def testJavaScriptTokenizerKnownOperatorValues( self ):
            """JavaScriptTokenizer.tokenize should give known result with known input"""
            for string, tokens in self.OperatorKnownValues:
                result = JavaScriptTokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result ) 
                
        def testJavaScriptTokenizerKnownIdentifierValues( self ):
            """JavaScriptTokenizer.tokenize should give known result with known input"""
            for string, tokens in self.IdentifierKnownValues:
                result = JavaScriptTokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result ) 
                
        def testJavaScriptTokenizerKnownComplexValues( self ):
            """JavaScriptTokenizer.tokenize should give known result with known input"""
            for string, tokens in self.ComplexKnownValues:
                result = JavaScriptTokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result ) 
        
        def testJavaScriptTokenizerKnownCommentValues( self ):
            """JavaScriptTokenizer.tokenize should give known result with known input"""
            for string, tokens in self.CommentKnownValues:
                result = JavaScriptTokenizer( string ).tokenize()
                self.assertEqualTokens( tokens, result ) 
    
    
    class KnownExceptions( unittest.TestCase ):
        def assertTokenizingRaises( self, exception, string ):
            tokenizer = JavaScriptTokenizer( string )
            return self.assertRaises( exception, tokenizer.tokenize )
        
        def testNumberBadExponent( self ):
            """JavaScriptTokenizer.tokenize should raise NumberBadExponent"""
            self.assertTokenizingRaises( NumberBadExponent, '1e')
            self.assertTokenizingRaises( NumberBadExponent, '1ex')
            self.assertTokenizingRaises( NumberBadExponent, '1E')
            self.assertTokenizingRaises( NumberBadExponent, '1EX')
            self.assertTokenizingRaises( NumberBadExponent, '1Ex')
            self.assertTokenizingRaises( NumberBadExponent, '1eX')
            self.assertTokenizingRaises( NumberBadExponent, '1.134eX')
            self.assertTokenizingRaises( NumberBadExponent, '1.0eX')
        
        def testNumberFollowedByCharacter( self ):
            """JavaScriptTokenizer.tokenize should raise NumberFollowedByCharacter"""
            self.assertTokenizingRaises( NumberFollowedByCharacter, '1x')
            self.assertTokenizingRaises( NumberFollowedByCharacter, '9000x097')
            self.assertTokenizingRaises( NumberFollowedByCharacter, '12.34fs')
    
        def testUnterminatedString( self ):
            """JavaScriptTokenizer.tokenize should raise UnterminatedString"""
            self.assertTokenizingRaises( UnterminatedString, '"xxx')
            self.assertTokenizingRaises( UnterminatedString, '\'xxx')
            self.assertTokenizingRaises( UnterminatedString, '\'xxx\n')
            self.assertTokenizingRaises( UnterminatedString, '\'xxx\r\n')
    
    unittest.main()