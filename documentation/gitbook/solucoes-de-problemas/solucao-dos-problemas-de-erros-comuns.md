---
description: >-
  Se estiver enfrentando um desses erros comuns do Kubernetes, aqui está um guia
  rápido para identificar e resolver o problema:
---

# Solução dos Problemas de Erros Comuns

***

## <mark style="color:red;">CreateContainerConfigError</mark>&#x20;

Esse erro geralmente é o resultado de um `Secret` ou `Configmap` ausente.&#x20;

* `Secrets` são objetos do Kubernetes usados ​​para armazenar informações confidenciais, como credenciais de banco de dados.&#x20;

***

* Os `Configmaps` armazenam dados como pares chave-valor e são normalmente usados ​​para armazenar informações de configuração usadas por vários pods.

***

#### <mark style="color:yellow;">**Como identificar o problema:**</mark>

```bash
kubectl get pods
```

> NAME                              READY               STATUS                                        RESTARTS      AGE
>
> pod-missing-config        0/1                     CreateContainerConfigError      0                      1m23s

***

#### <mark style="color:yellow;">**Obter informações detalhadas e resolver o problema:**</mark>&#x20;

Para obter mais informações sobre o problema, execute `kubectl describe [name]` e procure uma mensagem indicando qual `Configmap` está faltando:

```bash
kubectl describe pod pod-missing-config
```

> Warning Failed 34s (x6 over 1m45s) kubelet Error: configmap "configmap-3" not found

***

#### <mark style="color:yellow;">**Agora execute este comando para ver se o Configmap existe no cluster.**</mark>

```bash
kubectl get configmap configmap-3
```

> Se o resultado for _null_, o `Configmap` está ausente e você precisa criá-lo

* Certifique-se de que o `ConfigMap` esteja disponível executando _`get configmap [name]`_ novamente.

***

* Se você deseja visualizar o conteúdo do ConfigMap no formato YAML, adicione o sinalizador `-o yaml`

***

* Depois de verificar se o ConfigMap existe, execute `kubectl get pods` novamente e verifique se o pod está no status `Running`

***

## <mark style="color:red;">ImagePullBackOff or ErrImagePull</mark>&#x20;

Esse status significa que um pod não pôde ser executado porque tentou obter uma imagem de contêiner de um registro e falhou.&#x20;

O pod se recusa a iniciar porque não pode criar um ou mais contêineres definidos em seu manifesto.

***

#### <mark style="color:yellow;">**Como identificar o problema:**</mark>

```bash
kubectl get pods
```

> NAME                              READY               STATUS                                        RESTARTS      AGE
>
> mypod-1                          0/1                     ImagePullBackOff                        0                      58s

***

#### <mark style="color:yellow;">**Obter informações detalhadas e resolver o problema:**</mark>

```bash
kubectl describe pod [pod problemático] 
```

A saída desse comando indicará a causa raiz do problema. Isso pode ser um dos seguintes:

* **Nome da imagem ou tag incorretos**  - Isso normalmente acontece porque o nome da imagem ou tag foi digitado incorretamente no manifesto do pod. Verifique o nome da imagem correto usando `docker pull` e corrija-o no manifesto do pod.

***

* **Problema de autenticação no registro do contêiner** - O pod não pôde autenticar com o registro para recuperar a imagem.  Isso pode acontecer devido a um problema nas credenciais de retenção da secret ou porque o pod não possui uma função _`RBAC`_ que permita executar a operação.

***

> Certifique-se de que o pod e o nó tenham as permissões e as secrets apropriadas e tente a operação manualmente usando docker pull.

***

## <mark style="color:red;">CrashLoopBackOff</mark>&#x20;

Esse problema indica que um pod não pode ser agendado em um nó. Isso pode acontecer porque o nó não tem recursos suficientes para executar o pod ou porque o pod não conseguiu montar os volumes solicitados.

***

#### <mark style="color:yellow;">**Como identificar o problema:**</mark>

```bash
kubectl get pods
```

> NAME                              READY               STATUS                                        RESTARTS      AGE
>
> mypod-1                          0/1                     CrashLoopBackOff                      0                      58s

***

#### <mark style="color:yellow;">**Obter informações detalhadas e resolver o problema:**</mark>

```bash
kubectl describe pod [pod problemático] 
```

A saída ajudará você a identificar a causa do problema. Aqui estão as causas comuns:

* <mark style="color:yellow;">Recursos insuficientes</mark>  - Se houver recursos insuficientes no nó, você pode remover pods manualmente do nó ou escalar verticalmente seu cluster para garantir que mais nós estejam disponíveis para seus pods.

***

* <mark style="color:yellow;">Montagem de volume</mark> - Se você perceber que o problema está montando um volume de armazenamento, verifique qual volume o pod está tentando montar, certifique-se de que esteja definido corretamente no manifesto do pod e veja se um volume de armazenamento com essas definições está disponível.

***

* <mark style="color:yellow;">Uso de hostPort</mark>  - Se você estiver vinculando pods a um `hostPort`, poderá agendar apenas um pod por nó.&#x20;

> Na maioria dos casos, você pode evitar o uso de `hostPort` e usar um objeto `Service` para permitir a comunicação com seu pod.

***

## <mark style="color:red;">Kubernetes Node NotReady</mark>

Quando um nó do trabalhador é encerrado ou travado, todos os pods com informações de estado que residem nele ficam indisponíveis e o status do nó aparece como `NotReady`.

Se um nó tiver um status `NotReady` por mais de cinco minutos (por padrão), o Kubernetes altera o status dos pods agendados nele para `Unknown`, e tenta agendá-lo em outro nó, com status `ContainerCreating`.

***

#### <mark style="color:yellow;">**Como identificar o problema:**</mark>

```bash
kubectl get nodes
```

> NAME                           READY          STATUS                             AGE                          VERSION
>
> mynode-1                     0/1                NotReady                          1h                             v1.2.0

***

Para verificar se os pods agendados em seu nó estão sendo movidos para outros nós, execute o comando `get pods`

Verifique a saída para ver se um pod aparece duas vezes em dois nós diferentes, conforme a seguir:

> NAME            READY         STATUS                      RESTARTS      AGE      IP               NODE
>
> mypod-1        1/1               Unknown                     0                     10m      \[IP]             mynode-1
>
> mypod-1        0/1               ContainerCreating      0                     15s       \[none]        mynode-2

Se o nó com falha for capaz de se recuperar ou for reinicializado pelo usuário, o problema será resolvido sozinho.&#x20;

Depois que o nó com falha se recupera e ingressa no cluster, ocorre o seguinte processo:

1. O pod com status Desconhecido é excluído e os volumes são desanexados do nó com falha.
2. O pod é reagendado no novo nó, seu status muda de \[Unknown] para \[ContainerCreating] e os volumes necessários são anexados.
3. O Kubernetes usa um tempo limite de cinco minutos (por padrão), após o qual o pod será executado no nó e seu status mudará de \[ContainerCreating] para \[Running].

> Se você não tiver tempo para esperar ou o nó não se recuperar, precisará ajudar o Kubernetes a reagendar os pods com estado em outro nó funcional.&#x20;

Existem duas maneiras de conseguir isso:

* <mark style="color:yellow;">Remova o nó com falha do cluster:</mark>

```bash
kubectl delete node [name]
```

***

* <mark style="color:yellow;">Excluir pods com estado com status desconhecido:</mark>

```bash
kubectl delete pods [pod_name] --grace-period=0 --force -n [namespace]
```

***
