O Hyperledger Fabric é uma plataforma para soluções de contabilidade distribuída sustentadas por uma arquitetura modular que oferece altos graus de confidencialidade, resiliência, flexibilidade e escalabilidade. Ele foi projetado para oferecer suporte a implementações conectáveis ​​de diferentes componentes e acomodar a complexidade e os meandros existentes em todo o ecossistema econômico.

Este projeto blockchain possui dois clientes:

- Outro cliente recebe dados da API do FieldClimate os insere no blockchain

- Um cliente realiza um web scrape, recebendo os dados das estações em tempo real do website [Alerta Rio](http://alertario.rio.rj.gov.br/tabela-de-dados/), e os inserindo no blockchain (chaincode em construção)

Caso a plataforma não esteja instalada na maquina, existem alguns requisitos minimos necessarios para utilizar a rede, que podem ser encontrados no seguinte repósitório
<link>https://github.com/malkai/Inmetrochain-Vehicle</link>

Para mais detalhes, a documentação oficial do Hyperledger Fabric será um otimo guia com tutoriais de como a rede funciona -  <link>https://hyperledger-fabric.readthedocs.io/en/latest/</link>

# Tutorial de como usar o cliente FieldClimate

OBS: É necessário inserir suas próprias chaves pública e privada em blockchain/gateway/fieldclimate/modules/fieldclimateAPI.py

Para começar, abra o terminal e acesse a pasta do projeto.
A seguir abra a pasta "blockchain"

```
cd blockchain
```
Crie o canal com o comando:

```
./network.sh up createChannel -ca
```

Caso deseje definir um nome para o canal (o padrão é mychannel), utilize:

```
./network.sh up createChannel -ca nomecanal
```

Implemente o chaincode com o comando:

```
./network.sh deployCC -ccn fieldclimate -ccp contrato/BasicCRUD -ccl go
```

Entre na pasta gateway

```
cd gateway
```

E execute o seguinte comando para atualizar o arquivo json (necessário apenas 1 vez a cada inicialização da rede blockchain)

```
python3 findKey.py
```

Chegamos na etapa de execução dos clientes. Começando pelo FieldClimate, acesse sua pasta com o comando

```
cd fieldclimate
```

E insira o seguinte comando

```     
python3 client.py
```

Com isso, ele irá se conectar com o servidor do FieldClimate, buscar os dados da estação e dispositivos do usuário e inseri-los no blockchain

Também é possível deixar o cliente executando em loop, no qual ele faz a chamada automaticamente a cada 5 minutos e, caso os dados tenham sido atualizados, ele insere os novos dados no blockchain. Para usar, basta inserir o comando

```
python3 clientLoop.py
```

Para encerrar o loop, aperte CTRL + C no teclado (ou simplesmente feche o terminal)

# Alerta Rio (ainda em construção)

Similar a maneira como é acessada a pasta fieldclimate, acesse a pasta alertaRio pela pasta gateway

```
cd blockchain
cd gateway
cd alertario
```

Agora, para inicia-lo é necessário inserir um ID de estação disponível no [Alerta Rio](http://alertario.rio.rj.gov.br/tabela-de-dados/). Caso você insira um ID não disponível, o cliente irá retornar uma mensagem de erro e listar os IDs disponíveis para cada tabela no site.

Para executar o cliente, insira o comando:

```
python3 client_insert.py <ID da Estação>

Exemplo:

python3 client_insert.py 16
```

E pronto! O cliente irá buscar os dados e os inserir no ledger. Para retornar os últimos dados inseridos, use o comando

```
python3 client_get.py <ID da Estação>

Exemplo:

python3 client_get.py 16
```

Os dados são inseridos com um timestamp em Unix com base na última atualização realizada no [Alerta Rio](http://alertario.rio.rj.gov.br/tabela-de-dados/), e é possível retornar os dados inseridos no ledger de uma estação um horário específico. Para fazer isso, execute o seguinte comando:

```
python3 client_query.py <Horário em unix>

Exemplo:

python3 client_query.py 1690991400
```

# Derrubando a rede

Para fazer a rede parar utilize os comandos abaixo:

```
cd .. 
cd blockchain
./network.sh down
```