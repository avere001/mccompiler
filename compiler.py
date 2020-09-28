from lark import Lark, Transformer
from assembler import assemble


class MCTransformer(Transformer):
    bindings = {}
    def defs(self, items):
        print(items)
    
    def params(self, items):
        return list(map(str, items))



def parse(source):
    parser = Lark.open('minecraft.lark', rel_to=__file__, parser='lalr', start='program', transformer=MCTransformer())
    tree = parser.parse(open(source).read())
    #print(tree.pretty())
    return tree


result = parse("example.minecraft")
print(result)


