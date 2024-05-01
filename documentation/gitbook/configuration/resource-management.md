---
description: Controla os aspectos de recursos operacionais requisitados pelos containers.
---

# Resource Management

{% embed url="https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/" %}

{% hint style="info" %}
#### Todos os recursos utilizados nesses exemplos, estarão disponibilizados no Github:

[https://github.com/danncastro/nki-kubernetes-projects/tree/main/k8s-cka-exemples/pods](https://github.com/danncastro/nki-kubernetes-projects/tree/main/k8s-cka-exemples/pods)
{% endhint %}

***

## <mark style="color:red;">Requests</mark>

São referentes ao minimo de recursos necessários para o funcionamento da aplicação, (minimo de memória, minimo de CPU... etc.)

<mark style="color:blue;">**Requisitado por Container:**</mark>&#x20;

Os recursos de Kubernetes são requisitados para Containers e não para Pods, os recursos solicitados pelas Pods são uma somatória de todos os recursos requisitados por todos os containers dentro da Pod.

* Então digamos que a Pod tenha apenas um container, isso significa que o total de recursos que a Pod precisará é basicamente para atender esse unico container.&#x20;
* Agora caso a Pod tenha mais de um ou diversos outros Containers dentro dela, será feito uma somatória de todos os recursos minimos necessarios para que a aplicação possa funcionar.

<mark style="color:blue;">**Escalonamento no Kubernetes:**</mark>&#x20;

Garante que a somatória das requisições de recursos das Pods, não exceda a capacidade de recursos disponibilizados para os Nodes. Por exemplo se eu tiver um Node com 1GB de memória, a quantidade de recursos somados de todos os Pods, não poderá exceder o limite de 1GB do Node.

<mark style="color:blue;">**Recursos das Pods são Mandatórios:**</mark>&#x20;

Recursos das Pods são mandatorios sobre recursos de Containers, exemplo, se um container solicita 1 CPU, mas a configuração da pod especifica apenas 0.5 CPU, o container será implantado com apenas 0.5 CPU, obedecendo à mandatoriedade da pod.

<mark style="color:blue;">**Impacto no Desempenho e na Disponibilidade**</mark><mark style="color:blue;">:</mark>&#x20;

Solicitações de recursos afetam o desempenho e a disponibilidade das aplicações em execução no Kubernetes. Por exemplo, garantir solicitações adequadas de recursos pode evitar problemas de falta de recursos e ajudar na escalabilidade e na tolerância a falhas.

<mark style="color:blue;">**Políticas de QoS (Quality of Service)**</mark><mark style="color:blue;">:</mark>&#x20;

Uma menção rápida às políticas de QoS no Kubernetes, que são afetadas pelas solicitações de recursos. Por exemplo, as pods com solicitações de recursos definidas têm prioridade mais alta em relação às pods sem essas definições.

<mark style="color:blue;">**Ajustes Dinâmicos de Recursos**</mark><mark style="color:blue;">:</mark>&#x20;

Vale mencionar a capacidade do Kubernetes de fazer ajustes dinâmicos nos recursos alocados com base na demanda. Por exemplo, o Kubernetes pode dimensionar automaticamente o número de réplicas de um pod com base na carga de trabalho e nas solicitações de recursos definidas.

***

### <mark style="color:red;">Criando Pods - Implementando Requests</mark>



{% tabs %}
{% tab title="Create Pod" %}
```bash
kubectl get po -owide
```

No resources found in default namespace.

***

```bash
kubectl apply -f nki-kubernetes-projects/k8s_cka_exemples/pods/pod_resources_requests.yml
```

pod/request-resources-pod created

***

```bash
kubectl get po -owide
```

NAME                             READY    STATUS       RESTARTS     AGE        IP                 NODE

request-resources         1/1            Running       0                      49s        10.36.0.1      k8s-worker-node2
{% endtab %}

{% tab title="Describe" %}
```bash
kubectl describe po request-resources
```

Name:                            request-resources

Namespace:                  default

Priority:                           0

Service Account:          default

Node:                              k8s-worker-node2/192.168.0.52

Start Time:                    Sat, 27 Apr 2024 02:10:56 +0000

Labels:                            \<none>

Annotations:                  \<none>

Status:                            Running&#x20;

IP:                                     10.36.0.1

IPs:&#x20;

&#x20;   IP:           10.36.0.1&#x20;

Containers:                   &#x20;

&#x20;   apache-container:&#x20;

Container ID:   containerd://e6a153eba5bfc9c47d492e33d50a6fcf030684b87e323a75212a168cada80166&#x20;

Image:          httpd&#x20;

Image ID:     docker.io/library/httpd@sha256:36c8c79f900108f0f09fd4148ad35ade57cba0dc19d13f3d15be24ce94e6a639&#x20;

Port:                     \<none>

Host Port:            \<none>

State:                   Running&#x20;

&#x20;   Started:            Sat, 27 Apr 2024 02:11:18 +0000

Ready:                  True&#x20;

Restart Count:    0&#x20;

<mark style="color:orange;">Requests:</mark>&#x20;

&#x20;   <mark style="color:orange;">cpu: 500m</mark>&#x20;

&#x20;   <mark style="color:orange;">memory: 128Mi</mark>&#x20;

Environment:        \<none>

Mounts:&#x20;

&#x20;   /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-d5pzl (ro)

....

***
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl delete po request-resources
```

pod "request-resources" deleted

***
{% endtab %}
{% endtabs %}

***

## <mark style="color:red;">Limits</mark>

Refere-se ao máximo de recursos que um container pode utilizar.&#x20;

> Enquanto os "requests" (solicitações) definem o mínimo de recursos necessários para que um contêiner funcione corretamente, os "limits" definem o máximo que um contêiner pode utilizar.

Quando se define um limite para um contêiner, estamos especificando a quantidade máxima de CPU e memória que o contêiner pode consumir. Isso é útil para garantir que nenhum contêiner consuma mais recursos do que o necessário, o que pode levar a problemas de desempenho ou à indisponibilidade de recursos para outros contêineres no mesmo nó.

* Por exemplo, se você definir um limite de CPU de 1 núcleo e um limite de memória de 1 GB para um contêiner, ele nunca poderá consumir mais do que isso, mesmo que recursos adicionais estejam disponíveis no nó.&#x20;
* Isso ajuda a evitar que um único contêiner monopolize os recursos do sistema, garantindo um compartilhamento mais equitativo entre os contêineres em um cluster Kubernetes.

***

### <mark style="color:red;">Criando Pods - Implementando Limits</mark>

{% tabs %}
{% tab title="Create Pod" %}
```bash
kubectl get po -owide
```

No resources found in default namespace.

***

```bash
kubectl apply -f nki-kubernetes-projects/k8s_cka_exemples/pods/pod_resources_limits.yml
```

pod/limits-resources created

***

```bash
kubectl get po -owide
```

NAME                             READY    STATUS       RESTARTS     AGE        IP                 NODE

limits-resources             1/1            Running       0                      4s        10.36.0.1      k8s-worker-node2
{% endtab %}

{% tab title="Describe" %}
```bash
kubectl describe po limits-resources
```

Name:                            limits-resources

Namespace:                  default

Priority:                           0

Service Account:          default

Node:                              k8s-worker-node2/192.168.0.52

Start Time:                    Wed, 01 May 2024 17:44:08 +0000

Labels:                            \<none>

Annotations:                  \<none>

Status:                            Running&#x20;

IP:                                     10.36.0.1

IPs:&#x20;

&#x20;   IP:           10.36.0.1&#x20;

Containers:                   &#x20;

&#x20;   apache-container:&#x20;

Container ID:   containerd://5f4e922cdafa941022509de0cea42a38ef78dff33b8b4b53f5d70e5b051aaabc&#x20;

Image:          httpd&#x20;

Image ID:     docker.io/library/httpd@sha256:36c8c79f900108f0f09fd4148ad35ade57cba0dc19d13f3d15be24ce94e6a639&#x20;

Port:                     \<none>

Host Port:            \<none>

State:                   Running&#x20;

&#x20;   Started:            Wed, 01 May 2024 17:44:10 +0000

Ready:                  True&#x20;

Restart Count:    0&#x20;

<mark style="color:orange;">Limits:</mark>&#x20;

&#x20;   <mark style="color:orange;">cpu: 1</mark>

&#x20;   <mark style="color:orange;">memory: 256Mi</mark>&#x20;

Requests:&#x20;

&#x20;   cpu: 500m&#x20;

&#x20;   memory: 128Mi&#x20;

Environment:        \<none>

Mounts:&#x20;

&#x20;   /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-g79vj (ro)

....
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl delete po limits-resources
```

pod "limits-resources" deleted

***
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Criando Multiplos Containers- Implementando Limits e Requests</mark>

{% tabs %}
{% tab title="Create MultiContainers" %}
```bash
kubectl get po -owide
```

No resources found in default namespace.

***

```bash
kubectl apply -f nki-kubernetes-projects/k8s_cka_exemples/pods/pod_resources_multicontainers.yml
```

pod/request-resources-pod created

***

```bash
kubectl get po -owide
```

NAME                                      <mark style="color:orange;">READY</mark>   STATUS    RESTARTS   AGE    IP                 NODE

resources-multicontainers   <mark style="color:orange;">2/2</mark>          Running    0                      49s    10.36.0.1     k8s-worker-node2
{% endtab %}

{% tab title="Describe" %}
```bash
kubectl describe po resources-multicontainers
```

Name:                            resources-multicontainers

Namespace:                  default

Priority:                           0

Service Account:          default

Node:                              k8s-worker-node2/192.168.0.52

Start Time:                    Wed, 01 May 2024 17:58:51 +0000

Labels:                            \<none>

Annotations:                  \<none>

Status:                            Running&#x20;

IP:                                     10.36.0.1

IPs:&#x20;

&#x20;   IP:           10.36.0.1&#x20;

Containers:                   &#x20;

&#x20;   <mark style="color:orange;">apache-container:</mark>&#x20;

&#x20;       Container ID: containerd://ebcbfe26c0a998c573d9e17d586d4fd93eb43c9b7e852d606f549a0239f8feda&#x20;

Image:          httpd&#x20;

Image ID:     docker.io/library/httpd@sha256:36c8c79f900108f0f09fd4148ad35ade57cba0dc19d13f3d15be24ce94e6a639

Port:                     \<none>

Host Port:            \<none>

State:                   Running&#x20;

&#x20;   Started:            Wed, 01 May 2024 17:58:54 +0000

Ready:                  True&#x20;

Restart Count:    0&#x20;

<mark style="color:orange;">Limits:</mark>&#x20;

&#x20;   <mark style="color:orange;">cpu: 1</mark>

&#x20;   <mark style="color:orange;">memory: 256Mi</mark>&#x20;

<mark style="color:orange;">Requests:</mark>&#x20;

&#x20;   <mark style="color:orange;">cpu: 500m</mark>&#x20;

&#x20;   <mark style="color:orange;">memory: 128Mi</mark>&#x20;

Environment:        \<none>

Mounts:&#x20;

&#x20;   /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-tqz76 (ro)

....                  &#x20;

&#x20;   <mark style="color:orange;">redis-container:</mark>&#x20;

&#x20;       Container ID: containerd://dee34bc97268bebee7694bd57fc97d95e5c1561abe48fbe1e5ef0ecdc707aece

Image:          httpd&#x20;

Image ID:     docker.io/library/redis@sha256:f14f42fc7e824b93c0e2fe3cdf42f68197ee0311c3d2e0235be37480b2e208e6

Port:                     \<none>

Host Port:            \<none>

State:                   Running&#x20;

&#x20;   Started:            Wed, 01 May 2024 17:59:02 +0000

Ready:                  True&#x20;

Restart Count:    0&#x20;

<mark style="color:orange;">Limits:</mark>&#x20;

&#x20;   <mark style="color:orange;">cpu: 500m</mark>

&#x20;   <mark style="color:orange;">memory: 128Mi</mark>

<mark style="color:orange;">Requests:</mark>&#x20;

&#x20;   <mark style="color:orange;">cpu: 250m</mark>

&#x20;   <mark style="color:orange;">memory: 64Mi</mark>

Environment:        \<none>

Mounts:&#x20;

&#x20;   /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-tqz76 (ro)
{% endtab %}
{% endtabs %}

***
