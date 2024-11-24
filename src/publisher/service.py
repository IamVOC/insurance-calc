from .kafka import producer
from src.config import settings


def produce_message(message: str) -> None:
    producer.send(message.encode(), settings.KAFKA.TOPIC)
