---
description: >-
  O ambiente de gerenciamento, gerencia os nós de processamento workers e os
  pods dentro de um cluster.
---

# Componentes da Camada de Gerenciamento

***

{% hint style="info" %}
Em ambientes de produção, o ambiente de gerenciamento é geralmente executado em múltiplos computadores, provendo tolerância a falhas e alta disponibilidade.
{% endhint %}

Os componentes da camada de gerenciamento tomam decisões globais sobre o cluster, bem como detectam e respondem aos eventos do cluster.&#x20;

> Podem ser executados em qualquer máquina do cluster.&#x20;

Contudo, para simplificar, os scripts de configuração normalmente iniciam todos os componentes da camada de gerenciamento na mesma máquina.

***

### <mark style="color:red;">kube-apiserver</mark>&#x20;

O servidor de **API** do Kubernetes valida e configura dados para os objetos presentes no cluster, que incluem `pods`, `serviços`, `controladores de replicação` e outros. O **API Server** atende às operações e fornece o **Frontend** para o estado compartilhado do cluster por meio do qual todos os outros componentes interagem.

***

### <mark style="color:red;">etcd</mark>&#x20;

Componente importante de vários outros projetos. Ele se destaca por ser o armazenamento de dados principal do Kubernetes, é um armazenamento de valor em cluster. Ele ajuda a viabilizar atualizações automáticas mais seguras, coordena a programação de trabalhos em hots e ajuda a configurar redes de sobreposição para containers.

***

### <mark style="color:red;">kube-schenduler</mark>&#x20;

É um processo que atribui pods as nós (`nodes`). Ele determina quais são os posicionamentos válidos para cada pod na fila de agendamento de acordo com as restrições e os recursos disponíveis. _O **kube-schenduler** classifica cada node válido e vincula o pod a um Node adequado._

***

### <mark style="color:red;">kube-controller-manager</mark>&#x20;

No Kubernetes, um controlador é um loop que observa o estado compartilhado do cluster por meio do `kube-apiserver` e faz alterações tentando mover o estado atual para o estado desejado.

***
