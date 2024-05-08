---
description: >-
  Volumes são diretorios que os containers usaram para guardar e acessar
  arquivos, exitem volumes Ephemerals e volumes Persistentes.
---

# Volumes

{% embed url="https://kubernetes.io/docs/concepts/storage/volumes/" %}

{% hint style="info" %}
#### Todos os recursos utilizados nesses exemplos, estarão disponibilizados no Github:

[https://github.com/danncastro/nki-kubernetes-projects/tree/main/k8s-cka-exemples/pods](https://github.com/danncastro/nki-kubernetes-projects/tree/main/k8s-cka-exemples/pods)
{% endhint %}

***

## <mark style="color:red;">Overview</mark>

#### <mark style="color:blue;">Volume Abstraction</mark>

Suporta uma grande variedade de tipos de volumes, até mesmo volumes não suportados pelo Docker.

#### <mark style="color:blue;">Pod Volume Quantity Limit</mark>

Não há limite para quantidade de volumes que podem ser utilizados por um Pod

* Quando uma Pod é criada, um volume também é criado, isso é valido para volumes Ephemerals ou volumes Persistentes.
* Todos os containers implementados dentro da Pod, podem acessar, ler e gravar, os mesmo arquivos nesse volume.

#### <mark style="color:blue;">Ephemeral Volumes and Persistent Volumes</mark>

O Kubernetes trabalha com Volumes Ephemerals e Volumes Persistentes, no caso dos volumes Ephemeral, eles tem a vida util ligadas a vida util da Pod, ou seja quando uma Pod é removida os dados nesse Volume também seram.

#### <mark style="color:blue;">Volume Mount</mark>

Suporta montar sistemas de arquivos do tipo **tmpfs** - Temporary File System, que é um sistema de arquivos com suporte de RAM, armazenado na memória, que simula um disco, a vantagem de utilização do tmpfs, é  que se ganha uma grande velocidade, mas em contra partida é que tem um grande consumo de memória do container.

* Suporte a protocolos do tipo NFS & iSCSI
* Suporta armazenamentos em nuvem, como Elastic Block Store(Amazon), Files and Disk Storage(Azure) e Persistent Disk(Google).

***

## <mark style="color:red;">**Ephemeral**</mark>

#### <mark style="color:blue;">**On-Disk-Files - Container:**</mark>&#x20;

São arquivos guardados em discos dentro dos proprios containers, ou seja não são persistentes.

O problema da utilização de volumes ephemerals é que no momento em que uma Pod quebra(crash) ou é reiniciada, faz com que o Kubelet coloque o container em um estado chamado clean-state, ou seja todos os dados gravados previamente dentro dos containers, são perdidos.

#### <mark style="color:blue;">Sharing Data Between Containers</mark>

Um outro problema da utilização de volumes Ephemerals é o caso de haver compartilhamento de dados entre containers detro da mesmo Pod, e essa Pod for reiniciada, os dados armazenados que foram perdidos, também não poderam ser acessados pelos outros containers.

* Volumes compartilhados entre containers da mesma Pod, podem ser montados em caminhos diferentes, como se fossem alias para uma mesma localização.

#### <mark style="color:blue;">EmptyDir</mark>

Volumes do tipo emptyDir são volumes Ephemeral, mas ainda assim esse tipo de volume, sobrevive a uma reinicialização de container, como uma falha de liveness por exemplo, ele só será removido se a Pod morrer.

* Podem ser armazenados em diversos tipos de mídia nos Workers-Nodes

***

### <mark style="color:red;">Criando Volumes Efêmeros - emptyDir</mark>

{% tabs %}
{% tab title="Create" %}
```bash
kubectl apply -f nki-kubernetes-projects/k8s_cka_exemples/pods/pods_volume_ephemeral.yml
```

pod/volume-ephemeral-pod created

***

```bash
watch kubectl get po -owide
```

<figure><img src="../.gitbook/assets/image (95).png" alt=""><figcaption></figcaption></figure>

***
{% endtab %}

{% tab title="Exec" %}
1. Agora em outro terminal enquanto executa o watch, vamos conectar ao container criado

```bash
kubectl exec -it volume-ephemeral-pod bash
```

<figure><img src="../.gitbook/assets/image (91).png" alt=""><figcaption></figcaption></figure>

***

2. Vamos acessar o diretorio do volume montado, e criaremos um arquivo de exemplo lá.

```bash
echo "Hello Volume Ephemeral!" > volumeephetest.txt && cat volumeephetest.txt 
```

<figure><img src="../.gitbook/assets/image (92).png" alt=""><figcaption></figcaption></figure>

***
{% endtab %}

{% tab title="ProcPS" %}
Para continuar os testes, precisamos instalar dentro do contianer o Procps, para validar os processos em execução dentro do container.

```bash
apt update && apt install procps -y
```

```bash
ps aux
```

<figure><img src="../.gitbook/assets/image (89).png" alt=""><figcaption></figcaption></figure>

***
{% endtab %}

{% tab title="Restart" %}
1. Ainda com o comando `watch kubectl get po -owide` em execução em outro terminal vamos validar a aba restart para validarmos o teste de volumes ephemeral.

<figure><img src="../.gitbook/assets/image (94).png" alt=""><figcaption></figcaption></figure>

***

2.  De dentro do container vamos eliminar o processo do Redis que está em execução\


    <figure><img src="../.gitbook/assets/image (96).png" alt=""><figcaption></figcaption></figure>

***

<figure><img src="../.gitbook/assets/image (97).png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Arquivo" %}
1. Vamos acessar novamente o container para validar se o arquivo ainda estará lá

