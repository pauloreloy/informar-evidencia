import copy
from src.config                                     import env_config
from src.domain.enum.loglevel                       import LogLevel
from src.adapter.aws.aws_client                     import AWS
from src.domain.usecase.informar_evidencia_usecase  import InformarEvidenciaUseCase
from src.domain.exceptions.evidencia_exceptions     import EvidenciaRejeitadaException
from src.adapter.kafka.kafka_client                 import KafkaClient


aws_client      = AWS()
kafka_client    = KafkaClient(aws_client=aws_client, topic_name=env_config.get_kafka_topic_name())


def lambda_handler(event, context):
    input = copy.deepcopy(event)
    if not input:
        raise ValueError("Input data is missing in the event")
    event = InformarEvidenciaUseCase(aws_client, kafka_client).execute(input)
    return event
