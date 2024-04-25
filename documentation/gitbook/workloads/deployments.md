---
description: >-
  Deployment é uma abstração que gerencia um conjunto de réplicas de um
  aplicativo, garantindo que o número desejado de réplicas esteja sempre em
  execução e gerenciando a atualização dessas réplicas.
---

# Deployments

> `ReplicaSets` no kubernetes funcionam como `Replicas` do Docker Swarm



{% embed url="https://kubernetes.io/docs/concepts/workloads/controllers/deployment/" %}

***

## <mark style="color:red;">About Deployment</mark>

Um ponto interessante de um `deployment` é que o `replicaset` sempre tentará atingir o estado desejado dos `pods`. Ou seja, mesmo que os pods sejam deletados, o `replicaset` se encarregará de garantir o deployment dos mesmos.

Essa é uma das grandes "magias" do kubernetes, e é uma das maiores "pegadinhas" para aqueles que não conhecem o funcionamento do mesmo e tentam apagar os pods porem eles continuam reaparecendo.

{% hint style="info" %}
Para remover nossos pods precisamos remover o deployment.
{% endhint %}

#### <mark style="color:blue;">Responsável pela implantação da aplicação</mark>

Por default o Kubernetes utiliza a estratégia Rolling Updates (Rolling Release), que executa uma atualização baseada em um percentual de indisponibilidade de pods, que por padrão é ter no máximo 25% de indisponibilidade do total de pods em execução.

<figure><img src="../.gitbook/assets/image (41).png" alt=""><figcaption><p>Estrategia Rolling Updates</p></figcaption></figure>

Uma outra forma de implantação é a estratégia Recreate Deployment, mas não é recomendada pois isso pode causar uma indisponibilidade total da aplicação. Porém em ambas as estratégias utilizadas a sempre a possibilidade da utilização do Rollback, que retorna a aplicação ao estado anterior.

***

## <mark style="color:red;">Criando Deployments</mark>

{% tabs %}
{% tab title="Deployment" %}
```bash
kubectl apply -f k8s-cka-exemples/deployment/frontend_deploy.yml
```

deployment.apps/frontend-deploy created

***

1. Vamos visualizar as informações dos recursos criados.

```bash
kubectl get deploy
```

NAME                                   READY               UP-TO-DATE                 AVAILABLE                    AGE

frontend-deploy                 2/2                      2                                        2                                        15s

```bash
kubectl get rs -owide
```

NAME                                                         DESIRED          CURRENT              READY               AGE     &#x20;

frontend-deploy-7895bc4bdd             2                         2                                2                          40s      &#x20;

<pre class="language-bash"><code class="lang-bash"><strong>kubectl get po
</strong></code></pre>

NAME                                                                   READY              STATUS            RESTARTS           AGE     &#x20;

frontend-deploy-7895bc4bdd-c6xsb            1/1                       Running           0                             70s       &#x20;

frontend-deploy-7895bc4bdd-dgbtl              1/1                       Running           0                             70s
{% endtab %}

{% tab title="Rollout" %}
```bash
kubectl rollout status deployment.apps/frontend-deploy
```

deployment "frontend-deploy" sucessfullt rolled out
{% endtab %}

{% tab title="Decribe" %}
```bash
kubectl describe deploy frontend-deploy
```

Name:                            frontend-deploy

Namespace:                  default

CreationTimestamp       Fri, 11 Sep 2023 21:20:35  -0300     // Data de criação do Deployment

Labels:                            app=frontend                                     // Label relacionada ao Deployment

Annotations:                   deployment.kubernetes.io/revision: 1

Selector:                         env=production                                   // Label relacionada ao pod

Replicas:                         2  desired  |  2 updated  |  2 total  |  2 available  |  0 unavai

<mark style="color:orange;">StrategyType:                 RollingUpdate</mark>

MinReadySeconds:        0

<mark style="color:orange;">RollingUpdateStrategy   25% max unavailable, 25% max surge</mark>

Pod Template:

&#x20;    Labels:                        env=production

&#x20;    Containers:

&#x20;      container-nginx:

&#x20;         Image:                    nginx

&#x20;         Port:                       \<none>

&#x20;         HostPort:               \<none>

