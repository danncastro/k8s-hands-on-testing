---
description: >-
  Cria critérios para definir se a aplicação está saudável através de Probes,
  tornando visível ao Kubernetes que uma aplicação não está se comportando da
  maneira esperada.
---

# Probes

***

### <mark style="color:red;">livenessProbe</mark>&#x20;

Podem fazer a verificação em diferentes intervalos de tempo via HTTP.  Ele indicará falha caso o código de retorno seja menor que `200` ou maior/igual a `400`.

***

### <mark style="color:red;">readinessProbe</mark>&#x20;

Também podem fazer a verificação em diferentes intervalos de tempo via HTTP. Ele começará a executar os testes a partir do time definido depois do container ser criado.

> **LivenessProbe** são para saber se a aplicação está saudável e/ou se deve ser reiniciada, enquanto **ReadinessProbe** são para saber se a aplicação já está pronta para receber requisições depois de iniciar

{% hint style="info" %}
Além do HTTP, também pode fazer verificações via TCP
{% endhint %}

***

### <mark style="color:red;">startupProbe</mark>&#x20;

Voltado para aplicações legadas. Algumas aplicações legadas exigem tempo adicional para inicializar na primeira vez

***
