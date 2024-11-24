import datetime


def generate_kafka_message(action: str) -> str:
    return f"{action}|{datetime.datetime.now()}"
