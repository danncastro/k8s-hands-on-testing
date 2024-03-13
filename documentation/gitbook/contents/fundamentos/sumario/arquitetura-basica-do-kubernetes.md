# Arquitetura Básica do Kubernetes

***

### <mark style="color:red;">Cluster Kubernetes</mark>&#x20;

É um conjunto de nós de máquinas usadas para executar aplicações em contêineres dentro das `PODS`. Quando executa o Kubernetes, está executando um cluster

* No mínimo, um cluster contém um plano de controle `(control-plane)` e pelo menos uma máquina ou nó `(node)`.
* Todo cluster possui ao menos um servidor de processamento `(worker node)`.
* Consiste em um conjunto de servidores de processamento, chamado **nós (`nodes`)**, que executam aplicações em contêineres.
* O servidor de processamento (`Worker`) hospeda os Pods que são componentes de uma aplicação.

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

***

### <mark style="color:red;">Pods</mark>&#x20;

No Docker, a menor unidade computacional possível é o **Container**, já no Kubernetes a menor unidade computacional possível é o **Pod**. `Recurso que encapsula um container do Kubernetes`

* Um **Pod Kubernetes** é um conjunto de um ou mais contêineres **(como Docker)** que inclui armazenamento compartilhado (`volumes`), endereços IP e informações sobre como executa-lo, sendo a menor unidade de uma aplicação Kubernetes. Os pods são compostos por um container nos casos de uso mais comuns ou por vários containers fortemente acoplados em cenários mais avançados.
* Os containers são agrupados nesses pods para que os recursos sejam compartilhados de modo mais inteligente, recebem endereços IP's únicos e compartilham o mesmo Namespaces, incluindo endereços IP. `Containers em um mesmo pod se comunicam através de localhost`.
* Pods também contem redes compartilhadas e recursos de armazenamento entre os containers mas não podem compartilhar a mesma porta de acesso dentro de um mesmo pod.
* O Pod representa uma única instância de um processo em execução no cluster e são `efêmeros`.

> A palavra **Pod** significa unidade destacável ou independente em uma aeronave, espaçonave, veículo ou navio, tendo uma função particular. Muitas vezes Pod é referido a um grupo de baleias que é o símbolo do docker.

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

***

### <mark style="color:red;">Network pods</mark>&#x20;

O modelo de rede do Kubernetes dita que os pods precisam ser acessíveis pelo seu endereço IP através dos nós. Isso quer dizer que o endereço IP de um pod está sempre visível para outros pods na rede, e cada pod visualiza seu próprio endereço IP da mesma forma que outros pods o veem.

***

* <mark style="color:yellow;">ClusterIP:</mark> Expõe o serviço a um IP interno ao cluster. Quando escolhemos este valor fazemos com que o serviço seja acessível apenas por dentro do cluster. É o modelo padrão de `ServiceType`.

***

* <mark style="color:yellow;">NodePort:</mark> Expõe o serviço em todos os IP's dos nós em uma porta estática a (`NodePort`). Você conseguirá acessar o serviço por fora do cluster através de `<NodeIP>:<NodePort>`.

***

### <mark style="color:red;">Armazenamento</mark>&#x20;

Os pods podem especificar uma série de volumes de armazenamento que podem ser compartilhados entre containers.

***

### <mark style="color:red;">Aplicação</mark>&#x20;

Menor unidade do Kubernetes

* Uma abstração sobre o container
* Normalmente é executado uma aplicação por Pod

***

### <mark style="color:red;">Deployment</mark>&#x20;

O **Deployment**, em conjunto com o `ReplicaSet` é um dos principais controllers utilizados, garante que determinado número de réplicas de um pod esteja em execução nos **workers-nodes** do cluster.&#x20;

* Além disso, o Deployment também é responsável por gerenciar o ciclo de vida das aplicações, onde características associadas a aplicação, tais como `imagem`**,** `porta`**,** `volumes` **e variáveis de ambiente,** possam ser especificados em arquivos do tipo `yaml` ou `json` para posteriormente serem passados como parâmetro para o `kubectl` executar o deployment.
* Esta ação pode ser executada tanto para criação quanto para atualização e remoção do deployment;