&#x20;         Environment:         \<none>

&#x20;         Mounts:                  \<none>

&#x20;    Volumes:                     \<none>

Conditions:

&#x20;    Type                              Status                                 Reason

&#x20;     \-----                               -----                                    -----

&#x20;    Available                         True                                    MinimumReplicasAvailable

&#x20;    Progressing                    True                                    NewReplicaSetAvailable &#x20;

OldReplicaSets:                   \<none>

NewReplicaSets:                 frontend-deploy-7895bc4bdd-c6xsb (2/2 replicas created)

Events:

Type                   Reason                        Age                    From                             Message

\-----                     -----                          -----                    -----                                -----
{% endtab %}

{% tab title="Deleted" %}
```
kubectl delete -f k8s-cka-exemples/deployment/frontend_deploy.yml
```

deployment.apps/frontend-deploy deleted
{% endtab %}
{% endtabs %}

#### <mark style="color:blue;">RollingUpdateStrategy</mark>

**Max Unavailable (Máximo Indisponível)**: Isso define o número máximo de pods do aplicativo que podem estar indisponíveis durante a atualização. Por exemplo, se você definir `max unavailable` como 1, isso significa que durante a atualização, apenas um pod do aplicativo pode ser removido de cada vez. Os outros continuam funcionando normalmente, garantindo que o aplicativo permaneça disponível, mesmo durante a atualização.

**Max Surge (Máximo de Excesso)**: Este é o número máximo de pods extras que podem ser criados além do número original durante a atualização. Por exemplo, se você definir `max surge` como 1 em um aplicativo com 5 pods, durante a atualização, o Kubernetes pode temporariamente criar um sexto pod antes de remover os antigos. Isso ajuda a garantir que haja capacidade suficiente para lidar com qualquer aumento repentino na carga de trabalho durante a atualização.

***

### <mark style="color:red;">Rollout History</mark>

{% tabs %}
{% tab title="Create" %}
```bash
kubectl apply -f k8s-cka-exemples/deployment/frontend_deploy.yml
```

deployment.apps/frontend-deploy created

***

<pre class="language-bash"><code class="lang-bash"><strong>kubectl get po
</strong></code></pre>

NAME                                                                   READY              STATUS            RESTARTS           AGE     &#x20;

frontend-deploy-7895bc4bdd-9hlr2            1/1                       Running           0                             70s       &#x20;

frontend-deploy-7895bc4bdd-nscpm         1/1                       Running           0                             70s
{% endtab %}

{% tab title="Rollout" %}
```bash
kubectl rollout status deployment.apps/frontend-deploy
```

deployment "frontend-deploy" sucessfullt rolled out
{% endtab %}

{% tab title="History" %}
```bash
kubectl rollout history deployment.apps/frontend-deploy
```

deployment.apps/frontend-deploy

REVISION       CHANGE-CAUSE

1                      \<none>
{% endtab %}

{% tab title="Manifest" %}
Alteraremos o número de replicas no manifesto para 4

***

```bash
vim k8s-cka-exemples/deployment/frontend_deploy.yml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deploy
  labels:
    app: frontend

spec:
  template:
    metadata:
      name: pod-nginx
      labels:
        env: production
    spec:
      containers:
      - name: container-nginx
        image: nginx
  selector:
    matchLabels:
      env: production
  replicas: 4
```

***

```
kubectl apply -f k8s-cka-exemples/deployment/frontend_deploy.yml
```

deployment.apps/frontend-deploy configured
{% endtab %}

{% tab title="History" %}
Note que apenas alterar o número de replicas não altera o valor de revisão, isso acontece apenas quando a mudanças significativas, exemplo a versão da imagem do container.

***

```bash
kubectl rollout history deployment.apps/frontend-deploy
```

deployment.apps/frontend-deploy

REVISION       CHANGE-CAUSE

1                      \<none>
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Manifest" %}
Alteraremos a versão da imagem do container

***

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deploy
  labels:
    app: frontend

spec:
  template:
    metadata:
      name: pod-nginx
      labels:
        env: production
    spec:
      containers:
      - name: container-nginx
        image: nginx:1.18.0
  selector:
    matchLabels:
      env: production
  replicas: 4
