---
description: >-
  O Amazon Elastic Kubernetes Service é um serviço gerenciado de Kubernetes que
  descarta a necessidade de instalar e operar a camada de gerenciamento do
  cluster.
---

# Amazon EKS

***

Ele é certificado como compatível com o Kubernetes, portanto, você pode migrar qualquer aplicativo com facilidade para o EKS.



<details>

<summary>Provision an EKS Cluster</summary>

```
Deploy compute -> Connect to EKS -> Run Kubernetes applications
```

</details>

```bash
aws eks --region sa-east-1 describe-cluster --name nome-do-cluster --query cluster.status
```

```bash
aws eks --region sa-east-1 update-kubeconfig --name nome-cluster
```
