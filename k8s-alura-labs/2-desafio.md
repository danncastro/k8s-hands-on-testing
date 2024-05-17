# Desafio: criptografia de disco

Você é um administrador de cluster Kubernetes e sua tarefa é garantir que os dados confidenciais armazenados em secrets e configmaps estejam protegidos por encriptação quando estiverem em repouso. Sua missão é seguir um passo a passo para habilitar e configurar a encriptação de dados em um cluster Minikube.

Passo a passo:

Crie um novo arquivo de configuração de encriptação chamado encryption-config.yaml, conforme fornecido no enunciado;
Salve o arquivo encryption-config.yaml no local apropriado no nó do plano de controle;
Edite o manifesto do kube-apiserver localizado em kube-apiserver.yaml para adicionar a configuração de encriptação;
Realize a montagem do arquivo de configuração de encriptação no kube-apiserver conforme indicado no manifesto;
Reinicie o kube-apiserver para aplicar as alterações de configuração;
Verifique se a encriptação está funcionando corretamente criando um novo Secret e utilizando o etcdctl para ler o Secret do etcd e verificar a encriptação;
(Opcional) Para garantir que todos os Secrets existentes também sejam encriptados, utilize o comando kubectl para atualizar todos os Secrets.
Dica: Lembre-se de substituir os valores corretos no arquivo de configuração de encriptação e ajustar os caminhos de arquivos e diretórios conforme sua configuração.

Sinta-se livre para verificar a documentação oficial do Kubernetes a respeito de Encriptação de Disco

---

## A solução a seguir é apenas uma sugestão/possibilidade para vencer o desafio. Fique à vontade para solucionar o desafio da sua própria maneira.

### Etapa 1: Criar um novo arquivo de configuração de criptografia (encryption-config.yaml):

~~~bash
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
      - configmaps
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <SEGREDO CODIFICADO EM BASE 64>
~~~

### Etapa 2: Salvar o arquivo de configuração de criptografia (encryption-config.yaml)

Salve o arquivo em um local no nó do plano de controle, como /etc/kubernetes/enc/enc.yaml.

### Etapa 3: Editar o manifesto do kube-apiserver (kube-apiserver.yaml):

~~~bash
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
    - name: kube-apiserver
      command:
        - kube-apiserver
        ...
        - --encryption-provider-config=/etc/kubernetes/enc/enc.yaml
      volumeMounts:
        - name: enc
          mountPath: /etc/kubernetes/enc
          readOnly: true
  volumes:
    - name: enc
      hostPath:
        path: /etc/kubernetes/enc
        type: DirectoryOrCreate
~~~

### Etapa 4: Montar o arquivo de configuração de criptografia no manifesto do kube-apiserver (kube-apiserver.yaml)

### Etapa 5: Reiniciar o kube-apiserver

### Etapa 6: Verificar a criptografia dos dados

~~~bash
kubectl create secret generic secret1 -n default --from-literal=mykey=mydata
~~~

Use o programa de linha de comando etcdctl para ler o Secret do etcd e verificar a criptografia.

### Etapa 7: Garantir que todos os Secrets estejam criptografados (opcional):

~~~bash
kubectl get secrets --all-namespaces -o json | kubectl replace -f -
~~~

Repare que você precisará substituir <SEGREDO CODIFICADO EM BASE 64> pela chave aleatória de 32 bytes codificada em base 64 que você gerou na Etapa 1. Além disso, verifique se ajustou os caminhos e nomes de arquivo nos exemplos de acordo com sua configuração