```
{% endtab %}

{% tab title="Apply" %}
```bash
kubectl apply -f k8s-cka-exemples/deployment/frontend_deploy.yml
```

ddeployment.apps/frontend-deploy configured

***

Podemos verificar tudo que foi criado pelo nosso deployment através do comando:

```bash
$ kubectl get all -l app=frontend
```
{% endtab %}

{% tab title="Rollout" %}
```bash
kubectl rollout status deployment.apps/frontend-deploy
```

deployment "frontend-deploy" sucessfullt rolled out
{% endtab %}

{% tab title="History" %}
Podemos ver que uma nova versão de revisão foi criada devido a alteração feita na imagem

***

```bash
kubectl rollout history deployment.apps/frontend-deploy
```

deployment.apps/frontend-deploy

REVISION       CHANGE-CAUSE

1                      \<none>

2                      \<none>
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Manifest" %}
Voltaremos a imagem a versão anterior

***

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deploy
  labels:
    app: frontend

spec:
  template:
    metadata:
      name: pod-nginx
      labels:
        env: production
    spec:
      containers:
      - name: container-nginx
        image: nginx
  selector:
    matchLabels:
      env: production
  replicas: 4
```
{% endtab %}

{% tab title="Apply" %}
```bash
kubectl apply -f k8s-cka-exemples/deployment/frontend_deploy.yml
```

deployment.apps/frontend-deploy configured
{% endtab %}

{% tab title="History" %}
Note que a versão 1 de revisão sumiu, isso acontece por que o Kubernetes entende que nova revisão feita é exatamente igual a da versão 1 então ela cria a revisão 3 e recomeça a contagem a partir da revisão 3 que é exatamente igual a revisão 1

***

```bash
kubectl rollout history deployment.apps/frontend-deploy
```

deployment.apps/frontend-deploy

REVISION       CHANGE-CAUSE

2                      \<none>

3                      \<none>
{% endtab %}

{% tab title="Manifest" %}
Alteraremos novamente a versão da imagem

***

```bash
vim deployment.yml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deploy
  labels:
    app: frontend

spec:
  template:
    metadata:
      name: pod-nginx
      labels:
        env: production
    spec:
      containers:
      - name: container-nginx
        image: nginx:1.14.2
  selector:
    matchLabels:
      env: production
  replicas: 4
```
{% endtab %}

{% tab title="Apply" %}
```bash
kubectl apply -f k8s-cka-exemples/deployment/frontend_deploy.yml
```

deployment.apps/frontend-deploy configured
{% endtab %}

{% tab title="History" %}
1. Note que uma nova versão de revisão foi novamente criada seguindo a última revisão

***

```bash
kubectl rollout history deployment.apps/frontend-deploy
```

deployment.apps/frontend-deploy

REVISION       CHANGE-CAUSE

2                      \<none>

3                      \<none>

4                      \<none>

***

2. É possível também analisar uma versão de revisão especifica

```bash
kubectl rollout history deployment.apps/frontend-deploy --revision=2
```

deployment.apps/frontend-deploy with revision #2

Pod Template:

&#x20;   Labels:                                  env=production

&#x20;              pod-template-hash=7f78c8b5b

&#x20;   Containers:

&#x20;     nginx-container:

&#x20;       Image:                  nginx:1.18.0

&#x20;       Port:                     \<none>

&#x20;       Host Port:            \<none>

&#x20;       Environment:       \<none>

&#x20;       Mounts:                \<none>

&#x20;    Volumes:                 \<none>

***
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Rollback</mark>

{% tabs %}
{% tab title="Manifest" %}
```bash
vim k8s-cka-exemples/deployment/frontend_deploy.yml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deploy
  labels:
    app: frontend

spec:
  template:
    metadata:
      name: pod-nginx
      labels:
        env: production
    spec:
      containers:
      - name: container-nginx
        image: nginx:1.21.4
  selector:
    matchLabels:
      env: production
  replicas: 4
```
{% endtab %}

{% tab title="Apply" %}
<pre class="language-bash"><code class="lang-bash"><strong>kubectl apply -f k8s-cka-exemples/deployment/frontend_deploy.yml --record
</strong></code></pre>

