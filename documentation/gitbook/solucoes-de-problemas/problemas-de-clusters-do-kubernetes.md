# Problemas de Clusters do Kubernetes

***

## <mark style="color:red;">Como visualizar informações básicas do cluster</mark>

A primeira etapa para solucionar problemas de contêiner é obter informações básicas sobre os `nodes` do worker do Kubernetes e os serviços em execução no cluster.

Para ver uma lista de nós de trabalho e seus status, execute:

```bash
kubectl get nodes --show-labels
```

A saída será algo como isto:

> NAME         STATUS    ROLES        AGE     VERSION         LABELS
>
> worker0      Ready       \[none]        1d         v1.13.0           ...,kubernetes.io/hostname=worker0
>
> worker1       Ready       \[none]        1d         v1.13.0            ...,kubernetes.io/hostname=worker1
>
> worker2       Ready      \[none]        1d          v1.13.0           ...,kubernetes.io/hostname=worker2

Para obter informações sobre os serviços em execução no cluster, execute:

```bash
kubectl cluster-info
```

> Kubernetes master is running at https://104.197.5.247
>
> elasticsearch-logging is running at https://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy
>
> kibana-logging is running at https://104.197.5.247/api/v1/namespaces/kube-system/services/kibana-logging/proxy
>
> kube-dns is running at https://104.197.5.247/api/v1/namespaces/kube-system/services/kube-dns/proxy

***

## <mark style="color:red;">**Recuperando logs de cluster**</mark>

Para diagnosticar problemas mais profundos com nós em seu cluster, você precisará acessar os logs nos nós.&#x20;

A tabela a seguir explica onde localizar os logs.

<table><thead><tr><th width="146" align="center">NODE</th><th width="232" align="center">TYPE COMPONENT</th><th width="368" align="center">WHERE TO FIND LOGS</th></tr></thead><tbody><tr><td align="center">Master</td><td align="center">API Server</td><td align="center">/var/log/kube-apiserver.log</td></tr><tr><td align="center">Master</td><td align="center">Scheduler</td><td align="center">/var/log/kube-scheduler.log</td></tr><tr><td align="center">Master</td><td align="center">Controller Manager</td><td align="center">/var/log/kube-controller-manager.log</td></tr><tr><td align="center">Worker</td><td align="center">Kubelet </td><td align="center">/var/log/kubelet.log</td></tr><tr><td align="center">Worker </td><td align="center">Kube Proxy</td><td align="center">/var/log/kube-proxy.log</td></tr></tbody></table>

***

## <mark style="color:red;">**Cenários comuns de falha de cluster e como resolvê-los**</mark>

Vejamos vários cenários comuns de falha de cluster, seu impacto e como eles geralmente podem ser resolvidos.&#x20;

{% hint style="info" %}
Este não é um guia completo para solução de problemas de cluster, mas pode ajudá-lo a resolver os problemas mais comuns.
{% endhint %}

***

#### <mark style="color:blue;">API Server VM desliga ou falha</mark>

* **Impacto:** Se o servidor API estiver inativo, você não poderá iniciar, parar ou atualizar pods e serviços.

***

* **Resolução:** Reinicie a VM do servidor de API.

***

* **Prevenção:** Defina a VM do servidor de API para reiniciar automaticamente e configure a alta disponibilidade para o servidor de API.

#### <mark style="color:blue;">O serviço do plano de controle é encerrado ou trava</mark>

* **Impacto:** Serviços como _Replication Controller Manager_, _Scheduler_ e assim por diante são colocados com o API Server, portanto, se algum deles desligar ou travar, o impacto será o mesmo que o desligamento do API Server.

***

* **Resolução:** O mesmo que API Server VM desliga.

***

* **Prevenção:** O mesmo que API Server VM desliga.

#### <mark style="color:blue;">Armazenamento do servidor API perdido</mark>

* **Impacto:** O API Server falhará ao reiniciar após o desligamento.

***

* **Resolução:** Certifique-se de que o armazenamento esteja funcionando novamente, recupere manualmente o estado do API Server do backup e reinicie-o.

***

* **Prevenção:** Certifique-se de ter um instantâneo prontamente disponível do API Server. Use armazenamento confiável, como o Amazon Elastic Block Storage (EBS), que sobrevive ao desligamento da VM do API Server e prefira armazenamento altamente disponível.

#### <mark style="color:blue;">Nó de trabalho desligado</mark>

* **Impacto:** Os pods no nó param de ser executados, o Agendador tentará executá-los em outros nós disponíveis. O cluster agora terá menos capacidade geral para executar pods.

***

* **Resolução:** Identifique o problema no nó, recupere-o e registre-o no cluster.

***

* **Prevenção:** Use um controle de replicação ou um serviço na frente dos pods para garantir que os usuários não sejam afetados por falhas de nó. Projete aplicativos para serem tolerantes a falhas.

#### <mark style="color:blue;">Mau funcionamento do Kubelet</mark>

* **Impacto:** Se o kubelet travar em um nó, você não poderá iniciar novos pods nesse nó. Os pods existentes podem ou não ser excluídos e o nó será marcado como não íntegro.

***

* **Resolução:** Igual ao encerramento do nó de trabalho.

***

* **Prevenção:** Igual ao encerramento do nó de trabalho.

<mark style="color:blue;">Particionamento de rede não planejado Desconectando alguns nós do mestre</mark>

* **Impacto:** Os nós mestres pensam que os nós na outra partição de rede estão inativos e esses nós não podem se comunicar com o API Server.

***

* **Resolução:** Reconfigure a rede para permitir a comunicação entre todos os nós e o API Server.

***

* **Prevenção:** Use uma solução de rede que possa reconfigurar automaticamente os parâmetros de rede do cluster.

#### <mark style="color:blue;">Erro humano por operador de cluster</mark>

* **Impacto:** Um comando acidental por um operador humano ou componentes do Kubernetes mal configurados podem causar perda de pods, serviços ou componentes do plano de controle. Isso pode resultar na interrupção do serviço para alguns ou todos os nós.

***

* **Resolução:** A maioria dos erros do operador de cluster pode ser resolvida restaurando o estado do API Server a partir do backup.

***

* **Prevenção:** Implemente uma solução para revisar e corrigir automaticamente erros de configuração em seus clusters Kubernetes.

***
