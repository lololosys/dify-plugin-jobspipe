# JobsPipe — Dify Tool Plugin

**Every job posting, one API.**

This Dify tool plugin searches normalized live job postings through the [JobsPipe](https://jobspipe.dev) HTTPS API.

- **Source repository**: https://github.com/lololosys/dify-plugin-jobspipe
- **Product**: https://jobspipe.dev
- **API docs**: https://docs.jobspipe.dev/
- **OpenAPI**: https://jobspipe.dev/openapi.json
- **Contact**: dvir@jobspipe.dev

## What it does

The **Search Jobs** tool calls `POST https://api.jobspipe.dev/v1/jobs/search` with optional filters (title, skills, country, city, company, remote, employment type, posted age, minimum salary, limit, status) and returns the JSON response (`data` + `metadata`).

## Setup

1. Create an account and API key at [jobspipe.dev](https://jobspipe.dev) (keys look like `jp_live_…`).
2. Install this plugin from the Dify Marketplace (or load the `.difypkg` locally).
3. Authorize the provider with your JobsPipe API key.
4. Add **Search Jobs** to a workflow or agent and set filters as needed.

## Credentials

| Field | Required | Description |
| --- | --- | --- |
| JobsPipe API Key | Yes | Bearer token issued from the JobsPipe dashboard (`jobs:read` scope for search). |

## Network

Outbound HTTPS only to:

- `api.jobspipe.dev`

Declared in `manifest.yaml` under `network.domains`.

## Privacy

See [PRIVACY.md](./PRIVACY.md). The plugin forwards search queries to JobsPipe and does not store user data beyond that request/response.

## Development

```bash
# Package (requires Dify plugin CLI)
dify plugin package ./dify-plugin-jobspipe
```

Requires Python 3.12+ and `dify-plugin>=0.9.0`.

## License

MIT
