# Nexus private Vercel demo

This is an isolated source snapshot. The original nexus-b2a project is unchanged.
The snapshot uses temporary SQLite storage, seeded test credits and deterministic
extraction. Data can disappear or differ between Vercel instances. Do not enter
real invoices or use this deployment as a persistent shared marketplace.

The snapshot also adds the missing `datetime` and `timezone` imports to
`app/services/accounting_service.py`; purchases crashed without those imports.

The FastAPI entrypoint is `preview:app`. The generated `preview_config.py`
contains only a SHA-256 hash of a random preview password. The password itself
is stored separately outside the deployment package. An optional
`NEXUS_PREVIEW_PASSWORD` environment variable (at least 20 characters) overrides
the generated hash. Sign in with username `nexus` through the browser prompt.
The secure access cookie allows the console to use its agent bearer token.
Operator mutations are deliberately unavailable from the console in this demo.

Deploy from this folder:

```powershell
npx vercel@65.15.0 login
npx vercel@65.15.0 link
npx vercel@65.15.0 project inspect --non-interactive
npx vercel@65.15.0 deploy
```

Choose the intended personal account/team and a Nexus preview project during
linking. Enter the password in the Vercel CLI prompt; never commit it.
Keep Vercel Deployment Protection enabled. This package does not configure a
production release or automatic synchronization with the working source tree.

## Current verification and blocker

19 original tests passed after adding the missing datetime imports in this snapshot.
Anonymous access rejection, bad-password rejection, console access, secure cookie,
bearer-authenticated deterministic purchase, settlement and result retrieval pass.
No remote deployment is confirmed. The CLI requires a writable authentication
configuration; the host AppData location is read-only in this workspace.
A separate local Vercel session directory is used for the login handoff.
