from typing                             import Any
from src.config                         import params
from src.config                         import env_config
from src.config.topics                  import topics
from src.adapter.aws.aws_client         import AWS
from src.adapter.kafka.producer_client  import ProducerClient
from src.adapter.kafka.producer_config  import ProducerConfig


class KafkaClient:


    def __init__(self, aws_client: AWS, topic_name: str = None):
        self.aws_client     = aws_client
        self.topic_name     = topic_name
        self.kaas_user      = env_config.get_kafka_user()
        self.kaas_config    = ProducerConfig(self.kaas_user)
        self.init_client(
            topic_schema    = topics.get(topic_name, {}).get("topic_schema"),
            topic_subject   = topics.get(topic_name, {}).get("topic_subject")
        )


    def init_client(self, topic_schema: str, topic_subject: str):
        kaas_schema         = topic_subject
        kaas_schema_path    = params.KAFKA_SCHEMA_PATH + topic_schema
        self.client         = ProducerClient(aws_client=self.aws_client, kaas_config=self.kaas_config, \
                                             kaas_schema=kaas_schema, kaas_schema_path=kaas_schema_path)
        
    
    def send_message(self, message: Any, header: dict = None):
        return self.client.send_message(self.topic_name, message, header)