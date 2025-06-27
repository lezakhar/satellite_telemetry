from datetime import datetime

import tasks
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
    "telemetry_marts_calculation",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    calc_altitude_mart = PythonOperator(
        task_id="calc_altitude_mart",
        python_callable=tasks.calc_altitude_mart,
    )

    calc_speed_mart = PythonOperator(
        task_id="calc_speed_mart",
        python_callable=tasks.calc_speed_mart,
    )

    calc_temperature_mart = PythonOperator(
        task_id="calc_temperature_mart",
        python_callable=tasks.calc_temperature_mart,
    )

    trigger_anomaly_detection = TriggerDagRunOperator(
        task_id="trigger_anomaly_detection",
        trigger_dag_id="telemetry_anomaly_alerting",
        execution_date="{{ execution_date }}",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    (
        calc_altitude_mart
        >> calc_speed_mart
        >> calc_temperature_mart
        >> trigger_anomaly_detection
    )

with DAG(
    "telemetry_anomaly_alerting",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    tasks.alert_anomaly(tasks.detect_anomaly())
