---
description: >-
  Volumes são diretorios que os containers usaram para guardar e acessar
  arquivos, exitem volumes Ephemerals e volumes Persistentes.
---

# Volumes

{% embed url="https://kubernetes.io/docs/concepts/storage/volumes/" %}

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
{% tab title="Create Pod" %}
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
1. Agora em outro terminal vamos enquanto executa o watch, vamos conectar ao container criado

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

3 - Vamos acessar novamente o container e ver se o conteudo&#x20;

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

### <mark style="color:red;">PersistentVolume (PV)</mark>&#x20;

O gerenciamento de armazenamento é uma questão bem diferente do gerenciamento de instâncias computacionais.&#x20;

O subsistema `PersistentVolume` provê uma API para usuários e administradores que mostra de forma detalhada de como o armazenamento é provido e como ele é consumido. Para isso, o Kubernetes possui duas novas APIs:

&#x20;PVs são plugins de `volume`, porém eles têm um ciclo de vida independente de qualquer pod que utilize um PV. Essa API tem por objetivo mostrar os detalhes da implementação do armazenamento, seja ele **NFS, ISCSI, ou um armazenamento específico de um provedor de cloud pública**.

***

### <mark style="color:red;">PersistentVolumeClaim (PVC)</mark>&#x20;

PVC é uma requisição para armazenamento por um usuário.  Claims podem solicitar ao PV tamanho e modos de acesso específicos.  Uma reivindicação de volume persistente (PVC) é a solicitação de armazenamento, que é atendida vinculando a PVC a um volume persistente (PV). Exemplo:

***

### StorageClasses(SC)&#x20;

Fornecem dinamismo para criação de `PersistentVolume` conforme demanda. Também são capazes de criar discos de armazenamento

***

## <mark style="color:red;">Persistent Storage</mark>

Quando falamos de armazenamento persistente em Kubernetes, precisamos entender dois recursos, o `PersistentVolumes` ou `PV` e o `PersistentVolumeClaim` ou `PVC`

* <mark style="color:yellow;">Persistent Volume ou PV</mark> - `PVs` é um recurso de armazenamento virtual disponível no cluster, que aponta para um armazenamento físico na infraestrutura.

***

* <mark style="color:yellow;">Persistent Volume Claim ou PVC</mark> - `PVCs` são solicitações de volume feitas pelo kubernetes que será atrelado a um APP.

{% hint style="info" %}
Podemos resumir como `PV` sendo a unidade lógica atribuída a uma unidade de armazenamento físico que será disponibilizado para o kubernetes, e o `PVC` como a solicitação do kubernetes para que um volume com especificação `x` seja utilizado.
{% endhint %}

{% hint style="warning" %}
Um ponto importante a se notar é que o `PVC` sempre irá buscar o menor armazenamento possível que entregue todos os recursos que forem solicitados.
{% endhint %}

Caso um `PVC` solicite 500Mb e o menor volume com todas as características requisitadas tenha 1Gb, o `PVC` irá adquirir o `PV` de 1Gb e o utilizará para a aplicação.

***

#### <mark style="color:yellow;">Modos de Acesso</mark>

Os volumes no kubernetes podem ter diversos modos de acesso:

* `ReadWriteOnce` ou `RWO` - O volume pode ser montado como leitura e escrita por apenas um único nó

***

* `ReadOnlyMany` ou `ROX` - O volume pode ser montado como apenas leitura por diversos nós

***

* `ReadWriteMany` ou `RWX` - O volume pode ser montado como leitura e escrita por diversos nós

***

* `ReadWriteOncePod` ou `RWOP` - O volume pode ser montado como leitura e escrita por apenas um pod. (Apenas no Kubernetes 1.22+)

Precisamos descrever o modo de acesso quando criamos nossos volumes.

***

### <mark style="color:red;">Criando PVs</mark>

Como todo recurso no kubernetes, criamos `PVs` através de arquivos yaml. Porém precisaremos criar os volumes antes de criar os `PVs`, vamos conectar em nosso minikube e criar os volumes

