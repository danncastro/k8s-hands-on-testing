---
description: >-
  Se você estiver enfrentando um problema com um pod do Kubernetes e não
  conseguir localizar e resolver rapidamente o erro, veja como se aprofundar um
  pouco mais.
---

# Problemas de Pods do Kubernetes

{% hint style="info" %}
A primeira etapa para diagnosticar problemas de pod é executar
{% endhint %}

```bash
kubectl describe pod [name]
```

***

## <mark style="color:red;">**Compreendendo a saída do comando**</mark><mark style="color:red;">** **</mark><mark style="color:red;">**`kubectl describe pod`**</mark>

Aqui está um exemplo de saída do comando `kubectl describe pod`

> Name:		        nginx-deployment-1006230814-6winp
>
> Namespace:           default
>
> Node:		        kubernetes-node-wul5/10.240.0.9
>
> Start Time:	        Thu, 24 Mar 2016 01:39:49 +0000
>
> Labels:		        app=nginx, pod-template-hash=1006230814
>
> Annotations:           kubernetes.io/created-by {"kind":"SerializedReference","apiVersion":"v1","reference":{"kind": "ReplicaSet",    "namespace":"default","name":"nginx-deployment-1956810328","uid":"14e607e7-8ba1-11e7-b5cb-fa16" ...
>
> Status:		        Running
>
> IP:		                10.244.0.6
>
> Controllers:	        ReplicaSet/nginx-deployment-1006230814
>
> Containers:
>
> &#x20;    nginx:
>
> &#x20;        Container ID:	docker://90315cc9f513c724e9957a4788d3e625a078de84750f244a40f97ae355eb1149
>
> &#x20;         Image:		nginx
>
> &#x20;         Image ID:		docker://6f62f48c4e55d700cf3eb1b5e33fa051802986b77b874cc351cce539e5163707
>
> &#x20;         Port:		80/TCP
>
> &#x20;    QoS Tier:
>
> &#x20;          cpu:	        Guaranteed
>
> &#x20;          memory:	Guaranteed
>
> &#x20;    Limits:
>
> &#x20;          cpu:	         500m
>
> &#x20;          memory:	 128Mi
>
> &#x20;    Requests:
>
> &#x20;           memory:       128Mi
>
> &#x20;           cpu:		  500m
>
> &#x20;    State:		          Running
>
> &#x20;    Started:		  Thu, 24 Mar 2016 01:39:51 +0000
>
> &#x20;    Ready:		  True
>
> &#x20;    Restart Count:	   0
>
> &#x20;    Environment:        \[none]
>
> &#x20;    Mounts:                 /var/run/secrets/kubernetes.io/serviceaccount from default-token-5kdvl (ro)
>
> Conditions:
>
> &#x20;    Type                      Status
>
> &#x20;    Initialized               True
>
> &#x20;    Ready                     True
>
> &#x20;    PodScheduled       True
>
> Volumes:
>
> &#x20;    default-token-4bcbi:
>
> &#x20;    Type:	                     Secret (a volume populated by a Secret)
>
> &#x20;    SecretName:	      default-token-4bcbi
>
> &#x20;    Optional:                  false
>
> QoS Class:                    Guaranteed
>
> Node-Selectors:           \[none]
>
> Tolerations:                   \[none]
>
> Events:
>
> &#x20;      FirstSeen     LastSeen     Count     From     SubobjectPath     Type     Reason     Message
>
> &#x20;      \----------	    ----------	 ------	----	        -------------	    ----	  ------        -------  &#x20;
>
> &#x20;      54s		     54s		  1	        {default-scheduler }           Normal  Scheduled Successfully assigned nginx-deployment-1006230814-6winp to    kubernetes-node-wul5
>
> &#x20;       54s		      54s		  1	        {kubelet kubernetes-node-wul5}	spec.containers{nginx}	Normal		Pulling		pulling image "nginx"
>
> &#x20;       53s		      53s		  1	        {kubelet kubernetes-node-wul5}	spec.containers{nginx}	Normal		Pulled		Successfully pulled image "nginx"
>
> &#x20;       53s		       53s		  1	        {kubelet kubernetes-node-wul5}	spec.containers{nginx}	Normal		Created		Created container with docker id 90315cc9f513
>
> &#x20;        53s		        53s		  1	        {kubelet kubernetes-node-wul5}	spec.containers{nginx}	Normal		Started		Started container with docker id 90315cc9f513

***

<mark style="color:blue;">Name</mark> - Abaixo desta linha estão os dados básicos sobre o pod, como o nó em que está sendo executado, seus rótulos e o status atual.

***

<mark style="color:blue;">Status</mark> - Este é o estado atual do pod, que pode ser:

| Status       |
| ------------ |
| Pendente     |
| Correndo     |
| Sucesso      |
| Fracassado   |
| Desconhecido |

***

<mark style="color:blue;">Containers</mark> - Abaixo desta linha estão os dados sobre contêineres em execução na pod (apenas um neste exemplo, chamado nginx)

***

<mark style="color:blue;">Containers: State</mark> - Indica o status do contêiner, que pode ser:

| State      |
| ---------- |
| Esperando  |
| Correndo   |
| Rescindido |

***

<mark style="color:blue;">Volumes</mark> - Volumes de armazenamento, `Secrets` ou `Configmaps` montados por contêineres no pod.

***

<mark style="color:blue;">Events</mark> - Eventos recentes que ocorrem no pod, como imagens extraídas, contêineres criados e contêineres iniciados.

{% hint style="info" %}
Continue a depuração com base no estado do pod.
{% endhint %}

***

### <mark style="color:red;">**`Pod Stays Waiting`**</mark><mark style="color:red;">** **</mark><mark style="color:red;">**(Pod permanece pendente)**</mark>

Se o status de um pod for Pendente por um tempo, isso pode significar que ele não pode ser agendado em um nó.&#x20;

> Observe a saída do pod de descrição, na seção Eventos.

Tente identificar as mensagens que indicam por que o pod não pôde ser agendado. Por exemplo:

* <mark style="color:blue;">Recursos insuficientes no cluster</mark> - O cluster pode ter recursos insuficientes de CPU ou memória. Isso significa que você precisará excluir alguns pods, adicionar recursos em seus nós ou adicionar mais nós.

***

* <mark style="color:blue;">Requisitos de recursos</mark> - O pod pode ser difícil de agendar devido a requisitos de recursos específicos. Veja se você pode liberar alguns dos requisitos para tornar o pod elegível para agendamento em nós adicionais.

***

### <mark style="color:red;">**`Pod Stays Pending`**</mark><mark style="color:red;">** **</mark><mark style="color:red;">**(Pod fica esperando)**</mark>

Se o status de um pod for Aguardando, isso significa que ele está agendado em um nó, mas não pode ser executado. Observe a saída do `describe pod` , na seção '`Eventos`', e tente identificar os motivos pelos quais o pod não pode ser executado.

Na maioria das vezes, isso ocorre devido a um erro ao buscar a imagem. Em caso afirmativo, verifique o seguinte:

* <mark style="color:blue;">**`Nome da imagem`**</mark>  - Certifique-se de que o nome da imagem no manifesto do pod esteja correto

***

* <mark style="color:blue;">**`Imagem disponível`**</mark> - Garantir que a imagem esteja realmente disponível no repositório

***

* <mark style="color:blue;">**`Teste manualmente`**</mark> - Execute um comando docker pull na máquina local, garantindo que você tenha as permissões apropriadas, para ver se consegue recuperar a imagem

***

### <mark style="color:red;">**`Pod Is Running but Misbehaving`**</mark><mark style="color:red;">**(O pod está em execução, mas se comporta mal)**</mark>

Se um pod não estiver sendo executado conforme o esperado, pode haver duas causas comuns:&#x20;

> _erro no manifesto do pod_ ou _incompatibilidade entre o manifesto do pod local e o manifesto no servidor da API_.

Verificando se há um erro na descrição do seu pod:&#x20;

É comum introduzir erros na descrição de um pod, por exemplo, aninhando seções incorretamente ou digitando um comando incorretamente.

1. Tente excluir o pod e recriá-lo:&#x20;

```bash
kubectl apply --validate -f mypod1.yaml
```

2. Este comando fornecerá um erro como este se você digitou incorretamente um comando no manifesto do pod, por exemplo, se você escreveu \[`continers`] em vez de \[`containers`]:

> 46757 schema.go:126] campo desconhecido: continers
>
> 46757 schema.go:129] isso pode ser um alarme falso, consulte https://github.com/kubernetes/kubernetes/issues/5786  pods/mypod1