deployment.apps/frontend-deploy configured
{% endtab %}

{% tab title="History" %}
```bash
kubectl rollout history deployment.apps/frontend-deploy
```

deployment.apps/frontend-deploy

REVISION       CHANGE-CAUSE

2                      \<none>

3                      \<none>

4                      \<none>

5                      kubectl apply -f --filename=frontend\_deploy.yml --record=true
{% endtab %}

{% tab title="Rollback" %}
```bash
kubectl rollout undo deployment.apps/frontend-deploy
```

deployment.apps/frontend-deploy rolled back
{% endtab %}

{% tab title="History" %}
Note que a versão 4 sumiu, isso por que o Rollback foi feito na versão 5 para uma anterior,  fazendo com que a versão 4 se tornasse a versão 6.

***

```bash
kubectl rollout history deployment.apps/frontend-deploy
```

deployment.apps/frontend-deploy

REVISION       CHANGE-CAUSE

2                      \<none>

3                      \<none>

5                      kubectl apply -f --filename=frontend\_deploy.yml --record=true

<mark style="color:orange;">6                      \<none></mark>
{% endtab %}

{% tab title="Rollback" %}
Podemos também fazer Rollback para versões especificas, e do mesmo modo a versão escolhida para o Rollback é deletada, dando origem a uma nova versão, de forma simplória ela renomeia a versão para a próxima depois da ultima.

***

```bash
kubectl rollout undo deployment.apps/frontend-deploy --to-revision=2
```

deployment.apps/frontend-deploy rolled back

***

```bash
kubectl rollout history deployment.apps/frontend-deploy
```

deployment.apps/deployment

REVISION       CHANGE-CAUSE

3                      \<none>

5                      kubectl apply -f --filename=frontend\_deploy.yml --record=true

6                      \<none>

<mark style="color:orange;">7                      \<none></mark>

***

```bash
kubectl rollout history deployment.apps/frontend-deploy --revision=7
```

deployment.apps/frontend-deploy with revision #7

Pod Template:

&#x20;   Labels:                                  env=production

&#x20;              pod-template-hash=7f78c8b5b

&#x20;   Containers:

&#x20;     nginx-container:

&#x20;     [ <mark style="color:orange;">Image:                  nginx:1.18.0</mark>](deployments.md#historyr)

&#x20;       Port:                     \<none>

&#x20;       Host Port:            \<none>

&#x20;       Environment:       \<none>

&#x20;       Mounts:                \<none>

&#x20;    Volumes:                 \<none>
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Rollout Pause</mark>

{% tabs %}
{% tab title="Deleted" %}
```bash
kubectl delete -f k8s-cka-exemples/deployment/frontend_deploy.yml
```

deployment.apps/frontend-deploy deleted
{% endtab %}

{% tab title="Manifest" %}
```bash
vim k8s-cka-exemples/deployment/frontend_deploy.yml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deploy
  labels:
    app: frontend

spec:
  template:
    metadata:
      name: pod-nginx
      labels:
        env: production
    spec:
      containers:
      - name: container-nginx
        image: nginx:1.21.4
  selector:
    matchLabels:
      env: production
  replicas: 4
```
{% endtab %}

{% tab title="Apply" %}
<pre class="language-bash"><code class="lang-bash"><strong>kubectl apply -f k8s-cka-exemples/deployment/frontend_deploy.yml
</strong></code></pre>

deployment.apps/frontend-deploy configured

***

<pre class="language-bash"><code class="lang-bash"><strong>kubectl get po
</strong></code></pre>

NAME                                                                 READY             STATUS            RESTARTS        AGE     &#x20;

frontend-deploy-7895bc4bdd-vsfte            1/1                     Running            0                          70s       &#x20;

frontend-deploy-7895bc4bdd-1k3fl             1/1                     Running            0                          70s&#x20;

frontend-deploy-7895bc4bdd-x8e2f           1/1                     Running            0                          70s&#x20;

frontend-deploy-7895bc4bdd-p2fjh            1/1                     Running            0                          70s&#x20;
{% endtab %}

{% tab title="Manifest" %}
Vamos alterar a versão da imagem para gerar uma nova revisão

