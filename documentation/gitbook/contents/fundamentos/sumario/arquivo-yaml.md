---
description: >-
  O YAML é uma linguagem de serialização de dados muito usada na escrita de
  arquivos de configuração. O YAML usa um recuo no estilo Python para indicar o
  alinhamento.
---

# Arquivo YAML

***

> É necessário utilizar espaços em branco porque os caracteres de tabulação não são permitidos. Não há símbolos de formato comuns, como chaves, colchetes, tags de fechamento ou aspas.

{% hint style="info" %}
Os arquivos YAML têm a extensão **.yml** ou **.yaml**
{% endhint %}

***

### <mark style="color:red;">apiVersion</mark>&#x20;

API era uma única aplicação centralizada que foi dividida em diversas partes, por exemplo: a **versão alfa, a versão beta e a versão estável.**&#x20;

* Onde a alfa tem coisas que podem ainda estar contendo bug; embaixo nós temos a beta que já pode ser considerada segura, mas ainda não é bom utilizar definitivamente; e a versão estável que é um “v” seguido de um número inteiro, onde é a versão estável efetivamente para uso. E ela possui também diversos grupos para utilizar.&#x20;
* Por exemplo ao criar um pod, o pod está dentro da versão estável da API, logo está na versão **"v"** seguida de algum número - nesse caso ele está na versão **"v1"**.

<table><thead><tr><th width="146" align="center">POD</th><th width="228" align="center">Deployment </th><th width="368" align="center">Service</th></tr></thead><tbody><tr><td align="center">v1</td><td align="center">apps/v1</td><td align="center">v1</td></tr></tbody></table>

***

### <mark style="color:red;">kind</mark>&#x20;

Tipo de recurso que será executado

***

### <mark style="color:red;">metadata</mark>&#x20;

Dados de informações sobre o recurso

***

### <mark style="color:red;">Labels</mark>

***

### <mark style="color:red;">spec</mark>&#x20;

Especificações do que ira conter no recurso

***
