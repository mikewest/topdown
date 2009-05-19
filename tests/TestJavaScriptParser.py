import sys
sys.path.append('..')

from javascriptparser import JavaScriptParser
import unittest

class KnownValues( unittest.TestCase ):
  def assertEqualTree( self, expected, result ):
    self.assertEqual( expected, str( result ) )
  
  SimpleKnownValues = [
                        (
                          '1+2', '(+ (NUMBER 1) (NUMBER 2))'
                        ),
                        (
                          '1-2', '(- (NUMBER 1) (NUMBER 2))'
                        ),
                        (
                          '1*2', '(* (NUMBER 1) (NUMBER 2))'
                        ),
                        (
                          '1/2', '(/ (NUMBER 1) (NUMBER 2))'
                        ),
                        (
                          '1+2*3', '(+ (NUMBER 1) (* (NUMBER 2) (NUMBER 3)))'
                        ),
                        (
                          '1+2/3', '(+ (NUMBER 1) (/ (NUMBER 2) (NUMBER 3)))'
                        ),
                        (
                          '1*2/3', '(/ (* (NUMBER 1) (NUMBER 2)) (NUMBER 3))'
                        )
                      ]
  def testJavaScriptParserKnownSimpleValues( self ):
    """Parser.parse_tree should give known result with known input"""
    for string, tree in self.SimpleKnownValues:
      result = JavaScriptParser( string ).parse_tree
      self.assertEqualTree( tree, result )

if __name__ == "__main__":
  unittest.main()

