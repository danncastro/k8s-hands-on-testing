# from locust import HttpUser, task, between

# class QuickstartUser(HttpUser):
#     wait_time = between(1, 2)

#     @task
#     def on_start(self):
#         self.client.get("/login.html", cookies = {"Cookie": "SESS=I+RaO9EaDjGURwmaMsyEgoa1ExKimED+gwg9BUMc8ZQCPfeie3yGAK7hQ5zL8UQlm5+u6xFdXESZ17qOF2yDkZSacM6vmm098+9dZ22EuJ1UHkda9vENbx4iRqlqBt/o51UAthUR/odbIqFACvKSCvtW31wkdNORyCPPeXkAnjNIXOUMU0FWAeY0C4YkqH6x0c7Ew0k/Ly2IBevVd+3Helnwm/S3OIQ3Ve4eK+TQVnWMkKq62EnPv9nUnkOmc7FmPKgTF/MCvAEmJ0jVfv/t4rYw8mkHsUkrAgyZ+WWMp9K6zxZt/IwpYgdRwoW0fu1MBd4OmU7CoKlhYWUUnpPXJAAAAN1kMkIta067Pjsnrks18wq36Iye6XnrtTBiaihvm6lkXGm9Z7ZT21viydKpWBIsndSQqP9evGBxXLD8sHithh0jvItk25gFAWwnMJx9UKBMLJHjt4sAYhKXyuoA13V5X+pJkX2BYnga4zkv68kMaF6b0Q0vNxCoiHg6E6SP+RwGFcBZT0hu+GbxKnOmRIM+NDrbTXxgZCKGu34PCr0ahYuwFh6rBFZQbigF1xxYatJtEifM/SSKoKjh87uesySJx6xyAV/d2ViS9N+sXbLTrW+/Y/v3UP+TQaRdXa1iQ6OJ/Jk8vaaTFsCws40ggFr0DYA6A5OeTxa/J0Dt5bCq4e4fdGBZOaRxKMo38YsrbDE8oMKP9wHfhFPbXEodivEFgcYWZXIdh7anz/M/0KFFNexM+0iUwQBewpZfSsWb2tKplTrE05+kIW90rdKq2gKWI3N8dE4vdj43oaylx8BSU97pNPic6v+pA4xkSpsbh/IhC3M5Wv4d8ssh/bBMMU03TVHz9QmJycR0CyZcSMsZs161K+RMkSMyAGmqkQFbaiCDwBPrJuew234KgKdK3vkU8DPBWX+7pMY/iPDkk/11y0L9Azk8L/2vBX5Hh/zwIqh6ThfjkB6WBUIawhleStbWDxlqK1j6qWf2NtrZS6YC/Gyf3nXFXTLJqG/FKCNmgOPm0gd60BN8O1e9nfNbKAfLcUc4KD/yUOFq7GhaEt/A9PFZe1ctlDHPbMEOkywPwLhSfsDI/3NNJhctbHGI6DkBhHDs/wI6BGAoiKYqNqlm4FiSn7WlIMfpzK59gxuFhcSs0EdtdnGiFNdRq68h5ESli0YJiZJU6ytZfgBb2+qgUi3IzJKdUi4xykkjg3Fm3Eu4aDca+CA0kdBIr7OOIy9s+nkznHYtQ83SaJaw9U684eBa2q2iAG9suioM2/6Bo6OkBHUh; JS_SESS=; _hjSessionUser_1681130=eyJpZCI6ImZhYzVmZGRkLTFkZWUtNWMzMS1hY2NjLTkxNGM2NjM3YTVhNSIsImNyZWF0ZWQiOjE3MjU1NTI5Nzk5MDEsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.920176982.1719952100.1330187818.1725552913.1725553238; _hjSessionUser_1810057=eyJpZCI6Ijc3MmJhYTVjLWFiYzgtNTFhMC05NjRjLWUxOGNmMGYwNjdlOCIsImNyZWF0ZWQiOjE3MjU1NTM0NTcxOTAsImV4aXN0aW5nIjp0cnVlfQ==; _conv_r=s%3Aconta.uol.com.br*m%3Areferral*t%3A*c%3A; profile-user=1; widget-notificacao=1; DNA=a7c9a071ce9644bd9b888d3ce9f7053b|191e1ebc057|true;"})

#     # @task
#     # def hello_world(self):
#     #     self.client.get("/hello")
#     #     self.client.get("/world")

#     # @task(3)
#     # def view_item(self):
#     #     for item_id in range(10):
#     #         self.client.get(f"/api/advertisement/personAuth?id={item_id}")

from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task
    def load_homepage(self):
        self.client.get("/")

    # @task
    # def load_about_page(self):
    #     self.client.get("/about")

class WebsiteUser(HttpUser):
    tasks = {UserBehavior: 1}  # 1 significa que esse conjunto de tarefas é o único que será executado
    wait_time = between(1, 5)  # espera entre 1 a 5 segundos entre as tarefas

# Se você quiser testar diferentes domínios, você pode configurar o host na linha de comando ou passar como variável de ambiente
# Por exemplo, execute o Locust assim:
# locust -f locustfile.py --host=http://seu_dominio.com
