# Exercício Opcional

Crie um Pod através de um arquivo manifesto YAML com um container apache, contendo uma _label_ chamada _`app-type`_, com o valor _web_ (exemplo: _`app-type: web`_).&#x20;

Isso servirá para que outras aplicações identifiquem seu sistema por esta _label_ e saibam que se trata de uma aplicação web.&#x20;

Por fim, delete o Pod.

**Orientações adicionais:**

1 - Adicione a label como no enunciado: _`app-type: web`_

2 - Use a imagem do apache: _`image: httpd`_

3 - Não esqueça que **não pode usar Tab**, os campos devem estar alinhados como mostrado na aula e o _**case sensitive**_ (maiúsculas ou minúsculas) deve ser respeitado.

4 - Limpe o cluster, ou seja, delete sua Pod criada.



[https://medium.com/geekculture/a-step-by-step-demo-on-kubernetes-cluster-creation-f183823c0411](https://medium.com/geekculture/a-step-by-step-demo-on-kubernetes-cluster-creation-f183823c0411)
