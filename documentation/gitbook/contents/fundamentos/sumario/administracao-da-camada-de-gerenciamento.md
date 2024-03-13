# Administração da Camada de Gerenciamento

***

Ainda falta informações

***

### <mark style="color:red;">Kubeadm</mark>&#x20;

Comando para criar o cluster

***

### <mark style="color:red;">kubelet</mark>&#x20;

Componente que executa em todas as máquinas do cluster e gerencia tarefas como a inicialização de pods e contêineres.

* O **kubelet** pode ser visto como o **agente do k8s** que é executado nos `workers-nodes`.&#x20;
* Em cada worker-node deverá existir um agente Kubelet em execução.&#x20;
* O Kubelet é responsável por de fato gerenciar os pods, que foram direcionados pelo `controller` do cluster dentro dos nós, de forma que para isto o Kubelet pode **iniciar, parar e manter os contêineres e os pods em funcionamento** de acordo com o que foi instruído pelo controlador do cluster;

***

### <mark style="color:red;">kubectl</mark>&#x20;

Ferramenta de linha de comando do Kubernetes, permite executar comandos em clusters do Kubernetes, podendo ser usado para **implantar aplicativos, inspecionar e gerenciar recursos de cluster e visualizar logs**.

* É uma sigla para `Kubernetes Control`, muitas das vezes podemos ouvir seu nome pronunciado como `"Kube C T L"`, `"Kube Control"` e `"Kube Cuttle/Cuddle"`, esse ultimo surgiu como um apelido, devido ao seu "Mascote" ser o Cuttle fish (Em português Choco, sibas ou sépia) que é uma espécie de molusco parecido com o polvo

***

### <mark style="color:red;">kube-proxy</mark>&#x20;

Funciona como um `Proxy` e um `Load Balancer`.&#x20;

* Este componente é responsável por efetuar roteamento de requisições para os pods corretos, como também por cuidar da parte de rede dos nós;

***

### <mark style="color:red;">Container Runtime</mark>&#x20;

É o ambiente de execução de contêineres necessário para o funcionamento do k8s.

* Desde a **versão v1.24** o k8s requer que você utilize um container runtime compatível com o `CRI (Container Runtime Interface)` que foi apresentado em 2016 como uma interface capaz de criar um padrão de comunicação entre o container runtime e k8s.
* Versões anteriores à v1.24 ofereciam integração direta com o `Docker Engine` usando um componente chamado `dockershim` porém essa integração direta não está mais disponível.
* A documentação oficial do Kubernetes **(v1.24)** apresenta alguns ambientes de execução e suas respectivas configurações como o `containerd` um projeto avaliado com o nível graduado pela `CNCF(Cloud Native Computing Foundation)` e o **CRI-0** projeto incubado pela **CNCF**.

***
