


class DadosRetencao:

    
    def __init__(self):
        self.numero_portabilidade           = None
        self.codigo_identificacao_pessoa    = None
        self.codigo_motivo_retencao         = None
        self.codigo_canal_origem            = None
        self.numero_raiz_cnpj_proponente    = None


    def to_dict(self):
        return {
            'numero_portabilidade':         self.numero_portabilidade,
            'codigo_identificacao_pessoa':  self.codigo_identificacao_pessoa,
            'codigo_motivo_retencao':       self.codigo_motivo_retencao,
            'codigo_canal_origem':          self.codigo_canal_origem,
            'numero_raiz_cnpj_proponente':  self.numero_raiz_cnpj_proponente
        }


    def build(data: dict):
        _dados_retencao = DadosRetencao()
        _dados_retencao.numero_portabilidade        = data.get('numero_portabilidade')
        _dados_retencao.codigo_identificacao_pessoa = data.get('codigo_identificacao_pessoa')
        _dados_retencao.codigo_motivo_retencao      = data.get('codigo_motivo_retencao')
        _dados_retencao.codigo_canal_origem         = data.get('codigo_canal_origem')
        _dados_retencao.numero_raiz_cnpj_proponente = data.get('numero_raiz_cnpj_proponente')
        return _dados_retencao