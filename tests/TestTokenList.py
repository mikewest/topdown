import sys
sys.path.append('..')

from tokenizer import Token, TokenList
import unittest

if __name__ == "__main__":
    class TokenListTester( unittest.TestCase ):
        def testTokenListAppendSingle( self ):
            """TokenList.append should append a single Token correctly"""
            tokens      = TokenList()
            the_token   = Token( 'IDENTIFIER', 'x')
            tokens.append( the_token )
            self.assertEqual( the_token, tokens.next() )

        def testTokenListAppendList( self ):
            """TokenList.append should append a list correctly"""
            tokens      = TokenList()
            the_tokens  = [ Token( 'IDENTIFIER', 'first'), Token( 'IDENTIFIER', 'second' ) ]
            tokens.append( the_tokens )
            self.assertEqual( the_tokens[0], tokens.next() )
            self.assertEqual( the_tokens[1], tokens.next() )

        def testTokenListAppendTuple( self ):
            """TokenList.append should append a tuple correctly"""
            tokens      = TokenList()
            the_tokens  = ( Token( 'IDENTIFIER', 'first'), Token( 'IDENTIFIER', 'second' ) )
            tokens.append( the_tokens )
            self.assertEqual( the_tokens[0], tokens.next() )
            self.assertEqual( the_tokens[1], tokens.next() )

    unittest.main()