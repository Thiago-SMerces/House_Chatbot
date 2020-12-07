from generated_tree import Tree

t = Tree()
continua = None
erro = 0
while continua != "2":
    print("___________________________________________________________________\n")
    print("Chatbot de estimativa de preços ofertados por casas no CEP 98106 \n")
    print("___________________________________________________________________\n")
    continua = input("Fazer estimativa? (1 para sim, 2 para não)\n")
    if continua == "1":
        print(t.decision())
    elif continua == "2":
        print("Encerrando programa. Até mais!")
    else:
        print("Comando inválido, tente novamente!")
        erro +=1

    if erro == 3:
        print("Comandos inválidos sucessivos! Encerrando programa")
        break
