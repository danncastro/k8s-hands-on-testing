---
description: Ao implantar o Kubernetes, você obtém um cluster.
---

# Componentes do Kubernetes

## <mark style="color:red;">Cluster Kubernetes</mark>&#x20;

{% embed url="https://kubernetes.io/pt-br/docs/concepts/overview/components/" %}

Um cluster Kubernetes consiste em um conjunto de servidores de processamento, chamados nodes, que executam aplicações em contêineres  dentro das `PODS`.  Quando se executa o Kubernetes, está se executando um cluster. Todo cluster possui ao menos um servidor de processamento `Worker node`

* No mínimo, um cluster contém um plano de controle `Control-plane` e pelo menos um servidor de processamento `Worker node`.  "Máquina ou nó `(node)"`.

<figure><img src="../.gitbook/assets/image (26).png" alt=""><figcaption></figcaption></figure>

* Consiste em um conjunto de servidores de processamento, chamado **nós (`nodes`)**, que executam aplicações em contêineres.
* O servidor de processamento (`Worker`) hospeda os Pods que são componentes de uma aplicação.

<figure><img src="../.gitbook/assets/image (34).png" alt=""><figcaption></figcaption></figure>

> _O ambiente de gerenciamento cuida dos nós de processamento e os Pods no cluster._&#x20;

Em ambientes de produção, o ambiente de gerenciamento é geralmente executado em múltiplos computadores, provendo tolerância a falhas e alta disponibilidade.

***

## <mark style="color:red;">API-Resources</mark>

{% embed url="https://kubernetes.io/docs/reference/kubectl/" %}

Executando no terminal podemos visualizar uma descrição dos recursos disponíveis no Kubernetes assim como também possíveis abreviações aceitas pelo `kubectl`

```bash
kubectl api-resource
```

***
