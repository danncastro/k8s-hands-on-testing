---
description: >-
  O controle de acesso baseado em funções (RBAC Authorization) é um método de
  regular o acesso a recursos de computador ou rede com base nas funções de
  usuários individuais em sua organização.
---

# RBAC

***

A autorização RBAC usa o`rbac.authorization.k8s.io` [Grupo de APIs](https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-groups-and-versioning) para orientar decisões de autorização, permitindo configurar políticas dinamicamente por meio da API Kubernetes.

Para habilitar o RBAC, inicie o [Servidor API](https://kubernetes.io/docs/concepts/overview/components/#kube-apiserver) com o sinalizador `--authorization-mode` definido como uma lista separada por vírgulas que inclui `RBAC`; por exemplo:

```bash
kube-apiserver --authorization-mode=Example,RBAC --other-options --more-options
```

***

## <mark style="color:red;">API</mark> <a href="#api-overview" id="api-overview"></a>

{% embed url="https://kubernetes.io/docs/reference/access-authn-authz/rbac/#api-overview" %}

A API RBAC declara quatro tipos de objetos Kubernetes: _`Role`_` ``,`` `_`ClusterRole`_` ``,`` `_`RoleBinding`_` ``e`` `_`ClusterRoleBinding`_ . Você pode descrever ou alterar os  [objetos](https://kubernetes.io/docs/concepts/overview/working-with-objects/#kubernetes-objects)  RBAC usando ferramentas como `kubectl`, assim como qualquer outro objeto Kubernetes.

{% hint style="warning" %}
**Cuidado:** Esses objetos, por design, impõem restrições de acesso. Se você estiver fazendo alterações em um cluster conforme aprende, consulte [prevenção e inicialização de escalonamento de privilégios](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#privilege-escalation-prevention-and-bootstrapping) para entender como essas restrições podem impedir que você faça algumas alterações.
{% endhint %}

***

### <mark style="color:red;">ServiceAccount</mark>

{% embed url="https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/" %}

Uma _ServiceAccount_ fornece uma identidade para processos executados em um pod.

Um processo dentro de um pod pode usar a identidade da conta de serviço associada para se autenticar no servidor API do cluster.

> Para obter uma introdução às contas de serviço, leia [configurar contas de serviço](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) .

***

#### <mark style="color:yellow;">UserAccounts versus ServiceAccounts</mark> <a href="#user-accounts-versus-service-accounts" id="user-accounts-versus-service-accounts"></a>

{% embed url="https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/#user-accounts-versus-service-accounts" %}

* As contas de usuário são para humanos. As contas de serviço são para processos de aplicativos, que (para Kubernetes) são executados em contêineres que fazem parte de pods.

***

* As contas de usuário devem ser globais: os nomes devem ser exclusivos em todos os namespaces de um cluster. No Kubernetes, as contas de serviço têm namespaces: dois namespaces diferentes podem conter ServiceAccounts com nomes idênticos.

***

* Normalmente, as contas de usuário de um cluster podem ser sincronizadas a partir de um banco de dados corporativo, onde a criação de novas contas de usuário requer privilégios especiais e está vinculada a processos de negócios complexos. Por outro lado, a criação de contas de serviço pretende ser mais leve, permitindo que os usuários do cluster criem contas de serviço para tarefas específicas sob demanda. Separar a criação de ServiceAccount das etapas de integração de usuários humanos facilita que as cargas de trabalho sigam o princípio do menor privilégio.

***

* As considerações de auditoria para contas humanas e de serviço podem ser diferentes; a separação torna isso mais fácil de conseguir.

***

* Um pacote configurável para um sistema complexo pode incluir a definição de várias contas de serviço para componentes desse sistema. Como as contas de serviço podem ser criadas sem muitas restrições e têm nomes com namespaces, essa configuração geralmente é portátil

***

{% tabs %}
{% tab title="ServiceAccount Namespace" %}
Vamos criar uma ServiceAccount para posteriormente vincula-la a uma Role

***

```bash
kubectl create serviceaccount nsservice
```
{% endtab %}

{% tab title="Output" %}
```bash
kubectl get serviceaccount
```

&#x20;NAME                 SECRETS                                        AGE

default                 0                                                     2d9h  &#x20;

nsservice             0                                                     27s
{% endtab %}

{% tab title="ServiceAccount Cluster" %}
Criaremos outra ServiceAccount e daremos continuidade a criação das ClusterRole e ClusterRoleBinding.

***

```bash
kubectl create serviceaccount ctservice
```
{% endtab %}

{% tab title="Output" %}
```
kubectl get serviceaccount
```

***

&#x20;NAME                  SECRETS                                        AGE

default                  0                                                     2d9h  &#x20;

nsservice              0                                                     1m2s

ctservice               0                                                     28s
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Role e ClusterRole</mark>

{% embed url="https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole" %}

Uma RBAC  _role_ ou _ClusterRole_ contém regras que representam um conjunto de permissões. As permissões são puramente aditivas (não há regras de “negação”).

* Uma role sempre define permissões dentro de um determinado  [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces); ao criar uma função, você deve especificar o namespace ao qual ela pertence.

***

* ClusterRole, por outro lado, é um recurso sem namespace. Os recursos têm nomes diferentes (Role e ClusterRole) porque um objeto Kubernetes sempre precisa ter namespace ou não; não pode ser ambos.

ClusterRoles tem vários usos. Você pode usar um ClusterRole para:

1. definir permissões em recursos com namespace e receber acesso em namespaces individuais
2. definir permissões em recursos com namespace e receber acesso em todos os namespaces
3. definir permissões em recursos com escopo de cluster

> Se você quiser definir uma função dentro de um namespace, use uma Role; se desejar definir uma função em todo o cluster, use um ClusterRole.

***

{% tabs %}
{% tab title="Role" %}
Criaremos uma Role e iremos vincula-la a ServiceAccount criada anteriormente utilizando RoleBinding

***

```bash
kubectl create role nsrole --verb=get,list,watch --resource=pods
```
{% endtab %}

{% tab title="Output" %}
```
kubectl get role
```

***

NAME                      CREATED AT

nsrole                      2023-08-26T23:19:25Z
{% endtab %}

{% tab title="ClusterRole" %}
```bash
kubectl create clusterrole ctrole --verb=get,list,watch --resource=pods,secrets
```
{% endtab %}

{% tab title="Output" %}
```
kubectl get role
```

***

NAME                      CREATED AT

nsrole                      2023-08-26T23:19:25Z

clusterrole              2023-08-26T23:19:32Z
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">RoleBinding e ClusterRoleBinding</mark>

{% embed url="https://kubernetes.io/docs/reference/access-authn-authz/rbac/#rolebinding-and-clusterrolebinding" %}

Uma vinculação de função(RoleBinding) concede as permissões definidas em uma função a um usuário ou conjunto de usuários. Ele contém uma lista de _assuntos_ (usuários, grupos ou contas de serviço) e uma referência à função que está sendo concedida.

> Um RoleBinding concede permissões dentro de um namespace específico, enquanto um ClusterRoleBinding concede acesso em todo o cluster.

Um RoleBinding pode fazer referência a qualquer função no mesmo namespace. Como alternativa, um RoleBinding pode fazer referência a um ClusterRole e vincular esse ClusterRole ao namespace do RoleBinding.

{% hint style="info" %}
Se quiser vincular um ClusterRole a todos os namespaces em seu cluster, use um ClusterRoleBinding.
{% endhint %}

> O nome de um objeto RoleBinding ou ClusterRoleBinding deve ser um [nome de segmento de caminho](https://kubernetes.io/docs/concepts/overview/working-with-objects/names#path-segment-names) válido.

Depois de criar uma ligação, não será possível alterar a função ou ClusterRole a que ela se refere. Se você tentar alterar uma ligação `roleRef`, receberá um erro de validação. Se quiser alterar o `roleRef` de uma ligação, você precisará remover o objeto de ligação e criar um substituto.

Existem duas razões para esta restrição:

1. Tornar `roleRef` imutável  permite conceder permissão `update` a alguém sobre um objeto de ligação existente, para que possa gerenciar a lista de assuntos, sem poder alterar a função concedida a esses assuntos.

***

2. Uma ligação a uma função diferente é uma ligação fundamentalmente diferente. Exigir que uma ligação seja excluída/recriada para alterar `roleRef` garante que a lista completa de assuntos na ligação receba a nova função (em vez de ativar ou modificar acidentalmente apenas o roleRef sem verificar todos os assuntos existentes deve ser dadas as permissões da nova função).

O `kubectl auth reconcile`  utilitário de linha de comando cria ou atualiza um arquivo de manifesto contendo objetos RBAC e lida com a exclusão e recriação de objetos de ligação, se necessário, para alterar a função a que eles se referem. Consulte [uso de comandos e exemplos](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#kubectl-auth-reconcile) para obter mais informações

***

{% tabs %}
{% tab title="RoleBinding" %}
Criaremos o vinculo dos recursos de Role e ServiceAccount criados anteriormente

***

```bash
kubectl create rolebinding nsrolebinding --role=nsrole --serviceaccount=default:nsservice
```
{% endtab %}

{% tab title="Output" %}
```bash
kubectl get rolebinding -owide
```

***

NAME                    ROLE               AGE         USERS       GROUPS               SERVICEACCOUNTS

nsrolebinding       Role/nsrole      64s                                                          default/nsservice
{% endtab %}

{% tab title="Auth" %}
Podemos testar se a Role atribuída a ServiceAccount funcionou corretamente através do comando abaixo, com um output bem simples

***

```bash
kubectl auth can-i get pods --as=system:serviceaccount:default:nsservice -n defaultyes
```

> yes

***

```bash
kubectl auth can-i create pods --as=system:serviceaccount:default:nsservice -n default
```

> no
{% endtab %}

{% tab title="Permission" %}
Vamos alterar a permissão da Role para que seja possível a criação de pods, adicionando ao final do bloco "verbs" a opção create

***

```bash
kubectl edit role nsrole -n default
```

```yaml
# Please edit the object below. Lines beginning with a '#' will be ignored,
# and an empty file will abort the edit. If an error occurs while saving this 
# file will be
# reopened with the relevant failures.
#
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: "2023-08-26T23:19:25Z"
  name: nsrole
  namespace: default
  resourceVersion: "26273"
  uid: 9f2ad3bd-ca15-4f90-bb39-8c8953afb81c
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - get
  - list
  - watch
  - create
```
{% endtab %}

{% tab title="Output" %}
Obtemos agora uma resposta positiva em relação a criação de pod

```bash
kubectl auth can-i create pods --as=system:serviceaccount:default:nsservice -n default
```

> yes
{% endtab %}

{% tab title="Deleted" %}
Vamos deletar nossas configurações de ServiceAccount, Role e RoleBinding

***

```bash
kubectl delete serviceaccount nsservice
```

```bash
kubectl delete role nsrole
```

```bash
kubectl delete rolebinding nsrolebinding
```
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="ClusterRoleBinding" %}
```bash
kubectl create clusterrolebinding ctrolebinding --clusterrole=ctrole --serviceaccount=default:ctservice
```
{% endtab %}

{% tab title="Output" %}
```bash
kubectl get clusterrole | grep ctrole
```

ctrole                                                       2023-08-29T00:09:55Z

***

```bash
kubectl get clusterrolebinding | grep ctrolebinding
```

ctrolebinding                      53s              ClusterRole/ctrole
{% endtab %}

{% tab title="Get Namespace" %}
```bash
kubectl get ns
```

***

NAME                              STATUS                 AGE

default                              Active                   4d10h&#x20;

kube-node-lease             Active                   4d10h&#x20;

kube-public                      Active                   4d10hkube-system                    Active                   4d10h
{% endtab %}

{% tab title="Auth" %}
Vamos testar nossas RBAC  nas NS disponíveis

```bash
kubectl auth can-i create pods --as=system:serviceaccount:default:ctservice -n default
```

> yes

```bash
kubectl auth can-i create secrets --as=system:serviceaccount:default:ctservice -n kube-system
```

> yes

```bash
kubectl auth can-i create pods --as=system:serviceaccount:default:ctservice -n  kube-public
```

> yes

```bash
kubectl auth can-i create deploy --as=system:serviceaccount:default:ctservice -n  kube-public
```

> no
{% endtab %}
{% endtabs %}

***

#### <mark style="color:yellow;">Configmaps e Secrets</mark>

ConfigMaps e Secrets são objetos de API utilizamos para armazenar dados no kubernetes.

A diferença básica entre o `configMap` e o `secret` é que o `configMap` armazena os dados não confidenciais em formato chave-valor, ou seja, em texto plano.&#x20;

Enquanto o `secret` armazena dados sensíveis, ou seja, criptografado que pode ser utilizado na especificação de um Pod.&#x20;

> No geral, podemos dizer que o `configMap` e o `secret` do kubernetes funcionam da mesma maneira que o `configMap` e o `secret` do Docker Swarm

***
