# Major OCC read endpoints

Paths are relative to `/occ/v2`; replace `{baseSiteId}` with the configured site. Verify every path in the tenant's Swagger/OpenAPI before use.

| Data | Method | Endpoint | Result / notes |
|---|---|---|---|
| Product search/list | GET | `/{baseSiteId}/products/search` | Paginated product list; `currentPage`, `pageSize`, `fields` |
| Product count | HEAD | `/{baseSiteId}/products/search` | `x-total-count` when implemented |
| Product detail | GET | `/{baseSiteId}/products/{productCode}` | Individual product |
| Product incremental feed | GET | `/{baseSiteId}/products/expressupdate` | Timestamp feed in documented versions; verify cronjob/queue behavior |
| Customer profile | GET | `/{baseSiteId}/users/{userId}` | Individual user only |
| Customer addresses | GET | `/{baseSiteId}/users/{userId}/addresses` | Child addresses |
| Customer order history | GET | `/{baseSiteId}/users/{userId}/orders` | Paginated; user-scoped |
| Order count | HEAD | `/{baseSiteId}/users/{userId}/orders` | `x-total-count` where supported |
| Order detail | GET | `/{baseSiteId}/users/{userId}/orders/{code}` | Order includes entries/order lines |
| Cart detail | GET | `/{baseSiteId}/users/{userId}/carts/{cartId}` | Optional; verify tenant |
| Product stock | GET | `/{baseSiteId}/products/{productCode}/stock` | Optional; verify stock extension |
| Promotions | GET | `/{baseSiteId}/promotions` | Optional; verify tenant exposure |
| Catalog metadata | GET | `/{baseSiteId}/catalogs` | Catalog metadata; category-tree API varies by version/extensions |

## Resulticks relationship model
- Product parent → images, categories, price, stock.
- Customer parent → addresses.
- Order parent → `customer_id`; child `entries`; each entry references product code.
- Keep raw source JSON to avoid losing fields before Aura mappings are agreed.

## Critical limitation
The standard OCC contract reviewed does not establish a generic list-all-customers endpoint. Customer and order endpoints above are scoped to a supplied `userId`. Full customer population needs an approved Integration API/OData Integration Object, custom OCC endpoint or SAP-provided export. Never enumerate guessed IDs.

## Delta
Product express-update may be useful but confirm tenant setup and recovery semantics. Do not assume generic modified-since support for customer/order list APIs. Agree watermark, replay and deletion strategy with SAP team.
