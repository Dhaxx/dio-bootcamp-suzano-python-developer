"""
Você foi solicitado a criar um programa que analise uma lista de transações bancárias e filtre apenas aquelas que ultrapassam um valor limite.
Seu programa deve retornar uma nova lista contendo somente as transações cujo valor absoluto (ignorar sinal negativo) seja maior que o limite informado.

Atenção:
As transações incluem tanto depósitos (positivos) quanto saques (negativos).
Valor absoluto é o critério para filtrar, então tanto 300 (depósito) quanto -150 (saque) serão considerados, já que ambos têm módulo maior que 100.
"""
import ast

def main():
    transacoes_filtradas = []

    entrada = input()
    entrada_transacoes, limite = ast.literal_eval(entrada)
    transacoes = [x for x in entrada_transacoes if abs(x) > limite]

    print(f'Transações: {transacoes}')
if __name__ == '__main__':
    main()