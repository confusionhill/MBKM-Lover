import requests
import json

class Config:
    headers = {}
    def __init__(self, email, password, login_url, sptjm_url, berkas_url, kegiatan_url):
        self.email = email
        self.password = password
        self.login_url = login_url
        self.sptjm_url = sptjm_url
        self.berkas_url = berkas_url
        self.kegiatan_url = kegiatan_url
    

def initilizeConf() -> Config :
    with open('config.json') as json_file:
        data = json.load(json_file)
        return Config(data["email"], data["password"], data["login-url"], data["sptjm-url"], data["berkas-url"], data['kegiatan-url'])

def login(config: Config):
    response = requests.post(config.login_url, json={"email": config.email,"password": config.password})
    if response.status_code == 200:
        _locjson = response.json()
        config.headers = {
            "Authorization": f"Bearer {_locjson['data']['access_token']}"
        }
    else:
        print(response.json())

def get_berkas(config: Config):
    response = requests.get(config.sptjm_url, headers=config.headers)
    if response.status_code == 200:
        _locjson = response.json()
        for berkas in _locjson['data']:
            get_status(config, berkas['id'], berkas['name'])
    else:
        print(response.json())

def get_status(config: Config,berkas_id, type):
    url = f"{config.berkas_url}/{berkas_id}/users"
    response = requests.get(url, headers=config.headers)
    locjson = response.json()
    try:
        print(type, "Status :",locjson["data"]["status"])
    except:
        pass

def get_kegiatan(config: Config):
    response = requests.get(config.kegiatan_url, headers=config.headers)
    if response.status_code == 200:
        locjson = response.json()
        for kegiatan in locjson['data']:
            get_kegiatan_status(kegiatan)

def get_kegiatan_status(kegiatan):
    print(kegiatan['nama_kegiatan'],"status :",kegiatan['status'])

def main():
    print("Loading configuration file....")
    conf = initilizeConf()
    login(config=conf)
    print("\n\nGetting berkas status...")
    get_berkas(config=conf)
    print("\n\nGetting kegiatan status....")
    get_kegiatan(conf)

if __name__ == '__main__':
    main()