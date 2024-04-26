---
description: >-
  No Kubernetes, namespaces disponibilizam um mecanismo para isolar grupos de
  recursos dentro de um único cluster.
---

# Namespaces

{% embed url="https://kubernetes.io/pt-br/docs/concepts/overview/working-with-objects/namespaces/" %}

***

## <mark style="color:red;">Overview</mark>

<figure><img src="../.gitbook/assets/image (46).png" alt=""><figcaption></figcaption></figure>

Nomes de recursos precisam ser únicos dentro de um namespace, porém podem se repetir em diferentes namespaces.

> Escopos baseados em namespaces são aplicáveis apenas para objetos com namespace _(como: Deployments, Services, etc)_ e não em objetos que abrangem todo o cluster _(como: StorageClass, Nodes, PersistentVolumes, etc)_

{% hint style="info" %}
Namespaces devem ser utilizados em ambientes com múltiplos usuários espalhados por diversos times ou projetos.&#x20;
{% endhint %}

Para clusters com poucos ou até algumas dezenas de usuários, você não deveria precisar criar ou pensar a respeito de namespaces.&#x20;

* Comece a utilizar namespaces quando você precisar das funcionalidades que eles oferecem.

> Namespaces nos permitem dividir os recursos do cluster entre diferentes usuários (via [resource quota](https://kubernetes.io/docs/concepts/policy/resource-quotas/)).

{% hint style="info" %}
Não é necessário utilizar múltiplos namespaces para separar recursos levemente diferentes, como diferentes versões de um mesmo software: use [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels) para distinguir recursos dentro de um mesmo namespace
{% endhint %}

Criação e eliminação de namespaces estão descritas na [documentação de namespaces do guia de administradores](https://kubernetes.io/docs/tasks/administer-cluster/namespaces).

> **Nota:** Evite criar namespaces com o prefixo `kube-`, já que este prefixo é reservado para namespaces do sistema Kubernetes.

O Kubernetes é inicializado com quatro namespaces:

{% tabs %}
{% tab title="Namespaces" %}
```
kubectl get ns
```

NAME                                                                             STATUS                                              AGE

default                                                                            Active                                                 79m

kube-node-lease                                                           Active                                                 79m

kube-public                                                                    Active                                                 79m

kube-system                                                                  Active                                                 79m
{% endtab %}
{% endtabs %}

<mark style="color:blue;">default -</mark> O namespace padrão para objetos sem namespace

***

<mark style="color:blue;">kube-node-lease</mark> - O Kubernetes usa essa Namespace para fazer verificações dentro de um processo avançado como por exemplo, busca por falhas.&#x20;

* Este namespace contém os objetos de [Lease](https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/lease-v1/) associados com cada node. Node leases permitem que o kubelet envie [heartbeats](https://kubernetes.io/docs/concepts/architecture/nodes/#heartbeats) para que a camada de gerenciamento detecte falhas nos nodes.

***

<mark style="color:blue;">kube-public</mark>  - Este namespace é criado automaticamente e é legível por todos os usuários (incluindo usuários não autenticados).&#x20;

* Este namespace é reservado principalmente para uso do cluster, no caso de alguns recursos que precisem ser visíveis e legíveis publicamente por todo o cluster.&#x20;
* O aspecto público deste namespace é apenas uma convenção, não um requisito.

***

<mark style="color:blue;">kube-system</mark> - O namespace para objetos criados pelo sistema Kubernetes.

{% tabs %}
{% tab title="Pods" %}
Podemos validar as pods que são executadas por está Namespace ao subir um cluster Kubernetes

```bash
kubectl get po -n kube-system
```

NAME                                                                               READY       STATUS         RESTARTS     AGE

coredns-5dd5756b68-2jnbs                                        1/1             Running         0                     87m

coredns-5dd5756b68-bn9s4                                       1/1            Running         0                     87m

etcd-k8s-controller-node1                                             1/1            Running         0                     87m

kube-apiserver-k8s-controller-node1                          1/1            Running         0                     87m

kube-controller-manager-k8s-controller-node1       1/1            Running          0                    87m

kube-proxy-dp9xg                                                           1/1            Running         0                     87m

kube-proxy-mw8wb                                                        1/1            Running          0                    87m

kube-proxy-w9cxb                                                           1/1            Running          0                   87m             &#x20;

kube-scheduler-k8s-controller-node1                         1/1            Running          0                    87m              &#x20;

weave-net-4p48j                                                        1/1            Running          1 (85m ago)  87m

weave-net-65sqg                                                       1/1            Running          1 (85m ago)  87m

weave-net-79h64                                                       1/1            Running          1 (85m ago)  87m
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Criando Namespaces Imperative form</mark>

{% tabs %}
{% tab title="Create" %}
```bash
kubectl create namespace frontend --save-config
```

namespace/frontend created

***

```bash
kubectl get ns
```

NAME                                                                             STATUS                                              AGE

default                                                                            Active                                                 79m

<mark style="color:orange;">frontend                                                                         Active                                                 66s</mark>

kube-node-lease                                                           Active                                                 79m

kube-public                                                                    Active                                                 79m

kube-system                                                                  Active                                                 79m
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Utilizando a Namespace criada</mark>

{% hint style="info" %}
**Todos os recursos utilizados nesses exemplos, estarão disponibilizados no Github:**  [https://github.com/danncastro/kubernetes\_projects/tree/main/k8s\_cka\_exemples/namespaces](https://github.com/danncastro/kubernetes\_projects/tree/main/k8s\_cka\_exemples/namespaces)
{% endhint %}

{% tabs %}
{% tab title="Apply" %}
```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/networking/pod-to-pod-communication/tomcat.yml --namespace=frontend
```

pod/tomcat-pod created

***

```bash
kubectl get po
```

No resources found in default namespace.

***

```bash
kubectl get po -n frontend
```

NAME                                                                         READY       STATUS         RESTARTS     AGE

tomcat-pod                                                                1/1              Running         0                     68s
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Configurando Current Context Namespace</mark>&#x20;

Iremos definir como default a namespace criada anteriormente, não sendo mais a namespace `"default"` criada ao estanciar um cluster kubernetes

{% tabs %}
{% tab title="Current Context" %}
```bash
kubectl config set-context --current --namespace=frontend
```

Context "kubernetes-admin@kubernetes" modified.

***

```bash
kubectl run apache-pod --image httpd
```

pod/apache-pod created

***

```bash
kubectl get po
```

NAME                                                                         READY       STATUS         RESTARTS     AGE

apache-pod                                                               1/1              Running         0                     19s

tomcat-pod                                                                1/1              Running         0                     14m
{% endtab %}

{% tab title="Namespace Default" %}
```bash
kubectl get po -n default
```

No resources found in default namespace.

***

```bash
kubectl get po -n frontend
```

NAME                                                                       READY       STATUS         RESTARTS     AGE

apache-pod                                                             1/1              Running         0                     3m9s

tomcat-pod                                                              1/1              Running         0                     16m

***

```bash
kubectl config set-context --current --namespace=default
```

Context "kubernetes-admin@kubernetes" modified.
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl get po -n frontend
```

NAME                                                                    READY       STATUS         RESTARTS     AGE

apache-pod                                                          1/1              Running         0                     6m53s

tomcat-pod                                                           1/1              Running         0                     20m

***

```bash
kubectl delete po -n frontend apache-pod
```

pod "apache-pod" deleted

***

```bash
kubectl delete po -n frontend tomcat-pod
```

pod "tomcat-pod" deleted

***

```bash
kubectl delete namespace frontend
```

namespace "frontend" deleted

***

```bash
kubectl get ns
```

NAME                                                                             STATUS                                              AGE

default                                                                            Active                                                110m

kube-node-lease                                                           Active                                                110m

kube-public                                                                    Active                                                110m

kube-system                                                                  Active                                                110m
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Criando Namespaces Manifest File</mark>

{% tabs %}
{% tab title="Namespace" %}
```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/namespaces/backend-ns.yml
```

namespace/backend-ns created

***

```bash
kubectl get ns
```

NAME                                                                             STATUS                                              AGE

<mark style="color:orange;">backend-ns                                                                   Active                                                 75s</mark>

default                                                                            Active                                                 79m

kube-node-lease                                                           Active                                                 79m

kube-public                                                                    Active                                                 79m

kube-system                                                                  Active                                                 79m

***

```bash
kubectl get po -n backend-ns
```

No resources found in backend-ns namespace.
{% endtab %}

{% tab title="Pod" %}
```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/networking/pod-to-pod-communication/redis.yml --namespace=backend-ns
```

pod/redis-pod created

***

```bash
kubectl get po -n backend-ns
```

NAME                                                                         READY       STATUS         RESTARTS     AGE

redis-pod                                                                   1/1              Running         0                     49s
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl delete po -n backend-ns redis-pod
```

pod "redis-pod" deleted

***

```bash
kubectl delete namespace backend-ns
```

namespace "backend-ns" deleted

***

```bash
kubectl get ns
```

NAME                                                                             STATUS                                            AGE

default                                                                            Active                                               155m

kube-node-lease                                                           Active                                               155m

kube-public                                                                    Active                                               155m

kube-system                                                                  Active                                               155m
{% endtab %}
{% endtabs %}

Nós também podemos definir o campo `namespace` nos arquivos YAML. Exemplo: Aplicamos o arquivo redis-pod.yaml assim:

```bash
kubectl apply -f redis-pod.yaml --namespace=backend-ns
```

Outra opção seria definir o campo namespace no arquivo YAML do redis-pod, veja a linha 5:

<pre class="language-yaml"><code class="lang-yaml"><strong>1 apiVersion: v1
</strong>2 kind: Pod
3 metadata:
4   name: redis-pod
5   namespace: backend-ns #### definição do campo namespace
6   labels:
7      apps: backend
8    
9 spec:
10   containers:
11   - name: container-redis
12     image: redis
</code></pre>

Aplicando `redis.yml` de forma simples, o pod já seria inserido no namespace `backend-ns`, assim:

```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/networking/pod-to-pod-communication/redis.yml
```

***
