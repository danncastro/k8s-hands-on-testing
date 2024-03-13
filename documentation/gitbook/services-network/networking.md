# Networking

<figure><img src="../.gitbook/assets/image (49).png" alt=""><figcaption><p>Inter Node Pod Network Communication</p></figcaption></figure>

***

### <mark style="color:red;">Container to Container Communication</mark>

<figure><img src="../.gitbook/assets/image (50).png" alt=""><figcaption><p>Container to container communication</p></figcaption></figure>

* Um ou mais contêineres dentro de um pod compartilham o mesmo host network
* Neste caso os pods terão seu próprio endereço IP, fazendo com que todos os contêineres dentro da POD tenham o mesmo endereço IP mas funcionando em portas diferentes.
* A comunicação entre os contêineres acontecem dentro da própria pod porem em portas diferentes

***

### <mark style="color:red;">Pod to Pod Communication</mark>

<figure><img src="../.gitbook/assets/image (51).png" alt=""><figcaption><p>Pod to Pod Communication</p></figcaption></figure>

<mark style="color:yellow;">Intra Node Pod Network Communication</mark>

* Comunicação de pods rodando em um Single Node
* Neste caso todos os endereços IPS das pods serão diferentes e atribuídos a partir da rede local, pois compartilham o mesmo Host e a comunicação entre os pods ocorrem dentro do mesmo Worker Node
* O Kubernetes cria e virtualiza um Bridge Network para comunicação entre os pods, que permite que os contêineres se conversem entre si, **mesmo que em pods diferentes.**

<figure><img src="../.gitbook/assets/image (53).png" alt=""><figcaption></figcaption></figure>

{% @github-files/github-code-block %}

{% tabs %}
{% tab title="Create" %}
```bash
kubectl create -f k8s-cka-exemples/pod-to-pod-communication/tomcat.yml
```

pod/tomcat-pod created

***

```bash
kubectl create -f k8s-cka-exemples/pod-to-pod-communication/redis.yml
```

pod/redis-pod created  &#x20;

***

```bash
kubectl get pods
```

NAME                               READY                  STATUS                     RESTARTS               AGE      &#x20;

redis-pod                         1/1                         Running                     0                               37s&#x20;

tomcat-pod                      1/1                         Running                     0                               33s

***
{% endtab %}

{% tab title="Install iputils" %}
```bash
kubectl exec -it tomcat-pod -- bash
```

***

```bash
apt update
```

***

```bash
apt install iputils-ping -y
```

***
{% endtab %}

{% tab title="Ping test" %}
```bash
kubectl describe pods redis-pod | grep IP
```

<mark style="color:red;">IP</mark>:                                                  10.46.0.1&#x20;

<mark style="color:red;">IP</mark>s:&#x20;

&#x20;   <mark style="color:red;">IP</mark>: 10.46.0.1

***

```bash
kubectl exec -it tomcat-pod -- bash
```

***

```
ping 10.46.0.1 
```

PING 10.46.0.1 (10.46.0.1) 56(84) bytes of data.

64 bytes from 10.46.0.1: icmp\_seq=1 ttl=64 time=2.04 ms

64 bytes from 10.46.0.1: icmp\_seq=2 ttl=64 time=0.716 ms

64 bytes from 10.46.0.1: icmp\_seq=3 ttl=64 time=0.933 ms
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl get pods
```

NAME                               READY                  STATUS                     RESTARTS               AGE      &#x20;

redis-pod                         1/1                         Running                     0                               47m&#x20;

tomcat-pod                      1/1                         Running                     0                               47m

***

```bash
kubectl delete pods redis-pod
```

pod "redis-pod" deleted

***

```bash
kubectl delete pods tomcat-pod
```

pod "tomcat-pod" deleted

***

```bash
kubectl get pods
```

No resources found in default namespace.
{% endtab %}
{% endtabs %}

***

#### <mark style="color:yellow;">Inter Node Pod Network Communication</mark>

<figure><img src="../.gitbook/assets/image (52).png" alt=""><figcaption></figcaption></figure>

* Comunicação de pods rodando em Multi Nodes
* Estabelece comunicação entre os Workers Nodes
* A comunicação entre as pods neste caso acontece a partir de um plugin de rede do Kubernetes, que irá criar as tabelas de rotas necessárias, para que um contêineres possa se comunicar com outros contêineres dentro de pods diferentes em workers nodes diferentes independente do local ao qual esteja instanciado o cluster, podendo ser local ou em nuvem.

***
