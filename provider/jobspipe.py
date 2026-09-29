from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.search_jobs import SearchJobsTool


class JobspipeProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            for _ in SearchJobsTool.from_credentials(credentials, user_id="").invoke(
                tool_parameters={
                    "job_title_or": "software engineer",
                    "limit": 1,
                }
            ):
                pass
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e)) from e
