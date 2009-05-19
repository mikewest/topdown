from javascripttokenizer import JavaScriptTokenizer
from tokenexceptions import *

class SymbolBase( object ):
  id    = None
  value = None
  first = second = third = None
  
  def nud( self ):
    raise SyntaxError( 'Syntax Error ( %r )' % self.id )
  
  def led( self, left ):
    raise SyntaxError( 'Unknown Operator ( %r )' % self.id )
  
  def __repr__( self ):
    if self.id == "NUMBER" or self.id == "STRING" or self.id == "IDENTIFIER":
      return "(%s %s)" % ( self.id, self.value )
    out = [ self.id, self.first, self.second, self.third ]
    out = map( str, filter( None, out ) )
    return "(" + " ".join( out ) + ")"
  
class SymbolTable( object ):
  def __init__( self, parser ):
    self._table   = {}
    self._parser  = parser
    
    ### Generate symbols
    self.infix( '+', 10 )
    self.infix( '-', 10 )
    self.infix( '/', 20 )
    self.infix( '*', 20 )
    self.literal( 'NUMBER' )
    self.literal( 'STRING' )
    self.literal( 'IDENTIFIER' )
    self.new_symbol( 'END' )
  
  def get( self, id ):
    return self._table[ id ]
  
  def new_symbol( self, id, bp = 0 ):
    try:
      s = self._table[ id ]
    except KeyError:
      class s( SymbolBase ):
        pass
      s.__name__ = 'symbol-%s' % id
      s.id       = id
      s.lbp      = bp
      self._table[ id ] = s
    else:
      s.lbp      = max( bp, s.lbp )
    return s
  #
  #   Helpers for known types of Symbols
  #
  def infix( self, id, bp ):      # Left associative infix operators ( +, -, *, etc. )
    p = self._parser
    def led( self, left ):
      self.first  = left
      self.second = p.expression( bp )
      return self
    self.new_symbol( id, bp ).led = led
  
  def prefix( self, id, bp ):     # Prefix operators (!, +, -, etc.)
    p = self._parser
    def nud( self ):
      self.first  = p.expression( bp )
      self.second = None
      return self
    self.new_symbol( id, bp ).nud = nud
  
  def infix_r( self, id, bp ):    # Right associative infix operators
    p = self._parser
    def led( self, left ):
      self.first  = left
      self.second = p.expression( bp - 1 )
      return self
    self.new_symbol( id, bp ).led = led
  
  def literal( self, id ):    # Literals (strings, numbers, etc)
    def nud( self ):
      return self
    self.new_symbol( id ).nud = nud

class JavaScriptParser( object ):
    def __init__( self, string_to_parse ):
        self.string         = string_to_parse
        self.tokens         = JavaScriptTokenizer( string_to_parse ).tokenize()
        self.symbols        = SymbolTable( self )
        self.next()
        self.parse_tree     = self.expression()
#
#   Grab the next token, convert it to a symbol
#
    def next( self ):
      t = self.tokens.next()
      s = None
      if t is None:
        s = self.symbols.get( 'END' )()
      elif t.type is 'OPERATOR':
        s = self.symbols.get( t.value )()
      else:
        s = self.symbols.get( t.type )()
        s.value = t.value
      self.current_symbol = s

#
#   Expression is the core of the parser
#
    def expression( self, right_binding_power = 0 ):
        symbol              = self.current_symbol
        left                = symbol.nud()
        self.next()
        while right_binding_power < self.current_symbol.lbp:
            symbol              = self.current_symbol
            self.next()
            left                = symbol.led( left )

        
        return left

if __name__ == "__main__":
    
    print "Parser:"
    print "======="
    print
    p = JavaScriptParser('1 * 1')
    
    print "Parse Tree:"
    print "-----------"
    print p.parse_tree
    
    print "Generated Token List:"
    print "---------------------"
    print p.tokens