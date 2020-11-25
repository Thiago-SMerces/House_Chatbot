# Importar bibliotecas e classes que serão utilizadas no projeto
import pandas as pd
from sklearn import tree
from sklearn.tree import _tree

# Leitura do arquivo.csv em um dataframe
dataframe = pd.read_csv("zip_sheet.csv",sep=',')

'''
Lista de atributos que serão utilizados para fazer a previsão 
do custo das casas (barato ou caro).
Praticamente todas as colunas da tabela, com exceção de id, 
date e as definidas por nós (Expensive e price_by_built_area)
'''
features = list(dataframe.columns)[2:21]

# Definir parte dos dados que será utilizada para o treinamento da árvore
train = dataframe.iloc[0:324]

'''
Dados no csv estão definidos como True e False
Aqui fazemos um mapeamento desses dados e trocamos
True e False por Caro e Barato respectivamente, 
atribuindo ao objeto que corresponde a classificação
das casas (caro ou barato).
Pode ser entendido como a(s) variável(is) dependente(s)
'''
mapp = {False: 'Barato', True: 'Caro'}
y_train = train['Expensive'].map(mapp)

'''
Objeto que contém os dados para classificar as casas
Pode ser entendido como a(s) variável(is) independente(s)
'''
x_train = train[features] 

'''
Definir árvore de decisão com profundidade máxima 5, 
para evitar overfitting com base em experimentos/testes
e não prolongar muito a árvore gerada
'''
decision_tree = tree.DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=0)
decision_tree.fit(x_train, y_train)

# Criar arquivo .dot conforme instruído nas aulas
with open("arvore.dot", 'w') as f:
     f = tree.export_graphviz(decision_tree,
                              out_file=f,
                              max_depth = 20,
                              impurity = True,
                              feature_names = list(train[features]),
                              class_names = ['Barato', 'Caro'],
                              rounded = True,
                              filled= True )

'''
Teste de acurácia da árvore gerada, apenas para uso interno
Note que os índices terminam 1 anterior ao final do arquivo .csv
pois aqui em Python o primeiro índice é 0, não 1 como no csv 

Os testes executados aqui demonstram que o programa atinge 
os valores corretos em 9 de 10 casos (mesmo que a maior parte
dos casos teste sejam classificados como "barato")

tests = dataframe.iloc[325:335]
Xtest = tests[features]
Ytest = decision_tree.predict(Xtest)
print(Ytest)

'''


# Função para gerar um novo arquivo, contendo o código da tomada de decisões da árvore
def tree_to_code(tree, subarvores):
    # tree_ é um atributo que armazena a estrutura de árvore completa conforme definido em
    # https://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html
    attribute_tree = tree.tree_

    # Armazenar cada atributo do csv como uma subarvore distinta, separando também as folhas
    subarvores = [
        subarvores[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in attribute_tree.feature
    ]

    # Espaço de identação inicial, para separar a classe das funções
    space = "    "

    # Escrever um novo arquivo com nome generated_tree.py que armazena as decisões 
    # tomadas pela árvore em cada nó, como um if else
    with open("generated_tree.py", 'w') as f:
        # Aviso para não alterar o arquivo
        f.write("### WARNING \n## Self generated file \n# Please do not edit this file # \n## \n### \n\n")

        # Nome da classe
        f.write("class Tree():\n")

        # Função de inicialização, não executa nenhuma função, mas poderia 
        # caso conveniente ser usada para tarefas como instanciar atributos da classe
        f.write("{}def __init__(self):\n".format(space))
        f.write("{}{}pass\n".format(space, space))
        f.write("\n")

        # Função para fazer as perguntas de valor ao usuário
        f.write("{}def ask_value(self, attribute):\n".format(space))
        f.write("{}{}value = float(input('Por favor digite o valor de {{}}: '.format(attribute)))\n".format(space, space))
        f.write("{}{}return value\n".format(space, space))
        f.write("\n")

        # Função de tomada de decisão
        f.write("{}def decision(self):\n".format(space))

    # Manter o arquivo generated_tree.py aberto enquanto adicionamos novas linhas a ele
    file_object = open('generated_tree.py', 'a')

    '''
    Dicionário inicialmente vazio para controlar a entrada de dados por parte do usuário,
    de modo que as variáveis sejam criadas apenas quando forem utilizadas
    '''
    parameters = {}

    # Função recursiva interna para montar a estrutura de decisão
    def recurse(node, depth):
        # Identação de cada bloco if else
        indent = "    " * depth

        # Verificar se o nó não é uma folha, para continuar a estrutura
        if attribute_tree.feature[node] != _tree.TREE_UNDEFINED:
            # Atributo atual
            name = subarvores[node]

            # Valor limite do nó (ex. price <= 500000)
            threshold = attribute_tree.threshold[node]

            '''
            Se o atributo atual não estiver presente no dicionário parameters,
            adicioná-lo junto com a profundidade que ele se encontra, de modo 
            a não repetir perguntas desnecessariamente para cada if else
            '''
            if name not in parameters.keys():
                parameters.update({name : depth})
                file_object.write("{}{}{} = self.ask_value('{}')\n".format(space, indent, name, name))

            # Escrever estrutura de decisão conforme os nós aparecem
            file_object.write("{}{}if {} <= {}:\n".format(space, indent, name, threshold))
            # Chamar recursive enquanto houver subárvores a percorrer, ou seja, nós diferentes de folhas
            recurse(attribute_tree.children_left[node], depth + 1)
            # Idem as duas linhas superiores, mas para o senão/else 
            file_object.write("{}{}else:  # if self.{} > {}\n".format(space, indent, name, threshold))
            recurse(attribute_tree.children_right[node], depth + 1)

            '''
            Se o atributo atual estiver presente no dicionário e a profundidade
            corresponder a mesma de quando este atributo foi adicionado ao dicionário,
            remover o atributo do dicionário, pois as condições que o chamaram foram 
            encerradas.
            '''
            if parameters[name] == depth:
                del parameters[name]

        # Quando for um nó folha, definir a classe a que pertence
        else:
            classe = None
            # Total de respostas positivas e negativas no nó
            total = attribute_tree.value[node][0][0] + attribute_tree.value[node][0][1]

            # Condicionamento das classes, mais de 60% de "sim", atribuir como barata
            if attribute_tree.value[node][0][0] > total*0.6:
                classe = '"Barato"'
            # Entre 40% e 60% de "sim", atribuir como média
            elif attribute_tree.value[node][0][0] >= total*0.4 and attribute_tree.value[node][0][0] <= total*0.6:
                classe = '"Medio"'
            # Menos de 40% de "sim", atribuir como cara
            else:
                classe = '"Caro"'
            # Retornar a classificação da casa
            file_object.write("{}{}return {}\n".format(space, indent, classe))

    # Primeira chamada da função recursiva, devemos passar o nó inicial (raiz) = 0 e a profundidade dele = 1
    recurse(0, 1)

    # Fechar o objeto que abrimos para manipular o arquivo
    file_object.close()

# Invocar o código de geração de árvore
tree_to_code(decision_tree, features)