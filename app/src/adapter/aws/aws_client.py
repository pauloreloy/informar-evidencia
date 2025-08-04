
from src.adapter.aws.aws_dynamodb   import DynamoDB
from src.adapter.aws.aws_logs       import Logs

class AWS:


    def __init__(self):
        self.dynamodb_client    = DynamoDB()
        self.logs_client        = Logs()