```bash
$ minikube ssh
$ sudo mkdir /mnt/dados{1..3}
$ sudo sh -c "echo 'Kubernetes Storage Dados 1' > /mnt/dados1/index.html"
$ sudo sh -c "echo 'Kubernetes Storage Dados 2' > /mnt/dados2/index.html"
$ sudo sh -c "echo 'Kubernetes Storage Dados 3' > /mnt/dados3/index.html"
$ ls -lR /mnt
$ exit
```

Agora que temos nossos diretórios de dados, vamos criar nossos PersistentVolumes

```bash
$ vim pv.yml
```

```yml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv10m
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Mi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/dados1"
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv200m
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 200Mi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/dados2"
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv1g
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/dados3"
```

> Podemos descrever diversos recursos abrindo um novo yaml através do `---` em um mesmo arquivo

Vamos criar e listar nossos `PVs`

```bash
$ kubectl apply -f pv.yml
$ kubectl get persistentvolumes
$ kubectl get pv
```

```bash
NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   REASON   AGE
pv10m    10Mi       RWO            Retain           Available           manual                  42s
pv1g     1Gi        RWO            Retain           Available           manual                  42s
pv200m   200Mi      RWO            Retain           Available           manual                  42s
```

***

### <mark style="color:red;">Criando PVCs</mark>

Vamos criar nossos PVCs através de um arquivo yaml

```bash
$ vim pvc.yml
```

```yml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc100m
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc700m
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 700Mi
```

Vamos criar e listar nossos `PVs`

```bash
$ kubectl apply -f pvc.yml
$ kubectl get persistentvolumeclaims
$ kubectl get pvc
$ kubectl get pv 
```

```bash
NAME      STATUS   VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
pvc100m   Bound    pv200m   200Mi      RWO            manual         30s
pvc700m   Bound    pv1g     1Gi        RWO            manual         30s
```

```bash
NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM             STORAGECLASS   REASON   AGE
pv10m    10Mi       RWO            Retain           Available                     manual                  10m
pv1g     1Gi        RWO            Retain           Bound       default/pvc700m   manual                  10m
pv200m   200Mi      RWO            Retain           Bound       default/pvc100m   manual                  10m
```

Podemos ver que o os `PVs` que solicitamos foram atrelados ao `PV` que satisfaz todas suas necessidades listadas, ligando o `PVC` que solicitou 100Mi ao `pv200m` e o `PVC` que solicitou 700m ao `pv1g`.

***

### <mark style="color:red;">Atrelando Pod a Volumes.</mark>

Para ligar um Pod a um volume, precisamos declara-lo no yaml de criação do pod.

```bash
$ vim webserver.yml
```

```yml
apiVersion: v1
kind: Pod
metadata:
  name: webserver
spec:
  volumes:
    - name: webdata
      persistentVolumeClaim:
        claimName: pvc100m
  containers:
    - name: webserver
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: webdata
```

> Note que a configuração do Pod aponta para um `PVC` porém não especificamos o `PV`. Isso se dá porque pelo ponto de vista do Pod, um `Claim` é um volume.

Vamos executar nosso pod e verificar o volume

```bash
kubectl apply -f webserver.yml
kubectl get pods
kubectl exec -it webserver -- /bin/bash
curl localhost
exit
```

Vamos alterar nosso pod para utilizar o outro `PVC`.

```bash
kubectl detele pod/webserver
vim webserver.yml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: webserver
spec:
  volumes:
    - name: webdata
      persistentVolumeClaim:
        claimName: pvc700m
  containers:
    - name: webserver
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: webdata
```

Vamos executar nosso pod e verificar o volume

```bash
kubectl apply -f webserver.yml
kubectl get pods
kubectl exec -it webserver -- /bin/bash
curl localhost
exit
```

Mais informações sobre Volumes podem ser vistas na [Documentação Oficial](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

***

### <mark style="color:red;">Destruindo o Ambiente</mark>

Agora que passamos por todos os conceitos base do kubernetes, podemos destruir nosso ambiente do minikube

```bash
minikube delete
```
