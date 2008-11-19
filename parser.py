from tokenizer import Token, Tokenizer, TokenList
from tokenexceptions import *

class UndefinedFunction( Exception ):
    pass
class MissingOperator( Exception ):
    pass

class BaseSymbol( object ):
    def __init__( self, symbol_id, left_binding_power = 0):
        self.id     = self.value = symbol_id
        self.lbp    = left_binding_power
        
    def nud( self ):
        raise UndefinedFunction
        
    def led( self, left ):
        raise MissingOperator
        

class SymbolTable( object ):
    def __init__( self ):
        self.__table = {}

    

class Parser( object ):
    def __init__( self, string_to_parse ):
        self.string         = string_to_parse
        self.tokens         = Tokenizer( string_to_parse ).tokenize()
        self.current_token  = self.tokens.next()
        self.symbols        = SymbolTable()

    def expression( right_binding_power = 0 ):
        token               = self.current_token
        self.current_token  = self.tokens.next()
        left                = token.nud()

        while right_binding_power < self.current_token.lbp:
            token               = self.current_token
            self.current_token  = next()
            left                = token.led( left )
        
        return left

if __name__ == "__main__":
    
    print "Parser:"
    print "======="
    print
    p = Parser('1 + 1')
    
    print "Generated Token List:"
    print "---------------------"
    print p.tokens