***

```bash
vim k8s-cka-exemples/deployment/frontend_deploy.yml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deploy
  labels:
    app: frontend

spec:
  template:
    metadata:
      name: pod-nginx
      labels:
        env: production
    spec:
      containers:
      - name: container-nginx
        image: nginx:1.16.1
  selector:
    matchLabels:
      env: production
  replicas: 4
```
{% endtab %}

{% tab title="Pause" %}
> Deixe um terminal aberto com o comando `watch kubectl get pod` e outro com o comando de `pause` já preparados, pois como estamos utilizando um contexto de testes, existem poucas pods em execução, então a alteração das versões pode ocorrer de forma instantânea, sendo assim já dê o pause assim que executar o apply

```bash
kubectl apply -f k8s-cka-exemples/deployment/frontend_deploy.yml
```

deployment.apps/frontend-deploy configured

***

```bash
kubectl rollout pause deployment.apps/frontend-deploy
```

deployment.apps/frontend-deploy paused
{% endtab %}

{% tab title="Output" %}
Podemos ver que apenas 2 pods sofreram atualizações

***

<pre class="language-bash"><code class="lang-bash"><strong>kubectl get po
</strong></code></pre>

NAME                                                                READY              STATUS            RESTARTS        AGE     &#x20;

frontend-deploy-7895bc4bdd-vsfte            1/1                     Running            0                         2m20s       &#x20;

frontend-deploy-7895bc4bdd-1k3fl             1/1                     Running            0                        2m20s&#x20;

frontend-deploy-7895bc4bdd-x8e2f           1/1                     Running            0                         2m20s&#x20;

<mark style="color:orange;">frontend-deploy-7895bc4bdd-mkrjf            1/1                     Running            0                          20s</mark>&#x20;

<mark style="color:orange;">frontend-deploy-7895bc4bdd-pdi2f            1/1                     Running            0                          20s</mark>&#x20;
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Rollout Resume</mark>

{% tabs %}
{% tab title="Resume" %}
Após fazer as validações e ter certeza de que a aplicação está pronta para ser executada podemos utilizar o resume para voltar a atualização de versão das pods que não atualizaram

***

```bash
kubectl rollout resume deployment.apps/frontend-deploy
```

deployment.apps/frontend-deploy resumed
{% endtab %}

{% tab title="Output" %}
Agora todas as pods tiveram suas versões atualizadas

***

<pre class="language-bash"><code class="lang-bash"><strong>kubectl get po
</strong></code></pre>

NAME                                                                 READY              STATUS            RESTARTS        AGE     &#x20;

<mark style="color:orange;">frontend-deploy-7895bc4bdd-m3ff3           1/1                     Running            0                         10s</mark>       &#x20;

<mark style="color:orange;">frontend-deploy-7895bc4bdd-xtffg              1/1                     Running            0                        10s</mark>&#x20;

<mark style="color:orange;">frontend-deploy-7895bc4bdd-2kk2f            1/1                     Running            0                         10s</mark>&#x20;

frontend-deploy-7895bc4bdd-mkrjf             1/1                     Running            0                         1m10s&#x20;

frontend-deploy-7895bc4bdd-pdi2f             1/1                     Running            0                         1m10s
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Deployment Scale - Manifest File/Imperative form</mark>

{% tabs %}
{% tab title="Manifest" %}
Vamos escalar mais 2 pods no arquivo de manifesto ou o que chamamos de **scale up**

***

```bash
vim k8s-cka-exemples/deployment/frontend_deploy.yml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deploy
  labels:
    app: frontend

spec:
  template:
    metadata:
      name: pod-nginx
      labels:
        env: production
    spec:
      containers:
      - name: container-nginx
        image: nginx:1.16.1
  selector:
    matchLabels:
      env: production
  replicas: 7
```
{% endtab %}

{% tab title="Apply" %}
<pre class="language-bash"><code class="lang-bash"><strong>kubectl apply -f k8s-cka-exemples/deployment/frontend_deploy.yml
</strong></code></pre>

deployment.apps/frontend-deploy configured
{% endtab %}

{% tab title="Output" %}
<pre class="language-bash"><code class="lang-bash"><strong>kubectl get po
</strong></code></pre>

