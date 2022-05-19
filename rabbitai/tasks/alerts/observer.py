# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from sqlalchemy.orm import Session

from rabbitai import jinja_context
from rabbitai.models.alerts import Alert, SQLObservation

logger = logging.getLogger("tasks.email_reports")


def observe(alert_id: int, session: Session) -> Optional[str]:
    """
    收集警报的观察结果。如果观察者值无效，则返回错误消息。

    :param alert_id: 提醒标识。
    :param session: 数据库会话对象。
    :return:
    """

    alert = session.query(Alert).filter_by(id=alert_id).one()

    value = None

    tp = jinja_context.get_template_processor(database=alert.database)
    rendered_sql = tp.process_template(alert.sql)
    df = alert.database.get_df(rendered_sql)

    error_msg = validate_observer_result(df, alert.id, alert.label)

    if not error_msg and not df.empty and df.to_records()[0][1] is not None:
        value = float(df.to_records()[0][1])

    observation = SQLObservation(
        alert_id=alert_id, dttm=datetime.utcnow(), value=value, error_msg=error_msg,
    )

    session.add(observation)
    session.commit()

    return error_msg


def validate_observer_result(
    sql_result: pd.DataFrame, alert_id: int, alert_label: str
) -> Optional[str]:
    """
    验证指定 DataFrame SQL 查询结果是否包含 SQLObservation 的有效值。

    如果无效返回错误信息。

    :param sql_result: DataFrame SQL 查询结果。
    :param alert_id: 提醒标识。
    :param alert_label: 提醒标签。
    :return:
    """

    try:
        if sql_result.empty:
            # empty results are used for the not null validator
            return None

        rows = sql_result.to_records()

        assert (
            len(rows) == 1
        ), f"Observer for alert <{alert_id}:{alert_label}> returned more than 1 row"

        assert (
            len(rows[0]) == 2
        ), f"Observer for alert <{alert_id}:{alert_label}> returned more than 1 column"

        if rows[0][1] is None:
            return None

        float(rows[0][1])

    except AssertionError as error:
        return str(error)
    except (TypeError, ValueError):
        return (
            f"Observer for alert <{alert_id}:{alert_label}> returned a non-number value"
        )

    return None
