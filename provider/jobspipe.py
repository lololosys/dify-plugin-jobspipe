from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
import requests

from tools.search_jobs import describe_http_error, search_jobs


class JobspipeProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = credentials.get("api_key")
        if not api_key:
            raise ToolProviderCredentialValidationError("JobsPipe API key is required.")
        try:
            search_jobs(api_key, {"job_title_or": ["software engineer"], "limit": 1})
        except requests.exceptions.HTTPError as exc:
            raise ToolProviderCredentialValidationError(describe_http_error(exc)) from exc
        except requests.exceptions.RequestException as exc:
            raise ToolProviderCredentialValidationError(
                f"Could not reach JobsPipe: {exc}"
            ) from exc