Verificando uma incompatibilidade entre o manifesto do pod local e o `API Server` pode acontecer que o manifesto do pod, conforme registrado pelo `Kubernetes API Server`, não seja igual ao seu manifesto local, daí o comportamento inesperado.&#x20;

1. Execute este comando para recuperar o manifesto do pod do servidor API e salve-o como um arquivo YAML local:

```bash
kubectl get pods/[nome do pod] -o yaml > apiserver-[nome do pod].yaml
```

Agora você terá um arquivo local chamado `apiserver-[pod-name].yaml`, abra-o e compare com seu YAML local.&#x20;

Existem três casos possíveis:

* <mark style="color:blue;">Local YAML tem as mesmas linhas que API Server YAML e mais</mark> - Isso indica uma incompatibilidade. Exclua o pod e execute-o novamente com o manifesto do pod local (supondo que seja o correto).

***

* <mark style="color:blue;">O API Server YAML tem as mesmas linhas que o YAML local e mais</mark> - Isso é normal, porque o API Server pode adicionar mais linhas ao manifesto do pod ao longo do tempo. O problema está em outro lugar.

***

* Ambos os arquivos YAML são idênticos - Novamente, isso é normal e significa que o problema está em outro lugar.

***

## <mark style="color:red;">**Diagnosticando outros problemas de pod**</mark>

