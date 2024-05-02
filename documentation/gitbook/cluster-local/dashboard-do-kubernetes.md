---
description: Dashboard é uma interface de usuário do Kubernetes baseada na web.
---

# Dashboard do Kubernetes

{% embed url="https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/" %}

## <mark style="color:red;">Implante e acesse o painel do Kubernetes</mark>

Você pode usar o Dashboard para implantar aplicativos em contêineres em um cluster Kubernetes, solucionar problemas de seu aplicativo em contêineres e gerenciar os recursos do cluster.

O Dashboard também fornece informações sobre o estado dos recursos do Kubernetes em seu cluster e sobre quaisquer erros que possam ter ocorrido

<figure><img src="../.gitbook/assets/image (67) (1).png" alt=""><figcaption></figcaption></figure>

***

### <mark style="color:red;">Implantando a IU do painel</mark>[ ](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/#deploying-the-dashboard-ui) <a href="#deploying-the-dashboard-ui" id="deploying-the-dashboard-ui"></a>

{% embed url="https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/#deploying-the-dashboard-ui" %}

A UI do Dashboard não é implementada por padrão. Para implantá-lo, execute o seguinte comando:

{% embed url="https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md" %}

{% tabs %}
{% tab title="Dashboard" %}
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

***

```bash
kubectl get po -n kubernetes-dashboard
```

NAME                                                                             READY     STATUS       RESTARTS     AGE

dashboard-metrics-scraper-5657497c4c-87qxm      1/1             Running      0                     38s

kubernetes-dashboard-78f87ddfc-5z5qz                   1/1             Running      0                     39s
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Criando as permissões de acessos</mark>

{% hint style="warning" %}
**IMPORTANTE:** Certifique-se de saber o que está fazendo antes de prosseguir. Conceder privilégios de administrador à conta de serviço do Dashboard pode ser um risco de segurança.
{% endhint %}

> _Para cada um dos seguintes trechos de `ServiceAccount` e `ClusterRoleBinding`, você deve copiá-los para novos arquivos de manifesto `dashboard-adminuser.yaml` e usar `kubectl apply -f dashboard-adminuser.yaml` para criá-los._

#### <mark style="color:yellow;">Criando  ServiceAccount</mark> <mark style="color:yellow;">& ClusterRoleBinding</mark>

{% tabs %}
{% tab title="ServiceAccount" %}
Estamos criando uma conta de serviço com o nome `admin-user` no namespace `kubernetes-dashboard` primeiro.

{% embed url="https://github.com/danncastro/k8s-dashboard/blob/main/serviceaccount-admin-user.yml" %}
{% endtab %}

{% tab title="ClusterRoleBinding" %}
1. Na maioria dos casos, depois de provisionar o cluster usando `kops`, `kubeadm` ou qualquer outra ferramenta popular, o `ClusterRole` `cluster-admin` já existe no cluster.

```bash
kubectl get clusterrole | grep cluster-admin
```

cluster-admin                                                                                       2023-09-16T00:48:30Z

***

2. Podemos usá-lo e criar apenas um arquivo `ClusterRoleBinding` `ServiceAccount`. Se não existir, você precisará criar essa função primeiro e conceder os privilégios necessários manualmente.

{% embed url="https://github.com/danncastro/k8s-dashboard/blob/main/clusterrolebinding-admin-user.yml" %}
{% endtab %}

{% tab title="Create" %}
```bash
kubectl apply -f k8s-dashboard/serviceaccount.yml
```

serviceaccount/admin-user created

***

```bash
kubectl apply -f k8s-dashboard/clusterrolebinding.yml
```

clusterrolebinding.rbac.authorization.k8s.io/admin-user created
{% endtab %}
{% endtabs %}

***

#### <mark style="color:yellow;">Inicie o proxy do Kubectl</mark>

{% tabs %}
{% tab title="Kubectl proxy" %}
1º Como estamos gerenciando o cluster k8s de forma externa a partir de uma maquina virtual vagrant, devemos fazer um túnel acessando a partir da porta do Dashboard

```bash
ssh -L 8001:localhost:8001 vagrant@192.168.3.50
```

***

2º Vamos executar o proxy em segundo plano, apontando para o ip da VM do Vagrant

