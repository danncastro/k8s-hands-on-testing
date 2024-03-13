---
description: >-
  Um objeto da API usado para armazenar dados não confidenciais em pares
  chave-valor.
---

# Configmap

***

&#x20;[Pods](https://kubernetes.io/docs/concepts/workloads/pods/) podem consumir `Configmaps` como variáveis de ambiente, argumentos de linha de comando ou como arquivos de configuração em um [volume](https://kubernetes.io/docs/concepts/storage/volumes/).

Um ConfigMap ajuda a desacoplar configurações vinculadas ao ambiente das [imagens de contêiner](https://kubernetes.io/pt-br/docs/reference/glossary/?all=true#term-image), de modo a tornar aplicações mais facilmente portáveis.

***

### <mark style="color:red;">Criando configMap</mark>

{% tabs %}
{% tab title="Kind" %}
```bash
vim configmap.yml
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: configmap-app1
data:
  initial_refresh_value: "4"
  ui_properties_file_name: "user-interface.properties"
  user-interface.properties: |
    color.good=green
    color.bad=red
```
{% endtab %}

{% tab title="Apply" %}
```bash
kubectl apply -f configmap.yml
```
{% endtab %}

{% tab title="Output" %}
```bash
kubectl get configmap
```

***

NAME                                            DATA          AGE&#x20;

configmap-app1                           3                 10s

kube-root-ca.crt                           1                 4d12h
{% endtab %}

{% tab title="Describe" %}
Podemos descrever o conteúdo da `configMap`&#x20;

***

```bash
kubectl describe configmap configmap-app1 
```

***

Name:         configmap-app1&#x20;

Namespace:    default

Labels:       \<none>

Annotations:  \<none>

Data

\====

initial\_refresh\_value:

\----

4

ui\_properties\_file\_name:

\----

user-interface.properties:

user-interface.properties

\----

color.good=green

color.bad=red

Events:  \<none>
{% endtab %}
{% endtabs %}

***

{% tabs %}
{% tab title="Kind" %}
Para utilizarmos uma `configMap`  e configura-la com um volume

***

```bash
vim pod-configmap.yml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app1
spec:
  containers:
  - name: app1
    image: alpine
    command: ["ping", "8.8.8.8"]
    volumeMounts:
    - name: configs
      mountPath: "/etc/configs"
      readOnly: true
  volumes:
  - name: configs
    configMap:
      name: configmap-app1
```
{% endtab %}

{% tab title="Apply" %}
```bash
kubectl apply -f pod-configmap.yml 
```
{% endtab %}

{% tab title="Exec" %}
Podemos agora conectar no pod e verificar nosso volume com o `configMap`

***

```bash
kubectl exec -it pod/app1 -- ash
ls /etc/configs
cat /etc/configs/initial_refresh_value
cat /etc/configs/ui_properties_file_name 
cat /etc/configs/user-interface.properties
exit
```
{% endtab %}

{% tab title="Deleted" %}
```bash
kubectl delete pod/app1
```
{% endtab %}
{% endtabs %}

***

Existem 4 maneiras diferentes de utilizarmos um configmap para configurar um container dentro de um pod.

1. Dentro de um container através de comandos e argumentos
2. Variáveis de ambiente para um container
3. Adicionando o arquivo em um volume somente leitura para a aplicação ler.
4. Escrever o código a ser executado dentro de um pod que usa a Kubernetes API para ler o configMap

Para aprender sobre as outras maneiras, veja a [Documentação Oficial](https://kubernetes.io/docs/concepts/configuration/configmap/)

***
