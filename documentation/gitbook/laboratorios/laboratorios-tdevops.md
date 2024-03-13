---
description: Curso de DevOps Pro Fabricio Veronez
---

# Laboratórios TDevOps

***

### **APP-6-KUBERNETES-MYSQL**

```bash
```

```yml
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
