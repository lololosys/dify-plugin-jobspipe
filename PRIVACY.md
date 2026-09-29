# Privacy Policy — JobsPipe Dify Plugin

This plugin does **not** store, log, or retain user data on its own beyond what is required to forward a search request to JobsPipe and return the response to Dify.

## What is sent

When you run **Search Jobs**, the plugin sends:

- Your JobsPipe API key (as an `Authorization: Bearer` header)
- The search filters you (or the agent) provide — titles, skills, locations, company names, remote flag, employment type, salary floor, limit, and status

to the fixed HTTPS endpoint `https://api.jobspipe.dev/v1/jobs/search`.

## What is not collected by the plugin

- No local database, file cache, or analytics store
- No third-party destinations other than JobsPipe
- No sale or sharing of data by the plugin itself

## JobsPipe’s handling of data

JobsPipe processes API requests under its own terms and privacy practices. See:

- https://jobspipe.dev
- https://docs.jobspipe.dev/

Contact: dvir@jobspipe.dev
