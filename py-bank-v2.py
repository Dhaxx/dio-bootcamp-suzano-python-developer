'''
Imagine que você trabalha no setor de TI de um banco e precisa criar um programa que registre as transações de uma conta bancária.
Cada transação pode ser um depósito ou um saque, e todas elas serão armazenadas em uma lista. 
Seu programa deve calcular o saldo final da conta com base nas transações realizadas. 
Depósitos serão representados como valores positivos e saques como valores negativos.
'''
import ast

def main():
  try:
      values_list = input()
      values_list = ast.literal_eval(values_list)

      print(saldo_final(values_list))
  except ValueError:
      print(f'Código de operação inválido! Por favor, escolha uma operação válida.\n')

def saldo_final(transactions_list):
    return(f'Saldo: R$ {sum(transactions_list):.2f}')

if __name__ == '__main__':
    main()


# def main():
#     transactions_list = []

#     while True:
#         print("==BEM-VINDO AO PYBANK==\n[1] Depósito\n[2] Saque\n[3] Sair\n\nESCOLHA UMA OPERAÇÃO: \a")

#         try:
#             choice = int(input())
#             if choice == 3:
#                 break

#             value_input = float(input('Digite o valor da operação: '))

#             if choice == 1:
#                 operation_value = value_input
#             else:
#                 operation_value = -value_input

#             transactions_list.append(operation_value)
#             print(saldo_final(transactions_list))
#         except ValueError:
#             print(f'Código de operação inválido! Por favor, escolha uma operação válida.\n')

# def saldo_final(transactions_list):
#     return(f'Saldo: R${sum(transactions_list):.2f}')