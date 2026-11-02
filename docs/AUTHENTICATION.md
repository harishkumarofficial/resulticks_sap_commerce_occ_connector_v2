# OAuth modes

**Client application token (`client_credentials`)**: client ID/secret identify the integration app. It can call only resources permitted by the tenant's OAuth client configuration.

**Authenticated user token (`password`)**: client ID/secret plus an approved username/password. Only works if enabled by the deployment. It is not guaranteed to be available for every Commerce Cloud tenant.

The connector sends the resulting bearer token in the Authorization header. Token URL is configurable; SAP commonly documents `/authorizationserver/oauth/token`. Confirm whether the tenant expects HTTP Basic client authentication or a different client credential placement. Never log tokens/passwords; use least privilege and TLS.
