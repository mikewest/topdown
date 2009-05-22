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
                          '1+2', '(`+` (NUMBER 1) (NUMBER 2))'
                        ),
                        (
                          '1-2', '(`-` (NUMBER 1) (NUMBER 2))'
                        ),
                        (
                          '1*2', '(`*` (NUMBER 1) (NUMBER 2))'
                        ),
                        (
                          '1/2', '(`/` (NUMBER 1) (NUMBER 2))'
                        ),
                        (
                          '1+2*3', '(`+` (NUMBER 1) (`*` (NUMBER 2) (NUMBER 3)))'
                        ),
                        (
                          '1+2/3', '(`+` (NUMBER 1) (`/` (NUMBER 2) (NUMBER 3)))'
                        ),
                        (
                          '1*2/3', '(`/` (`*` (NUMBER 1) (NUMBER 2)) (NUMBER 3))'
                        )
                      ]
  BitwiseKnownValues  = [
                          (
                            '1&2', '(`&` (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1^2', '(`^` (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1|2', '(`|` (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1&&2', '(`&&` (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1||2', '(`||` (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1>>2', '(`>>` (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1<<2', '(`<<` (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1>>>2', '(`>>>` (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '1&2>>3', '(`&` (NUMBER 1) (`>>` (NUMBER 2) (NUMBER 3)))'
                          ),
                          (
                            '1>>>2|3>>4', '(`|` (`>>>` (NUMBER 1) (NUMBER 2)) (`>>` (NUMBER 3) (NUMBER 4)))'
                          ),
                          (
                            '1&&2|3>>4', '(`&&` (NUMBER 1) (`|` (NUMBER 2) (`>>` (NUMBER 3) (NUMBER 4))))'
                          ),
                          (
                            '1<<2^3||4', '(`||` (`^` (`<<` (NUMBER 1) (NUMBER 2)) (NUMBER 3)) (NUMBER 4))'
                          ),
                        ]
  TernaryKnownValues  = [
                          (
                            '1?2:3',      '(`?` (NUMBER 1) (NUMBER 2) (NUMBER 3))'
                          ),
                          (
                            '1?2:3>>4',   '(`?` (NUMBER 1) (NUMBER 2) (`>>` (NUMBER 3) (NUMBER 4)))'
                          ),
                          (
                            '1?2+3:4*5',  '(`?` (NUMBER 1) (`+` (NUMBER 2) (NUMBER 3)) (`*` (NUMBER 4) (NUMBER 5)))'
                          ),
                        ]
  ParenKnownValues    = [
                          (
                            '(1+2)',  '(`+` (NUMBER 1) (NUMBER 2))'
                          ),
                          (
                            '(1+2)*3', '(`*` (`+` (NUMBER 1) (NUMBER 2)) (NUMBER 3))'
                          ),
                          (
                            '(1+2)/3', '(`/` (`+` (NUMBER 1) (NUMBER 2)) (NUMBER 3))'
                          ),
                          (
                            '1*(2/3)', '(`*` (NUMBER 1) (`/` (NUMBER 2) (NUMBER 3)))'
                          ),
                          (
                            'a(b)',    '(`(` (IDENTIFIER a) [(IDENTIFIER b)])'
                          ),
                          (
                            'a(b,c,d)',    '(`(` (IDENTIFIER a) [(IDENTIFIER b), (IDENTIFIER c), (IDENTIFIER d)])'
                          )
                        ]
  CallKnownValues     = [
                          (
                            'a.b',              '(`.` (IDENTIFIER a) (IDENTIFIER b))'
                          ),
                          (
                            'a.b(c)',           '(`(` (`.` (IDENTIFIER a) (IDENTIFIER b)) [(IDENTIFIER c)])'
                          ),
                          (
                            'a.b.c.d',          '(`.` (`.` (`.` (IDENTIFIER a) (IDENTIFIER b)) (IDENTIFIER c)) (IDENTIFIER d))'
                          ),
                          (
                            'a["b"]',           '(`[` (IDENTIFIER a) (STRING b))'
                          ),
                          (
                            'a["b"]["c"]',      '(`[` (`[` (IDENTIFIER a) (STRING b)) (STRING c))'
                          ),
                          (
                            'a["b"](c)',        '(`(` (`[` (IDENTIFIER a) (STRING b)) [(IDENTIFIER c)])'
                          ),
                          (
                            'a[ 1 + 2 + "b" ]', '(`[` (IDENTIFIER a) (`+` (NUMBER 1) (`+` (NUMBER 2) (STRING b))))'
                          ),
                          (
                            ### Thanks to jQuery for this appalling example
                            'e[ val == "toggle" ? hidden ? "show" : "hide" : val ]( param )', '(`(` (`[` (IDENTIFIER e) (`?` (`==` (IDENTIFIER val) (STRING toggle)) (`?` (IDENTIFIER hidden) (STRING show) (STRING hide)) (IDENTIFIER val))) [(IDENTIFIER param)])'
                          )
                        ]
  JSONKnownValues     = [
                          (
                            '{"a": "b"}',           '(`{` [((STRING a), (STRING b))])'
                          ),
                          (
                            '{"a": "b", "c": "d"}', '(`{` [((STRING a), (STRING b)), ((STRING c), (STRING d))])'
                          ),
                          (
                            '{"a": "b", "c": {"d": "e"}}', '(`{` [((STRING a), (STRING b)), ((STRING c), (`{` [((STRING d), (STRING e))]))])'
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
  
  def testJavaScriptParserKnownParenValues( self ):
    """Parser.parse_tree should give known result with known parenthisized structures"""
    for string, tree in self.ParenKnownValues:
      result = JavaScriptParser( string ).parse_tree
      self.assertEqualTree( tree, result )

  def testJavaScriptParserKnownCallValues( self ):
    """Parser.parse_tree should give known result with known call structures"""
    for string, tree in self.CallKnownValues:
      result = JavaScriptParser( string ).parse_tree
      self.assertEqualTree( tree, result )

  def testJavaScriptParserKnownJSONValues( self ):
    """Parser.parse_tree should give known result with known JSON structures"""
    for string, tree in self.JSONKnownValues:
      result = JavaScriptParser( string ).parse_tree
      self.assertEqualTree( tree, result )
      
if __name__ == "__main__":
  unittest.main()