***

### <mark style="color:red;">ReplicaSets</mark>&#x20;

É um objeto responsável por garantir a quantidade de pods em execução nos nós;

***

### <mark style="color:red;">Services</mark>&#x20;

Abstração para expor aplicações executadas em um ou mais pods, proveem IP's fixos para comunicação através de um `ClusterIP`, `NodePort` ou `LoadBalancer` para distribuir as requisições entre os diversos pods de um determinado **Deployment**.&#x20;

Proveem um DNS para um ou mais pods. Funciona como um balanceador de carga.

***

* <mark style="color:yellow;">ClusterIP</mark> - Faz a comunicação entre diferentes pods dentro de um mesmo cluster.

***

* <mark style="color:yellow;">NodePort</mark> - Permitem a comunicação com o mundo externo. enviar uma requisição de uma na que não está dentro do nosso cluster para o nosso cluster, para algum pod dentro dele.

***

* <mark style="color:yellow;">LoadBalancer</mark> - o LoadBalancer nada mais é do que um ClusterIP que permite a comunicação entre uma maquina do mundo externo e os nosso pods. Só que ele automaticamente se integra ao LoadBalancer do nosso cloud provider.

***

* <mark style="color:yellow;">External Name</mark> - Expõe um serviço externo para ser acessado através do pod interno

```bash
externalName: mongo-service.database.svc.cluster.local
```

<table><thead><tr><th width="177" align="center">Nome do serviço</th><th align="center">Namespace </th><th width="181" align="center">Tipo de Resources</th><th align="center">Cluster default </th></tr></thead><tbody><tr><td align="center">mongo-service</td><td align="center"><code>database</code></td><td align="center"><code>svc</code></td><td align="center"><code>cluster.local</code></td></tr></tbody></table>

***

### <mark style="color:red;">Portas de serviço</mark>

**Control Plane**

<table><thead><tr><th align="center">Protocol</th><th align="center">Direction</th><th width="129" align="center">Port Range</th><th width="148" align="center">Purpose</th><th align="center">Used By</th></tr></thead><tbody><tr><td align="center">TCP</td><td align="center">Inbound</td><td align="center">6443*</td><td align="center">Kubernetes API server</td><td align="center">All</td></tr><tr><td align="center">TCP</td><td align="center">Inbound</td><td align="center">2379-2380</td><td align="center">etcd server client API</td><td align="center">kube-apiserver, etcd</td></tr><tr><td align="center">TCP</td><td align="center">Inbound</td><td align="center">10250</td><td align="center">Kubelet API</td><td align="center">Self, Control plane</td></tr><tr><td align="center">TCP</td><td align="center">Inbound</td><td align="center">10251</td><td align="center">kube-schenduler</td><td align="center">Self</td></tr><tr><td align="center">TCP</td><td align="center">Inbound</td><td align="center">10252</td><td align="center">kube-controller-manager</td><td align="center">Self</td></tr></tbody></table>

**Workers**

<table><thead><tr><th width="114" align="center">Protocol</th><th align="center">Direction</th><th align="center">Port Range</th><th align="center">Purpose</th><th align="center">Used By</th></tr></thead><tbody><tr><td align="center">TCP</td><td align="center">Inbound</td><td align="center">10250</td><td align="center">Kubelet API</td><td align="center">Self, Control plane</td></tr><tr><td align="center">TCP</td><td align="center">Inbound</td><td align="center">30000-32767</td><td align="center">NodePort</td><td align="center">Services All</td></tr></tbody></table>

**Metallb**

***

### <mark style="color:red;">Configmap</mark>

***

### <mark style="color:red;">Controller</mark>&#x20;

É o objeto responsável por interagir com o **API Server** e orquestrar algum outro objeto. Um exemplo de objeto desta classe são os `Deployments`;

***

