# PBL-Redes-de_Computadores
 
# Supermercado Inteligente

## Índice

- [Introdução](#introdução)
- [Fundamentação Teórica](#fundamentação-teórica)
- [Desenvolvimento](#desenvolvimento)
- [Funcionalidades e Interfaces](#funcionalidades-e-interfaces)
- [Considerações Finais](#considerações-finais)

## Introdução

Com o avanço contínuo da tecnologia, a implementação de sistemas inteligentes tornou-se uma prática padrão em muitos setores, inclusive no setor de varejo. O projeto "Supermercado Inteligente" visa otimizar a experiência de compra para clientes e a gestão para administradores através da integração de tecnologias de Nuvem IoT, proporcionando uma abordagem centralizada para o processamento de compras.

## Fundamentação Teórica

### Arquitetura de Nuvem IoT

A Internet das Coisas (IoT) refere-se à interconexão de dispositivos do dia-a-dia à internet. Quando combinada com a computação em nuvem, ela permite que dispositivos remotos se conectem, enviem e recebam dados em uma infraestrutura centralizada. Isso proporciona uma gestão e processamento de dados mais eficientes, especialmente em aplicações que requerem a análise e reação em tempo real a eventos gerados por esses dispositivos.

### API REST

A Representational State Transfer (REST) é uma arquitetura de estilo que define um conjunto de restrições a serem usadas para criar serviços web. Uma API REST é uma interface que permite a interação com recursos em um servidor. Esta abordagem foi escolhida para a implementação do projeto devido à sua escalabilidade, facilidade de integração e capacidade de interagir com diferentes plataformas e dispositivos.

### SERVIDOR NO RASPBARRY REALIZANDO A LEITURA DO RFID

O projeto também possui um módulo de código que tem uma função de servidor para rodar no raspbarry, onde ao ser chamado pelo caixa ele realiza uma leitura das tag do sensor e armazena em uma lista de produtos do carrinho, mas antes é realizada uma leitura em uma lista pre definida das TAGS porque cada TAG já é um produto definido, ao adicionar produtos do carrinho ele manda para o cliente e formato JSON o conteúdo

## Desenvolvimento

O sistema foi projetado seguindo uma arquitetura de Nuvem IoT centralizada. As compras feitas em cada caixa são transmitidas pela internet para um centro de dados em nuvem.

![APIREST drawio](https://github.com/tassiocarvalho/PBL-1-Redes-de-Computadores/assets/90158519/237fd084-7df9-4806-b1d4-dfe315707285)

Para testar o protótipo, o caixa do supermercado foi simulado através de um software usado via terminal que gera compras fictícias. Esse software emula um cenário onde os produtos no carrinho são identificados através de um leitor RFID.

Ao aderir ao protocolo de uma API REST, implementamos duas interfaces principais:

1. **Interface do Caixa**: Aqui, o usuário pode iniciar a compra com opções de usar o sensor ou realizar uma compra manual, verificar itens e finalizar o pagamento.
2. **Interface do Supermercado**: Nesta interface, o administrador tem acesso a várias funções. Ele pode ver informações sobre os caixas, bloquear ou liberar um caixa, visualizar o histórico de compras e acompanhar as compras em tempo real e atualizar estoque de produtos.

Para manter a integridade e a segurança do projeto, foi decidido não utilizar frameworks de terceiros. Assim, utilizamos apenas mecanismos básicos presentes no sistema operacional para implementar a comunicação com base em uma arquitetura de rede baseada na Internet (TCP/IP).

## Como Executar a Aplicação

Para executar o servidor, abra o terminal e navegue até o diretório onde está o arquivo `Dockerfile`. Em seguida, siga os passos abaixo:

### Utilizando Docker

1. **Criar um Container**

    ```bash
    docker build -t server .
    ```

2. **Executar o Container (Configurando a Porta)**

    ```bash
    docker run -p 3389:3389 server
    ```

3. **Executar no Modo Interativo**

    ```bash
    docker run -it server
    ```

Esses comandos são válidos tanto para o módulo do caixa quanto para o módulo do administrador.


## Funcionalidades e Interfaces

### Interface do Caixa

- **Iniciar Compra**: Os usuários podem começar a adicionar produtos ao carrinho, ou usando o leitor do sensor RFID
- **Verificar Itens**: Antes de finalizar, os usuários têm a capacidade de verificar os itens adicionados ao carrinho.
- **Pagar Compra**: Uma vez que todos os itens desejados são adicionados, os usuários podem finalizar a compra.

### Interface do Supermercado

- **Visualizar Caixas**: O administrador pode ver informações em tempo real sobre cada caixa.
- **Bloquear/Liberar Caixa**: Em caso de qualquer discrepância, o administrador tem o poder de bloquear ou liberar um caixa.
- **Histórico de Compras**: Todos os registros de compras são armazenados e podem ser acessados por administradores.
- **Acompanhar Compras em Tempo Real**: Para a tomada de decisões imediatas, os administradores podem acompanhar as compras em tempo real.
- **Atualizar estoque**: O administrador pode atualizar o estoque dos produtos

## Uso de Docker Containers
Um ponto crucial que merece destaque é a utilização de Docker Containers para executar os módulos de cliente e servidor do projeto. O Docker oferece uma abstração e automação em nível de sistema operacional que facilita a distribuição de aplicações. Isso permite que o projeto seja altamente portátil e possa ser executado em qualquer sistema que suporte contêineres Docker, independentemente das configurações e dependências locais. Isso é especialmente valioso em um ambiente de desenvolvimento distribuído e para facilitar a implantação em diferentes plataformas de nuvem ou servidores locais.

O uso de Docker Containers não só acelera o desenvolvimento e implantação, mas também fornece um ambiente isolado que aumenta a segurança, ao minimizar o risco de conflitos de dependência e potenciais vulnerabilidades.

## Áreas para Melhorias e Expansão

Como é típico de muitos protótipos iniciais, existem áreas evidentes para melhoria e expansão. Uma delas, por exemplo, é a introdução de uma interface visual mais intuitiva e amigável para o usuário, que poderia melhorar significativamente a experiência do cliente e do administrador. Esta interface visual não só poderia simplificar o processo de compra para os clientes, mas também fornecer ao administrador uma visão mais clara e analítica das operações do supermercado.

Ao incorporar esses recursos adicionais e tecnologias, o sistema estará ainda mais preparado para atender às demandas e desafios do setor de varejo moderno.

## Considerações Finais

O projeto "Supermercado Inteligente", conforme apresentado, contempla uma parcela significativa do que foi solicitado inicialmente. Demonstrou-se uma abordagem centralizada da arquitetura de Nuvem IoT, alavancando as vantagens de uma API REST para a comunicação entre o caixa e o centro de dados. A simulação do caixa do supermercado, junto com o software de geração de compras fictícias, oferece uma visão tangível de como tal sistema poderia funcionar na prática.
No entanto, como é típico de muitos protótipos iniciais, existem áreas evidentes para melhoria e expansão. Uma delas, por exemplo, é a introdução de uma interface visual mais intuitiva e amigável para o usuário, que poderia melhorar significativamente a experiência do cliente e do administrador. Esta interface visual não só poderia simplificar o processo de compra para os clientes, mas também fornecer ao administrador uma visão mais clara e analítica das operações do supermercado.

