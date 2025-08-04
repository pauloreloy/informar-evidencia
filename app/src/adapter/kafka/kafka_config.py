from src.config                     import params
from src.config                     import env_config
from src.adapter.aws.aws_client     import AWS


class KafkaConfig:


    def __init__(self):
        pass


    def get_config(self):
        config = {
            "bootstrap.servers":    env_config.get_kafka_url(),
            "client.id":            env_config.get_kafka_client_id(),
        }
        #config["security.protocol"]           = self.security_protocol
        #config["ssl.ca.location"]             = self.ssl_ca_location
        #config["ssl.certificate.location"]    = self.ssl_certificate_location
        #config["ssl.key.location"]            = self.ssl_key_location
        return config