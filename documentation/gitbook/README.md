---
description: >-
  Kubernetes é uma ferramenta de orquestração de containers criado pelo google
  em 2014.
---

# Kubernetes

<figure><img src=".gitbook/assets/image (48).png" alt=""><figcaption><p>Fonte: https://kubernetes.io/pt-br/docs/tutorials/kubernetes-basics</p></figcaption></figure>

***

## <mark style="color:red;">Historia do Kubernetes</mark>

Começada em 2003 com o lançamento da ferramenta Google Borg (Container Orchestration System), que é o Orchestrador de Serviços desenvolvido pela Google.&#x20;

Necessitada de uma ferramenta mais robusta pois o Google Borg ainda hoje, implementa mais de 12 bilhões de aplicações por mês, surgindo assim o Kubernetes que foi introduzido em 2014 sendo uma ramificação do Borg, tornando - se a plataforma dominante a partir de 2019, hoje mantido pela Cloud Native Computing Foundation

***

## <mark style="color:red;">O que é o Kubernetes</mark>

Sistema open source utilizado para implantação, automatização de `deployments`, escalonamento e gerenciamento de aplicativos em contêineres, também conhecido pelas abreviaturas `k8s` ou `kube`.

> _O nome **k8s** é uma abreviação de **"Kubernetes"**, sendo `k` + `8 letras` + `s`._

Isso por que nos anos 80 os programadores eram "preguiçosos" e gostavam de abreviar as palavras baseando sempre em primeira letra, ultima letra e o numero de letras entre eles.

{% hint style="info" %}
Seguindo este padrão, surgiu o **k8s**.
{% endhint %}

A palavra "Kubernetes", faz alusão a um navio cargueiro;

* Kubernetes -> "Kuvernetes" (em Grego) -> "Timoneiro" (Aquele que conduz o navio).

<figure><img src=".gitbook/assets/image (53).png" alt=""><figcaption></figcaption></figure>

* Muitos dos contextos e termos do k8s incluindo o logotipo com 7 Malaguetas, uma foi uma homenagem á personagem da série Star Trek "projeto Seven of Nine", e Borg também é uma homenagem a série pois significa:  "Organismo cibernético de Star Trek."

K8s ajuda a organizar e administrar aplicações em ambientes onde existem dezenas e até milhares de containers. As aplicações podem estar em diferentes ambientes de implementação:

* Infraestrutura local
* Máquinas virtuais
* Cloud Pública
* Cloud Híbrida

#### <mark style="color:blue;">Alguns Exemplos de termos abreviados:</mark>

* Kubernetes `(k8s)`
* Internationalization `(i18n)`
* Localization `(l10n)`
* Globalization `(g11n)`
* Localizability `(l12y)`

Também vemos alguns termos como `k3s` e `k0s` quando falamos de Kubernetes, estes se referem a distribuições de Kubernetes.

* [K3s](https://k3s.io/) - Distribuição com foco em ter a metade do tamanho em consumo de memória. Kubernetes é uma palavra de 10 letras estilizada como k8s. Portanto, algo com a metade do tamanho do Kubernetes seria uma palavra de 5 letras estilizada como K3s.

***

* [K0s](https://k0sproject.io/) - Distribuição com foco em facilitação. _**"K0s é para Kubernetes o que Docker é para containers"**_. O nome zero é utilizado para significar zero atrito, zero custo e zero sobrecarga.

***

### <mark style="color:red;">O que é um orquestrador de containers</mark>

São sistemas de automatização, e visam automatizar todo o ciclo de vida dos containers e da aplicação e estão focados em:

* Implantação
* Provisionamento
* Networking
* Dimensionamento
* Disponibilidade
* Gerenciamento do ciclo de vida dos containers

#### <mark style="color:blue;">Quais necessidades de uma ferramenta de orquestração de containers?</mark>

* Migração de aplicações monolíticas para microsserviços;
* Disponibilidade da aplicação _(diminuição do downtime)_
* Escalabilidade e alta performance;
* Recuperação de desastre _**(Backup/Restore)**_

#### _<mark style="color:blue;">**Alguns Orquestradores além do Kubernetes**</mark>_

<figure><img src=".gitbook/assets/image (56).png" alt=""><figcaption></figcaption></figure>

***

### <mark style="color:red;">Características do K8s</mark>

#### <mark style="color:blue;">Imutabilidade Kubernetes</mark>

* Princípios da infraestrutura imutável
* Substituir um objeto criado
* Incremento de segurança contra indisponibilidade

#### <mark style="color:blue;">Disponibilidade do K8s</mark>

* Configuração declarativa (Arquivos)
  * Comandos imperativos (Ações no terminal)
  * Configurações declarativas (Estado)
* Self-Healing System
* Autoscale Up/Down
* DevOps Automation Tool
* Fault Protection (Ações preventivas)

#### <mark style="color:blue;">Escalabilidade -> Services/Applications</mark>

* YAML/JSON manifest files
* Escala declarativa
* Cluster Scale Support
* Service-based decoupling for teams
* Separation of Responsibilities Concept
  * Desenvolvedores (Dev)
  * Administradores K8s (Ops)



<figure><img src=".gitbook/assets/image (60).png" alt=""><figcaption></figcaption></figure>

***

#### <mark style="color:blue;">Abstração de Infraestrutura</mark>

Possibilidades para criações de Clusters

* Cloud Abstraction
* Bare metal
* Virtual Machines
* Kind
* Raspberry Pi

***

### <mark style="color:red;">Glossário</mark>

{% embed url="https://kubernetes.io/pt-br/docs/reference/glossary/?all=true#term-cluster" %}
