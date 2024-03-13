---
description: >-
  Esse projeto foi desenvolvido baseado na documentação oficial do Kubernetes e
  tem como intuito demonstrar os passos que executei para criar um cluster
  Kubernetes local utilizando o Kubeadm
---

# Criação de um Cluster Kubernetes Local

***

{% embed url="https://kubernetes.io/docs/home/" %}
Kubernetes Documentation
{% endembed %}

***

## <mark style="color:red;">**Objetivos**</mark>

* Instalar um único cluster Kubernetes de plano de controle
* Instale uma rede de pods no cluster para que seus pods possam se comunicar

***

## <mark style="color:red;">**Pré-requisitos**</mark>

| Antes de você começar                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p></p><p>2 GB ou mais de RAM por máquina (menos que isso deixará pouca memória para as suas aplicações).</p>                                                                                                                                                                                                                                                                                                                                                                                           |
| 2 CPUs ou mais                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Conexão de rede entre todas as máquinas no cluster. Seja essa pública ou privada.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| <p>Swap desabilitado. Você <em>precisa</em> desabilitar a funcionalidade de swap para que o <code>kubelet</code> funcione de forma correta. </p><ul><li>Por exemplo, <code>sudo swapoff -a</code> desabilitará a troca temporariamente. Para tornar essa alteração persistente nas reinicializações, certifique-se de que a troca esteja desabilitada em arquivos de configuração como <code>/etc/fstab</code>, <code>systemd.swap</code>, dependendo de como foi configurado em seu sistema.</li></ul> |
| Assegure-se de que o módulo `br_netfilter` está carregado. Isso pode ser feito executando o comando `lsmod \| grep br_netfilter`. Para carrega-lo explicitamente execute `sudo modprobe br_netfilter`                                                                                                                                                                                                                                                                                                   |
| Como um requisito para que seus nós Linux enxerguem corretamente o tráfego agregado de rede, você deve garantir que a configuração `net.bridge.bridge-nf-call-iptables` do seu `sysctl` está configurada com valor 1                                                                                                                                                                                                                                                                                    |
| Instale um [container runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes) e kubeadm em todos os hosts. Para obter instruções detalhadas e outros pré-requisitos, consulte [Instalando o kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) .                                                                                                                                                                             |

{% hint style="info" %}
O ambiente de desenvolvimento dessa documentação foi provisionado utilizando vagrant, abaixo segue link do Gitbook de vagrant, nele é possível encontrar a documentação que utilizei para subir os nós.
{% endhint %}

{% embed url="https://danniel-gutierres-de-castro.gitbook.io/vagrant/" %}
Gitbook Vagrant
{% endembed %}

***

### <mark style="color:red;">**Desabilite o arquivo de paginação**</mark>

```bash
sudo swapoff -a
```

* O comando acima desativa o arquivo de troca até que o sistema seja reinicializado. Temos que garantir que ele permaneça desligado mesmo após uma reinicialização.
* Para fazer isso, edite o arquivo `fstab` comentando a linha  `/swapfile`

```bash
sudo vi /etc/fstab
```

```bash
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```

***

## <mark style="color:red;">Como instalar um ambiente de execução de contêiner</mark> <a href="#installing-runtime" id="installing-runtime"></a>

{% embed url="https://kubernetes.io/docs/setup/production-environment/container-runtimes/" %}
Documentação Oficial Container Runtimes Kubernetes
{% endembed %}

***

#### <mark style="color:yellow;">Instalar e configurar pré-requisitos</mark> <a href="#install-and-configure-prerequisites" id="install-and-configure-prerequisites"></a>

Encaminhando o IPv4 e permitindo que o iptables veja o tráfego em ponte. Execute as instruções abaixo mencionadas:

```bash
# Adicione os modulos que serão carregados no sysctl
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
```

```bash
sudo modprobe overlay
sudo modprobe br_netfilter
```

```bash
# sysctl params required by setup, params persist across reboots
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
```

```bash
# Apply sysctl params without reboot
sudo sysctl --system
```

Verifique se os módulos `br_netfilter`, `overlay`  estão carregados executando os seguintes comandos:

```bash
lsmod | grep br_netfilter
lsmod | grep overlay
```

***

#### <mark style="color:yellow;">Instalação  do containerd.io</mark>

