---
description: >-
  Expõe uma ou mais pods, provendo IPs fixos para comunicação através de um
  ClusterIP, NodePort ou LoadBalancer para distribuir as requisições entre os
  diversos pods de um determinado Deployment.
---

# Services

{% embed url="https://kubernetes.io/docs/concepts/services-networking/service/" %}

***

## <mark style="color:red;">K8s Services</mark>

Os services, são um tipo de recursos do Kubernetes que expõe os aplicativos para fora do Cluster, as aplicações se tornam acessíveis de fora do cluster utilizando certos tipos de serviços do Kubernetes.

<figure><img src="../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Proveem um DNS exposto aos pods que executam no cluster. Ou seja esse serviço de DNS é responsável por resolver todos os nomes para que se cheguem até as Pods
{% endhint %}

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>

> _O DNS do Cluster é um servidor DNS Real. Faz parte de toda infraestrutura de rede virtualizada de um cluster Kubernetes._

Os serviços podem ser consumidos de duas formas, pelo próprio cluster, que é quando as aplicações internas acessam esses serviços ou External, acessando pela internet de fora do cluster, chegando até as aplicações através dos serviços, como mostrado abaixo:

<figure><img src="../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>

***

### <mark style="color:red;">Portas de serviço</mark>

<table><thead><tr><th align="center">Nodes</th><th align="center">Protocol</th><th align="center">Direction</th><th width="129" align="center">Port Range</th><th width="146" align="center">Purpose</th><th align="center">Used By</th></tr></thead><tbody><tr><td align="center">Control Plane </td><td align="center">TCP</td><td align="center">Inbound</td><td align="center">6443*</td><td align="center">Kubernetes API server</td><td align="center">All</td></tr><tr><td align="center">Control Plane</td><td align="center">TCP</td><td align="center">Inbound</td><td align="center">2379-2380</td><td align="center">etcd server client API</td><td align="center">kube-apiserver, etcd</td></tr><tr><td align="center">Control Plane / Workers</td><td align="center">TCP</td><td align="center">Inbound</td><td align="center">10250</td><td align="center">Kubelet API</td><td align="center">Self, Control plane</td></tr><tr><td align="center">Control Plane</td><td align="center">TCP</td><td align="center">Inbound</td><td align="center">10251</td><td align="center">kube-schenduler</td><td align="center">Self</td></tr><tr><td align="center">Control Plane</td><td align="center">TCP</td><td align="center">Inbound</td><td align="center">10252</td><td align="center">kube-controller-manager</td><td align="center">Self</td></tr><tr><td align="center">Workers</td><td align="center">TCP</td><td align="center">Inbound</td><td align="center">30000-32767</td><td align="center">NodePort</td><td align="center">Services All</td></tr></tbody></table>

***

### <mark style="color:red;">Forward Port</mark>

Podemos também criar um tipo de encaminhamento interno de portas da pod para ser acessível. Vamos começar criando nossa Pod ao qual estará executando um banco de dados. Esse banco de dados não terá acesso externo, sendo necessário a criação de um encaminhamento.

{% tabs %}
{% tab title="Kind" %}
```bash
mysql.yml
```

```yaml
apiVersion: v1
kind: Pod
metada:
  name: mysql-pod
  labels:
    app: mysql-pod
spec:
  containers:
  - name: myapp
    image: mysql:latest
    env:
    - name: "MYSQL_DATABASE"
      value: "mybase"
    - name: "MYSQL_ROOT_PASSWORD"
      value: "Senha123"
    ports:
    - containerPort: 3306
```
{% endtab %}

{% tab title="Apply" %}
```bash
kubectl apply -f mysql.yml
```
{% endtab %}

{% tab title="Output" %}
```
kubectl get po
```

NAME                READY                      STATUS                       RESTARTS                          AGE

myapp-pod       1/1                              Running                       0                                         15s
{% endtab %}

{% tab title="Forward" %}
```bash
kubectl port-forward pod/myapp-pod 3306:3306
```

Forwarding from 127.0.0.1:3606 -> 3306

Forwarding from \[::1]:3306 -> 3306
{% endtab %}

{% tab title="Database" %}
```sql
CREATE TABLE mensagens (
    id int,
    nome varchar(50),
    mensagem varchar(100)
);
```

```sql
INSERT INTO mensagens (id,nome,mensagem) VALUES (1, 'Carlos da Silva', 'Hello World!!');
```

```sql
SELECT * FROM mensagens
```

***
{% endtab %}
{% endtabs %}

***

{% hint style="info" %}
#### Todos os recursos utilizados nesses exemplos, estarão disponibilizados no Github:

