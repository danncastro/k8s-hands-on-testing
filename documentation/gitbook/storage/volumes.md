---
description: >-
  Possuem ciclos de vida independentes dos containers. Porém, são dependentes
  dos pods
---

# Volumes

***

<mark style="color:yellow;">**Persistência de dados:**</mark> O gerenciamento de armazenamento é uma questão bem diferente do gerenciamento de instâncias computacionais.&#x20;

O subsistema `PersistentVolume` provê uma API para usuários e administradores que mostra de forma detalhada de como o armazenamento é provido e como ele é consumido. Para isso, o Kubernetes possui duas novas APIs:

***

### <mark style="color:red;">PersistentVolume (PV)</mark>&#x20;

&#x20;PVs são plugins de `volume`, porém eles têm um ciclo de vida independente de qualquer pod que utilize um PV. Essa API tem por objetivo mostrar os detalhes da implementação do armazenamento, seja ele **NFS, ISCSI, ou um armazenamento específico de um provedor de cloud pública**.

***

### <mark style="color:red;">PersistentVolumeClaim (PVC)</mark>&#x20;

PVC é uma requisição para armazenamento por um usuário.  Claims podem solicitar ao PV tamanho e modos de acesso específicos.  Uma reivindicação de volume persistente (PVC) é a solicitação de armazenamento, que é atendida vinculando a PVC a um volume persistente (PV). Exemplo:

***

### StorageClasses(SC)&#x20;

Fornecem dinamismo para criação de `PersistentVolume` conforme demanda. Também são capazes de criar discos de armazenamento

***

### <mark style="color:red;">Statefullset</mark>&#x20;

Podem ser usados quando estados devem ser persistidos.&#x20;

1. Usam **`PersistentVolume`** e **`PersistentVolumeClaim`** para persistência de dados.
2. Garante unicidade de Pods durante reinícios e atualizações
3. Clusters possuem StorageClasses "default" e podem ser usados automaticamente se não definirmos qual será utilizado

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
