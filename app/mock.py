def get(entity):
    data={
    "products":[{"entity":"product","id":"SKU-1001","parent":None,"children":{"categories":[{"code":"electronics"}],"images":[],"price":{"value":499,"currencyIso":"USD"},"stock":{"stockLevel":12}},"source":{"code":"SKU-1001","name":"Sample Headphones"}}],
    "categories":[{"entity":"catalog","id":"sampleProductCatalog","parent":None,"children":{},"source":{"id":"sampleProductCatalog","name":"Sample catalog"}}],
    "customers":[{"entity":"customer","id":"cust01","parent":None,"children":{"addresses":[{"id":"addr01","town":"Sample City"}]},"source":{"uid":"cust01","name":"Sample Customer"}}],
    "orders":[{"entity":"order","id":"ORD-1001","parent":{"customer_id":"cust01"},"children":{"entries":[{"entryNumber":0,"quantity":2,"product":{"code":"SKU-1001"}}]},"source":{"code":"ORD-1001","status":"COMPLETED"}}]}
    return data.get(entity,[])
