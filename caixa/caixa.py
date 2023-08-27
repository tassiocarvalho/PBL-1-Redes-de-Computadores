import json
import requests

def realizar_compra():
    produtos = []
    
    while True:
        print("\nInforme os detalhes do produto ou digite 'sair' para finalizar a compra.")
        
        nome = input("Nome do produto: ")
        if nome.lower() == 'sair':
            break
        
        preco = float(input("Preço do produto: "))
        quantidade = int(input("Quantidade: "))

        produto = {
            'nome': nome,
            'preco': preco,
            'quantidade': quantidade
        }
        
        produtos.append(produto)

    return produtos

def exibir_carrinho(compras):
    total = 0
    print("\nItens no Carrinho:")
    for produto in compras:
        print(f"Nome: {produto['nome']}, Preço: {produto['preco']:.2f}, Quantidade: {produto['quantidade']}")
        total += produto['preco'] * produto['quantidade']
    
    print(f"\nTotal a Pagar: {total:.2f}")
    return total

def pagar_compra(total):
    print(f"\nTotal da Compra: {total:.2f}")
    pago = float(input("Informe o valor pago: "))
    
    if pago >= total:
        troco = pago - total
        print(f"\nTroco: {troco:.2f}")
        return True
    else:
        print("\nValor insuficiente.")
        return False

def escolher_caixa():
    response = requests.get("http://192.168.1.24:8000/caixa")
    if response.status_code == 200:
        caixas = response.json()
        
        # Filtrando caixas disponíveis
        caixas_disponiveis = [caixa for caixa in caixas if caixa.get('status', False)]
        
        # Se todos os caixas estiverem bloqueados
        if not caixas_disponiveis:
            print("\nTodos os caixas estão bloqueados no momento.")
            return None
        
        ids_disponiveis = [caixa["id"] for caixa in caixas_disponiveis]
        
        print("\nCAIXAS DISPONÍVEIS ID:", ", ".join(map(str, ids_disponiveis)))
        
        while True:
            try:
                escolha = int(input("Escolha qual caixa para iniciar: "))
                caixa_escolhido = next((caixa for caixa in caixas_disponiveis if caixa['id'] == escolha), None)
                
                if caixa_escolhido:
                    if not caixa_escolhido.get('status', False):
                        print("\nO caixa selecionado está bloqueado. Escolha outro.")
                    else:
                        return escolha
                else:
                    print("\nID de caixa inválido. Tente novamente.")
            except ValueError:
                print("\nPor favor, insira um número válido para o ID do caixa.")
    else:
        print("Erro ao recuperar caixas.")
        return None

def main():
    id_caixa = escolher_caixa()
    print(f"\nVocê escolheu o caixa com ID: {id_caixa}")
    
    compras = []
    while True:
        print("\nOpções:")
        print("1: Adicionar produto à compra")
        print("2: Verificar itens no carrinho")
        print("3: Pagar compra")
        print("4: Sair")

        escolha = input("\nSelecione uma opção: ")

        if escolha == '1':
            compras += realizar_compra() # Concatenando as novas compras à lista
        elif escolha == '2':
            exibir_carrinho(compras)
        elif escolha == '3':
            total = exibir_carrinho(compras)
            if pagar_compra(total):
                # Se o pagamento for bem-sucedido, envia a lista de compras para o servidor via POST
                response = requests.post("http://192.168.1.24:8000/compras", json=compras)
                
                if response.status_code == 201:
                    print("\nCompra realizada com sucesso!")
                    compras = []  # Resetando a lista de compras após o pagamento bem-sucedido
                else:
                    print("\nErro ao realizar compra.")
        elif escolha == '4':
            print("\nSaindo...")
            break
        else:
            print("\nOpção inválida!")

if __name__ == "__main__":
    main()
