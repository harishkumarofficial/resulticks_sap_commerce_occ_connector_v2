# Resulticks – SAP Commerce OCC Read-only Connector

Configurable Python starter package for extracting SAP Commerce (SAP Hybris) data through OCC REST APIs and preparing parent/child JSON for Resulticks Aura ETL.

## Scope
- Read-only business APIs: GET and HEAD only. OAuth token acquisition uses POST to the token endpoint.
- OAuth client application grant (`client_credentials`) and authenticated-user grant (`password`) when enabled by the tenant.
- Dynamic tenant settings: URL, OCC prefix, base site, token URL, credentials, grant, fields, paging, language and currency.
- Mock fixtures and sample JSON for local validation.
- Output envelope preserves raw source fields under `source`, with relationships in `parent` and `children`.

## Windows quick start
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m pytest -q
python -m app.main extract products
python -m app.main extract customers
python -m app.main extract orders
```
Default is local-only: `IS_PRODUCTION_ENV=0`, `SAP_USE_MOCK_DATA=1`.

## Live tenant configuration
Edit `.env`; never commit secrets:
```dotenv
IS_PRODUCTION_ENV=0
SAP_USE_MOCK_DATA=0
SAP_ALLOW_NETWORK_IN_NON_PRODUCTION=1
SAP_BASE_URL=https://your-commerce-host
SAP_OCC_PREFIX=/occ/v2
SAP_BASE_SITE_ID=your-base-site
SAP_OAUTH_TOKEN_URL=https://your-commerce-host/authorizationserver/oauth/token
SAP_OAUTH_GRANT_TYPE=client_credentials
SAP_CLIENT_ID=...
SAP_CLIENT_SECRET=...
SAP_USERNAME=
SAP_PASSWORD=
SAP_PAGE_SIZE=100
SAP_MAX_PAGES=100
SAP_FIELDS=DEFAULT
SAP_USER_IDS=uid1,uid2
```
For production set `IS_PRODUCTION_ENV=1`. For approved non-production testing keep it 0 and set `SAP_ALLOW_NETWORK_IN_NON_PRODUCTION=1`. `SAP_USE_MOCK_DATA=1` always avoids SAP network calls.

### Authentication
1. `client_credentials`: client ID/secret identify the integration application. Use only where the OAuth client has permission to read the relevant OCC resources.
2. `password`: client ID/secret plus a tenant-approved service username/password. This grant may be disabled by the deployment. Do not assume it is available.

The token is sent as `Authorization: Bearer ...`. The grants may have different permissions. Changing credentials alone is not sufficient to guarantee compatibility: base URL, base site, version, scopes/roles, OCC extensions, catalog configuration and custom fields can vary.

## Commands
```powershell
python -m app.main extract products --limit 100
python -m app.main extract categories
python -m app.main extract customers
python -m app.main extract orders
python -m app.main extract all
```
JSON files are written to `output/`.

## Critical data coverage caveat
Standard OCC customer profile and address APIs are user-scoped (`/users/{userId}`). The standard contract reviewed does not establish a generic tenant-wide list-all-customers endpoint. Supply an approved list of user IDs using `SAP_USER_IDS`, or obtain a tenant-approved Integration API/OData Integration Object, custom OCC endpoint, or export for full customer population. Do not guess/enumerate IDs. Standard order history is also user-scoped.

## Aura parent/child shape
- Product parent → categories, images, price, stock children/attributes.
- Customer parent → addresses.
- Order parent → customer reference; entries/order lines as children; each line references product code.
- Raw source payload remains under `source` until Aura mapping is finalized.

## Before rollout
Verify tenant Swagger/OpenAPI, version, OAuth grant, permissions, baseSiteId, exact response fields, pagination, rate limits, full-customer source, delta strategy, deletion handling and reconciliation. Product express-update may be available but its feed/cronjob semantics must be tested. This is a reusable starter, not a promise that every SAP tenant is identical.
