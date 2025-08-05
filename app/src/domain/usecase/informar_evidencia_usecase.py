
from src.adapter.kafka.kafka_client     import KafkaClient
from src.adapter.aws.aws_client         import AWS

class InformarEvidenciaUseCase:


    def __init__(self, aws_client: AWS, kafka_client: KafkaClient):
        self.aws_client = aws_client
        self.kafka_client = kafka_client


    def execute(self, payload: dict):
        message = {
            "codigo_identificacao_repositorio": str(payload.get("dados_conteudo", {}).get("codigo_identificacao_repositorio")),
        }
        return self.kafka_client.send_message(message)