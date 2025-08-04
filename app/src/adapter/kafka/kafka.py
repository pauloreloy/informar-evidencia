import json
from confluent_kafka                    import Producer
from src.adapter.kafka.kafka_config     import KafkaConfig


class Kafka:


    def __init__(self, topic: str):
        self.config     = KafkaConfig()
        self.producer   = Producer(self.config.get_config())


    def _delivery_report(self, err, msg):
        if err:
            print(f"[ERROR] Delivery failed for key={msg.key()}: {err}")
        else:
            print(f"[OK] Delivered key={msg.key()} to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


    def send(self, key: str, value: dict, topic: str = None):
        target = topic or self.config.topic
        self.producer.produce(
            topic=target,
            key=key,
            value=json.dumps(value),
            callback=self._delivery_report,
        )
        self.producer.poll(0)


    def flush(self, timeout: float = 10.0):
        self.producer.flush(timeout)