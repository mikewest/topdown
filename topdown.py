class Tokenizer:
    """
        Given a string, Tokenizer provides an interface to iterate through
        it's tokens.
    """
    def __init__( self, string_to_tokenize = '' ):
        self.original   =   string_to_tokenize
        self.current    =   0
    
    def tokenize( self ):
        return [ self.original ]
        
    
        
if __name__ == "__main__":
   t = Tokenizer('1 + 1')
   
   print "Tokenize Results:"
   print "-----------------"
   print t.tokenize()
   