```bash
kubectl proxy --port=8001 &
```

\[1] 11996

Starting to serve on 127.0.0.1:8001

***

2º Podemos validar a execução do proxy em segundo plano através do seguinte comando:

```bash
ps aux | grep kubectl
```

vagrant 6617 2.5 2.0 4955500 41268 pts/0 Sl 13:50 0:00 kubectl proxy --address=192.168.3.50 --accept-hosts=.\*&#x20;

vagrant 6625 0.0 0.0 6432 720 pts/0 S+ 13:50 0:00 grep --color=auto kubectl
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">Acessando o painel</mark>

{% embed url="http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login" %}

#### <mark style="color:yellow;">Bearer Token  ServiceAccount</mark>

{% tabs %}
{% tab title="Bearer Token" %}
Agora precisamos encontrar o token que podemos usar para fazer login.&#x20;

```bash
kubectl -n kubernetes-dashboard create token admin-user
```

Deve imprimir algo como:

eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLXY1N253Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiIwMzAzMjQzYy00MDQwLTRhNTgtOGE0Ny04NDllZTliYTc5YzEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZXJuZXRlcy1kYXNoYm9hcmQ6YWRtaW4tdXNlciJ9.Z2JrQlitASVwWbc-s6deLRFVk5DWD3P\_vjUFXsqVSY10pbjFLG4njoZwh8p3tLxnX\_VBsr7\_6bwxhWSYChp9hwxznemD5x5HLtjb16kI9Z7yFWLtohzkTwuFbqmQaMoget\_nYcQBUC5fDmBHRfFvNKePh\_vSSb2h\_aYXa8GV5AcfPQpY7r461itme1EXHQJqv-SN-zUnguDguCTjD80pFZ\_CmnSE1z9QdMHPB8hoB4V68gtswR1VLa6mSYdgPwCHauuOobojALSaMc3RH7MmFUumAgguhqAkX3Omqd3rJbYOMRuMjhANqd08piDC3aIabINX6gP5-Tuuw2svnV6NYQ
{% endtab %}

{% tab title="Secrete" %}
Obtendo um token de portador de longa duração para ServiceAccount. Também podemos criar um token com o segredo que vincula a conta de serviço e o token será salvo no segredo:

{% embed url="https://github.com/danncastro/k8s-dashboard/blob/main/secret-admin-user.yml" %}
{% endtab %}

{% tab title="Create" %}
```bash
kubectl create -f k8s-dashboard/secret-admin-user.yml
```

secret/admin-user created
{% endtab %}

{% tab title="Token" %}
Após a criação do Secret, podemos executar o seguinte comando para obter o token que foi salvo no Secret:

```bash
kubectl get secret admin-user -n kubernetes-dashboard \
-o jsonpath={".data.token"} | \
base64 -d
```
{% endtab %}
{% endtabs %}

1. Agora copie o token e cole-o no campo `Enter token` da tela de login.

<figure><img src="../.gitbook/assets/image (68) (1).png" alt=""><figcaption></figcaption></figure>

2. Clique no botão `Sign in` e pronto. Agora você está logado como administrador.

<figure><img src="../.gitbook/assets/image (69) (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
A UI _só_ pode ser acessada na máquina onde o comando é executado.
{% endhint %}

{% hint style="info" %}
**Nota:** O método de autenticação kubeconfig **não** suporta provedores de identidade externos ou autenticação baseada em certificado X.509.
{% endhint %}

***

### <mark style="color:red;">Limpeza e próximas etapas</mark>



Remova o administrador `ServiceAccount`e `ClusterRoleBinding`

```bash
kubectl -n kubernetes-dashboard delete serviceaccount admin-user
kubectl -n kubernetes-dashboard delete clusterrolebinding admin-user
```

Revogue a conta de serviço (Service Account) e  a vinculação de função (Role Binding)

```bash
kubectl delete serviceaccount -n kubernetes-dashboard admin-user
kubectl delete clusterrolebinding admin-user
```

Para saber mais sobre como conceder/negar permissões no Kubernetes, leia a documentação oficial [de autenticação](https://kubernetes.io/docs/reference/access-authn-authz/authentication/) e [autorização .](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)

***
