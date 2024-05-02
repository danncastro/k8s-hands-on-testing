# Statefullset

###

Podem ser usados quando estados devem ser persistidos.&#x20;

1. Usam **`PersistentVolume`** e **`PersistentVolumeClaim`** para persistência de dados.
2. Garante unicidade de Pods durante reinícios e atualizações
3. Clusters possuem StorageClasses "default" e podem ser usados automaticamente se não definirmos qual será utilizado
