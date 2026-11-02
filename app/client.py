import requests
from urllib.parse import urljoin
class OCC:
    def __init__(self,s): self.s=s; self.token=None
    def auth(self):
        if self.token: return self.token
        s=self.s; data={"grant_type":s.grant}
        if s.grant=="password": data.update(username=s.username,password=s.password)
        r=requests.post(s.token_url,data=data,auth=(s.client_id,s.client_secret),timeout=s.timeout,verify=s.verify); r.raise_for_status()
        self.token=r.json().get("access_token")
        if not self.token: raise RuntimeError("OAuth response missing access_token")
        return self.token
    def path(self,suffix): return f"/{self.s.prefix}/{self.s.site}/{suffix.lstrip('/')}"
    def call(self,method,path,params=None):
        if method.upper() not in ("GET","HEAD"): raise ValueError("Read-only connector: GET/HEAD only")
        self.s.validate()
        url=urljoin(self.s.base_url+"/",path.lstrip("/"))
        r=requests.request(method.upper(),url,params=params,headers={"Authorization":"Bearer "+self.auth(),"Accept":"application/json"},timeout=self.s.timeout,verify=self.s.verify)
        r.raise_for_status()
        return r if method.upper()=="HEAD" else r.json()
