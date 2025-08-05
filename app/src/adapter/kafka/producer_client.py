import json
from uuid                                   import uuid4
from src.adapter.aws.aws_client             import AWS   
from confluent_kafka.schema_registry        import SchemaRegistryClient, topic_record_subject_name_strategy
from confluent_kafka.schema_registry.avro   import AvroSerializer
from confluent_kafka.serialization          import StringSerializer
from confluent_kafka                        import SerializingProducer
from src.utils.utils                        import Utils
from src.domain.enum.loglevel               import LogLevel


class ProducerClient:


    kafka_producer = None


    def _callback_delivery(self, err, msg):
        if err is not None:
            self.aws_client.logs_client.custom_log(LogLevel.ERROR,
                                                   f"Message delivery failed: {err}")
        else:
            self.aws_client.logs_client.custom_log(LogLevel.INFO,
                                                   f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


    def __init__(self, aws_client: AWS, kaas_config, kaas_schema, kaas_schema_path):
        self.aws_client         = aws_client   
        self.kaas_config        = kaas_config
        self.kaas_schema        = kaas_schema
        self.kaas_schema_path   = kaas_schema_path
        self.kafka_producer     = self.create_producer()


    def create_producer(self):
        key_serializer          = StringSerializer("utf_8")
        schema_registry_client  = SchemaRegistryClient(
            conf=self.kaas_config.get_schema_registry_config()
        )
        avro_serializer = AvroSerializer(
            schema_str=self.load_schema_file(),
            schema_registry_client=schema_registry_client,
            to_dict=Utils._convert_to_dict,
            conf={
                "auto.register.schemas": False,  # ativa registro automático
                "subject.name.strategy": topic_record_subject_name_strategy
            }
        )
        producer_conf                       = self.kaas_config.get_kafka_settings(key_serializer, avro_serializer)
        producer_conf["key.serializer"]     = key_serializer
        producer_conf["value.serializer"]   = avro_serializer
        producer_kafka                      = SerializingProducer(conf=producer_conf)
        return producer_kafka


    def send_message(self, topic_name, message, header=None):
        if not self.kafka_producer:
            raise ValueError("Kafka producer is not initialized.")
        try:
            self.kafka_producer.produce(
                topic=topic_name,
                key=str(uuid4()),
                value=message,
                headers=header,
                on_delivery=self._callback_delivery
            )
            self.kafka_producer.poll(1)
            self.kafka_producer.flush()
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to send message: {e}")


    def load_schema_file(self):
        try:
            with open(self.kaas_schema_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Schema file not found at: {self.kaas_schema_path}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while loading schema: {e}")