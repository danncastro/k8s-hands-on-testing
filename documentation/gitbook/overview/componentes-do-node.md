---
description: >-
  Os componentes do nó são executados em todos os nós, mantendo os Pods em
  execução e fornecendo o ambiente de execução do Kubernetes.
---

# Componentes do Node

## <mark style="color:red;">Glossário</mark>

{% embed url="https://kubernetes.io/pt-br/docs/reference/glossary/?all=true#term-cluster" %}

***

## <mark style="color:red;">kubelet</mark>&#x20;

{% embed url="https://kubernetes.io/pt-br/docs/concepts/overview/components/#node-components" %}

Um agente que é executado em cada [nó](https://kubernetes.io/pt-br/docs/concepts/architecture/nodes/) no cluster. Ele garante que os [contêineres](https://kubernetes.io/docs/concepts/containers/) estejam sendo executados em um [Pod](https://kubernetes.io/docs/concepts/workloads/pods/).

> _Componente que executa em todas as máquinas do cluster e gerencia tarefas como a inicialização de pods e contêineres._ Ele é responsável por garantir que os contêineres estejam em execução nos nós, gerenciando os pods e fornecendo informações sobre a saúde dos nós de volta ao kube-apiserver.

{% hint style="info" %}
O kubelet só entra em cena quando o kube-scheduler já decidiu onde agendar um pod e precisa garantir que o pod esteja em execução no nó correspondente.
{% endhint %}

O kubelet utiliza um conjunto de `PodSpecs` que são fornecidos por vários mecanismos e garante que os contêineres descritos nesses `PodSpecs` estejam funcionando corretamente.&#x20;

{% hint style="warning" %}
O kubelet não gerencia contêineres que não foram criados pelo Kubernetes.
{% endhint %}

* O **kubelet** pode ser visto como o **agente do k8s** que é executado nos `workers-nodes`.

***

* Em cada worker-node deverá existir um agente Kubelet em execução.&#x20;

***

* O Kubelet é responsável por de fato gerenciar os pods, que foram direcionados pelo `controller` do cluster dentro dos nós, de forma que para isto o Kubelet pode **iniciar, parar e manter os contêineres e os pods em funcionamento** de acordo com o que foi instruído pelo controlador do cluster;

***

## <mark style="color:red;">kube-proxy</mark>&#x20;

Mantém regras de rede no host e lida com o balanceamento de carga de serviços.

kube-proxy é um _proxy_ de rede executado em cada [nó](https://kubernetes.io/pt-br/docs/concepts/architecture/nodes/) no _cluster_, implementando parte do conceito de [serviço](https://kubernetes.io/docs/concepts/services-networking/service/) do Kubernetes.

* Este componente é responsável por efetuar roteamento de requisições para os pods corretos, como também por cuidar da parte de rede dos nós;

[kube-proxy](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) mantém regras de rede nos nós. Estas regras de rede permitem a comunicação de rede com seus _pods_ a partir de sessões de rede dentro ou fora de seu _cluster_.

kube-proxy usa a camada de filtragem de pacotes do sistema operacional se houver uma e estiver disponível. Caso contrário, o kube-proxy encaminha o tráfego para ele mesmo.

***

## <mark style="color:red;">Container Runtime</mark>&#x20;

O agente de execução (_runtime_) de contêiner é o software responsável por executar os contêineres. É o ambiente de execução de contêineres necessário para o funcionamento do k8s.&#x20;

{% hint style="info" %}
**Observação:** O Kubernetes não executa containers, quem faz esse trabalho é o "`Container runtime`"
{% endhint %}

<figure><img src="../.gitbook/assets/image (38).png" alt=""><figcaption></figcaption></figure>

> _O Kubernetes suporta diversos agentes de execução de contêineres:_ [_Docker_](https://docs.docker.com/engine/)_,_ [_containerd_](https://containerd.io/docs/)_,_ [_CRI-O_](https://cri-o.io/#what-is-cri-o)_, e qualquer implementação do_ [_Kubernetes CRI (Container Runtime Interface)_](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-node/container-runtime-interface.md)_._

* Desde a **versão v1.24** o k8s requer que você utilize um container runtime compatível com o `CRI (Container Runtime Interface)` que foi apresentado em 2016 como uma interface capaz de criar um padrão de comunicação entre o container runtime e k8s.

***

* Versões anteriores à v1.24 ofereciam integração direta com o `Docker Engine` usando um componente chamado `dockershim` porém essa integração direta não está mais disponível.

***

* A documentação oficial do Kubernetes **(v1.24)** apresenta alguns ambientes de execução e suas respectivas configurações como o `containerd` um projeto avaliado com o nível graduado pela `CNCF(Cloud Native Computing Foundation)` e o **CRI-0** projeto incubado pela **CNCF**.

***

## <mark style="color:red;">kubectl</mark>&#x20;

{% embed url="https://kubectl.docs.kubernetes.io/" %}

Ferramenta de linha de comando do Kubernetes, permite executar comandos em clusters do Kubernetes, podendo ser usado para **implantar aplicativos, inspecionar e gerenciar recursos de cluster e visualização de logs**.

* É uma sigla para `Kubernetes Control`, muitas das vezes podemos ouvir seu nome pronunciado como `"Kube C T L"`, `"Kube Control"` e `"Kube Cuttle/Cuddle"`, esse ultimo surgiu como um apelido, devido ao seu "Mascote" ser o Cuttle fish (Em português Choco, sibas ou sépia) que é uma espécie de molusco parecido com o polvo

Os comandos do `kubectl` seguem a seguinte semântica:

```bash
kubectl + VERBO + recurso + OPÇÕES
```

Alguns exemplos de verbos:

> &#x20;_get, list, describe, create, update, patch, delete ..._

Alguns exemplos de recursos:

> _nodes, pods, namespaces, services, deployment, replicaset, pv(persistent volume), pvc(persistent volume claim) ..._

* No Kubernetes podemos utilizar o termo `all` como recurso para trabalhar com todos os recursos.

***

#### <mark style="color:yellow;">Kubernetes: Principais Comandos</mark> <a href="#firstheading" id="firstheading"></a>

{% embed url="https://ebasso.net/wiki/index.php?title=Kubernetes:_Principais_Comandos" %}

***

## <mark style="color:red;">Kubeadm</mark>&#x20;

{% embed url="https://kubernetes.io/docs/tasks/tools/" %}

Uma ferramenta para instalar rapidamente o Kubernetes e configurar um cluster seguro.

Você pode usar o kubeadm para instalar a [camada de gerenciamento](https://kubernetes.io/pt-br/docs/reference/glossary/?all=true#term-control-plane) e os componentes dos [nós de processamento](https://kubernetes.io/pt-br/docs/concepts/architecture/nodes/).

***

## <mark style="color:red;">Complementos (</mark>_<mark style="color:red;">addons</mark>_<mark style="color:red;">)</mark> <a href="#addons" id="addons"></a>

{% embed url="https://kubernetes.io/pt-br/docs/concepts/overview/components/#addons" %}

***