[https://github.com/danncastro/kubernetes\_projects/tree/main/k8s\_cka\_exemples/services](https://github.com/danncastro/kubernetes\_projects/tree/main/k8s\_cka\_exemples/services)
{% endhint %}

## <mark style="color:red;">ClusterIP</mark>&#x20;

Serviço padrão do Kubernetes, utilizado para comunicação interna do cluster. Faz a comunicação entre diferentes pods dentro de um mesmo cluster. Torna os serviços acessíveis apenas dentro do cluster.

<figure><img src="../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

* Não é possível chamar os serviço de fora do cluster sem a utilização de um Proxy.
* Mantem os serviços apenas internos ao cluster

#### <mark style="color:blue;">Ports envolvidas na comunicação com Serviços</mark>

<figure><img src="../.gitbook/assets/image (8).png" alt=""><figcaption></figcaption></figure>

Utilizado para acessar os recursos do Kubernetes, através dessas portas que os serviços são disponibilizados.

#### <mark style="color:blue;">TargetPort</mark>

<figure><img src="../.gitbook/assets/image (13) (1).png" alt=""><figcaption></figcaption></figure>

Informa em qual porta foi disponibilizado a aplicação dentro do container em um Pod.

* Caso o valor de targetPort seja omitido, ele automaticamente assumirá o mesmo valor do atributo port.

<figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

#### <mark style="color:blue;">Características</mark>

<figure><img src="../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Pods não possuem IPs estáticos
{% endhint %}

Ou seja quando um pod e reinicializado ou até mesmo deletado, ele pode retornar com um novo endereço IP.&#x20;

* Nesse contexto o Kube-DNS se encarrega de resolver o caminho até os pods. Ou seja ele se encarrega de todo esse endereçamento IP.
* Ajuda o Administrador apenas a se preocupar com o serviço.

***

### <mark style="color:red;">Criando serviço do tipo ClusterIP</mark>

{% tabs %}
{% tab title="Pod" %}
1. Essa é a Pod que usaremos para testar a conectividade do serviço, nela temos instalado um servidor web Apache que responde na porta 80 e um serviço Tomcat que responde na porta 8080.

```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/pods/pod_web_server.yml
```

pod/web-server-pod created

***

2. Verifique os pods

```bash
kubectl get pods
```

NAME                           READY          STATUS                            RESTARTS              AGE

web-server-pod          1/1                 Running                           0                               4m44s
{% endtab %}

{% tab title="ClusterIP" %}
1. Crie o serviço do tipo ClusterIP.

```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/services/service_front-cluster-ip.yml
```

service/front-cluster-ip created

***

1. Verifique o serviço criado

```
kubectl get svc
```

NAME                            TYPE                  CLUSTER-IP          EXTERNAL-IP     PORT(S)       AGE

<mark style="color:orange;">front-cluster-ip            ClusterIP            10.110.131.92         \<none>                80/TCP         86s</mark>

kubernetes                   ClusterIP            10.96.0.1                 \<none>               443/TCP       7d4h
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Consumindo serviço do tipo ClusterIP</mark>

Neste exemplo subiremos uma pod Debian para testar se a conectividade do serviço ClusterIP está funcionando corretamente em ambas as portas apontadas no targetPort da pod **web-pod.**

{% hint style="warning" %}
**IMPORTANTE:** As aplicações que utilizam os serviços do tipo ClusterIP são acessadas através dos IPS disponibilizados em **CLUSTER-IP** ao listar os serviços criados, ou seja os IPS do serviço, e dos **TargetPorts** configurados no manifesto aplicado.
{% endhint %}

{% tabs %}
{% tab title="Pod Debian" %}
Iremos testar a conectividade das portas da Pod através de uma pod Debian.

```bash
kubectl run -it debian-pod --image=debian bash
```

If you don't see a command prompt, try pressing enter.

root@debian-pod:/#

***

1. Vamos atualizar a pod

```bash
apt update
```

***

2. Após finalizada atualização instalaremos o curl na pod debian

```bash
apt install curl -y
```
{% endtab %}

{% tab title="targetPort 80" %}
Vamos validar o targetPort atual da web-server-pod que está apontando para nosso container Apache.

```bash
kubectl describe service front-cluster-ip
```

&#x20;Name:                       front-cluster-ip

Namespace:              default

Labels:                       \<none>

Annotations:              \<none>

Selector:                    type=pod-web-server

Type:                          ClusterIP

IP Family Policy:        SingleStack

IP Families:                IPv4

IP:                              10.110.131.92

IPs:                            10.110.131.92

Port:                         http 80/TCP

<mark style="color:orange;">TargetPort:               80/TCP</mark>

Endpoints:                10.38.0.3:80

Session Affinity:       None

Events:                     \<none>

***

Execute o curl utilizando o IP do serviço apontando para a porta do serviço `front-cluster-ip` que é mostrado ao listar os serviços criados.

```bash
curl 10.110.131.92:80
```

\<html>\<body>\<h1>It works!\</h1>\</body>\</html>
{% endtab %}

{% tab title="Tomcat" %}
Dentro do manifesto do serviço iremos alterar o targetPort que está apontado para porta 80 do servidor Apache, apontando então para a porta 8080 do serviço Tomcat.

```yaml
targetPort: 8080
```

***

```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/services/service_front-cluster-ip.yml
```

service/front-cluster-ip configured
{% endtab %}

{% tab title="targetPort 8080" %}
Validaremos novamente o targetPort do serviço para saber se a alteração foi feita com sucesso

```bash
kubectl describe service front-cluster-ip
```

&#x20;Name:                       front-cluster-ip

Namespace:              default

Labels:                       \<none>

Annotations:              \<none>

Selector:                    type=pod-web-server

Type:                          ClusterIP

IP Family Policy:        SingleStack

IP Families:                IPv4

IP:                              10.110.131.92

IPs:                            10.110.131.92

Port:                         http 80/TCP

<mark style="color:orange;">TargetPort:               8080/TCP</mark>

Endpoints:                10.38.0.3:8080

Session Affinity:       None

Events:                     \<none>

***

Na pod debian, execute novamente o curl apontando para a porta do serviço frontend-service que é mostrado ao listar os serviços criados.

```bash
curl 10.110.131.92:80
```

\<! doctype html >< html lang="en" >< head>HTTP Status 404 – Not Found\</ title>body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}\</ style >< /head >< body >HTTP Status 404 – Not Found< /h1>\<hr class="line" / >< p>Type\</ b> Status Report< /p>< p>< b>Description\</ b> The origin server did not find a current representation for the target resource or is not willing to disclose that one exists.\</ p ><mark style="color:orange;">Apache Tomcat/10.1.15</mark>
{% endtab %}

