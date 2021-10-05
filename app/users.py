import requests
import os
from functools import partial
from multiprocessing.pool import ThreadPool
from pymongo import MongoClient
from random import choices
from typing import List


# MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
# MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PORT_OUTPUT = int(os.getenv("MONGO_PORT_OUTPUT"))

def names_for_External_EPI(n):
    """
        get random full names from API
        link: http://www.wjr.eti.br/nameGenerator/index.php?q=60&o=plain 
    """
    N = int(n * 1.2)
    url = f"http://www.wjr.eti.br/nameGenerator/index.php?q={N}&o=json"

    headers = {
        'content-type': 'application/json',
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
        }
    r = requests.get(url, headers=headers)
    # import ipdb; ipdb.set_trace()
    res = set(r.json())
    n_res = len(res)
    if n_res < n:
        res_ = names_for_External_EPI(n - n_res)
        res = res.union(res_)
        n_res = len(res)

    elif n_res > n:
        res = list(res)[0:n]

    return list(res)
    


class Users:
    def __init__(self, number:int):
        number = int(number)
        self.names = names_for_External_EPI(number)
        self.number = len(self.names)
        self.url_login = os.getenv("URL_LOGIN")

        # url = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@127.0.0.1:{MONGO_PORT_OUTPUT}/"
        url = f"mongodb://127.0.0.1:{MONGO_PORT_OUTPUT}/"
        url = "mongodb://127.0.0.1:27017/"

        self.mongodb = MongoClient(url)
        self.db = self.mongodb["Itau"]
        self.users = self.db["users"]
        # self.users.drop()
        # import ipdb; ipdb.set_trace()


    
    def login(self, url: str, number:int):
        n = 10
        p = ThreadPool(n)
        names = choices(self.names, k=number)
        _login = partial(self._login, url=url)
        # import ipdb; ipdb.set_trace()
        print(f"Usando {n} threads para fazer login")
        res = p.map(_login, names)
        print(f"Finalizado ...")
        # import ipdb; ipdb.set_trace()
    

        # for name in names:
        #     r = self._login(url, name)
        #     if "error" in r["error"]:
        #         import ipdb; ipdb.set_trace()
            

    def _login(self, name, url):
        value = self.users.find_one({"name": name})
        r = requests.post(url, data=value)
        try:
            _json = r.json()
        except:
            _json = {"error": "converting error"}
        return _json



    def save(self):
        hashs = [hash(name) for name in self.names]
        it = zip(range(self.number), self.names, hashs)
        data = [{"_id": i,"name": name, "password": _hash} for i, name, _hash in it]
        # import ipdb; ipdb.set_trace()
        self.users.insert_many(data)


