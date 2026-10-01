import re
import spacy

# Carrega o modelo de linguagem do spaCy para português
nlp = spacy.load("pt_core_news_sm")

def anonimizar_texto(texto: str) -> str:
    """
    Função responsável por anonimizar PII (Informações Pessoais Identificáveis)
    combinando Named Entity Recognition (NER) para nomes de pessoas via spaCy
    e expressões regulares robustas para identificadores estruturados 
    (CPF, RG, e-mails, contas e agências bancárias).
    
    Assinatura fixa exigida pelo CP5.
    """
    if not isinstance(texto, str):
        return str(texto)

    doc = nlp(texto)
    texto_anon = texto
    
    # 1. Tratamento de nomes de pessoas (NER - PER) de trás para frente para manter os índices válidos
    for ent in sorted([e for e in doc.ents if e.label_ == "PER"], key=lambda x: x.start_char, reverse=True):
        texto_anon = texto_anon[:ent.start_char] + "[ANONIMIZADO]" + texto_anon[ent.end_char:]

    # 2. Tratamento de identificadores estruturados via Regex
    # CPFs (formatados ou não)
    texto_anon = re.sub(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b', '[CPF_ANONIMIZADO]', texto_anon)
    texto_anon = re.sub(r'\b\d{11}\b', '[CPF_ANONIMIZADO]', texto_anon)
    
    # RGs (formatados ou não)
    texto_anon = re.sub(r'\b\d{2}\.\d{3}\.\d{3}-[0-9Xx]\b', '[RG_ANONIMIZADO]', texto_anon)
    texto_anon = re.sub(r'\b\d{8,9}\b', '[RG_ANONIMIZADO]', texto_anon)
    
    # E-mails
    texto_anon = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_ANONIMIZADO]', texto_anon)
    
    # Agências Bancárias
    texto_anon = re.sub(r'\b(ag[eê]ncia|ag\.?)\s*\d{4}-?\d?\b', '[AGENCIA_ANONIMIZADA]', texto_anon, flags=re.IGNORECASE)
    
    # Contas Bancárias
    texto_anon = re.sub(r'\b(conta|cc\.?)\s*\d+-\d\b', '[CONTA_ANONIMIZADA]', texto_anon, flags=re.IGNORECASE)

    return texto_anon

if __name__ == "__main__":
    # Teste rápido da função
    teste_str = "Cliente Carlos Silva, CPF 123.456.789-09, conta 1234-5, email carlos@email.com"
    print("Original:", teste_str)
    print("Anonimizado:", anonimizar_texto(teste_str))