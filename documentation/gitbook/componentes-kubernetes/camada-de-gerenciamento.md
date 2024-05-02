---
description: >-
  Os componentes da camada de gerenciamento tomam decisões globais sobre o
  cluster, bem como detectam e respondem aos eventos do cluster.
---

# Camada de Gerenciamento

{% embed url="https://kubernetes.io/pt-br/docs/concepts/overview/components/#componentes-da-camada-de-gerenciamento" %}

{% hint style="info" %}
Em ambientes de produção, o ambiente de gerenciamento é geralmente executado em múltiplos computadores, provendo tolerância a falhas e alta disponibilidade.
{% endhint %}

> _Podem ser executados em qualquer máquina do cluster. Contudo, para simplificar, os scripts de configuração normalmente iniciam todos os componentes da camada de gerenciamento na mesma máquina._

***

## <mark style="color:red;">kube-apiserver</mark>&#x20;

É o componente central que expõe a API do Kubernetes e serve como ponto de entrada para o cluster.

> Toda ação que acontece dentro do Cluster, passa pela kube-apiserver, somente ela pode escrever as configurações do _"banco de dados"_ do Kubernetes(etcd)

O servidor de **API** do Kubernetes valida e configura dados para os objetos presentes no cluster, que incluem `pods`, `serviços`, `controladores de replicação` e outros.

O **API Server** atende às operações e fornece o **Frontend** para o estado compartilhado do cluster por meio do qual todos os outros componentes interagem.

<figure><img src="../.gitbook/assets/image (52) (1).png" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:red;">etcd</mark>&#x20;

{% embed url="https://etcd.io/" %}

`etcd` é um banco de dados do tipo "chave -> valor"  distribuído e fortemente consistente que fornece uma maneira confiável de armazenar dados que precisam ser acessados ​​por um sistema distribuído ou cluster de máquinas. Ele lida com as eleições de líder durante partições de rede e pode tolerar falhas de máquina, mesmo no nó líder.

Ele se destaca por ser o principal armazenamento de dados do Kubernetes, ele ajuda a viabilizar atualizações automáticas mais seguras, coordena a programação de trabalhos em hots e ajuda a configurar redes de sobreposição para containers.

> _etcd é um componente importante de vários outros projetos, não apenas do Kubernetes, ou seja ele é um componente externo aplicado a infraestrutura Kubernetes._

***

## <mark style="color:red;">kube-schenduler</mark>&#x20;

Faz o agendamento dos pods em nós apropriados com base em requisitos e restrições definidos, como recursos e afins.

Ele recebe as requisições vindas do kube-apiserver, e gerência da melhor forma onde será instânciado a nova aplicação.&#x20;

<figure><img src="../.gitbook/assets/image (17) (1).png" alt=""><figcaption></figcaption></figure>

> Ele consulta o API Server para obter informações sobre os recursos do cluster e decide onde colocar os pods com base em políticas de agendamento.

É um processo que atribui pods as nós (`nodes`). Ele determina quais são os posicionamentos válidos para cada pod na fila de agendamento de acordo com as restrições e os recursos disponíveis.&#x20;

> _O **kube-schenduler** classifica cada node válido e vincula o pod a um Node adequado._

***

## <mark style="color:red;">kube-controller-manager</mark>&#x20;

Responsável por gerenciar os controladores que regulam o estado desejado do sistema. Há vários controladores, como o controlador de replicação, o controlador de serviço, etc.

No Kubernetes, um controlador é um loop que observa o estado compartilhado do cluster por meio do `kube-apiserver` e faz alterações tentando mover o estado atual para o estado desejado.

> _Executa todas as operações de gerenciamento para manter a disponibilidade do cluster._

<figure><img src="../.gitbook/assets/image (16) (1).png" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:red;">Cloud-controller-manager</mark>

***
