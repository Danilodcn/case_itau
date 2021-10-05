import os
import requests
from app.users import Users

n = int(os.getenv("USER_NUMBER", 300))
n = 1000
# import ipdb; ipdb.set_trace()
print(f"Buscando {n} nomes aleatórios usando uma API")
users = Users(n)
users.users.drop()
print("Salvando os nomes no banco MongoDB")
users.save()

HOST = os.getenv("FLASK_HOST")
PORT = 3000
URL_LOGIN = os.getenv("FLASK_URL_LOGIN")

url = "http://{}:{}".format(HOST, PORT) + URL_LOGIN
print("Iniciando o processo de login")
users.login(url, n)

# import ipdb; ipdb.set_trace()



# payload = {'key1': 'value1', 'key2': 'value2'}
# x = requests.post(url + URL_LOGIN, data=payload)
# import ipdb; ipdb.set_trace()

# import ipdb; ipdb.set_trace()
# v = x.users.find()
# m = 0
# while True:
#     try:
#         f = next(v)
#         if m % 100 == 0:
#             print(f)
#         # import ipdb; ipdb.set_trace()
#     except StopIteration:
#         import ipdb; ipdb.set_trace()
#         break
#     except:
#         import ipdb; ipdb.set_trace()