from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from openai import AzureOpenAI

def azure_call(task_id):
    client = AzureOpenAI(
        api_key="your-api-key",  # replace with yours
        api_version="2023-05-15",
        azure_endpoint="https://your-endpoint.openai.azure.com/"  # replace with yours
    )

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Say hi"},
            {"role": "user", "content": "Hi, how Azure is working?"}
        ]
    )
    print(f"{task_id} →", completion.choices[0].message.content)

default_args = {
    'start_date': datetime(2024, 1, 1),
    'catchup': False
}

with DAG('azure_parallel_test', default_args=default_args, schedule_interval=None, tags=['demo']) as dag:

    t1 = PythonOperator(
        task_id='azure_call_1',
        python_callable=lambda: azure_call("Task 1")
    )

    t2 = PythonOperator(
        task_id='azure_call_2',
        python_callable=lambda: azure_call("Task 2")
    )

    t3 = PythonOperator(
        task_id='azure_call_3',
        python_callable=lambda: azure_call("Task 3")
    )

    [t1, t2, t3]  # Parallel execution
