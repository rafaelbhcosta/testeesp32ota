# Para tudo funcionar como deve, nunca mexa nesse documento.
# Ele est谩 todo comentado para fins de compreens茫o.
# Caso mofique algo, n茫o nos responsabilizamos pelo n茫o funcionamento do protoc贸lo. 

import urequests
import uhashlib

class Duck:
    raw = "https://raw.githubusercontent.com"
    github = "https://github.com"

    def __init__(self, user, repo, url=None, branch="master", working_dir="app", files=["boot.py", "main.py"], headers={}):
        #Duck OTA.
        #Args:
        #user (str): usu谩rio do GitHub.
        #repo (str): reposit贸rio do GitHub para buscar.
        #branch (str): Ramo de reposit贸rio do GitHub. (mestre)
        #working_dir (str): Diret贸rio dentro do reposit贸rio GitHub onde est谩 o aplicativo micropython.
        #url (str): URL para o diret贸rio raiz.
        #files (list): Arquivos inclu铆dos na atualiza莽茫o OTA.
        #headers (list, opcional): Cabe莽alhos para urequests.
        
        self.base_url = "{}/{}/{}".format(self.raw, user, repo) if user else url.replace(self.github, self.raw)
        self.url = url if url is not None else "{}/{}/{}".format(self.base_url, branch, working_dir)
        self.headers = headers
        self.files = files

    def _check_hash(self, x, y):
        x_hash = uhashlib.sha1(x.encode())
        y_hash = uhashlib.sha1(y.encode())
        x = x_hash.digest()
        y = y_hash.digest()
        if str(x) == str(y):
            return True
        else:
            return False

    def _get_file(self, url):
        payload = urequests.get(url, headers=self.headers)
        code = payload.status_code
        if code == 200:
            return payload.text
        else:
            return None

    def _check_all(self):
        changes = []
        for file in self.files:
            latest_version = self._get_file(self.url + "/" + file)
            if latest_version is None:
                continue
        try:
            with open(file, "r") as local_file:
                local_version = local_file.read()
        except:
            local_version = ""
        if not self._check_hash(latest_version, local_version):
            changes.append(file)
        return changes

    def fetch(self):
        # Verifique se a vers茫o mais recente est谩 dispon铆vel.
        # Devolu莽玫es:
        # True - se for, False - se n茫o.
        if not self._check_all():
            return False
        else:
            return True

    def update(self):
        #Substitui todos os arquivos alterados por um mais recente.
        #Retorno:
        #True - se as altera莽玫es foram feitas False - se n茫o.
        changes = self._check_all()
        for file in changes:
            with open(file, "w") as local_file:
                local_file.write(self._get_file(self.url + "/" + file))
        if changes:
            return True
        else:
            return False
