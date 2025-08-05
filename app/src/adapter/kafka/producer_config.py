import os
from src.config     import env_config


class ProducerConfig:


    def __init__(self, kcert_user):
        self.caroot     = os.path.join(env_config.get_kafka_cert_path(), 'CARoot.crt')
        self.certfile   = os.path.join(env_config.get_kafka_cert_path(), f'{kcert_user}-cert.pem')
        self.keyfile    = os.path.join(env_config.get_kafka_cert_path(), f'{kcert_user}-key.pem')

    
    def get_kafka_settings(self, key_serializer, avro_serializer):
        kafka_settings = { 
            'bootstrap.servers': env_config.get_kafka_url(),
            'acks':              'all',
            'client.id':         env_config.get_kafka_client_id(),
        }
        if os.path.exists(self.certfile):
            kafka_settings.update({
                'security.protocol':        'SSL',
                'ssl.ca.location':          self.caroot,
                'ssl.certificate.location': self.certfile,
                'ssl.key.location':         self.keyfile,
                'key.serializer':           key_serializer,
                'value.serializer':         avro_serializer
            })
        return kafka_settings
    

    def get_schema_registry_config(self):
        config = {
            'url': env_config.get_kafka_schema_registry_url(),
        }
        if os.path.exists(self.certfile):
            config.update({
                'ssl.ca.location':          self.caroot,
                'ssl.certificate.location': self.certfile,
                'ssl.key.location':         self.keyfile
            })
        return config