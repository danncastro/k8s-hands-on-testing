---
description: >-
  A API de métricas no Kubernetes não é habilitada automaticamente no kubelet
  quando você cria um cluster com o kubeadm.
---

# Habilitando Métricas da API

{% hint style="info" %}
Precisamos configurar manualmente o kubelet para expor a API de métricas.&#x20;
{% endhint %}

A API de métricas fornece informações detalhadas sobre o desempenho e o estado do kubelet e dos contêineres em execução no nó.

> _Abaixo estão os passos para habilitar a API de métricas no kubelet usando o `kubeadm`:_

***

### <mark style="color:red;">**Validação de status**</mark>

Para validar aonde o arquivo está criado basta ver o status do serviço do kubelet

{% tabs %}
{% tab title="Status" %}
```bash
systemctl status kubelet
```

kubelet.service - kubelet: The Kubernetes Node Agent

&#x20;       Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)

&#x20;    <mark style="color:orange;">Drop-In: /usr/lib/systemd/system/kubelet.service.d</mark>&#x20;

&#x20;                   <mark style="color:orange;">└─10-kubeadm.conf</mark>&#x20;

&#x20;       Active: active (running) since Sat 2023-09-16 02:30:18 UTC; 5min ago&#x20;

&#x20;              Docs: https://kubernetes.io/docs/&#x20;

&#x20;     Main PID: 28757 (kubelet)&#x20;

&#x20;           Tasks: 12 (limit: 3448)

&#x20;         Memory: 36.7M&#x20;

&#x20;         CGroup: /system.slice/kubelet.service&#x20;

&#x20;                  └─28757 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var...
{% endtab %}
{% endtabs %}

***

### <mark style="color:red;">**Edite o arquivo de configuração do kubelet**</mark>

Certifique-se de que este arquivo exista. Se não existir, você pode criá-lo manualmente.

{% tabs %}
{% tab title="10-kubeadm.conf" %}
```bash
sudo vi /lib/systemd/system/kubelet.service.d/10-kubeadm.conf
```

***

Essas opções habilitam a API de métricas e especificam o caminho para o arquivo de autoridade de certificação (CA) do Kubernetes.

1. Adicione a opção `--authentication-token-webhook` e `--kubelet-certificate-authority` na linha de comando do kubelet:

```bash
Environment="KUBELET_EXTRA_ARGS=--authentication-token-webhook=true \
--kubelet-certificate-authority=/etc/kubernetes/pki/ca.crt"
```

***

2. Salve o arquivo e saia do editor de texto.

***

3. Recarregue o systemd para aplicar as alterações:

```bash
sudo systemctl daemon-reload
```
{% endtab %}

{% tab title="Kubelet" %}
Reinicie o kubelet para aplicar as configurações atualizadas:

```bash
sudo systemctl restart kubelet
```

***

Agora, a API de métricas do kubelet deve estar habilitada e acessível em `http://<ip-node>:10255/metrics`, onde `<ip-node>` é o endereço do nó em que o kubelet está sendo executado. Você pode usar ferramentas de monitoramento como o Prometheus para coletar e visualizar essas métricas.
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Lembre-se de que, ao expor a API de métricas do kubelet, você está permitindo o acesso a informações detalhadas sobre o estado do nó e dos contêineres em execução. Certifique-se de que o acesso a essa API seja restrito e seguro, de acordo com as melhores práticas de segurança do Kubernetes.
{% endhint %}
