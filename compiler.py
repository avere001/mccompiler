from lark import Lark, Transformer
from assembler import assemble

        

    

def assign(var0, var1):
    namespace0="vars"
    namespace1='vars'
    return "U scoreboard players operation {} {} = {} {}".format(var0,namespace0, var1, namespace1)

def const_assign(var, val):
    namespace="vars"
    return "U scoreboard players set {} {} {}".format(var, namespace, val)

def compare(a, op, b, cond_var):
   namespace="vars"
   default_false = [ f"U scoreboard players set {cond_var} vars 0" ]
   case_true = [ "U execute if score {} vars {} {} vars run scoreboard players set {} vars 1 ".format(a,op,b, cond_var) ]
   return default_false + case_true

def compile(tree):
   
   #If we hit a base token 
   if str(type(tree)) == "<class 'lark.lexer.Token'>":
       return [str(tree)]

   if tree.data == "program":
       program = []
       for child in tree.children:
         program += compile(child)
       return program
   if tree.data == "defs":
       name, params, body = tree.children
       return [".{}:".format(name)] + compile(params) + compile(body)

   if tree.data == "params":
      return [ assign(str(p), "param"+str(i) ) for i, p in enumerate(tree.children)]

   if tree.data == "body":
       body = []
       for child in tree.children:
         body += compile(child)
       return body

   if tree.data == "while":
       condition, body = tree.children
       a, op, b = condition.children
       cond_var = "WHILE_VAR_{}".format(str(a.line))
       compare_asm = compare( a, op, b, cond_var)
       jmp = # TODO implement jump, create assembly for it
       return compare_asm + ["U execute if score {} vars matches 1 run {}".format(cond_var, jmp) ]
       
    
   if tree.data == "value":
       return compile(tree.children[0])

   if tree.data == "const_assignment":
       var, val = tree.children
       return [ const_assign(var, compile(val)[0]) ]
   if tree.data == "assignment":
       var0, var1 = tree.children
       return [ assign(var0, var1) ]

   return [ str(tree.data) ]

def parse(source):
    parser = Lark.open('minecraft.lark', rel_to=__file__, parser='lalr', start='program')
    tree = parser.parse(open(source).read())
    print(tree.pretty())
    print(tree)
    return tree

source = "example.minecraft"
target = "example.mcasm"
assembly = compile(parse(source))
print(assembly)
with open(target, 'w') as filehandle:
    for line in assembly:
        filehandle.write('{}\n'.format(line))


