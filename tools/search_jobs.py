from typing import Any, Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
import requests

JOBSPIPE_SEARCH_URL = "https://api.jobspipe.dev/v1/jobs/search"


def _split_csv(value: str | None) -> list[str] | None:
    if not value:
        return None
    items = [part.strip() for part in str(value).split(",") if part.strip()]
    return items or None


def search_jobs(api_key: str, body: dict[str, Any]) -> dict[str, Any]:
    """POST a search to JobsPipe and return the decoded JSON body.

    Raises requests.exceptions.HTTPError on a non-2xx status and
    requests.exceptions.RequestException on network failures, so callers
    (the tool and the provider's credential check) decide how to surface them.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.post(
        JOBSPIPE_SEARCH_URL,
        json=body,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def describe_http_error(exc: requests.exceptions.HTTPError) -> str:
    response = exc.response
    if response is None:
        return "JobsPipe API error (?): no response"
    try:
        detail = response.json().get("error", response.text[:300])
    except Exception:
        detail = (response.text or "")[:300]
    return f"JobsPipe API error ({response.status_code}): {detail}"


class SearchJobsTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials.get("api_key")
        if not api_key:
            yield self.create_text_message("JobsPipe API key is required.")
            return

        body: dict[str, Any] = {}
        mapping = {
            "job_title_or": _split_csv(tool_parameters.get("job_title_or")),
            "skills_or": _split_csv(tool_parameters.get("skills_or")),
            "job_country_code_or": _split_csv(
                tool_parameters.get("job_country_code_or")
            ),
            "city_or": _split_csv(tool_parameters.get("city_or")),
            "company_name_or": _split_csv(tool_parameters.get("company_name_or")),
            "employment_type_or": _split_csv(
                tool_parameters.get("employment_type_or")
            ),
        }
        for key, value in mapping.items():
            if value:
                body[key] = value

        remote = tool_parameters.get("remote")
        if remote is not None:
            body["remote"] = bool(remote)

        for int_key in ("posted_at_max_age_days", "min_salary_usd", "limit"):
            raw = tool_parameters.get(int_key)
            if raw is not None and raw != "":
                try:
                    body[int_key] = int(raw)
                except (TypeError, ValueError):
                    yield self.create_text_message(
                        f"Invalid integer for {int_key}: {raw}"
                    )
                    return

        status = tool_parameters.get("status") or "active"
        if status in ("active", "closed", "any"):
            body["status"] = status

        if "limit" not in body:
            body["limit"] = 10

        try:
            payload = search_jobs(api_key, body)
        except requests.exceptions.HTTPError as exc:
            yield self.create_text_message(describe_http_error(exc))
            return
        except requests.exceptions.RequestException as exc:
            yield self.create_text_message(
                f"An error occurred while calling JobsPipe: {exc}."
            )
            return

        jobs = payload.get("data") or []
        summary = f"Found {len(jobs)} job posting(s)."
        yield self.create_text_message(summary)
        yield self.create_json_message(payload)
