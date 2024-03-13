# Gerenciamento do Kubernetes

***

{% embed url="https://kubernetes.io/docs/tasks/tools/" %}

***

```bash
kubectl get endpoints
kubectl delete node nome-do-node
kubectl expose deployment nome-do-deployment --type=LoadBalancer --name=app-html --port=80
kubectl exec --stdin --tty nome-do-pod -- /bin/bash
kubectl logs -f nome-do-container
kubectl create deployment nome-do-deployment --image imagem --replicas x -n nome-da namespace
kubectl create deployment nome-do-deployment --image imagem --replicas x -n nome-da namespace --port x --dry-run=client -o yaml
kubectl explain nome-do-recurso
```
