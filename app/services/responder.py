def generate_response(category: str) -> str:
    """
    Gera resposta automática com base na categoria.
    
    Args:
        category (str): "Produtivo" ou "Improdutivo"

    Returns:
        str: resposta apropriada
    """
    responses = {
        "Produtivo": "Obrigado pelo contato! Sua solicitação será analisada em breve.",
        "Improdutivo": "Agradecemos sua mensagem e ficamos felizes pelo reconhecimento.",
    }

    if category not in responses:
        raise ValueError(f"Categoria inválida: {category}")

    return responses[category]
