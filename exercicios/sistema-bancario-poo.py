from abc import ABC, abstractmethod
from datetime import datetime

class Conta:
    def __init__(self, **dados):
        self.numero = dados['numero']
        self.agencia = dados['agencia']
        self.cliente = dados['cliente']
        self.__saldo = 0.00
        self.historico = Historico()
    
    @property
    def saldo(self):
        return f'Conta/Ag: {self.numero}/{self.agencia} - Saldo: R$ {self.__saldo}'
    
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
        for transacao in self.__transacoes:
            print(f'Data/Hora: {transacao['data_hora']} - Valor Movimentado: {transacao['valor']}')      

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

dados = {
    'numero': 1,
    'agencia': 1,
    'cliente': 'Kaio'
}
conta1 = ContaCorrente(**dados)
print(conta1)

conta1.depositar()
print(conta1.saldo)

conta1.sacar()
print(conta1.saldo)

print(conta1.historico.movimentacoes)