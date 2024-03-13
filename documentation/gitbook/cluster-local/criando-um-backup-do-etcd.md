---
description: Todos os objetos Kubernetes são armazenados no etcd.
---

# Criando um backup do etcd

Fazer backup periódico dos dados do cluster etcd é importante para recuperar clusters Kubernetes em cenários de desastre, como a perda de todos os nós do plano de controle.

## <mark style="color:red;">Backup do etcd</mark>

{% embed url="https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster" %}

{% tabs %}
{% tab title="Kube-system" %}
1. Vamos visualizar a pod do etcd que está sendo executada na Namespace padrão do Cluster `kube-system`

```bash
kubectl get po -n kube-system -owide
```

***

2. Com isso podemos descrever a pod em execução para obter as informações necessárias para executar o backup do etcd.

```bash
kubectl describe po etcd-k8s-master-node1 -n kube-system
```

***

3. Busque no output do terminal as informações de:

\--trusted-ca-file=

\--key-file=

\--trusted-ca-file=
{% endtab %}

{% tab title="Backup" %}
Execute o comando para efetuar o backup do etcd passando ao final do comando um nome

```bash
ETCDCTL_API=3 etcdctl --cacert=/etc/kubernetes/pki/etcd/ca.crt \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key \
snapshot save backup.db
```
{% endtab %}
{% endtabs %}

***

## <mark style="color:red;">Restore etcd</mark>

Vamos executar o Restore do etcd apontando para um caminho diferente do original

{% embed url="https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#restoring-an-etcd-cluster" %}

{% tabs %}
{% tab title="Restore" %}
```bash
ETCDCTL_API=3 etcdctl snapshot restore backup.db \
--data-dir /var/lib/etcd-backup
```
{% endtab %}

{% tab title="ps aux" %}
1. Vamos buscar  informações de onde está o arquivo de configuração do kubelet&#x20;

```bash
ps aux | grep 'kubelet'
```

***

2. Busque pelo caminho apontado na opção `--config=`

\--config=/var/lib/kubelet/config.yaml
{% endtab %}

{% tab title="config.yaml" %}
1. Vamos localizar no arquivo config.yaml onde está mapeado os arquivos de pods estáticas do kubernetes

```bash
sudo cat /var/lib/kubelet/config.yaml
```

***

2. Procuraremos pela variável `staticPodPath:`

staticPodPath: /etc/kubernetes/manifests
{% endtab %}

{% tab title="Manifest" %}
1. No arquivo do diretório manifests,  imprima em tela o conteúdo do arquivo etcd.yaml e nele encontre no bloco de volumes aonde está localizado o path montado do etcd

```bash
cat etcd.yaml
```

volumes:

\-  hostPath:&#x20;

&#x20;       path: /etc/kubernetes/pki/etcd&#x20;

&#x20;       type: DirectoryOrCreate&#x20;

&#x20;   name: etcd-certs

\-  hostPath:&#x20;

&#x20;        path: /var/lib/etcd

***

2. Altere o hostPath:  `/var/lib/etcd` para o valor criado na realização do Restore `/var/lib/etcd-backup`

***

3. Aguarde até que os nós sejam reinicializados com o novo caminho do backup. Após podemos visualizar a subida do nó através do comando

```bash
watch kubectl get no -owide
```

***

4. Podemos visualizar também que a pod do etcd está sendo criada

```bash
kubectl get po -n kube-system -owide
```

etcd-k8s-master-node1       0/1           Pending       0 92s        \<none>         k8s-master-node1

***

{% hint style="info" %}
Note que o estado da pod não sairá de Pending
{% endhint %}

5. Esse estado se dá por não estarmos utilizando o caminho padrão da pod, então não carregará todas as configurações
{% endtab %}

{% tab title="Output" %}
Voltaremos o caminho  do etcd para o padrão, alterando o hostPath: `/var/lib/etcd-backup`   para `/var/lib/etcd`

***

Podemos notar que a pod voltou ao seu estado normal em Running

```bash
kubectl get po -n kube-system -owide
```

etcd-k8s-master-node1        1/1             Running       0 9h    192.168.3.50     k8s-master-node1
{% endtab %}
{% endtabs %}

***

{% hint style="warning" %}
**Observação:**

Se algum servidor API estiver em execução em seu cluster, você não deverá tentar restaurar instâncias do etcd. Em vez disso, siga estas etapas para restaurar o etcd:

1. pare _todas as_ instâncias do servidor API
2. restaurar o estado em todas as instâncias do etcd
3. reinicie todas as instâncias do servidor API

Também recomendamos reiniciar quaisquer componentes (por exemplo `kube-scheduler, kube-controller-manager, , kubelet`) para garantir que eles não dependam de alguns dados obsoletos.&#x20;

Observe que, na prática, a restauração demora um pouco. Durante a restauração, os componentes críticos perderão o bloqueio do líder e reiniciarão.
{% endhint %}

***
