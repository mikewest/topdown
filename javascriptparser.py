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
    if self.id == "(NUMBER)" or self.id == "(STRING)" or self.id == "(IDENTIFIER)":
      return "(%s %s)" % ( self.id[ 1:-1 ], self.value )
    elif self.id == "(OBJECT)":
      return "(%s %s)" % ( self.id[ 1:-1 ], self.first )
    out = [ '`%s`' % self.id, self.first, self.second, self.third ]
    out = map( str, filter( None, out ) )
    return "(" + " ".join( out ) + ")"
  
class SymbolTable( object ):
  def __init__( self, parser ):
    self._table   = {}
    self._parser  = parser
    
### Generate operator symbols
    
    #####################################################################(150)
    # call, member
    def led( self, left ):
      self.first  = left
      if parser.current_symbol.type != '(IDENTIFIER)':
        raise SyntaxError( 'Expected identifier, got `%r`' % parser.current_symbol )
      self.second = parser.current_symbol
      parser.next()
      return self
    self.infix(   '.',    150, led=led )
    
    def led( self, left ):
      self.first  = left
      self.second = parser.expression()
      parser.next( ']' )
      return self
    self.infix(   '[',    150, led=led )
    
    def nud( self ):
      expr = parser.expression()
      parser.next( ')' )
      return expr
    def led( self, left ):
      self.first  = left
      self.second = []
      if parser.current_symbol.id != ')':
        while 1:
          self.second.append( parser.expression( 10 ) ) # "," has a bp of 10
          if ( parser.current_symbol.id != ',' ):
            break
          parser.next( ',' )
      parser.next( ')' )
      return self
    self.new_symbol(  '(',    150, nud=nud, led=led )
    
    def nud( self ):
      self.id     = '(OBJECT)'
      self.first  = []
      if parser.current_symbol.id != '}':
        while 1:
          a = parser.expression( 10 )
          parser.next( ':' )
          b = parser.expression( 10 )
          self.first.append( ( a, b ) )
          if ( parser.current_symbol.id != ',' ):
            break
          parser.next( ',' )
      parser.next( '}' )
      return self
    self.new_symbol(  '{', 150, nud=nud )
    
    #####################################################################(140)
    # negation/increment
    self.prefix(  '++',   140 )  # Pre-increment
    self.prefix(  '--',   140 )  # Pre-decrement
    self.prefix(  '!',    140 )  # Boolean negation
    self.prefix(  '~',    140 )  # Bitwise complement
    self.prefix(  '-',    140 )  # Unary negation
    self.prefix(  '+',    140 )  # Unary posation (not a word.  :) )
    
    #####################################################################(130)
    # multiply/divide
    self.infix(   '*',    130 )  # Multiplication
    self.infix(   '/',    130 )  # Division
    self.infix(   '%',    130 )  # Modulus
    
    #####################################################################(120)
    # addition/subtraction
    self.infix(   '+',    120 )  # Addition
    self.infix(   '-',    120 )  # Subtraction
    
    #####################################################################(110)
    # bitwise shift
    self.infix(   '<<',   110 )  # left shift
    self.infix(   '>>',   110 )  # right shift
    self.infix(   '>>>',  110 )  # right shift, zero filled
    
    #####################################################################(100)
    # relational
    self.infix(   '<',    100 )  # less than
    self.infix(   '>',    100 )  # greater than
    self.infix(   '<=',   100 )  # less than or equal to
    self.infix(   '>=',   100 )  # greater than or equal to
    
    #####################################################################( 90)
    # equality
    self.infix(   '==',   90  ) # equal to
    self.infix(   '!=',   90  ) # not equal to
    self.infix(   '===',  90  ) # strictly equal to
    self.infix(   '!==',  90  ) # not strictly equal to
    
    #####################################################################( 80)
    # bitwise and
    self.infix(   '&',    80  ) # bitwise and
    
    #####################################################################( 70)
    # bitwise xor ^
    self.infix(   '^',    70  ) # bitwise xor
    
    #####################################################################( 60)
    # bitwise or  |
    self.infix(   '|',    60  ) # bitwise or
    
    #####################################################################( 50)
    # logical and &&
    self.infix(   '&&',   50  ) # logical and
    
    #####################################################################( 40)
    # logical or  ||
    self.infix(   '||',   40  ) # logical or
    
    #####################################################################( 30)
    # conditional ?:
    def led( self, left ):
      self.first  = left
      self.second = parser.expression( 0 )
      parser.next( ':' )
      self.third  = parser.expression( 0 )
      return self
    self.new_symbol( '?', 30, led=led )
    

    #####################################################################( 20)
    # assignment  = += -= *= /= %= <<= >>= >>>= &= ^= |=
    self.infix(   '=',    20  ) # simple assignment
    self.infix(   '+=',   20  ) # addition assignment
    self.infix(   '-=',   20  ) # subtraction assignment
    self.infix(   '*=',   20  ) # multiplication assignment
    self.infix(   '/=',   20  ) # division assignment
    self.infix(   '<<=',  20  ) # left shifty assignment
    self.infix(   '>>=',  20  ) # right shifty assignment
    self.infix(   '>>>=', 20  ) # right shifty assignment with zero fill
    self.infix(   '&=',   20  ) # bitwise and assignment
    self.infix(   '^=',   20  ) # bitwise xor assignment
    self.infix(   '|=',   20  ) # bitwise or assignment
    
    #####################################################################( 10)
    # statement seperators, closers
    self.infix(   ',',    10  ) # comma
    self.new_symbol( ';' )
    self.new_symbol( ':' )
    self.new_symbol( '}' )
    self.new_symbol( ')' )
    self.new_symbol( ']' )
    self.new_symbol( 'else' )
    
    