{% tab title="Deleted" %}
Vamos deletar todos os recursos padrões criados.

```bash
kubectl delete all --all
```

pod "debian-pod" deleted&#x20;

pod "web-pod" deleted&#x20;

service "frontend-service" deleted&#x20;

service "kubernetes" deleted

***

```bash
kubectl get all
```

NAME                            TYPE                  CLUSTER-IP          EXTERNAL-IP     PORT(S)       AGE

kubernetes                   ClusterIP            10.96.0.1                 \<none>               443/TCP      38s
{% endtab %}
{% endtabs %}

***

## <mark style="color:red;">NodePort</mark>&#x20;

Permitem a comunicação externa ao cluster, disponibilizando uma porta ao qual é possível enviar requisições ao node, direcionada a alguma aplicação rodando nas Pods

<figure><img src="../.gitbook/assets/image (54).png" alt=""><figcaption></figcaption></figure>

Quando configuramos um serviço para `NodePort`, o kubernetes aloca uma porta de um range (por padrão 30000-32767). &#x20;

* Cada nó faz um proxy para aquela porta no serviço.

<figure><img src="../.gitbook/assets/image (55).png" alt=""><figcaption></figcaption></figure>

Quando falamos de `NodePort` temos 3 parâmetros importantes:

* <mark style="color:blue;">port</mark> - Expõe o serviço kubernetes na `port` para o cluster, ou seja, utilizada para a comunicação com a Pod

***

* <mark style="color:blue;">targetPort</mark> - Porta na qual o serviço enviará requests para o pod

***

* <mark style="color:blue;">nodePort</mark> - Porta na qual o serviço será acessível através dos IP's dos nodes de forma externa ao Cluster.

<figure><img src="../.gitbook/assets/image (56).png" alt=""><figcaption></figcaption></figure>

***

### <mark style="color:red;">Criando serviço do tipo NodePort</mark>

{% tabs %}
{% tab title="NodePort" %}
Vamos utilizar o manifesto de pod anterior removendo apenas o container do tomcat.

```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/pods/pod_web_server.yml
```

pod/web-server-pod created

```bash
kubectl apply -f  kubernetes_projects/k8s_cka_exemples/services/service_front-node-port.yml
```

service/frontend-node-port created

***

```bash
kubectl get all
```

NAME                                       READY                          STATUS                 RESTARTS            AGE

pod/web-server-pod              1/1                                  Running                0                            76s



NAME                                   TYPE           CLUSTER-IP       EXTERNAL-IP    PORT(S)              AGE

