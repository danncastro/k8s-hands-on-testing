---
description: >-
  Kubernetes é uma ferramenta de orquestração de containers criado pelo google
  em 2014. Deu certo
---

# Kubernetes

***

## <mark style="color:red;">Historia do Kubernetes</mark>

Começada em 2003 com o lançamento da ferramenta Google Borg Container Orchestration System, que é um gerenciador de cluster usado pelo Google.&#x20;

Necessitada de uma ferramenta mais robusta pois o Google Borg ainda hoje, implementa mais de 12 bilhões de aplicações por mês, surgindo assim o Kubernetes que foi introduzido em 2014 sendo uma ramificação do Borg, tornando - se a plataforma dominante a partir de 2019, hoje mantido pela Cloud Native Computing Foundation

***

## <mark style="color:red;">O que é o Kubernetes</mark>

Sistema open source utilizado para implantação, automatização de `deployments`, escalonamento e gerenciamento de aplicativos em contêineres, também conhecido pelas abreviaturas `k8s` ou `kube`.

> O nome _**k8s**_ é uma abreviação de **"Kubernetes"**, sendo `k` + `8 letras` + `s`.

Isso por que nos anos 80 os programadores eram "preguiçosos" e gostavam de abreviar as palavras baseando sempre em primeira letra, ultima letra e o numero de letras entre eles.

{% hint style="info" %}
Seguindo este padrão, surgiu o **k8s**.
{% endhint %}

A palavra "Kubernetes", faz alusão a um navio cargueiro;

* Kubernetes -> "Kuvernetes" (em Grego) -> "Timoneiro" (Aquele que conduz o navio).

<figure><img src=".gitbook/assets/image (28).png" alt=""><figcaption></figcaption></figure>

***

* Muitos dos contextos e termos do k8s incluindo o logotipo com 7 Malaguetas, uma foi uma homenagem á personagem da série Star Trek "projeto Seven of Nine", e Borg também é uma homenagem a série pois significa:  "Organismo cibernético de Star Trek."

K8s ajuda a organizar e administrar aplicações em ambientes onde existem dezenas e até milhares de containers. As aplicações podem estar em diferentes ambientes de implementação:

* Infraestrutura local
* Máquinas virtuais
* Cloud Pública
* Cloud Híbrida

***

#### <mark style="color:yellow;">Alguns Exemplos de termos abreviados:</mark>

* Kubernetes `(k8s)`
* Internationalization `(i18n)`
* Localization `(l10n)`
* Globalization `(g11n)`
* Localizability `(l12y)`

Também vemos alguns termos como `k3s` e `k0s` quando falamos de Kubernetes, estes se referem a distribuições de Kubernetes.

***

* [K3s](https://k3s.io/) - Distribuição com foco em ter a metade do tamanho em consumo de memória. Kubernetes é uma palavra de 10 letras estilizada como k8s. Portanto, algo com a metade do tamanho do Kubernetes seria uma palavra de 5 letras estilizada como K3s.

***

* [K0s](https://k0sproject.io/) - Distribuição com foco em facilitação. _**"K0s é para Kubernetes o que Docker é para containers"**_. O nome zero é utilizado para significar zero atrito, zero custo e zero sobrecarga.

***

### <mark style="color:red;">O que é um orquestrador de containers</mark>

<figure><img src=".gitbook/assets/image (23).png" alt=""><figcaption><p>Fonte: https://kubernetes.io/pt-br/docs/tutorials/kubernetes-basics</p></figcaption></figure>

Sistema de automatização, visa, automatizar todo o ciclo de vida dos  containers e da aplicação e estão focados em:

* Implantação
* Provisionamento
* Networking
* Dimensionamento
* Disponibilidade
* Gerenciamento do ciclo de vida dos containers

***

### <mark style="color:red;">Quais necessidades de uma ferramenta de orquestração de containers?</mark>

* Migração de aplicações monolíticas para microsserviços;
* Disponibilidade da aplicação _(diminuição do downtime)_
* Escalabilidade e alta performance;
* Recuperação de desastre _**(Backup/Restore)**_

***

#### _<mark style="color:yellow;">**Alguns Orquestradores além do Kubernetes**</mark>_

<figure><img src=".gitbook/assets/image (31).png" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:red;">Características do K8s</mark>

#### <mark style="color:yellow;">Imutabilidade Kubernetes</mark>

1. Princípios da infraestrutura imutável
2. Substituir um objeto criado
3. Incremento de segurança contra indisponibilidade

***

#### <mark style="color:yellow;">Disponibilidade do K8s</mark>

1. Configuração declarativa (Arquivos)
   1. Comandos imperativos (Ações no terminal)
   2. Configurações declarativas (Estado)
2. Self-Healing System
3. Autoscale Up/Down
4. DevOps Automation Tool
5. Fault Protection (Ações preventivas)

***

#### <mark style="color:yellow;">Escalabilidade -> Services/Applications</mark>

1. YAML/Json Manifest files
2. Escala declarativa
3. Cluster scale support
4. Service-based decoupling for teams
5.  Separation of Responsibilities Concept

    1. Desenvolvedores (Dev)
    2. Administradores K8s (Ops)



    <figure><img src=".gitbook/assets/image (35).png" alt=""><figcaption></figcaption></figure>

***

#### <mark style="color:yellow;">Abstração de Infraestrutura</mark>

Possibilidades para criações de Clusters

1. Cloud Abstraction
2. Bare metal
3. Virtual Machines
4. Kind
5. Raspberry Pi

***