Para instalar o containerd em seu sistema, siga as instruções de [introdução ao containerd](https://github.com/containerd/containerd/blob/main/docs/getting-started.md), utilizaremos a opção 2 `apt-get` ou `dnv do Github`

> Nesse cenário seguiremos apenas com a configuração de repositório, mas instalaremos apenas o containerd

[**Configurar o repositório**](https://docs.docker.com/engine/install/ubuntu/#set-up-the-repository)&#x20;

1. Atualize o `apt` índice do pacote e instale os pacotes para permitir `apt`o uso de um repositório por HTTPS:

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
```

2. Adicione a chave GPG oficial do Docker:

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

3. Use o seguinte comando para configurar o repositório:

```bash
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

4. Atualize o `apt`índice do pacote:

```bash
sudo apt-get update
```

{% hint style="warning" %}
Vale ressaltar que não seguiremos com a instalação completa do Docker, instalaremos apenas a dependência do `container.io`
{% endhint %}

5. Instale o containerd.

```bash
sudo apt-get install containerd.io
```

{% hint style="info" %}
Outro ponto é que o pacote `containerd.io` também contém `runc`, mas não contém plug-ins CNI.
{% endhint %}

> Utilizaremos a opção 1 neste mesmo Github para instalar manualmente os binários de plug-ins CNI

{% embed url="https://github.com/containernetworking/plugins/releases" %}

6. Baixe dentro da instancia provisionada a versão mais atual do plug-in CNI, que nesse exemplo é a `v1.3.0`

```bash
cd /tmp
wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-amd64-v1.3.0.tgz
```

7. Siga até o passo 3 aonde pede para que extraia o arquivo .tar baixado e crie o diretório /opt/cni/bin

```bash
sudo mkdir -p /opt/cni/bin
```

```bash
sudo tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.3.0.tgz
```

8. Após a instalação, executaremos as etapas necessárias para usar containerd como tempo de execução CRI
9. `Podemos validar que a configuração ocorreu tudo bem através do comando:`

```bash
systemctl status containerd
```

***

#### <mark style="color:yellow;">Configurando o driver cgroup systemd</mark>

Para usar o driver cgroup `systemd` defina `runc` com  `/etc/containerd/config.toml`&#x20;

1. Crie o arquivo `config.toml` ou edite-o caso já exista. Você pode encontrar esse arquivo no caminho `/etc/containerd/config.toml`

```bash
sudo vi /etc/containerd/config.toml
```

* e ao final do arquivo adicione:

```bash
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
  SystemdCgroup = true
```

> No Linux, o socket CRI padrão para containerd é `/run/containerd/containerd.sock`. No Windows, o endpoint padrão do CRI é `npipe://./pipe/containerd-containerd`

{% hint style="info" %}
**Observação:**

Se você instalou o containerd de um pacote (por exemplo, RPM ou `.deb`), poderá descobrir que o plug-in de integração do CRI está desabilitado por padrão.

Você precisa do suporte CRI ativado para usar o containerd com o Kubernetes. Certifique-se de que `cri` não está incluído na `disabled_plugins`lista dentro de `/etc/containerd/config.toml`; se você fez alterações nesse arquivo, reinicie também `containerd`.
{% endhint %}

2. Comente a linha `disabled_plugins = ["cri"] caso a mesma esteja descomentada.`
3. Certifique-se de reiniciar o containerd:

```bash
sudo systemctl restart containerd
```

4. Ativamos o início automático do serviço **containerd** no início do sistema operacional:

```bash
sudo systemctl enable containerd
```

5. Valide novamente o status do serviço

```bash
systemctl status containerd
```

***

{% hint style="success" %}
Após executar os passos de instalação do containerd vamos efetuar a instalação das ferramentas kubeadm, kubelet e kubectl, assim como descrito na documentação
{% endhint %}

***

## <mark style="color:red;">Instalando kubeadm, kubelet e kubectl</mark> <a href="#installing-kubeadm-kubelet-and-kubectl" id="installing-kubeadm-kubelet-and-kubectl"></a>

***

#### <mark style="color:yellow;">Repositórios de pacotes do Kubernetes</mark> <a href="#dpkg-k8s-package-repo" id="dpkg-k8s-package-repo"></a>

> Estas instruções são para o Kubernetes 1.28

1. Atualize o índice  `apt` do pacote e instale os pacotes necessários para usar o repositório `apt` Kubernetes:

```bash
sudo apt-get update
# apt-transport-https may be a dummy package; if so, you can skip that package
sudo apt-get install -y apt-transport-https ca-certificates curl
```

2. Baixe a chave de assinatura pública para os repositórios de pacotes Kubernetes. A mesma chave de assinatura é usada para todos os repositórios para que você possa desconsiderar a versão na URL:

```bash
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
```

3. Adicione o repositório Kubernetes apropriado `apt`:

```bash
# This overwrites any existing configuration in /etc/apt/sources.list.d/kubernetes.list
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

4. Atualize o índice `apt` do pacote, instale kubelet, kubeadm e kubectl e fixe sua versão:

```bash
sudo apt-get update
```

{% hint style="info" %}
Uma dica importante é que valide a versão de instalação do kubeadm e instale um especifica, no caso a "última", pois isso facilita em possíveis troubleshoots futuros
{% endhint %}

```bash
apt list -a kubeadm
```

5. Instale a última versão disponivel

```bash
sudo apt-get install -y kubeadm=1.28.0-1.1
```

6. Desabilite atualizações automáticas e remoção de pacotes instalados:

```bash
sudo apt-mark hold kubelet kubeadm kubectl
```

***

{% hint style="info" %}
Uma outra dica é baixar as imagens de containers que serão usados na inicialização do cluster para sabermos o que está sendo acontecendo por baixo dos panos
{% endhint %}

```bash
sudo kubeadm config images pull --kubernetes-version=1.28.0
```

***

## <mark style="color:red;">**Inicialização do cluster Kubernetes:**</mark>

```bash
sudo kubeadm init --kubernetes-version=1.28.0
```

> Observe que, para adicionar outro servidor ao cluster, você precisará fazer o mesmo trabalho de instalação e configuração do servidor e, em seguida, executar o comando _"`kubeadm join`_" com o token apropriado para o servidor com a função Master ou Worker.

***

#### <mark style="color:yellow;">Pós inicialização</mark>

1. Inicialmente criaremos o diretório `.kube` caso não tenha, para conseguir acessar as configs do Kubernetes

```bash
mkdir -p $HOME/.kube
```

***

2. Copie as configs do `admin.conf` para as configs do Kubernetes:

```bash
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
```

***

3. Altere a propriedade do arquivo

```bash
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

***

4. Liste os endereços do Master e dos serviços:

```bash
kubectl cluster-info
```

***

5. Liste as pods que estão sendo executadas na Namespace kube-system

```bash
kubectl get po -n kube-system
```

***

6. Agora podemos ver uma lista de todos os nós no cluster e o status de cada nó:

```bash
kubectl get nodes
```

***

{% hint style="info" %}
Note que após listar os nodes o cluster mostra na aba STATUS`NotReady`, isso acontece por que falta o plug-in de redes, que nos auxiliará no gerenciamento de IPs do Cluster
{% endhint %}

***

#### <mark style="color:yellow;">Installing  plug-in de redes</mark>

{% hint style="info" %}
Os nós estão no status `“NotReady”`. Para corrigir isso, você precisa instalar CNI (Container Network Interface) ou complementos de rede, como `Calico`, `Flannel` e `weave-net`.
{% endhint %}

***

{% embed url="https://kubernetes.io/docs/concepts/cluster-administration/addons/" %}

***

1. Installing o Weaver Net

{% embed url="https://www.weave.works/docs/net/latest/kubernetes/kube-addon/" %}

```bash
kubectl apply -f https://github.com/weaveworks/weave/releases/download/v2.8.1/weave-daemonset-k8s.yaml
```

***

2. Verifique o status dos pods no namespace kube-system:

```bash
kubectl get po -n kube-system
```

***

3. Liste os nós no cluster e o status de cada nó

```bash
kubectl get nodes
```

***

{% hint style="info" %}
Caso não tenha anotado o comando gerado na inicialização do cluster é possível ver novamente qual o token para atribuir o nó worker ao control-plane
{% endhint %}

```bash
kubeadm token create --print-join-command
```

***

### <mark style="color:red;">**Resetando o nó control-plane**</mark>

```bash
kubeadm reset
```

> Ao executar o comando a cima as configurações são resetadas e o cluster é desfeito

***

### <mark style="color:red;">**Adicione um nó Worker ao cluster Kubernetes**</mark>

1. Execute os mesmos passos de construção do nó control-plane até a etapa de instalação do [kubeadm](criacao-de-um-cluster-kubernetes-local.md#installing-kubeadm-kubelet-and-kubectl)
2. Execute o comando na maquina master para coletar o token que será utilizado para inicializar o nó worker ao nó control-plane

```bash
kubeadm token create --print-join-command
```

3. Execute o comando de join para atribuir o nó ao cluster

```bash
# Exemplo de token criado
kubeadm join 192.168.3.50:6443 --token s1ch4f.j6dn4nrm27oyxjr9 \
        --discovery-token-ca-cert-hash sha256:5d5a232100ec046161b028f29554201732de4e3943469be5f93ff985ced0aa90
```

> Os nós estão no status “Pronto” e o cluster Kubernetes está pronto para funcionar.

***
