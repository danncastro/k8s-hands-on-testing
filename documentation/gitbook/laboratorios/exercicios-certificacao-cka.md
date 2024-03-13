---
description: Exercícios propostos no treinamento da Certificação CKA
---

# Exercícios Certificação CKA

***

### <mark style="color:red;">Cluster Architecture</mark>

1. Faça a criação de um namespace e crie um POD no NS

```
kubectl create ns ctarchi
```

```
kubectl run ctpod --image=nginx -n ctarchi
```

```bash
kubectl get po -n ctarchi -owide
```

> NAME        READY       STATUS       RESTARTS        AGE                  IP                   NODE
>
> ctarchi       1/1              Running       0                       2m2s               10.44.0.1        k8s-worker-node1

***

2. Crie uma POD no namespace Default.

```
kubectl run dfpod --image=nginx -n default
```

```bash
kubectl get po -n default -owide
```

> NAME        READY       STATUS       RESTARTS        AGE                  IP                   NODE
>
> dfpod         1/1              Running       0                       2m2s               10.44.0.2        k8s-worker-node1

***

1. Acesse a POD do namespace Default e veja se a mesma se comunica com a POD do namespace criado previamente. (você pode realizar um teste com o comando PING ou CURL).

```bash
kubectl exec -it default -n default -- curl -v 10.44.0.1
```

> \* Connected to 10.44.0.1 (10.44.0.1) port 80 (#0)
>
> < HTTP/1.1 200 OK ...
>
> Welcome to nginx!
>
> ## Welcome to nginx!
>
> If you see this page, the nginx web server is successfully installed and working. Further configuration is required.
>
> For online documentation and support please refer to [nginx.org](http://nginx.org/).\
> Commercial support is available at [nginx.com](http://nginx.com/).
>
> _Thank you for using nginx._
>
> \* Connection #0 to host 10.44.0.1 left intact \* Trying 0.0.0.80:80...

***
