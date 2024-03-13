---
description: Curso de DevOps Pro Fabricio Veronez
---

# Laboratórios TDevOps

***

```bash
mkdir app
cd /app
mkdir kubernetes
cd kubernetes
```

***

### **APP-1-KUBERNETES-POD-SIMPLES**

```bash
simple-pod.yml
```

```yml
apiVersion: v1
kind: Pod
metadata:
    name: app-html
    labels:
        app: app-html
spec:
    containers:
    - name: app-html
      image: httpd:latest
      ports:
      - containerPort: 80
```

***

### **APP-2-KUBERNETES-DEPLOYMENT-SIMPLES**

```bash
simple-deployment.yml
```

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: app-html-deployment
    labels:
        app: app-html
spec:
    replicas: 3
    selector:
        matchLabels:
            app: app-html
    template:
        metadata:
            labels:
                app: app-html
        spec:
        containers:
        - name: app-html
        image: httpd:latest
        ports:
        - containerPort: 80
```

***

### **APP-3-KUBERNETES-LOADBALANCER**

```bash
app-html-lb.yml
```

```yml
apiVersion: v1
kind: Service
metadata:
    name: app-html-lb
spec:
    selector:
        app: app-html
    ports:
        - port: 80
          targetPort: 8080
    type: LoadBalancer
```

***

### **APP-4-KUBERNETES-NODEPORT**

```bash
index.php
```

```php
<html>
    <head>
        <title>MyApp PHP 1.0</title>
    </head>
    <body>
        <h1>MyApp PHP 1.0</h1>
    <?php

    echo gethostname();
    echo "<br>";
    echo $_SERVER["REMOTE_ADDR"];
    echo "<br>";
    echo date('Y-m-d H:i:s');

    ?>
    </body>
</html>
```

***

```bash
Dockerfile
```

```dockerfile
FROM        php:7.4-apache

WORKDIR     /var/www/html
COPY        index.html /var/www/html

RUN         apt-get update && apt-get install -y \
                libfreetype6-dev \
                libjpeg62-turbo-dev \
                libpng-dev \
            && docker-php-ext-configure gd --with-freetype --with-jpeg \
            && docker-php-ext-install -j$(nproc) gd \
            && docker-php-ext-install pdo_mysql \
            && docker-php-ext-install mysqli

EXPOSE      80
```

***

```bash
nodePort.yml
```

```yml
apiVersion: v1
kind: Service
metada:
    name: myapp-php-service
spec:
    type: NodePort
    selector:
        app: myapp-php
    ports:
        - port: 80
          targetPort: 80
          #nodePort: 30007
```

***

```bash
pod.yml
```

```yml
apiVersion: v1
kind: Pod
metada:
    name: myapp-php
    labels:
        app: myapp-php
spec:
    containers:
    - name: myapp-php
      image: danncastro/myapp-php:1.0
      ports:
      - containerPort: 80
```

***

### **APP-5-KUBERNETES-DEPLOYMEN-&-SERVICE**

```bash
app-deployment-service.yml
```

```yml
apiVersion: v1
kind: Pod
metada:
    name: myapp-php
    labels:
        app: myapp-php
spec:
    containers:
    - name: myapp-php
      image: danncastro/myapp-php:1.0
      ports:
      - containerPort: 80

---

apiVersion: v1
kind: Service
metada:
    name: myapp-php-service
spec:
    type: NodePort
    selector:
        app: myapp-php
    ports:
        - port: 80
          targetPort: 80
          nodePort: 30007
```

***

### **APP-6-KUBERNETES-MYSQL**

```bash
mysql.yml
```

```yml
apiVersion: v1
kind: Pod
metada:
    name: mysql-pod
    labels:
        app: mysql-pod
spec:
    containers:
    - name: myapp
      image: mysql:latest
      env:
        - name: "MYSQL_DATABASE"
          value: "mybase"
        - name: "MYSQL_ROOT_PASSWORD"
          value: "Senha123"
      ports:
      - containerPort: 3306
```

***

```bash
persistent-volume.yml
```

```yml
apiVersion: v1
kind: PersistentVolume
metadata:
    name: local
    labels:
        type: local
spec:
    storageClassName: manual
    capacity:
        storage: 100Mi
    accessModes:
        - ReadWriteOnce
    hostPath: 
        path: /meubanco/
```

***

```bash
persistent-volume-claim.yml
```

```yml
apiVersion: v1
kind: PersistentVolumeClain
metadata:
    name: local
spec:
    storageClassName: manual
    accessModes:
        - ReadWriteOnce
    resources:
        requests:
            storage: 100Mi
    hostPath: 
        path: /meubanco/
```

> `dentro-da-aplicação`

```yml
    volumeMounts:
    - name: local
      mountPath: /caminho
volumes:
- name: local
  PersistentVolumeClainm:
    claimName: local
```

***

```bash
http-nfs.yml
```

```yml
apiVersion: v1
kind: PersistentVolume
metadata:
    name: fileserver
spec:
    capacity:
        storage: 50Gi
    acessModes:
    - ReadWriteMany
    nfs:
        path: /dados
        server: ip-servidor ou disco

---

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
    name: fileserver-httpd
spec:
    accessModes:
    - ReadWriteMany
    storageClassName: ""
    volumeName: fileserver-httpd
    resources:
        requests:
            storage: 50Gi

---

apiVersion: app/v1
kind: Deployment
metadata:
    name: httpd
spec:
    replicas: 5
    selector:
        matchLabels:
            app: httpd
    template:
        metadata:
            labels:
                app: httpd
        spec:
            containers:
            - image: httpd:latest
              name: httpd
              ports:
              - containerPort: 80
                name: httpd

              volumeMounts:
              - name: fileserver
                mountPath: /usr/local/apache2/htdocs/
            volumes:
            - name: fileserver
              persistentVolumeClaim:
                claimName: fileserver
```

***
