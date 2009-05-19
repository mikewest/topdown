import sys
sys.path.append('..')

from javascriptparser import JavaScriptParser
import unittest

class KnownExpressionValues( unittest.TestCase ):
  """Testing correct evaluation of simple expressions: single statements"""
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
  BitwiseKnownValues  = [
                          (
                            '1&2', '(& (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1^2', '(^ (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1|2', '(| (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1&&2', '(&& (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1||2', '(|| (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1>>2', '(>> (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1<<2', '(<< (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1>>>2', '(>>> (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1&2>>3', '(& (NUMBER 1) (>> (NUMBER 2) (NUMBER 3)))'
                          ),
                          (
                            '1>>>2|3>>4', '(| (>>> (NUMBER 1) (NUMBER 2)) (>> (NUMBER 3) (NUMBER 4)))'
                          ),
                          (
                            '1&&2|3>>4', '(&& (NUMBER 1) (| (NUMBER 2) (>> (NUMBER 3) (NUMBER 4))))'
                          ),
                          (
                            '1<<2^3||4', '(|| (^ (<< (NUMBER 1) (NUMBER 2)) (NUMBER 3)) (NUMBER 4))'
                          ),
                        ]
  TernaryKnownValues  = [
                          (
                            '1?2:3',      '(? (NUMBER 1) (NUMBER 2) (NUMBER 3))'
                          ),
                          (
                            '1?2:3>>4',   '(? (NUMBER 1) (NUMBER 2) (>> (NUMBER 3) (NUMBER 4)))'
                          ),
                          (
                            '1?2+3:4*5',  '(? (NUMBER 1) (+ (NUMBER 2) (NUMBER 3)) (* (NUMBER 4) (NUMBER 5)))'
                          ),
                        ]
  def testJavaScriptParserKnownSimpleValues( self ):
    """Parser.parse_tree should give known result with known input"""
    for string, tree in self.SimpleKnownValues:
      result = JavaScriptParser( string ).parse_tree
      self.assertEqualTree( tree, result )
      
  def testJavaScriptParserKnownBitwiseValues( self ):
    """Parser.parse_tree should give known result with known bitwise input"""
    for string, tree in self.BitwiseKnownValues:
      result = JavaScriptParser( string ).parse_tree
      self.assertEqualTree( tree, result )
      
  def testJavaScriptParserKnownTernaryValues( self ):
    """Parser.parse_tree should give known result with known ternary if structures"""
    for string, tree in self.TernaryKnownValues:
      result = JavaScriptParser( string ).parse_tree
      self.assertEqualTree( tree, result )

if __name__ == "__main__":
  unittest.main()

