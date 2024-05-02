---
description: Ao implantar o Kubernetes, você obtém um cluster.
---

# Cluster Kubernetes

{% embed url="https://kubernetes.io/pt-br/docs/concepts/overview/components/" %}

***

## <mark style="color:red;">Overview</mark>

Um cluster Kubernetes consiste em um conjunto de servidores de processamento, chamados nodes, que executam aplicações em contêineres  dentro das `PODS`. &#x20;

> _Quando se executa o Kubernetes, está se executando um cluster._&#x20;

* No mínimo, um cluster K8s contém um plano de controle `Control-plane` e pelo menos um servidor de processamento `Worker node` ("Máquina ou nó `(node)"`).

<figure><img src="../.gitbook/assets/image (51) (1).png" alt=""><figcaption></figcaption></figure>

* O servidor de processamento (`Worker`) hospeda os Pods que são componentes de uma aplicação.

<figure><img src="../.gitbook/assets/image (59) (1).png" alt=""><figcaption></figcaption></figure>

> _O ambiente de gerenciamento cuida dos nós de processamento e os Pods no cluster._&#x20;

{% hint style="info" %}
Em ambientes de produção, o ambiente de gerenciamento é geralmente executado em múltiplos computadores, provendo tolerância a falhas e alta disponibilidade.
{% endhint %}

***

## <mark style="color:red;">API-Resources</mark>

{% embed url="https://kubernetes.io/docs/reference/kubectl/" %}

Executando no terminal podemos visualizar uma descrição dos recursos disponíveis no Kubernetes assim como também possíveis abreviações aceitas pelo `kubectl`

```bash
kubectl api-resource
```

***
