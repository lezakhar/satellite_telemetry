import asyncio

import configs
from airflow.decorators import task
from typing_ import Anomaly
from utils.alert import send_alert


@task
def alert_anomaly(anomalies: list[Anomaly]):
    for anomaly in anomalies:
        message = f"""
            {anomaly.description}
            {anomaly.data}
        """
        asyncio.run(
            send_alert(
                bot_token=configs.BOT_TOKEN,
                chat_id=configs.CHAT_ID,
                message=message,
            )
        )
