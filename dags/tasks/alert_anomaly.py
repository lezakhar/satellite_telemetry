from airflow.decorators import task

import configs
import asyncio

from _typing import Anomaly
from alert import send_alert


@task
def alert_anomaly(anomalies: list[Anomaly]):
    for anomaly in anomalies:
        message = f"""
            description: {anomaly.description}
            data: {anomaly.data}
        """

        asyncio.run(
            send_alert(
                bot_token=configs.BOT_TOKEN,
                chat_id=configs.CHAT_ID,
                message=message,
            )
        )
