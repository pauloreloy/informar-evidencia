

from src.config                                             import params
from src.domain.entity.dados_retencao                       import DadosRetencao
from src.adapter.aws.aws_client                             import AWS
from src.domain.usecase.consultar_dados_controle_usecase    import ConsultarDadosControleUseCase
from src.domain.exceptions.evidencia_exceptions             import EvidenciaRejeitadaException


class ValidarRetencaoUseCase:


    def __init__(self, aws_client: AWS):
        self.aws_client = aws_client


    def validar_codigo_retencao(self, dados_retencao: DadosRetencao, input: dict):
        if dados_retencao.codigo_motivo_retencao in self.get_codigos_evidencia():
            input = input | {"validar_evidencia": True}
            return input
        input = input | {"validar_evidencia": False}
        return input
    
    
    def validar_evidencia(self, dados_retencao: DadosRetencao, input: dict):
        dados_evidencia = {}
        dados_evidencia["dados_evidencia"] = {}
        _dados_tabela   = ConsultarDadosControleUseCase(self.aws_client).execute(dados_retencao.numero_portabilidade, \
                                                                               dados_retencao.codigo_identificacao_pessoa)
        cod_repo            = _dados_tabela.get("codigo_identificacao_documento_repositorio", None)
        status_evidencia    = _dados_tabela.get("descricao_situacao_evidencia", None)
        if cod_repo and status_evidencia == params.STATUS_EVIDENCIA_ACEITA:
            dados_evidencia["dados_evidencia"]["evidencia_aceita"] = True
            dados_evidencia["dados_evidencia"]["codigo_identificacao_documento_repositorio"] = cod_repo
            return input | dados_evidencia
        if status_evidencia == params.STATUS_EVIDENCIA_REJEITADA:
            dados_evidencia["dados_evidencia"]["evidencia_aceita"] = False
            return input | dados_evidencia
        return input


    def execute(self, input: dict):
        if not self.get_fluxo_validacao_habilitado():
            return input | {"fluxo_validacao_ativo": False}
        input           = input | {"fluxo_validacao_ativo": True}
        dados_retencao  = input.get('dados_retencao', {})
        dados_retencao  = DadosRetencao.build(dados_retencao)
        input           = self.validar_codigo_retencao(dados_retencao, input)
        input           = self.validar_evidencia(dados_retencao, input)
        return input
    

    def get_codigos_evidencia(self):
        return ["1", "17"]
    
    
    def get_fluxo_validacao_habilitado(self):
        return 1