### Generate literal symbols
    self.literal( '(NUMBER)' )
    self.literal( '(STRING)' )
    self.literal( '(IDENTIFIER)' )

### End!
    self.new_symbol( ';' )
    self.new_symbol( '(END)' )
  
  def get( self, id ):
    return self._table[ id ]
  
  def new_symbol( self, id, bp = 0, nud = None, led = None ):
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
    
    if nud is not None:
      s.nud = nud
    if led is not None:
      s.led = led
    
    return s
  #
  #   Helpers for known types of Symbols
  #
  def infix( self, id, bp, nud=None, led=None ):      # Left associative infix operators ( +, -, *, etc. )
    if led is None:
      p = self._parser
      if led is None:
        def led( self, left ):
          self.first  = left
          self.second = p.expression( bp )
          return self
    self.new_symbol( id, bp, nud, led )
  
  def prefix( self, id, bp, nud=None, led=None ):     # Prefix operators (!, +, -, etc.)
    if nud is None:
      p = self._parser
      def nud( self ):
        self.first  = p.expression( bp )
        self.second = None
        return self
    self.new_symbol( id, bp, nud, led )
  
  def infix_r( self, id, bp, nud=None, led=None ):    # Right associative infix operators
    if led is None:
      p = self._parser
      def led( self, left ):
        self.first  = left
        self.second = p.expression( bp - 1 )
        return self
    self.new_symbol( id, bp, nud, led )
  
  def literal( self, id, nud=None, led=None  ):    # Literals (strings, numbers, etc)
    if nud is None:
      def nud( self ):
        return self
    self.new_symbol( id, 0, nud, led )

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
    def next( self, id = None ):
      if ( id is not None and self.current_symbol.id != id ):
        raise SyntaxError( 'Expected `%r`, got `%r`' % ( id, self.current_symbol.id ) )
      
      t = self.tokens.next()
      s = None
      if t is None:
        s = self.symbols.get( '(END)' )()
      elif t.type == '(OPERATOR)':
        s = self.symbols.get( t.value )()
        s.type  = t.type
      else:
        s       = self.symbols.get( t.type )()
        s.value = t.value
        s.type  = t.type
      self.current_symbol = s

#
#   Expression is the core of the parser
#
    def expression( self, right_binding_power = 0 ):
        symbol              = self.current_symbol
        self.next()
        left                = symbol.nud()
        while right_binding_power < self.current_symbol.lbp:
            symbol              = self.current_symbol
            self.next()
            left                = symbol.led( left )

        
        return left

if __name__ == "__main__":
    
    print "Parser:"
    print "======="
    print
    p = JavaScriptParser('1 ; 1 ;')
    
    print "Parse Tree:"
    print "-----------"
    print p.parse_tree
    
    print "Generated Token List:"
    print "---------------------"
    print p.tokens