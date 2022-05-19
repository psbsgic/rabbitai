import logging
from typing import Any, Dict, Optional

from flask import Request
from marshmallow import ValidationError

from rabbitai import cache
from rabbitai.charts.commands.exceptions import (
    ChartDataCacheLoadError,
    ChartDataQueryFailedError,
)
from rabbitai.charts.schemas import ChartDataQueryContextSchema
from rabbitai.commands.base import BaseCommand
from rabbitai.common.query_context import QueryContext
from rabbitai.exceptions import CacheLoadError
from rabbitai.extensions import async_query_manager
from rabbitai.tasks.async_queries import load_chart_data_into_cache

logger = logging.getLogger(__name__)


class ChartDataCommand(BaseCommand):
    """图表数据命令。"""

    def __init__(self) -> None:
        self._form_data: Dict[str, Any]
        self._query_context: QueryContext
        self._async_channel_id: str

    def run(self, **kwargs: Any) -> Dict[str, Any]:
        # caching is handled in query_context.get_df_payload(also evals `force` property)
        cache_query_context = kwargs.get("cache", False)
        force_cached = kwargs.get("force_cached", False)
        try:
            payload = self._query_context.get_payload(
                cache_query_context=cache_query_context, force_cached=force_cached
            )
        except CacheLoadError as exc:
            raise ChartDataCacheLoadError(exc.message)

        for query in payload["queries"]:
            if query.get("error"):
                raise ChartDataQueryFailedError(f"Error: {query['error']}")

        return_value = {
            "query_context": self._query_context,
            "queries": payload["queries"],
        }
        if cache_query_context:
            return_value.update(cache_key=payload["cache_key"])

        return return_value

    def run_async(self, user_id: Optional[str]) -> Dict[str, Any]:
        job_metadata = async_query_manager.init_job(self._async_channel_id, user_id)
        load_chart_data_into_cache.delay(job_metadata, self._form_data)

        return job_metadata

    def set_query_context(self, form_data: Dict[str, Any]) -> QueryContext:
        self._form_data = form_data
        try:
            self._query_context = ChartDataQueryContextSchema().load(self._form_data)
        except KeyError:
            raise ValidationError("Request is incorrect")
        except ValidationError as error:
            raise error

        return self._query_context

    def validate(self) -> None:
        self._query_context.raise_for_access()

    def validate_async_request(self, request: Request) -> None:
        jwt_data = async_query_manager.parse_jwt_from_request(request)
        self._async_channel_id = jwt_data["channel"]

    def load_query_context_from_cache(self, cache_key: str) -> Dict[str, Any]:
        cache_value = cache.get(cache_key)
        if not cache_value:
            raise ChartDataCacheLoadError("Cached data not found")

        return cache_value["data"]
