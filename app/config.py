import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()
def flag(k, d=False): return os.getenv(k, str(int(d))).lower() in ("1","true","yes")
@dataclass
class Settings:
    production: bool = flag("IS_PRODUCTION_ENV")
    mock: bool = flag("SAP_USE_MOCK_DATA", True)
    allow_nonprod: bool = flag("SAP_ALLOW_NETWORK_IN_NON_PRODUCTION")
    base_url: str = os.getenv("SAP_BASE_URL","").rstrip("/")
    prefix: str = os.getenv("SAP_OCC_PREFIX","/occ/v2").strip("/")
    site: str = os.getenv("SAP_BASE_SITE_ID","")
    token_url: str = os.getenv("SAP_OAUTH_TOKEN_URL","")
    grant: str = os.getenv("SAP_OAUTH_GRANT_TYPE","client_credentials")
    client_id: str = os.getenv("SAP_CLIENT_ID","")
    client_secret: str = os.getenv("SAP_CLIENT_SECRET","")
    username: str = os.getenv("SAP_USERNAME","")
    password: str = os.getenv("SAP_PASSWORD","")
    page_size: int = int(os.getenv("SAP_PAGE_SIZE","100"))
    max_pages: int = int(os.getenv("SAP_MAX_PAGES","100"))
    fields: str = os.getenv("SAP_FIELDS","DEFAULT")
    timeout: int = int(os.getenv("SAP_TIMEOUT_SECONDS","30"))
    verify: bool = flag("SAP_VERIFY_TLS", True)
    output: str = os.getenv("SAP_OUTPUT_DIR","output")
    user_ids: list = None
    def __post_init__(self):
        self.user_ids = [x.strip() for x in os.getenv("SAP_USER_IDS","").split(",") if x.strip()]
    def validate(self):
        if self.mock: return
        if not (self.production or self.allow_nonprod): raise RuntimeError("Network blocked; explicitly enable production or approved non-production networking.")
        if not all([self.base_url,self.site,self.token_url,self.client_id,self.client_secret]): raise RuntimeError("Missing SAP URL/site/token/client configuration.")
        if self.grant not in ("client_credentials","password"): raise RuntimeError("Unsupported OAuth grant.")
        if self.grant == "password" and not (self.username and self.password): raise RuntimeError("Password grant requires SAP_USERNAME and SAP_PASSWORD.")
