---
description: >-
  Um Secret é um objeto que contém uma pequena quantidade de informação
  sensível, como senhas, tokens ou chaves.
---

# Secrets

***

{% embed url="https://kubernetes.io/pt-br/docs/concepts/configuration/secret/" %}

***

Este tipo de informação, poderia, em outras circunstâncias, ser colocada diretamente em uma configuração de [Pod](https://kubernetes.io/docs/concepts/workloads/pods/) ou em uma [imagem de contêiner](https://kubernetes.io/pt-br/docs/reference/glossary/?all=true#term-image).&#x20;

> O uso de Secrets evita que você tenha de incluir dados confidenciais no seu código.

Secrets podem ser criados de forma independente dos Pods que os consomem. Isto reduz o risco de que o Secret e seus dados sejam expostos durante o processo de criação, visualização e edição ou atualização de Pods.

Kubernetes e as aplicações que rodam no seu cluster podem também tomar outras precauções com Secrets, como por exemplo evitar a escrita de dados confidenciais em local de armazenamento persistente (não volátil).

Secrets são semelhantes a [ConfigMaps](https://kubernetes.io/pt-br/docs/concepts/configuration/configmap), mas foram especificamente projetados para conter dados confidenciais.

{% hint style="warning" %}


**Cuidado:**

Os Secrets do Kubernetes são, por padrão, gravados não encriptados no sistema de armazenamento de dados utilizado pelo servidor da API (etcd). Qualquer pessoa com acesso à API ou ao etcd consegue obter ou modificar um Secret. Além disso, qualquer pessoa que possui autorização para criar Pods em um namespace consegue utilizar este privilégio para ler qualquer Secret naquele namespace. Isso inclui acesso indireto, como por exemplo a permissão para criar Deployments.

Para utilizar Secrets de forma segura, siga pelo menos as instruções abaixo:

1. [Habilite encriptação em disco](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) para Secrets.
2. Habilite ou configure [regras de RBAC](https://kubernetes.io/docs/reference/access-authn-authz/authorization/) que restrinjam o acesso de leitura a Secrets (incluindo acesso indireto).
3. Quando apropriado, utilize mecanismos como RBAC para limitar quais perfis e usuários possuem permissão para criar novos Secrets ou substituir Secrets existentes.
{% endhint %}

Existem três formas principais para um Pod utilizar um Secret:

* Como [arquivos](https://kubernetes.io/pt-br/docs/concepts/configuration/secret/#using-secrets-as-files-from-a-pod) em um [volume](https://kubernetes.io/docs/concepts/storage/volumes/) montado em um ou mais de seus contêineres.

***

* Como uma [variável de ambiente](https://kubernetes.io/pt-br/docs/concepts/configuration/secret/#using-secrets-as-environment-variables) de um contêiner.

***

* Pelo [kubelet ao baixar imagens de contêiner](https://kubernetes.io/pt-br/docs/concepts/configuration/secret/#using-imagepullsecrets) para o Pod.

A camada de gerenciamento do Kubernetes também utiliza Secrets. Por exemplo, os [Secrets de tokens de auto inicialização](https://kubernetes.io/pt-br/docs/concepts/configuration/secret/#bootstrap-token-secrets) são um mecanismo que auxilia a automação do registro de nós

Existem diversas formas de criar um Secret:

* [Crie um Secret utilizando o comando `kubectl`](https://kubernetes.io/pt-br/docs/tasks/configmap-secret/managing-secret-using-kubectl/)

***

* [Crie um Secret a partir de um arquivo de configuração](https://kubernetes.io/pt-br/docs/tasks/configmap-secret/managing-secret-using-config-file/)

***

* [Crie um Secret utilizando a ferramenta kustomize](https://kubernetes.io/pt-br/docs/tasks/configmap-secret/managing-secret-using-kustomize/)

> O nome de um Secret deve ser um [subdomínio DNS válido](https://kubernetes.io/pt-br/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

Secrets individuais são limitados a 1MiB em tamanho. Esta limitação tem por objetivo desencorajar a criação de Secrets muito grandes que possam exaurir a memória do servidor da API e do kubelet.

No entanto, a criação de vários Secrets pequenos também pode exaurir a memória.&#x20;

> Você pode utilizar uma [cota de recurso](https://kubernetes.io/pt-br/docs/concepts/policy/resource-quotas/) a fim de limitar o número de Secrets (ou outros recursos) em um namespace

Secrets podem ser montados como volumes de dados ou expostos como [variáveis de ambiente](https://kubernetes.io/pt-br/docs/concepts/containers/container-environment/) para serem utilizados num container de um Pod.

Secrets também podem ser utilizados por outras partes do sistema, sem serem diretamente expostos ao Pod.&#x20;

* Por exemplo, Secrets podem conter credenciais que outras partes do sistema devem utilizar para interagir com sistemas externos no lugar do usuário.

***

### <mark style="color:red;">Criando Secrets</mark>

Quando criamos secrets, precisamos definir o tipo do secret a ser criado, existem diversos modelos de secrets por padrão no kubernetes, tais como:

<table data-header-hidden><thead><tr><th width="369"></th><th></th></tr></thead><tbody><tr><td><strong>Builtin Type</strong></td><td><strong>Uso</strong></td></tr><tr><td><code>Opaque</code></td><td>Valor arbitrário definido pelo usuário</td></tr><tr><td><code>kubernetes.io/service-account-token</code></td><td>Token de conta de Serviço</td></tr><tr><td><code>kubernetes.io/dockercfg</code></td><td>Arquivo <code>~/.dockercfg</code> serializado</td></tr><tr><td><code>kubernetes.io/dockerconfigjson</code></td><td>Arquivo <code>~/.docker/config.json</code> serializado</td></tr><tr><td><code>kubernetes.io/basic-auth</code></td><td>Credenciais para autenticação Básica</td></tr><tr><td><code>kubernetes.io/ssh-auth</code></td><td>Credenciais para autenticação SSH</td></tr><tr><td><code>kubernetes.io/tls</code></td><td>Informação TLS para um cliente ou servidor</td></tr><tr><td><code>bootstrap.kubernetes.io/token</code></td><td>Dados de token bootstrap</td></tr></tbody></table>

***

#### <mark style="color:yellow;">Basic-auth</mark>

{% tabs %}
{% tab title="Kind" %}
Vamos criar um secret do tipo `basic-auth`

***

```bash
vim secret.yml
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: senha-mysql
type: kubernetes.io/basic-auth
stringData:
  username: danncastro
  password: senha@123
```
{% endtab %}

{% tab title="Apply" %}
```bash
kubectl apply -f secret.yml
```
{% endtab %}

{% tab title="Output YAML" %}
```bash
kkubectl get secret senha-mysql -oyaml 
```

***

apiVersion: v1&#x20;

data:&#x20;

&#x20;   password: c2VuaGFAMTIz&#x20;

&#x20;   username: ZGFubmNhc3Rybw==&#x20;

kind: Secret&#x20;

metadata:&#x20;

&#x20;   creationTimestamp: "2023-08-26T22:27:28Z"&#x20;

&#x20;   name: senha-mysql&#x20;

&#x20;   namespace: default&#x20;

&#x20;   resourceVersion: "22007"&#x20;

&#x20;   uid: e9e68908-a49e-49c1-9f33-60a1928eebdd&#x20;

type: kubernetes.io/basic-auth

***

{% hint style="warning" %}
Note que o valor das secrets está encriptado em base64, não expondo o conteúdo seu conteúdo em texto limpo
{% endhint %}
{% endtab %}

{% tab title="Decode" %}
Podemos confirmar se o conteúdo da secret é o mesmo informado no arquivo gerado.

***

```bash
echo 'c2VuaGFAMTIz' | base64 --decode
```
{% endtab %}
{% endtabs %}

***

#### <mark style="color:yellow;">Opaque</mark>

{% tabs %}
{% tab title="Kind" %}
Criaremos também uma secret pelo terminal do tipo Opaque

***

```bash
kubectl create secret generic name-secret --from-literal=user=danncastro --from-literal=password=senha@123
```
{% endtab %}

{% tab title="Output" %}
```bash
kubectl get secrets
```

***

&#x20;NAME                TYPE                                               DATA           AGE

&#x20;name-secret     Opaque                                           2                  65s

&#x20;senha-mysql     kubernetes.io/basic-auth              2                  15m
{% endtab %}

{% tab title="Output YAML" %}
```bash
kubectl get secret name-secret -oyaml
```

***

apiVersion: v1&#x20;

data:&#x20;

&#x20;   password: c2VuaGFAMTIz&#x20;

&#x20;   username: ZGFubmNhc3Rybw==&#x20;

kind: Secret&#x20;

metadata:&#x20;

&#x20;   creationTimestamp: "2023-08-26T22:42:21Z"

&#x20;   name: name-secret

&#x20;   namespace: default&#x20;

&#x20;   resourceVersion: "23233"&#x20;

&#x20;   uid: fb4ff41e-2a75-404f-9625-ca9bca703a4d

type: kubernetes.io/basic-au
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Utilizando as Secrets criadas</mark>

Neste exemplo utilizaremos a secret `type: kubernetes.io/basic-auth` que foi criada no exemplo anterior

***

{% tabs %}
{% tab title="Kind" %}
Para utilizarmos o secret criaremos um arquivo de pod e nele iremos indica-la,  através de variáveis de ambiente

***

```bash
vim pod-secret.yml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mysql-db
spec:
  containers:
  - name: mysql-db
    image: mysql
    env:
    - name: MYSQL_ROOT_PASSWORD
      valueFrom:
        secretKeyRef:
          name: senha-mysql
          key: password
```
{% endtab %}

{% tab title="Mysql" %}
Vamos verificar se o secret foi configurado corretamente

***

```bash
$ kubectl exec -it mysql-db -- mysql -udanncastro -psenha@123
mysql> show databases;
mysql> exit
```

***




{% endtab %}

{% tab title="ENV" %}
Podemos visualizar também as env de ambiente carregadas para dentro da pod

***

```bash
kubectl  exec -it mysql-db -- env
```
{% endtab %}

{% tab title="Deleted" %}
Agora podemos remover nosso pod e nossas secrets criadas

***

```bash
kubectl delete pod/mysql-db
```

```bash
kubectl delete secrets --all
```
{% endtab %}
{% endtabs %}

***

Existem 3 maneiras diferentes configurarmos secrets

1. Como variáveis de ambiente de um container
2. Como arquivos dentro de um volume montado em um ou mais containers
3. Pelo `kubelet` ao fazer o download de imagens para um Pod.

Para aprender sobre as outras maneiras e tipos de secrets, veja a [Documentação Oficial](https://kubernetes.io/docs/concepts/configuration/secret/)

***
