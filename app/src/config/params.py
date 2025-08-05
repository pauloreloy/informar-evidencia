AWS_REGION                  = "us-east-1"
AWS_ACCESS_KEY_ID           = None
AWS_ACCESS_SECRET_KEY       = None
AWS_ENDPOINT                = "localhost:4566"

LAMBDA_LOG_GROUP            = "CONTROLE"
LAMBDA_NAME                 = "lbd-atualizar-controle-retencao"

TABELA_CONTROLE             = "tbl_controle"
PK_CONTROLE                 = "num_prde"
SK_CONTROLE                 = "cod_idef_pess"
MAPPER_PATH                 = "src/models/mappers"

KAFKA_BROKER_URL            = "kafka.pre.dev.br:9092"
KAFKA_SCHEMA_REGISTRY_URL   = "http://kafka.pre.dev.br:8080"
KAFKA_CLIENT_ID             = "client"
KAFKA_USER                  = "kafka_user"
KAFKA_CERT_PATH             = "certs/kaas/"
KAFKA_SCHEMA_PATH           = "src/models/schemas/"
KAFKA_TOPIC_NAME            = "registro-evidencias"
