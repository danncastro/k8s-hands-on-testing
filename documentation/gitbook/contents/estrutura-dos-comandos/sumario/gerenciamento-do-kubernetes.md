# Gerenciamento do Kubernetes

***

{% embed url="https://kubernetes.io/docs/tasks/tools/" %}

***

```bash
kubectl get service
kubectl get pods
kubectl get pods -o wide
kubectl get pods --namespace nome-da-namespace
kubectl get nodes --watch
kubectl get deployment
kubectl get deployment --namespace nome-da-namespace
kubectl get endpoints
kubectl get endpoints --namespace nome-da-namespace
```

```bash
kubectl delete pod nome-do-pod
kubectl delete node nome-do-node
kubectl delete deployment nome-do-deployment
```

```bash
kubectl describe pod nome-do-pod
kubectl describe nodes nome-do-node
kubectl describe deployment nome-do-deployment
kubectl describe service nome-do-service
```

```bash
kubectl scale deployment nome-do-deployment --replicas=x
```

```bash
kubectl expose deployment nome-do-deployment --type=LoadBalancer --name=app-html --port=80
```

```bash
kubectl exec --stdin --tty nome-do-pod -- /bin/bash
kubectl exec -ti nome-do-pod bash
```

```bash
kubectl port-forward pod/nome-do-pod portUsage:portPod
kubectl port-forward pod/nome-do-pod 3306:3306
```

```bash
kubectl run nginx --image nginx --port 80
```

```bash
kubectl logs -f nome-do-container
```

```bash
kubectl create namespace nome-da-nomespace
kubectl create deployment nome-do-deployment --image imagem --replicas x -n nome-da namespace
```

```bash
kubectl create deployment nome-do-deployment --image imagem --replicas x -n nome-da namespace --port x --dry-run=client -o yaml
```

```bash
kubectl apply -f nome-do-arquivo.yml
```

```bash
kubectl explain nome-do-recurso
```

```bash
kubectl edit resource
```

kubectl rollout undo deployment --to-revision=\<versão a ser retornada> kubectl rollout

kubectl config get-contexts

setaws='kubectl config set-context production-sa-east-1a' setdev='kubectl config set-context gcp.dev.uc1a' setgcp='kubectl config set-context gcp.prd.sp1a' useaws='kubectl config use-context production-sa-east-1a' usedev='kubectl config use-context gcp.dev.uc1a' usegcp='kubectl config use-context gcp.prd.sp1a'

kubectl describe ns labels kubectl get ns nome\_label=dados

kubectl config current-context
