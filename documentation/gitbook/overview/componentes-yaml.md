---
description: >-
  O YAML é uma linguagem de serialização de dados muito usada na escrita de
  arquivos de configuração. O YAML usa um recuo no estilo Python para indicar o
  alinhamento.
---

# Componentes YAML

***

YAML significa -> "**Y**AML **A**int't **M**arkup **L**anguage"

<figure><img src="../.gitbook/assets/image (39).png" alt=""><figcaption></figcaption></figure>

1. Case sensitive
2. UTF-8 ou UTF-16
3. **Não se deve utilizar o tab**

> _É necessário utilizar espaços em branco porque os caracteres de tabulação não são permitidos. Não há símbolos de formato comuns, como chaves, colchetes, tags de fechamento ou aspas._

4. Os arquivos YAML têm a extensão **.yml** ou **.yaml**

<figure><img src="../.gitbook/assets/image (40).png" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:red;">apiVersion</mark>&#x20;

{% embed url="https://kubernetes.io/docs/reference/using-api/#api-versioning" %}

Qual a versão de API do objeto que será usado no Kubernetes para criar esse objeto. API era uma única aplicação centralizada que foi dividida em diversas partes, por exemplo:&#x20;

> _a **versão alfa, a versão beta e a versão estável.**_&#x20;

* Onde a alfa tem coisas que podem ainda estar contendo bug;&#x20;

***

* Embaixo nós temos a beta que já pode ser considerada segura, mas ainda não é bom utilizar definitivamente;&#x20;

***

* E a versão estável que é um **“v”** seguido de um número inteiro, onde é a versão estável efetivamente para uso.&#x20;

> _E ela possui também diversos grupos para utilizar._

Por exemplo ao criar um pod, o pod está dentro da versão estável da API, logo está na versão **"v"** seguida de algum número. Nesse caso ele está na versão **"v1"**.

<table><thead><tr><th width="146" align="center">POD</th><th width="218" align="center">Deployment </th><th width="180" align="center">Service</th><th align="center">ReplicaSet</th></tr></thead><tbody><tr><td align="center">v1</td><td align="center">apps/v1</td><td align="center">v1</td><td align="center">apps/v1</td></tr></tbody></table>

***

## <mark style="color:red;">Kind</mark>&#x20;

Qual tipo de objeto pretende criar.  Tipo de recurso que será executado.&#x20;

> _Ex: (Pod, Deployment, Service... etc.)_

***

## <mark style="color:red;">Metadata</mark>&#x20;

Dados que ajudam a identificar de forma única o objeto, incluindo uma string `nome`, `UID` e um `namespace`.&#x20;

> _Dados de informações sobre o recurso_

***

### <mark style="color:red;">Labels</mark>

_Labels_ são pares chave/valor anexados a [objetos](https://kubernetes.io/docs/concepts/overview/working-with-objects/#kubernetes-objects) como pods. Os _Labels_ destinam-se a ser usados ​​para especificar atributos de identificação de objetos que são significativos e relevantes para os usuários, mas não implicam diretamente em semântica para o sistema central.

* Os _Labels_ podem ser usados ​​para organizar e selecionar subconjuntos de objetos.

***

* As _Labels_ podem ser anexadas aos objetos no momento da criação e posteriormente adicionadas e modificadas a qualquer momento.

***

* Cada objeto pode ter um conjunto de _Labels_ de chave/valor definidos.

***

* Cada chave deve ser exclusiva para um determinado objeto.

***

## <mark style="color:red;">Spec</mark>&#x20;

Que estado deseja para o objeto. Especificações do que ira conter no container.  O formato preciso do objeto `spec` é diferente para cada objeto Kubernetes, e contém campos aninhados específicos para aquele objeto.&#x20;

* A documentação de [referência da API do Kubernetes](https://kubernetes.io/docs/reference/kubernetes-api/) pode ajudar a encontrar o formato de especificação para todos os objetos que você pode criar usando Kubernetes.

***

### <mark style="color:red;">Selectors</mark>

Os _Seletores de Campos_ permitem que você [selecione recursos do Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects) baseado no valor de um ou mais campos de um recurso.&#x20;

Seguem alguns exemplos de buscas utilizando seletores de campos:

`metadata.name=my-service`

`metadata.namespace!=default`

`status.phase=Pending`

***
