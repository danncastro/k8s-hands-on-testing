---
description: >-
  Um ReplicaSet no Kubernetes (k8s) é um controlador que garante que um número
  especificado de réplicas de um pod esteja em execução a qualquer momento no
  cluster.
---

# ReplicaSets

{% embed url="https://kubernetes.io/pt-br/docs/concepts/workloads/controllers/replicaset/" %}

Ele garante alta disponibilidade e escalabilidade ao monitorar continuamente o estado dos pods e iniciar ou encerrar réplicas conforme necessário para manter o estado desejado.&#x20;

Se um pod falhar ou for removido por qualquer motivo, o ReplicaSet iniciará automaticamente uma nova réplica para substituí-lo, garantindo que o número desejado de réplicas seja mantido em execução.

> _Por isso, é geralmente utilizado para garantir a disponibilidade de um certo número de Pods idênticos._

{% hint style="info" %}
Uma das desvantagens da utilização de ReplicasSet, é que ele não faz a alteração dos recursos automaticamente, então toda vez que uma alteração é feita, um novo deploy deve ser aplicado.
{% endhint %}

***

## <mark style="color:red;">Criando ReplicaSets</mark>

{% hint style="info" %}
**Todos os recursos utilizados nesses exemplos, estarão disponibilizados no Github:**\
[https://github.com/danncastro/kubernetes\_projects/tree/main/k8s\_cka\_exemples/replicasets](https://github.com/danncastro/kubernetes\_projects/tree/main/k8s\_cka\_exemples/replicasets)
{% endhint %}

{% tabs %}
{% tab title="Create ReplicaSet" %}
1. Vamos validar os recursos disponíveis antes de deployar o projeto

```bash
kubectl get po -owide
```

No resources found in default namespace.

```bash
kubectl get rs -owide
```

No resources found in default namespace.

***

```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/replicasets/frontend_app.yml
```

replicaset.apps/frontend-rs created

***

2. Vamos novamente validar, após o deploy

```bash
kubectl get po -owide
```

NAME                             READY     STATUS     RESTARTS   AGE       IP                NODE

frontend-rs-2pjlw         1/1              Running     0                    28s         10.44.0.1     k8s-worker-node2

frontend-rs-c6xsb        1/1              Running     0                    28s         10.47.0.2     k8s-worker-node1

frontend-rs-dgbtl          1/1             Running     0                     28s         10.47.0.1     k8s-worker-node1

***

```bash
kubectl get rs -owide
```

\---

frontend-rs        3          3          3        20m        container-nginx        nginx          apps=webserver-app
{% endtab %}

{% tab title="Deleted Pod" %}
1. Vamos deletar uma das pods para testar a escalabilidade dos recursos

```bash
kubectl delete po frontend-rs-2pjlw
```

pod "frontend-2pjlw" deleted

***

2. Após a deleção, outro recurso será aplicado automaticamente para manter as quantidades de replicas indicadas no manifesto.

```bash
kubectl get po -owide
```

NAME                               READY   STATUS    RESTARTS   AGE        IP                   NODE

<mark style="color:orange;">frontend-rs-7bv6f          1/1            Running    0                  11s              10.44.0.2      k8s-worker-node2</mark>

frontend-rs-c6xsb          1/1            Running    0                  4m24s      10.47.0.2      k8s-worker-node1

frontend-rs-dgbtl           1/1            Running    0                  4m24s      10.47.0.1       k8s-worker-node1
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">ReplicaSet Scale - Manifest File</mark>

{% tabs %}
{% tab title="Scale Up" %}
1. Vamos aumentar o valor de replicas dentro do manifesto

```yaml
  replicas: 5
```

```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/replicasets/frontend_app.yml
```

replicaset.apps/frontend-rs configured

***

2. Podemos visualizar que a quantidade de pods aumentaram.

```bash
kubectl get po -owide
```

NAME                               READY   STATUS    RESTARTS   AGE      IP                NODE

frontend-rs-7bv6f          1/1          Running    0                  7m25s   10.44.0.2     k8s-worker-node2

frontend-rs-c6xsb         1/1           Running   0                   11m        10.47.0.2      k8s-worker-node1

frontend-rs-dgbtl           1/1          Running    0                   11m         10.47.0.1     k8s-worker-node1

<mark style="color:orange;">frontend-rs-hdb9c         1/1          Running    0                   18s         10.44.0.1     k8s-worker-node2</mark>

<mark style="color:orange;">frontend-rs-nrmqd         1/1          Running    0                   18s         10.47.0.3     k8s-worker-node1</mark>

***

```bash
kubectl get rs -owide
```

\---

frontend-rs        5          5          5        20m        container-nginx        nginx          apps=webserver-app
{% endtab %}

{% tab title="Scale Down" %}
1. Vamos novamente ajustar o manifesto, e diminuir a quantidade de replicas.

```yaml
  replicas: 2
```

***

```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/replicasets/frontend_app.yml
```

replicaset.apps/frontend-rs configured

***

2. Visualizando novamente os recursos, podemos notar que agora a quantidade em execução é de 2 pods.

```bash
kubectl get po -owide
```

NAME                               READY   STATUS    RESTARTS   AGE      IP                  NODE

frontend-rs-c6xsb          1/1           Running    0                   11m          10.47.0.2     k8s-worker-node1

frontend-rs-dgbtl            1/1          Running    0                    11m         10.47.0.1       k8s-worker-node1

***

```bash
kubectl get rs -owide
```

\---

frontend-rs        2          2          2        20m        container-nginx        nginx          apps=webserver-app
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl delete rs frontend-rs
```

replicaset.apps "frontend-rs" deleted

***

```bash
kubectl get po -owide
```

No resources found in default namespace.

```bash
kubectl get rs -owide
```

No resources found in default namespace.
{% endtab %}
{% endtabs %}

***

### &#x20;<mark style="color:red;">ReplicaSet Scale - Imperative Form</mark>

{% tabs %}
{% tab title="ReplicaSet" %}
```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/replicasets/frontend_app.yml
```

replicaset.apps/frontend-rs created

***

```bash
kubectl get po -owide
```

NAME                               READY   STATUS     RESTARTS   AGE      IP                 NODE

frontend-rs-7htlt            1/1            Running     0                    11s         10.44.0.1      k8s-worker-node2

frontend-rs-j9mcm        1/1            Running     0                    11s         10.47.0.2     k8s-worker-node1

frontend-rs-pxm6k        1/1            Running     0                    11s         10.44.0.2     k8s-worker-node2

***

```bash
kubectl get rs -owide
```

\---

frontend-rs        3          3          3        20m        container-nginx        nginx          apps=webserver-app
{% endtab %}

{% tab title=" Scale Down" %}
<pre class="language-bash"><code class="lang-bash"><strong>kubectl scale rs frontend-rs --replicas=1
</strong></code></pre>

replicaset.apps/frontend-rs scaled

***

```bash
kubectl get po -owide
```

NAME                               READY   STATUS     RESTARTS   AGE      IP                 NODE

frontend-rs-j9mcm        1/1           Running     0                     11s         10.47.0.2     k8s-worker-node1

***

```bash
kubectl get rs -owide
```

\---

frontend-rs        1          1          1        20m        container-nginx        nginx          apps=webserver-app
{% endtab %}

{% tab title="Scale Up" %}
<pre class="language-bash"><code class="lang-bash"><strong>kubectl scale rs frontend-rs --replicas=3
</strong></code></pre>

replicaset.apps/frontend scaled

***

```bash
kubectl get po -owide
```

NAME                                READY   STATUS     RESTARTS   AGE      IP                 NODE

frontend-rs-6fs6c           1/1          Running      0                     11s         10.44.0.1     k8s-worker-node2

frontend-rs-gz9wx          1/1          Running      0                     11s         10.47.0.1      k8s-worker-node1

frontend-rs-j9mcm          1/1          Running     0                     10m       10.47.0.2     k8s-worker-node1

***

```bash
kubectl get rs -owide
```

\---

frontend-rs        3          3          3        20m        container-nginx        nginx          apps=webserver-app
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl delete rs frontend-rs
```

replicaset.apps "frontend-rs" deleted

***

```bash
kubectl get po -owide
```

No resources found in default namespace.

```bash
kubectl get rs -owide
```

No resources found in default namespace.
{% endtab %}
{% endtabs %}

***