NAME                                                                 READY              STATUS            RESTARTS        AGE     &#x20;

frontend-deploy-7895bc4bdd-m3ff3           1/1                     Running            0                        2m25s       &#x20;

frontend-deploy-7895bc4bdd-xtffg              1/1                     Running            0                       2m25s&#x20;

frontend-deploy-7895bc4bdd-2kk2f            1/1                     Running            0                        2m25s&#x20;

frontend-deploy-7895bc4bdd-mkrjf             1/1                     Running            0                        2m25s&#x20;

frontend-deploy-7895bc4bdd-pdi2f             1/1                     Running            0                        2m25s

frontend-deploy-7895bc4bdd-ffvaw            1/1                     Running            0                          20s

frontend-deploy-7895bc4bdd-mmf2s          1/1                     Running            0                          20s
{% endtab %}

{% tab title="Scale down" %}
Faremos a redução de pods mas dessa vez diretamente pelo terminal de forma imperativa

***

```bash
kubectl scale deployment.apps/frontend-deploy --replicas=2
```

deployment.apps/frontend-deploy scaled
{% endtab %}

{% tab title="Output" %}
<pre class="language-bash"><code class="lang-bash"><strong>kubectl get po
</strong></code></pre>

NAME                                                                  READY              STATUS            RESTARTS        AGE     &#x20;

frontend-deploy-7895bc4bdd-m3ff3           1/1                     Running            0                        2m25s       &#x20;

frontend-deploy-7895bc4bdd-xtffg              1/1                     Running            0                       2m25s&#x20;
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Recreate Strategy Type</mark>

Como dito anteriormente o Strategy type padrão do Kubernetes é o Rolling Updates (Rolling Release) isso por que ele faz as atualizações baseado na disponibilidade da aplicação, ao qual é diferente do Strategy Type Recreate, que deleta todas as pods em execução e sobem novas não visando sua disponibilidade&#x20;

{% tabs %}
{% tab title="Output" %}
Vamos descrever as pods em execução e ver que o Strategy Type padrão estará setado.

***

<pre class="language-bash"><code class="lang-bash"><strong>kubectl describe deployment.apps/frontend-deploy | grep StrategyType
</strong></code></pre>

&#x20;StrategyType:               RollingUpdate
{% endtab %}

{% tab title="Manifest" %}
Vamos novamente alterar a versão da imagem para gerar um novo valor de revisão, e também alteraremos o StrategyType do manifesto.

***

```bash
vim k8s-cka-exemples/deployment/frontend_deploy.yml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deploy
  labels:
    app: frontend

spec:
  template:
    metadata:
      name: pod-nginx
      labels:
        env: production
    spec:
      containers:
      - name: container-nginx
        image: nginx:1.19.3
  selector:
    matchLabels:
      env: production
  strategy:
    type: Recreate
  replicas: 2
```
{% endtab %}

{% tab title="Apply" %}
```bash
kubectl apply -f k8s-cka-exemples/deployment/frontend_deploy.yml
```

deployment.apps/frontend-deploy configured

***

```bash
watch kubectl get po
```

NAME                                                        READY              STATUS            RESTARTS        AGE     &#x20;

frontend-deploy-7895bc4bdd-m3ff3           1/1                     Terminating      0                        2m25s       &#x20;

frontend-deploy-7895bc4bdd-xtffg              1/1                     Terminating     0                         2m25s
{% endtab %}

{% tab title="Output" %}
Vamos descrever as pods em execução novamente e ver que o Strategy Type foi alterado

***

```bash
kubectl describe deployment.apps/frontend-deploy | grep StrategyType
```

&#x20;StrategyType:               Recreate
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Deletando os recursos criados</mark>

{% tabs %}
{% tab title="Deleted" %}
```bash
kubectl delete -f k8s-cka-exemples/deployment/frontend_deploy.yml
```

deployment.apps/frontend-deploy  deleted
{% endtab %}

{% tab title="Output" %}
```bash
kubectl get po -owide
```

No resources found in default namespace.

***

```bash
kubectl get deploy -owide
```

No resources found in default namespace.
{% endtab %}
{% endtabs %}

***