<mark style="color:orange;">service/front-node-port     NodePort    10.104.168.149    \<none>              80:30008/TCP   86s</mark>

kubernetes                           ClusterIP     10.96.0.1             \<none>              443/TCP        3d23h

***
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Consumindo serviço do tipo NodePort</mark>

{% hint style="warning" %}
Para que a comunicação esteja funcionando, deve se atentar ao Endpoint, essa frag indica que a pod foi atachada corretamente ao serviço, caso ela esteja como none, avalie se a pod está up, ou se foi configurada corretamente.
{% endhint %}

{% tabs %}
{% tab title="Describe" %}
```bash
kubectl describe service front-node-port
```

&#x20;Name:                             front-node-port

Namespace:                    default

Labels:                             \<none>

Annotations:                    \<none>

Selector:                          type=pod-web-server

Type:                                NodePort

IP Family Policy:              SingleStack

IP Families:                       IPv4

IP:                                      10.97.86.27

IPs:                                    10.97.86.27

Port:                                  http 80/TCP

TargetPort:                        80/TCP

NodePort:                          http 30008/TCP

<mark style="color:orange;">Endpoints:                        10.38.0.3:80</mark>

Session Affinity:                None

External Traffic Policy:      Cluster

Events:                               \<none>
{% endtab %}

{% tab title="NodePort 30008" %}
1. Diferente do serviços ClusterIP, com os NodePorts as aplicações são acessadas através dos IPS dos nós. Qualquer um dos INTERNAL-IP dos nós funcionariam para acessar a porta da aplicação exposta através do NodePort.

```bash
kubectl get no
```

NAME                             STATUS       ROLES                 AGE           VERSION           INTERNAL-IP

k8s-controller-node1    Ready          control-plane      11d             v1.28.3              192.168.3.50

k8s-worker-node1         Ready          \<none>               11d             v1.28.3              192.168.3.51&#x20;

<mark style="color:orange;">k8s-worker-node2         Ready         \<none>                11d             v1.28.3              192.168.3.52</mark>

***

2. Podemos resumir o comando assima da seguinte forma:

```
kubectl get nodes -o yaml | grep address
```

<mark style="color:red;">address</mark>es:

\-- <mark style="color:red;">address</mark>: 192.168.0.50

\-- <mark style="color:red;">address</mark>: k8s-controller-node1

\-- <mark style="color:red;">address</mark>: 192.168.0.51

\-- <mark style="color:red;">address</mark>: k8s-worker-node1

***

3. Usaremos o nó k8s-worker-node2 como exemplo, mas poderíamos acessar com qualquer um dos IPS dos nós

```bash
curl http://192.168.0.51:30008
```

\<html>\<body>\<h1>It works!\</h1>\</body>\</html>

***

<figure><img src="../.gitbook/assets/image (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Deleted" %}
Vamos deletar os recursos criados.

```bash
kubectl delete service/front-node-port
```

service "front-node-port" deleted

```
kubectl delete pod/web-server-pod
```

pod "web-server-pod" deleted

***

```bash
kubectl get all
```

NAME                            TYPE                  CLUSTER-IP          EXTERNAL-IP     PORT(S)       AGE

kubernetes                   ClusterIP            10.96.0.1                 \<none>               443/TCP      38s
{% endtab %}
{% endtabs %}

***

## <mark style="color:red;">LoadBalancer</mark>&#x20;

O LoadBalancer é muito similar ao NodePort, que permite a comunicação entre uma maquina do mundo externo aos nossos pods. As diferenças são que os LoadBalancers normalmente ficam alocados em um Cloud provider, e que ele automaticamente distribuí as cargas de acesso entre nós do cluster.

> Caso seja necessario a utilização do serviço do tipo LoadBalancer, será utilizado o Recurso Cloud Controller Manager (C-C-M)

<figure><img src="../.gitbook/assets/image (57).png" alt=""><figcaption></figcaption></figure>

***

### <mark style="color:red;">Criando serviço do tipo LoadBalancer</mark>

Neste exemplo criaremos um serviço do tipo LoadBalancer expondo um ip externo acessível que será utilizado pela Pod que também iremos criar.

{% tabs %}
{% tab title="LoadBalancer" %}
Vamos utilizar o manifesto de pod anterior removendo apenas o container do tomcat.

```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/pods/pod_web-server-pod.yml
```

pod/web-server-pod created

```bash
kubectl apply -f kubernetes_projects/k8s_cka_exemples/services/service_front_loadbalancer.yml
```

service/front-loadbalancer created

***

```bash
kubectl get all
```

NAME                                       READY                          STATUS                 RESTARTS        AGE

