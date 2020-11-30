from generated_tree import Tree
t = Tree()
continua = input("Continua? ")
while continua != "0":
    print(t.decision())
    continua = input("Continua? ")
