---
description: >-
  Seu propósito é gerenciar um conjunto de réplicas de Pods em execução a
  qualquer momento. Por isso, é geralmente utilizado para garantir a
  disponibilidade de um certo número de Pods idênticos.
---

# ReplicaSets

> Uma das desvantagens da utilização de ReplicasSet, é que ele não faz a alteração dos recursos automaticamente, então toda vez que uma alteração é feita, um novo deploy deve ser aplicado.

#### <mark style="color:yellow;">Os recursos utilizados no exemplo, estão disponibilizados no Github abaixo:</mark>

{% embed url="https://github.com/danncastro/k8s-cka-exemples.git" %}
As nomenclaturas dos recursos são: recurso\_nome-metadata
{% endembed %}

## <mark style="color:red;">Criando ReplicaSets</mark>

{% tabs %}
{% tab title="ReplicaSet" %}
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
kubectl apply -f k8s-cka-exemples/rs_frontend.yml
```

replicaset.apps/frontend created

***

2. Vamos novamente validar, após o deploy

```bash
kubectl get po -owide
```

NAME                       READY     STATUS     RESTARTS   AGE       IP                NODE

frontend-2pjlw         1/1            Running     0                  28s         10.44.0.1     k8s-worker-node2

frontend-c6xsb        1/1            Running     0                  28s         10.47.0.2     k8s-worker-node1

frontend-dgbtl          1/1           Running     0                  28s          10.47.0.1     k8s-worker-node1

***

```bash
kubectl get rs -owide
```

NAME             DESIRED   CURRENT  READY  AGE        CONTAINERS       IMAGES    SELECTOR

frontend         3                3                 3           5m55s    container-nginx   nginx         apps=app
{% endtab %}

{% tab title="Deleted" %}
1. Vamos deletar uma das pods para testar a escalabilidade dos recursos

```bash
kubectl delete po frontend-2pjlw
```

pod "frontend-2pjlw" deleted

***

2. Após a deleção, outro recurso será aplicado automaticamente para manter as quantidades de replicas indicadas no manifesto.

```bash
kubectl get po -owide
```

NAME                         READY   STATUS    RESTARTS   AGE        IP                 NODE

<mark style="color:orange;">frontend-7bv6f          1/1           Running    0                  11s         10.44.0.2     k8s-worker-node2</mark>

frontend-c6xsb          1/1          Running    0                  4m24s   10.47.0.2      k8s-worker-node1

frontend-dgbtl           1/1          Running    0                  4m24s   10.47.0.1       k8s-worker-node1
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
kubectl apply -f k8s-cka-exemples/rs_frontend.yml
```

replicaset.apps/frontend configured

***

2. Podemos visualizar que a quantidade de pods aumentaram.

```bash
kubectl get po -owide
```

NAME                          READY   STATUS    RESTARTS   AGE      IP                NODE

frontend-7bv6f          1/1           Running    0                  7m25s   10.44.0.2     k8s-worker-node2

frontend-c6xsb         1/1           Running   0                   11m        10.47.0.2     k8s-worker-node1

frontend-dgbtl           1/1          Running    0                   11m         10.47.0.1     k8s-worker-node1

<mark style="color:orange;">frontend-hdb9c         1/1          Running    0                   18s         10.44.0.1     k8s-worker-node2</mark>

<mark style="color:orange;">frontend-nrmqd         1/1          Running    0                   18s         10.47.0.3     k8s-worker-node1</mark>

***

```bash
kubectl get rs -owide
```

NAME             DESIRED   CURRENT  READY  AGE        CONTAINERS       IMAGES    SELECTOR

frontend         5                5                 5           5m55s    container-nginx   nginx         apps=app
{% endtab %}

{% tab title="Scale Down" %}
1. Vamos novamente ajustar o manifesto, e diminuir a quantidade de replicas.

```yaml
  replicas: 2
```

***

```bash
kubectl apply -f k8s-cka-exemples/rs_frontend.yml
```

replicaset.apps/frontend configured

***

2. Visualizando novamente os recursos, podemos notar que agora a quantidade em execução é de 2 pods.

```bash
kubectl get po -owide
```

NAME                          READY   STATUS    RESTARTS   AGE      IP                NODE

frontend-c6xsb          1/1           Running   0                   11m        10.47.0.2     k8s-worker-node1

frontend-dgbtl            1/1          Running    0                  11m         10.47.0.1     k8s-worker-node1

***

```bash
kubectl get rs -owide
```

NAME             DESIRED   CURRENT  READY  AGE        CONTAINERS       IMAGES    SELECTOR

frontend         2                2                 2            20m       container-nginx   nginx         apps=app
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl delete rs frontend
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
kubectl apply -f k8s-cka-exemples/rs_frontend.yml
```

replicaset.apps/frontend created

***

```bash
kubectl get po -owide
```

NAME                         READY   STATUS     RESTARTS   AGE      IP                 NODE

frontend-7htlt            1/1           Running    0                   11s         10.44.0.1    k8s-worker-node2

frontend-j9mcm        1/1          Running    0                   11s         10.47.0.2     k8s-worker-node1

frontend-pxm6k        1/1          Running    0                   11s         10.44.0.2     k8s-worker-node2

***

```bash
kubectl get rs -owide
```

NAME             DESIRED   CURRENT  READY  AGE        CONTAINERS       IMAGES    SELECTOR

frontend-rs    3                3                3            14s          container-nginx   nginx         apps=app
{% endtab %}

{% tab title=" Scale Down" %}
<pre class="language-bash"><code class="lang-bash"><strong>kubectl scale rs frontend --replicas=1
</strong></code></pre>

replicaset.apps/frontend scaled

***

```bash
kubectl get po -owide
```

NAME                         READY   STATUS     RESTARTS   AGE      IP                 NODE

frontend-j9mcm        1/1          Running    0                   11s         10.47.0.2     k8s-worker-node1

***

```bash
kubectl get rs -owide
```

NAME             DESIRED   CURRENT  READY  AGE        CONTAINERS       IMAGES    SELECTOR

frontend         1                1                 1             7m9s      container-nginx   nginx         apps=app
{% endtab %}

{% tab title="Scale Up" %}
<pre class="language-bash"><code class="lang-bash"><strong>kubectl scale rs frontend --replicas=3
</strong></code></pre>

replicaset.apps/frontend scaled

***

```bash
kubectl get po -owide
```

NAME                         READY   STATUS     RESTARTS   AGE      IP                 NODE

frontend-6fs6c          1/1          Running    0                   11s         10.44.0.1     k8s-worker-node2

frontend-gz9wx        1/1          Running    0                   11s         10.47.0.1      k8s-worker-node1

frontend-j9mcm        1/1          Running    0                   10m        10.47.0.2     k8s-worker-node1

***

```bash
kubectl get rs -owide
```

NAME             DESIRED   CURRENT  READY  AGE        CONTAINERS       IMAGES    SELECTOR

frontend        3                3                 3            7m9s      container-nginx   nginx         apps=app
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl delete rs frontend
```

replicaset.apps "frontend" deleted

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
