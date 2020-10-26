import pandas as pd
import os
import sys
import math 

class Transform_Data():
    def __init__(self):
        pass

    def get_split(self):
        # Obter dados da planilha e escrever no data frame
        dados_planilha = pd.read_csv("zip_sheet.csv",sep=',')

        #Lista de separadores/divisores que efetivamente irão limitar os dados
        # para dividir as sub-árvores
        # Ex. bedrooms     CARO
        #       1          SIM
        #       2          SIM
        #       3          NÃO
        #       4          NÃO
        #       5          SIM
        # #bedrooms <= 2. Separador encontrado = 2
        tuned_splits = []

        # Iniciar operações sobre o data frame, como as colunas são minoria e 
        # os dados para comparação são definidos por elas, estas formam o laço externo
        # Começando do índice 2 (a partir de 0) pois no csv os primeiros são ID e Date que não 
        # acrescentam nada de útil ao programa
        for column in range (2, dados_planilha.shape[1]-5):
            # Lista para armazenar todos os valores possíveis de splits para a coluna
            divisores = []

            # Percorrer as linhas e por consequência o data frame completo para determinar
            # todos os divisores (splits) possíveis
            for row in range (dados_planilha.shape[0]):    
                valor = float(dados_planilha.iloc[row, column])
                if (not math.isnan(valor) and valor not in divisores):
                    divisores.append(float(valor))
            
            # Ordenar a lista em ordem crescente para facilitar a manipulação e gini index
            divisores.sort()

            # Número de elementos
            contador_div = len(divisores)

            # Lista geral de gini's obtidos para cada sub-árvore
            gini_div = []

            # Para cada elemento possível de split, calcular o gini
            for cont in range(contador_div):

                # Probabilidades de              ESCOLHA
                #                               /       \
                #                              /         \
                #                       Verdadeiro        Falso
                #                          /   \          /   \
                #                         /     \        /     \
                #                       Sim     Nao     Sim    Nao
                true_prob_sim = 0
                false_prob_sim = 0
                true_prob_nao = 0
                false_prob_nao = 0
                for row in range (dados_planilha.shape[0]):    
                    valor = float(dados_planilha.iloc[row, column])
                    decisor = dados_planilha.iloc[row, dados_planilha.shape[1]-1]

                    # Obs. Não sei se caso isolado mas se trocar os if's i.e.
                    #if (valor <= divisores[cont] and decisor):
                    #    true_prob_sim += 1
                    #elif (valor <= divisores[cont] and not decisor):
                    #    false_prob_sim += 1
                    #elif (valor > divisores[cont] and decisor):
                    #    true_prob_nao += 1
                    #elif (valor > divisores[cont] and not decisor):
                    #    false_prob_nao += 1
                    # Os gini finais da função permanecem os mesmos

                    if (valor >= divisores[cont] and decisor):
                        true_prob_sim += 1
                    elif (valor >= divisores[cont] and not decisor):
                        false_prob_sim += 1
                    elif (valor < divisores[cont] and decisor):
                        true_prob_nao += 1
                    elif (valor < divisores[cont] and not decisor):
                        false_prob_nao += 1
                
                # Variáveis auxiliares para calcular Gini
                total_esquerda = (true_prob_sim + false_prob_sim)
                total_direita = (true_prob_nao + false_prob_nao)
                # Instanciando gini_total com um valor abstrato (poderia ser -1, 0, 2...)
                gini_total = 1

                # Verificar se os valores são nulos
                if (total_esquerda == 0 or total_direita == 0):
                    pass
                else:
                    # Calcular Gini dos nós filhos da esquerda e direita
                    gini_esquerda = 1 - (true_prob_sim / total_esquerda)**2 - (false_prob_sim / total_esquerda)**2
                    gini_direita = 1 - (true_prob_nao / total_direita)**2 - (false_prob_nao / total_direita)**2
                    
                    # Variável auxiliar para o gini total da sub-árvore
                    esquerda_direita = total_esquerda + total_direita

                    #Cálculo do gini
                    gini_total = (total_esquerda / (esquerda_direita)) * gini_esquerda + (total_direita / (esquerda_direita)) * gini_direita

                    # Adicionar gini calculado a lista geral de gini's
                    gini_div.append(gini_total)

            #Gini's mínimos para efetivamente selecionar o melhor divisor/separador/split
            if (len(gini_div) > 1):
                #Adicionar menor gini a lista inicial de Gini
                tuned_splits.append(divisores[gini_div.index(min(gini_div))])
            else:
                tuned_splits.append(0)

        # Nomes das colunas
        cols = dados_planilha.columns 

        # Mensagem de sugestão
        for i in range(2, len(cols)-5):
            print("Melhor split para sub-árvore:", cols[i], "=", tuned_splits[i-2])
            
        return tuned_splits
        
td = Transform_Data()
td.splits = td.get_split()
# Verifica se os dados foram retornados corretamente
print(td.splits)