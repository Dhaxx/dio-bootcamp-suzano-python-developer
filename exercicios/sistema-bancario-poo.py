from abc import ABC, abstractmethod
from datetime import datetime
from re import fullmatch

class Conta:
    __numero = 0

    def __init__(self, **dados):
        Conta.__numero += 1
        self.numero = Conta.__numero
        self.agencia = dados['agencia']
        self.cliente = dados['cliente'].nome
        self.__saldo = 0.00
        self.historico = Historico()
    
    @property
    def saldo(self):
        return self.__saldo
    
    def atualizar_saldo(self, valor):
        self.__saldo += valor
    
    def sacar(self):
        print(f'===SAQUE===')
        print(f'Saldo Atual: R$ {self.__saldo:.2f}\n')
        valor = float(input('Sacar R$ '))
        if (self.__saldo - valor) < 0.00:
            print('Operação Cancelada, saldo insuficiente!')
        else:
            Saque(valor).registrar(self)

    def depositar(self):
        print('===DEPÓSITO===')
        print(f'Saldo Atual: R$ {self.__saldo:.2f}\n')
        valor = float(input('Depositar R$ '))
        Deposito(valor).registrar(self) if valor > 0.00 else print('Operação Cancelada, valor inválido!')

    @classmethod
    def abre_conta(cls, cliente):
        print("\n===ABRIR NOVA CONTA===")
        agencia = input('Digite a agência: ')
        if not agencia:
            raise ValueError('A agência deve ser informada!')
        conta = cls(agencia=agencia, cliente=cliente)
        cliente.vincula_conta(conta)
        print(f'\nConta {conta.numero} registrada com sucesso!')

class ContaCorrente(Conta):
        def __init__(self, **dados):
            super().__init__(**dados)
            self.__limite = 500.00
            self.__limite_saques = 1000.00

        @property
        def limite(self):
            return self.__limite
        
        def set_limite(self, valor):
            self.__limite = valor

        @property
        def limite_saques(self):
            return self.__limite_saques

        def set_limite_saques(self, valor):
            self.__limite_saques = valor

        def sacar(self):
            print(f'\n===SAQUE (LIMITE: R$ {self.__limite_saques})===')
            print(f'Saldo Atual: R$ {self.saldo:.2f}\n')
            valor = float(input('Sacar R$ '))
            if (valor > self.__limite_saques) or (self.saldo - valor) <= 0.00:
                print('Operação Cancelada, saldo insuficiente!')
            else:
                Saque(valor).registrar(self)

        def depositar(self):
            print(f'\n===DEPÓSITO (LIMITE R$ {self.__limite})===')
            print(f'Saldo Atual: R$ {self.saldo:.2f}\n')
            valor = float(input('Depositar R$ '))
            Deposito(valor).registrar(self) if self.__limite >= valor > 0.00 else print('Operação Cancelada, valor inválido!')

        def __str__(self):
            return f'Conta: {self.numero} - AG: {self.agencia} - Cliente: {self.cliente} - Saldo: {self.saldo}'

class Transacao(ABC):
    @abstractmethod
    def registrar(cls, conta):
        ...

class Historico:
    def __init__(self):
        self.__transacoes = []
    
    def adiciona_transacao(self, transacao):
        self.__transacoes.append({
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "valor": transacao.valor
        })
    
    @property
    def movimentacoes(self):
        print('\n===MOVIMENTAÇÕES EFETUADAS===')
        if len(self.__transacoes) > 0:
            for transacao in self.__transacoes:
                print(f'\nData/Hora: {transacao['data_hora']} - Valor Movimentado: {transacao['valor']}')
        else:
            raise UserWarning(f'\nNenhuma movimentação registrada!')

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta):
        conta.atualizar_saldo(self.valor)
        conta.historico.adiciona_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = -valor

    def registrar(self, conta):
        conta.atualizar_saldo(self.valor)
        conta.historico.adiciona_transacao(self)

class Cliente:
    def __init__(self, endereco):
        self.__endereco = endereco
        self.contas = dict()
    
    def vincula_conta(self, Conta):
        self.contas[Conta.numero] = Conta
    
    def lista_contas(self):
        print(f'\n===CONTAS DE {cliente.nome}==='.upper()) 
        if len(cliente.contas) > 0:  
            for numero, conta in cliente.contas.items():
                print(f'Número: {numero} - Saldo: R$ {conta.saldo:.2f}')
        else:
            raise UserWarning('Você não possui nenhuma conta cadastrada!')

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
    
    @classmethod
    def registra_pessoa(cls, *args):
        if any(arg is None for arg in args):
            raise ValueError("Para se registrar, se faz obrigatório os preenchimento de todos os dados corretamente!")
        return cls(*args)

##############
def main():
    global clientes
    global cliente
    clientes = set()
    cliente = None
    while True:
        print(f"\n===BEM-VINDO(A) AO PYBANK{', '+str(cliente.nome).capitalize() if cliente is not None else None}===\n[1] Criar Conta\n[2] Depósito\n[3] Saque\n[4] Extrato\n[5] Sair\n\nESCOLHA UMA OPERAÇÃO: \a")
        try:
            opcao = int(input())

            if opcao == 5:
                print('Obrigado por usar o Pybank!')
                break
            elif opcao in (1,2,3,4):
                cliente = valida_existe_cliente() if cliente is None else cliente
                if opcao == 1:
                    ContaCorrente.abre_conta(cliente=cliente)
                elif opcao in (2,3):
                    menu_opcao_deposito_ou_saque(opcao)
                else:
                    conta = lista_contas_cliente()
                    conta.historico.movimentacoes
            else:
                raise ValueError('Código de operação inválido!')
        except Exception as e:
            print(f'{e}\n')

def valida_existe_cliente() -> Cliente:
    cpf = str(input('\nInsira seu cpf (sem pontuação): '))
    if not validar_cpf(cpf):
        raise ValueError(f'O cpf {cpf} é inválido!')
    cliente = next((x for x in clientes if x.cpf == cpf),False)
    if not cliente:
        print("\n===REGISTRE-SE===")
        endereco = input('Insira seu endereço: ')
        nome = input('Insira seu nome: ')
        dtnascimento = input('insira sua data de nascimento: ')
        cliente = PessoaFisica.registra_pessoa(endereco, cpf, nome, dtnascimento,)
        clientes.add(cliente)
        print('Registro realizado!')
    return cliente

def validar_cpf(cpf: str) -> bool:
    return bool(fullmatch(r"\d{11}", cpf))

def menu_opcao_deposito_ou_saque(operacao):
    conta_escolhida = lista_contas_cliente()
    if operacao == 2:
        conta_escolhida.depositar()
    if operacao == 3:
        conta_escolhida.sacar()
    print(f'{'Saque' if operacao == 3 else 'Depósito'} realizado com sucesso!')

def lista_contas_cliente():
    cliente.lista_contas()
    conta_escolhida = int(input('Digite a conta para operação: '))
    conta_escolhida = next((conta for numero, conta in cliente.contas.items() if numero == conta_escolhida),None)

    if not conta_escolhida:
        raise KeyError('Conta inválida!')

    return conta_escolhida

if __name__ == '__main__':
    main()