pod/web-server-pod              1/1                                  Running                0                        3m45s



NAME                                       TYPE                   CLUSTER-IP    EXTERNAL-IP     PORT(S)        <mark style="color:orange;">service/front-loadbalancer     LoadBalancer    10.99.87.8        \<pending>          80:30008/TCP</mark> &#x20;

kubernetes                               ClusterIP            10.96.0.1           \<none>               443/TCP
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Consumindo Serviço do tipo LoadBalancer</mark>



{% tabs %}
{% tab title="Describe" %}
```bash
kubectl describe service/front-loadbalancer
```

Name:                             front-loadbalancer

Namespace:                    default

Labels:                             \<none>

Annotations:                    \<none>

Selector:                          type=pod-web-server

Type:                                LoadBalancer

IP Family Policy:              SingleStack

IP Families:                       IPv4

IP:                                      10.99.87.8

IPs:                                    10.99.87.8

Port:                                  http 80/TCP

TargetPort:                        80/TCP

NodePort:                         http 30008/TCP

Endpoints:                        10.38.0.3:80

Session Affinity:                None

External Traffic Policy:      Cluster

Events:                               \<none>
{% endtab %}

{% tab title="LoadBalancer 30008" %}
1. Assim como com NodePort, qualquer um dos INTERNAL-IP dos nós funcionariam para acessar a porta da aplicação exposta através do NodePort.

```bash
kubectl get no
```

NAME                             STATUS       ROLES                 AGE           VERSION           INTERNAL-IP

<mark style="color:orange;">k8s-controller-node1    Ready          control-plane      11d             v1.28.3              192.168.3.50</mark>

k8s-worker-node1         Ready          \<none>               11d             v1.28.3              192.168.3.51&#x20;

k8s-worker-node2         Ready         \<none>                11d             v1.28.3              192.168.3.52

***

2. Usaremos o nó k8s-worker-node2 como exemplo, mas poderíamos acessar com qualquer um dos IPS dos nós

```bash
curl http://192.168.3.50:30008
```

\<html>\<body>\<h1>It works!\</h1>\</body>\</html>

***

<figure><img src="../.gitbook/assets/image (3) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Deleted" %}
Vamos deletar os recursos criados.

```bash
kubectl delete service/front-loadbalancer
```

service "front-loadbalancer" deleted

```
kubectl delete pod/web-server-pod
```

pod "web-server-pod" deleted

***

```bash
kubectl get all
```

NAME                            TYPE                  CLUSTER-IP          EXTERNAL-IP     PORT(S)       AGE

kubernetes                   ClusterIP            10.96.0.1                 \<none>               443/TCP      38s
{% endtab %}
{% endtabs %}

***

## <mark style="color:red;">External Name</mark>&#x20;

É um tipo de serviço especial que atua como um alias para um host externo. Ele não direciona o tráfego para um pod interno, como outros tipos de serviços, mas sim redireciona para um nome de host externo.

Digamos que tenhamos um serviço ou recurso fora do cluster do Kubernetes, como um banco de dados hospedado em algum lugar na internet. Podemos querer acessar esse banco de dados de dentro do cluster Kubernetes. Para fazer isso, podemos criar um serviço `externalName` que mapeia o nome do serviço do Kubernetes para o nome de host externo do banco de dados.

> Expõe um serviço externo para ser acessado através do pod interno, por exemplo um banco de dados.

```yaml
externalName: mongo-service.database.svc.cluster.local
```

<table><thead><tr><th width="207" align="center">Nome do serviço</th><th align="center">Namespace </th><th width="181" align="center">Tipo de Resources</th><th align="center">Cluster default </th></tr></thead><tbody><tr><td align="center"><code>mongo-service</code></td><td align="center"><code>database</code></td><td align="center"><code>svc</code></td><td align="center"><code>cluster.local</code></td></tr></tbody></table>

<figure><img src="../.gitbook/assets/image (58).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (59).png" alt=""><figcaption></figcaption></figure>

* Caso precise modificar esse banco de dados, só é preciso alterar o serviço do externalName, sem que precise alterar diretamente a estrutura da aplicação.

<figure><img src="../.gitbook/assets/image (60).png" alt=""><figcaption></figcaption></figure>

***

### <mark style="color:red;">Criando serviço do tipo externalName</mark>

{% tabs %}
{% tab title="ExternalName" %}
```
kubectl apply -f kubernetes_projects/k8s_cka_exemples/services/service_front_external-name.yml
```
{% endtab %}
{% endtabs %}

<figure><img src="../.gitbook/assets/image (61).png" alt=""><figcaption></figcaption></figure>

***
