import copy
from src.domain.enum.loglevel                       import LogLevel
from src.adapter.aws.aws_client                     import AWS
from src.domain.usecase.validar_retencao_usecase    import ValidarRetencaoUseCase
from src.domain.exceptions.evidencia_exceptions     import EvidenciaRejeitadaException
from src.adapter.kafka.kafka                        import Kafka


aws_client = AWS()
kafka_client = Kafka(topic="retencao-evidencias")


def lambda_handler(event, context):
    kafka_client.send(
        key=event.get('key', 'default_key'),
        value=event.get('value', {}),
        topic="retencao-evidencias"
    )
    kafka_client.flush()
    #aws_client.logs_client.custom_log(
    #    log_level=LogLevel.INFO,
    #    message="Lambda function started processing event"
    #)
    #input = copy.deepcopy(event)
    #if not input:
    #    raise ValueError("Input data is missing in the event")
    #try:
    #    event = ValidarRetencaoUseCase(aws_client).execute(input)
    #except EvidenciaRejeitadaException as e:
    #    raise EvidenciaRejeitadaException(e)
    #return event
