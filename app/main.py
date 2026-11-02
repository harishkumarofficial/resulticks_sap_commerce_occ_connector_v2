import argparse,json
from pathlib import Path
from datetime import datetime,timezone
from app.config import Settings
from app.client import OCC
from app.mock import get
def pages(fetch,s):
    for p in range(s.max_pages):
        obj=fetch(p); yield obj
        pg=obj.get("pagination") or obj.get("deprecatedPagination") or {}
        if pg.get("totalPages") is not None and pg.get("currentPage",p)+1>=pg["totalPages"]: break
        arr=next((v for v in obj.values() if isinstance(v,list)),[])
        if len(arr)<s.page_size: break

def envelope(entity,key,src,parent=None,children=None):
    return {"entity":entity,"id":str(key) if key is not None else None,"parent":parent,"children":children or {},"extracted_at":datetime.now(timezone.utc).isoformat(),"source":src}

def run(entity,limit=None):
    s=Settings()
    if s.mock: records=get(entity)
    else:
        c=OCC(s); records=[]
        if entity in ("products","all"):
            for obj in pages(lambda p:c.call("GET",c.path("products/search"),{"currentPage":p,"pageSize":s.page_size,"fields":s.fields}),s):
                for x in obj.get("products",[]): records.append(envelope("product",x.get("code"),x,children={k:x.get(k) for k in ("categories","images","price","stock") if k in x}))
                if limit and len(records)>=limit: break
            if entity=="products": records=records[:limit] if limit else records
            
        if entity in ("categories","all"):
            obj=c.call("GET",c.path("catalogs"))
            records += [envelope("catalog",x.get("id") or x.get("catalogId"),x) for x in obj.get("catalogs",[])]

        if entity in ("customers","orders","all"):
            if not s.user_ids: raise RuntimeError("Customer/order OCC endpoints are user-scoped. Set approved SAP_USER_IDS or configure a tenant bulk export/API.")
            for uid in s.user_ids:
                if entity in ("customers","all"):
                    u=c.call("GET",c.path(f"users/{uid}"),{"fields":s.fields})
                    a=c.call("GET",c.path(f"users/{uid}/addresses"),{"fields":s.fields})
                    records.append(envelope("customer",uid,u,children={"addresses":a.get("addresses",[])}))
                if entity in ("orders","all"):
                    path=c.path(f"users/{uid}/orders")
                    for obj in pages(lambda p:c.call("GET",path,{"currentPage":p,"pageSize":s.page_size,"fields":s.fields}),s):
                        for order in obj.get("orders",[]):
                            code=order.get("code")
                            detail=c.call("GET",c.path(f"users/{uid}/orders/{code}"),{"fields":s.fields}) if code else order
                            records.append(envelope("order",code,detail,parent={"customer_id":uid},children={"entries":detail.get("entries",[])}))
        if entity=="all" and limit: records=records[:limit]
    out=Path(s.output); out.mkdir(exist_ok=True,parents=True); dest=out/(entity+".json")
    dest.write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"{len(records)} records -> {dest.resolve()}")

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True); e=sub.add_parser("extract")
    e.add_argument("entity",choices=["products","categories","customers","orders","all"]); e.add_argument("--limit",type=int)
    a=p.parse_args(); run(a.entity,a.limit)

if __name__=="__main__": main()