Se você não conseguiu diagnosticar o problema do seu pod usando os métodos acima, existem vários métodos adicionais para realizar uma depuração mais profunda do seu pod:

* Examinando logs de pod
* Depurando com Container Exec
* Depurando com um contêiner de depuração efêmero
* Executando um pod de depuração no nó

#### <mark style="color:blue;">Examinando logs de Pods</mark>

Você pode recuperar logs de um contêiner com defeito usando este comando:

```bash
kubectl logs [nome do pod] [nome do contêiner]
```

* Se o contêiner travou, você pode usar o sinalizador `--previous` para recuperar seu log de travamento, assim:

```bash
kubectl logs --previous [nome do pod] [nome do contêiner]
```

#### <mark style="color:blue;">Depurando com Container Exec</mark>&#x20;

Muitas imagens de contêiner contêm utilitários de depuração, isso vale para todas as imagens derivadas de imagens de base do Linux e do Windows. Isso permite que você execute comandos em um shell dentro do contêiner com defeito, como segue:

```bash
kubectl exec [nome do pod] -c [nome do contêiner] -- [seu-comandos-shell]
```

* Existem vários casos em que você não pode usar o comando `kubectl exec` O contêiner já travou. A imagem do contêiner não tem distribuição ou propositadamente não inclui um utilitário de depuração

{% hint style="info" %}
A solução, suportada no _**Kubernetes v.1.18**_ e posterior, é executar um `containerEfêmero`.
{% endhint %}

* Este é um container que roda junto com seu container de produção e espelha sua atividade, permitindo que você execute comandos de shell nele, como se estivesse executando-os no container real, e mesmo depois de travar.

#### <mark style="color:blue;">Crie um contêiner efêmero usando:</mark>

```bash
kubectl debug -it [pod-name] --image=[image-name] --target=[pod-name]
```

* O sinalizador `--target` é importante porque permite que o contêiner efêmero se comunique com o Namespace do processo de outros contêineres em execução no pod.

***

* Depois de executar o comando _`debug`_, o kubectl mostrará uma mensagem com o nome do contêiner efêmero **anote esse nome para poder trabalhar com o contêiner:**

> Defaulting debug container name to debugger-8xzrl
>
> Creating debugging pod node-debugger-mynode-pdx84 with container debugger on node \[node-name]

Agora você pode executar _kubectl exec_ em seu novo contêiner efêmero e usá-lo para depurar seu contêiner de produção.

#### <mark style="color:blue;">Executando um Pod de depuração no nó</mark>

Se nenhuma dessas abordagens funcionar, você pode criar um pod especial no nó, executando no Namespace do host com privilégios de host. Este método não é recomendado em ambientes de produção por motivos de segurança.

* Execute um pod de depuração especial em seu nó usando:

```bash
kubectl debug node/[node-name] -it --image=[image-name]
```

* Depois de executar o comando debug, o kubectl mostrará uma mensagem com seu novo pod de depuração&#x20;

{% hint style="warning" %}
Anote este nome para poder trabalhar com ele:
{% endhint %}

> Creating debugging pod node-debugger-mynode-pdx84 with container debugger on node \[node-name]

Observe que o novo pod executa um contêiner nos Namespaces host IPC, Network e PID. O sistema de arquivos raiz é montado em `/host`

Quando terminar com o pod de depuração, exclua-o usando:

```bash
kubectl delete pod [debug-pod-name]
```

***