* <mark style="color:yellow;">Jobs e CronJobs:</mark> São objetos responsáveis pelo gerenciamento de jobs isolados ou recorrentes.

***

### <mark style="color:red;">Volumes</mark>&#x20;

Possuem ciclos de vida independentes dos containers. Porém, são dependentes dos pods

**Persistência de dados:** O gerenciamento de armazenamento é uma questão bem diferente do gerenciamento de instâncias computacionais.&#x20;

O subsistema `PersistentVolume` provê uma API para usuários e administradores que mostra de forma detalhada de como o armazenamento é provido e como ele é consumido. Para isso, o Kubernetes possui duas novas APIs:

***

* <mark style="color:yellow;">PersistentVolume (PV)</mark> - PVs são plugins de `volume`, porém eles têm um ciclo de vida independente de qualquer pod que utilize um PV. Essa API tem por objetivo mostrar os detalhes da implementação do armazenamento, seja ele **NFS, ISCSI, ou um armazenamento específico de um provedor de cloud pública**.

***

* <mark style="color:yellow;">PersistentVolumeClaim (PVC)</mark> - PVC é uma requisição para armazenamento por um usuário.  Claims podem solicitar ao PV tamanho e modos de acesso específicos.  Uma reivindicação de volume persistente (PVC) é a solicitação de armazenamento, que é atendida vinculando a PVC a um volume persistente (PV). Exemplo:

```yml
    volumeMounts:
    - name: local
      mountPath: /caminho
volumes:
- name: local
  PersistentVolumeClainm:
    claimName: local
```

***

* <mark style="color:yellow;">StorageClasses(SC)</mark> - Fornecem dinamismo para criação de `PersistentVolume` conforme demanda. Também são capazes de criar discos de armazenamento

***

* <mark style="color:yellow;">Statefullset</mark> - Podem ser usados quando estados devem ser persistidos.&#x20;

1. Usam **`PersistentVolume`** e **`PersistentVolumeClaim`** para persistência de dados.
2. Garante unicidade de Pods durante reinícios e atualizações
3. Clusters possuem StorageClasses "default" e podem ser usados automaticamente se não definirmos qual será utilizado

***

### <mark style="color:red;">Probes</mark>&#x20;

Cria critérios para definir se a aplicação está saudável através de Probes, tornando visível ao Kubernetes que uma aplicação não está se comportando da maneira esperada.

***

* <mark style="color:yellow;">livenessProbe</mark> - Podem fazer a verificação em diferentes intervalos de tempo via HTTP.  Ele indicará falha caso o código de retorno seja menor que `200` ou maior/igual a `400`.

***

* <mark style="color:yellow;">readinessProbe</mark> - Também podem fazer a verificação em diferentes intervalos de tempo via HTTP. Ele começará a executar os testes a partir do time definido depois do container ser criado.

***

> **LivenessProbe** são para saber se a aplicação está saudável e/ou se deve ser reiniciada, enquanto **ReadinessProbe** são para saber se a aplicação já está pronta para receber requisições depois de iniciar

{% hint style="info" %}
Além do HTTP, também pode fazer verificações via TCP
{% endhint %}

***

* <mark style="color:yellow;">StartupProbe</mark> - Voltado para aplicações legadas. Algumas aplicações legadas exigem tempo adicional para inicializar na primeira vez

***

### <mark style="color:red;">Horizontal Pod Autoscaler</mark>&#x20;

O `HPA` visa manter o consumo médio de CPU o mais próximo do valor definido e escalona uma nova pod conforme a necessidade.&#x20;

São responsáveis por definir em quais circunstâncias escalaremos nossa aplicação automaticamente

***

### <mark style="color:red;">Vertical Pod Autoscaler</mark>&#x20;

O `VerticalPodAutoscaler` remove a necessidade de definir limites e pedidos por recursos do sistema, como cpu e memória.&#x20;

* Quando definido, ele define os consumos de maneira automática baseada na utilização em cada um dos nós, além disso, quanto tem disponível ainda de recurso.

```bash
kubectl scale deployment nome-deploy --replicas x
```

***
