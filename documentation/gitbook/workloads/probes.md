---
description: >-
  Cria critérios para definir se a aplicação está saudável através de Probes,
  tornando visível ao Kubernetes que uma aplicação não está se comportando da
  maneira esperada.
---

# Probes

{% embed url="https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/" %}

***

## <mark style="color:red;">livenessProbe</mark>&#x20;

Basicamente, é uma maneira de garantir que um contêiner esteja "vivo" e funcionando corretamente.

A liveness probe é uma funcionalidade do Kubernetes que permite verificar continuamente a saúde de um contêiner em execução dentro de um pod. Essa verificação é realizada em intervalos definidos pelo usuário e pode ser feita de várias maneiras, incluindo via HTTP, TCP socket ou execução de comandos dentro do contêiner.

No contexto da verificação via HTTP, a liveness probe faz solicitações regulares para um endpoint específico do contêiner. Se o código de retorno da solicitação estiver fora do intervalo esperado (geralmente menor que 200 ou maior ou igual a 400), o Kubernetes considera o pod como não saudável e pode tomar medidas, como reiniciar o pod para tentar recuperá-lo.

Vamos imaginar que tem um aplicativo em execução dentro de um contêiner. Às vezes, esse aplicativo pode travar ou enfrentar algum problema que o impeça de funcionar corretamente, mas o contêiner ainda está tecnicamente "rodando". É aí que entra a liveness probe.

A liveness probe é uma espécie de verificação automática que o Kubernetes faz no seu contêiner em intervalos regulares. Ele executa uma verificação específica para determinar se o aplicativo dentro do contêiner está funcionando conforme o esperado. Se a verificação for bem-sucedida, o Kubernetes sabe que o contêiner está "vivo" e funcionando corretamente. Se a verificação falhar repetidamente, o Kubernetes pode reiniciar o contêiner para tentar corrigir o problema.

{% hint style="info" %}
Além do HTTP, também pode fazer verificações via TCP Socket e Comandos CLI
{% endhint %}

### <mark style="color:red;">Criando LivenessProbe</mark>

{% hint style="info" %}
**Todos os recursos utilizados nesses exemplos, estarão disponibilizados no Github:**  [https://github.com/danncastro/kubernetes\_projects/tree/main/k8s\_cka\_exemples/pods](https://github.com/danncastro/kubernetes\_projects/tree/main/k8s\_cka\_exemples/pods)
{% endhint %}

{% tabs %}
{% tab title="livenessProbe" %}
```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/pods/liveness_probe.yml && \
sleep 5 && kubectl get po && sleep 30 && kubectl describe po liveness-pod && \
sleep 35 && kubectl describe po liveness-pod && sleep 30 &&\
kubectl describe po liveness-pod && kubectl get po liveness-pod

```
{% endtab %}
{% endtabs %}

* Após a execução desse comando podemos validar na aba events do describe, tudo que aconteceu durante a inicialização do container.
* A aplicação não ficará ativa, até que o livenessProbe retorne Success

***

## <mark style="color:red;">readinessProbe</mark>&#x20;

A readinessProbe é uma funcionalidade do Kubernetes que verifica se um contêiner está pronto para receber tráfego de rede. Enquanto a livenessProbe verifica se a aplicação está saudável e se deve ser reiniciada em caso de falha, a readinessProbe se concentra em determinar se a aplicação está pronta para aceitar solicitações de entrada após ser iniciada. Ela pode fazer verificações via HTTP ou TCP para garantir que a aplicação tenha atingido um estado operacional estável.

A readinessProbe pode ser configurada para realizar verificações via HTTP, o que significa que pode enviar solicitações HTTP regulares para um endpoint específico da aplicação e verificar se a resposta indica que a aplicação está pronta. Além disso, também é possível configurar a readinessProbe para realizar verificações via TCP, o que é útil para aplicativos que podem não ter um endpoint HTTP acessível imediatamente após a inicialização.

Ao definir os parâmetros da readinessProbe, como o período de tempo entre as verificações e o tempo de espera para uma resposta bem-sucedida, os administradores de sistemas podem garantir que os contêineres estejam prontos para receber tráfego de rede de forma confiável e eficiente.

> **LivenessProbe** são para saber se a aplicação está saudável e/ou se deve ser reiniciada, enquanto **ReadinessProbe** são para saber se a aplicação já está pronta para receber requisições depois de iniciar

{% hint style="info" %}
Além do HTTP, também pode fazer verificações via TCP
{% endhint %}

***

## <mark style="color:red;">startupProbe</mark>&#x20;

O `startupProbe` é especificamente projetado para verificar o estado inicial de um contêiner no momento em que ele é iniciado ou reiniciado. Ele difere das probes regulares, como o `livenessProbe` e o `readinessProbe`, que verificam a saúde contínua do contêiner após sua inicialização.

Quando um contêiner é iniciado, o `startupProbe` é acionado para verificar se o aplicativo dentro do contêiner está pronto para receber tráfego. Se o `startupProbe` falhar, o Kubernetes pode reiniciar o contêiner, ou até mesmo falhar na inicialização do pod inteiro, dependendo da configuração.

Essa sonda é útil para aplicativos que podem levar algum tempo para se inicializarem completamente ou para inicializações complexas que podem falhar inicialmente, mas se recuperarem depois de um tempo. Ao usar o `startupProbe`, você pode garantir que o Kubernetes não direcione o tráfego para um contêiner que ainda não está pronto para lidar com ele.

> muito util para aplicações legadasque necessitam tempo adicional para inicializar na primeira vez

***
