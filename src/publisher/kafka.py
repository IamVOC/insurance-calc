from kafka import KafkaProducer

from src.config import settings


producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA.BOOTSTRAP_SERVER,
)
