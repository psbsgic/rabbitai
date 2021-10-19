# -*- coding: utf-8 -*-

import json
import logging
import uuid
from typing import Any, Dict, List, Optional, Tuple

import jwt
import redis
from flask import Flask, g, request, Request, Response, session

logger = logging.getLogger(__name__)


class AsyncQueryTokenException(Exception):
    pass


class AsyncQueryJobException(Exception):
    pass


def build_job_metadata(
    channel_id: str, job_id: str, user_id: Optional[str], **kwargs: Any
) -> Dict[str, Any]:
    """
    构建任务元数据，Json格式字典。

    :param channel_id: 通道标识。
    :param job_id: 任务标识。
    :param user_id: 用户标识。
    :param kwargs: 关键字参数。
    :return:
    """
    return {
        "channel_id": channel_id,
        "job_id": job_id,
        "user_id": int(user_id) if user_id else None,
        "status": kwargs.get("status"),
        "errors": kwargs.get("errors", []),
        "result_url": kwargs.get("result_url"),
    }


def parse_event(event_data: Tuple[str, Dict[str, Any]]) -> Dict[str, Any]:
    event_id = event_data[0]
    event_payload = event_data[1]["data"]
    return {"id": event_id, **json.loads(event_payload)}


def increment_id(redis_id: str) -> str:
    # redis stream IDs are in this format: '1607477697866-0'
    try:
        prefix, last = redis_id[:-1], int(redis_id[-1])
        return prefix + str(last + 1)
    except Exception:  # pylint: disable=broad-except
        return redis_id


class AsyncQueryManager:
    """异步查询管理器。"""

    MAX_EVENT_COUNT = 100
    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_ERROR = "error"
    STATUS_DONE = "done"

    def __init__(self) -> None:
        super().__init__()
        self._redis: redis.Redis
        self._stream_prefix: str = ""
        self._stream_limit: Optional[int]
        self._stream_limit_firehose: Optional[int]
        self._jwt_cookie_name: str
        self._jwt_cookie_secure: bool = False
        self._jwt_cookie_domain: Optional[str]
        self._jwt_secret: str

    def init_app(self, app: Flask) -> None:
        """
        依据指定应用的配置对象初始化该实例。

        :param app: Flask应用实例。
        :return:
        """

        config = app.config
        if (
            config["CACHE_CONFIG"]["CACHE_TYPE"] == "null"
            or config["DATA_CACHE_CONFIG"]["CACHE_TYPE"] == "null"
        ):
            raise Exception(
                """
                必须缓存后端 (CACHE_CONFIG, DATA_CACHE_CONFIG)，为了启用异步查询还要非空。
                """
            )

        if len(config["GLOBAL_ASYNC_QUERIES_JWT_SECRET"]) < 32:
            raise AsyncQueryTokenException("请提供 JWT 秘钥至少 32 字节")

        self._redis = redis.Redis(  # type: ignore
            **config["GLOBAL_ASYNC_QUERIES_REDIS_CONFIG"], decode_responses=True
        )
        self._stream_prefix = config["GLOBAL_ASYNC_QUERIES_REDIS_STREAM_PREFIX"]
        self._stream_limit = config["GLOBAL_ASYNC_QUERIES_REDIS_STREAM_LIMIT"]
        self._stream_limit_firehose = config[
            "GLOBAL_ASYNC_QUERIES_REDIS_STREAM_LIMIT_FIREHOSE"
        ]
        self._jwt_cookie_name = config["GLOBAL_ASYNC_QUERIES_JWT_COOKIE_NAME"]
        self._jwt_cookie_secure = config["GLOBAL_ASYNC_QUERIES_JWT_COOKIE_SECURE"]
        self._jwt_cookie_domain = config["GLOBAL_ASYNC_QUERIES_JWT_COOKIE_DOMAIN"]
        self._jwt_secret = config["GLOBAL_ASYNC_QUERIES_JWT_SECRET"]

        @app.after_request
        def validate_session(  # pylint: disable=unused-variable
            response: Response,
        ) -> Response:
            """
            验证会话，每次请求后要调用的方法，重置用户令牌。

            :param response: 响应对象。
            :return:
            """
            user_id = None

            try:
                user_id = g.user.get_id()
                user_id = int(user_id)
            except Exception:  # pylint: disable=broad-except
                pass

            reset_token = (
                not request.cookies.get(self._jwt_cookie_name)
                or "async_channel_id" not in session
                or "async_user_id" not in session
                or user_id != session["async_user_id"]
            )

            if reset_token:
                async_channel_id = str(uuid.uuid4())
                session["async_channel_id"] = async_channel_id
                session["async_user_id"] = user_id

                sub = str(user_id) if user_id else None
                token = self.generate_jwt({"channel": async_channel_id, "sub": sub})

                response.set_cookie(
                    self._jwt_cookie_name,
                    value=token,
                    httponly=True,
                    secure=self._jwt_cookie_secure,
                    domain=self._jwt_cookie_domain,
                )

            return response

    def generate_jwt(self, data: Dict[str, Any]) -> str:
        """
        生成JWT。

        :param data:
        :return:
        """
        encoded_jwt = jwt.encode(data, self._jwt_secret, algorithm="HS256")
        return encoded_jwt.decode("utf-8")

    def parse_jwt(self, token: str) -> Dict[str, Any]:
        data = jwt.decode(token, self._jwt_secret, algorithms=["HS256"])
        return data

    def parse_jwt_from_request(self, req: Request) -> Dict[str, Any]:
        token = req.cookies.get(self._jwt_cookie_name)
        if not token:
            raise AsyncQueryTokenException("Token not preset")

        try:
            return self.parse_jwt(token)
        except Exception as exc:
            logger.warning(exc)
            raise AsyncQueryTokenException("Failed to parse token")

    def init_job(self, channel_id: str, user_id: Optional[str]) -> Dict[str, Any]:
        """
        初始化一个任务。

        :param channel_id:
        :param user_id:
        :return:
        """
        job_id = str(uuid.uuid4())
        return build_job_metadata(
            channel_id, job_id, user_id, status=self.STATUS_PENDING
        )

    def read_events(
        self, channel: str, last_id: Optional[str]
    ) -> List[Optional[Dict[str, Any]]]:
        stream_name = f"{self._stream_prefix}{channel}"
        start_id = increment_id(last_id) if last_id else "-"
        results = self._redis.xrange(  # type: ignore
            stream_name, start_id, "+", self.MAX_EVENT_COUNT
        )
        return [] if not results else list(map(parse_event, results))

    def update_job(
        self, job_metadata: Dict[str, Any], status: str, **kwargs: Any
    ) -> None:
        """
        更新任务。添加到 Redis。

        :param job_metadata:
        :param status:
        :param kwargs:
        :return:
        """

        if "channel_id" not in job_metadata:
            raise AsyncQueryJobException("No channel ID specified")

        if "job_id" not in job_metadata:
            raise AsyncQueryJobException("No job ID specified")

        updates = {"status": status, **kwargs}
        event_data = {"data": json.dumps({**job_metadata, **updates})}

        full_stream_name = f"{self._stream_prefix}full"
        scoped_stream_name = f"{self._stream_prefix}{job_metadata['channel_id']}"

        logger.debug("********** logging event data to stream %s", scoped_stream_name)
        logger.debug(event_data)

        self._redis.xadd(  # type: ignore
            scoped_stream_name, event_data, "*", self._stream_limit
        )
        self._redis.xadd(  # type: ignore
            full_stream_name, event_data, "*", self._stream_limit_firehose
        )
