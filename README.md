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

## Desenvolvimento

O sistema foi projetado seguindo uma arquitetura de Nuvem IoT centralizada. As compras feitas em cada caixa são transmitidas pela internet para um centro de dados em nuvem.

Para testar o protótipo, o caixa do supermercado foi simulado através de um software que gera compras fictícias. Esse software emula um cenário onde os produtos no carrinho são identificados através de um leitor RFID.

Ao aderir ao protocolo de uma API REST, implementamos duas interfaces principais:

1. **Interface do Caixa**: Aqui, o usuário pode iniciar a compra, verificar itens e finalizar o pagamento.
2. **Interface do Supermercado**: Nesta interface, o administrador tem acesso a várias funções. Ele pode ver informações sobre os caixas, bloquear ou liberar um caixa, visualizar o histórico de compras e acompanhar as compras em tempo real.

Para manter a integridade e a segurança do projeto, foi decidido não utilizar frameworks de terceiros. Assim, utilizamos apenas mecanismos básicos presentes no sistema operacional para implementar a comunicação com base em uma arquitetura de rede baseada na Internet (TCP/IP).

## Funcionalidades e Interfaces

### Interface do Caixa

- **Iniciar Compra**: Os usuários podem começar a adicionar produtos ao carrinho.
- **Verificar Itens**: Antes de finalizar, os usuários têm a capacidade de verificar os itens adicionados ao carrinho.
- **Pagar Compra**: Uma vez que todos os itens desejados são adicionados, os usuários podem finalizar a compra.

### Interface do Supermercado

- **Visualizar Caixas**: O administrador pode ver informações em tempo real sobre cada caixa.
- **Bloquear/Liberar Caixa**: Em caso de qualquer discrepância, o administrador tem o poder de bloquear ou liberar um caixa.
- **Histórico de Compras**: Todos os registros de compras são armazenados e podem ser acessados por administradores.
- **Acompanhar Compras em Tempo Real**: Para a tomada de decisões imediatas, os administradores podem acompanhar as compras em tempo real.

## Considerações Finais

O projeto "Supermercado Inteligente" representa um marco no setor de varejo, tornando o processo de compra e gestão mais eficiente através da integração de tecnologias avançadas. Embora tenhamos simulado apenas uma parte do que um verdadeiro supermercado inteligente pode oferecer, este projeto serve como um protótipo robusto para futuras expansões e integrações. Com a contínua evolução da tecnologia, as oportunidades para otimização e melhoria são infinitas.