```bash
kubectl exec -it volume-ephemeral-pod bash
```

```
cat /volume-test/volumeephetest.txt
```

<figure><img src="../.gitbook/assets/image (98).png" alt=""><figcaption></figcaption></figure>

***

2. Vamos validar o que acontece em caso de deleção e recriação da Pod

```bash
kubectl delete po volume-ephemeral-pod
```

pod "volume-ephemeral-pod" deleted

```bash
kubectl apply -f nki-kubernetes-projects/k8s_cka_exemples/pods/pods_volume_ephemeral.yml
```

pod/volume-ephemeral-pod created

***

3 - Vamos acessar novamente o container e ver se o conteudo ainda está lá.

```bash
kubectl exec -it volume-ephemeral-pod bash
```

```bash
cd /volume-test
ls
```

<figure><img src="../.gitbook/assets/image (99).png" alt=""><figcaption></figcaption></figure>

***
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl delete po volume-ephemeral-pod
```

pod "volume-ephemeral-pod" deleted
{% endtab %}
{% endtabs %}

***

## <mark style="color:red;">hostPath</mark>

É um tipo de volume que fornece persistência de dados, o que significa que os dados armazenados em um volume desse tipo permanecem disponíveis mesmo após o reinício de contêineres ou a remoção/recriação de pods, isso é possivel devido ao hostPath criar um volume no próprio disco do nó de trabalho (Worker Node) do cluster. Isso significa que os dados salvos em um hostPath volume, permanece lá até que o cluster ou o Worker Node seja removido, ou então até que os arquivos sejam removidos manualmente.

> _Por conta dos dados serem armazenados localmente no Worker Node, não são replicados automaticamente em outros nós. Isso significa que, se o pod for movido para outro nó, ele não terá acesso aos dados armazenados no hostPath do nó original, a menos que o volume seja montado em todos os nós ou os dados sejam movidos manualmente._

***

### <mark style="color:red;">Criando Volumes Persistente- hostPaths</mark>



{% tabs %}
{% tab title="Create" %}
```bash
kubectl apply -f nki-kubernetes-projects/k8s-cka-exemples/pods/pods_volumes_hostpath.yml
```

pod/volume-hostpath-pod created

***

```bash
watch kubectl get po -owide
```

<figure><img src="../.gitbook/assets/image (8).png" alt=""><figcaption></figcaption></figure>

***
{% endtab %}

{% tab title="Exec" %}
1. Vamos executar o comando abaixo para conectar dentro do container

```bash
kubectl exec -it volume-hostpath-pod bash
```

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

***

2. Vamos acessar o diretorio do volume montado, e criaremos um arquivo de exemplo lá.

```bash
cd /data-persistent/ && \
echo "Hello Volume hostPath!" > volumehptest.txt && cat volumehptest.txt 
```

<figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

***
{% endtab %}

{% tab title="Arquivo" %}
1. Vamos acessar o Worker Node ao qual a Pod foi designado, como mostrado anteriormente está no node `k8s-worker-node2`

```bash
ssh vagrant@ip_do_k8s-worker-node2
```

```bash
sudo -i
```

```bash
cat /var/lib/data-persistent/volumehptest.txt
```

<figure><img src="../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

***
{% endtab %}

{% tab title="Destroyer" %}
1. Vamos deletar a Pod criada.

```bash
kubectl delete po volume-hostpath-pod
```

pod "volume-hostpath-pod" deleted

***

2. Podemos visualizar que mesmo após a deleção da Pod, o arquivo que foi mapeado para dentro do Worker Node 2, permanece lá.

<figure><img src="../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

***
{% endtab %}

{% tab title="Recreate" %}
1. Vamos recriar a Pod anteriormente destruida.&#x20;

```bash
kubectl apply -f nki-kubernetes-projects/k8s-cka-exemples/pods/pods_volumes_hostpath.yml
```

pod/volume-hostpath-pod created

***

2. Vamos novamente validar em qual Node a Pod foi criada

```bash
kubectl get po -owide
```

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>

* Essa etapa de validação do Node, é importante pois caso a Pod tenha sido designada a um Nó diferente o arquivo não aparecerá onde está mapeado.

***

3. Agora vamos novamente acessar a Pod

```bash
kubectl exec -it volume-hostpath-pod bash
```

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

***

3. Podemos notar que o arquivo ainda estará lá no volume que foi montado de forma persistente.

<figure><img src="../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>

***
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl delete po volume-hostpath-pod
```

pod "volume-hostpath-pod" deleted

***

```bash
kubectl get po
```

No resources found in default namespace.

***
{% endtab %}
{% endtabs %}

***
