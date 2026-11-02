# Aura parent/child JSON shape

```json
{
  "entity": "order",
  "id": "ORD-1001",
  "parent": {"customer_id": "cust01"},
  "children": {"entries": [{"entryNumber": 0, "quantity": 2, "product": {"code": "SKU-1001"}}]},
  "extracted_at": "UTC timestamp",
  "source": {"code": "ORD-1001", "status": "COMPLETED"}
}
```

Stable keys to confirm: product `code`; customer `uid` or tenant customer key; order `code`; order line order code + entry number; address source ID. Current package nests children. Aura can split arrays into child datasets during mapping.
