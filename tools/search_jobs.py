from typing import Any, Generator

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

JOBSPIPE_SEARCH_URL = "https://api.jobspipe.dev/v1/jobs/search"


def _split_csv(value: str | None) -> list[str] | None:
    if not value:
        return None
    items = [part.strip() for part in str(value).split(",") if part.strip()]
    return items or None


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

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.post(
                JOBSPIPE_SEARCH_URL,
                json=body,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.exceptions.HTTPError as exc:
            detail = ""
            if exc.response is not None:
                try:
                    detail = exc.response.json().get("error", exc.response.text[:300])
                except Exception:
                    detail = (exc.response.text or "")[:300]
            yield self.create_text_message(
                f"JobsPipe API error ({exc.response.status_code if exc.response else '?'}): {detail}"
            )
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
