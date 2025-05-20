# app.py

# Imports necessários
from flask import Flask, jsonify, request, json
from flask_cors import CORS
from google import genai
import os
from dotenv import load_dotenv
import re # Importe o módulo de expressões regulares

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

# Definindo a função para criar o roteiro de viagem (ou sugestão de passeio)
def criar_sugestao_passeio(cidade, perfil):
    prompt = f"""
        Crie uma sugestão de passeio detalhada para a cidade/região: {cidade},
        com base no perfil do viajante: {perfil}.
        Em caso de termos inapropriados ou não relacionados a viagens, ignore-os e
        alerte o usuário sobre o uso responsável da ferramenta de geração de roteiros,
        mantendo a mesma estrutura do JSON do roteiro.

        A sugestão deve incluir:
        - um título descritivo do passeio
        - uma breve introdução
        - 3 a 5 pontos turísticos ou atividades principais (locais_principais)
        - dicas adicionais relevantes para o perfil (dicas_extras)
        - uma frase de encerramento.

        Devolva no formato JSON de acordo com o modelo:
        {{
            "titulo": "Título do Passeio na Cidade",
            "introducao": "Breve descrição do passeio.",
            "locais_principais": [
                "Nome do Local 1: Breve descrição ou o que fazer.",
                "Nome do Local 2: Breve descrição ou o que fazer."
            ],
            "dicas_extras": [
                "Dica 1 para o perfil.",
                "Dica 2 para o perfil."
            ],
            "encerramento": "Frase para finalizar o roteiro."
        }}
        """
    try:
        response_gemini = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
            }
        )
        
        # O Gemini pode retornar texto extra ou markdown, vamos tentar limpar
        raw_text = response_gemini.text.strip()
        print(f"DEBUG (backend): Resposta bruta da IA: {raw_text}") # Log para depuração

        # Tenta remover ```json e ```
        if raw_text.startswith('```json'):
            raw_text = raw_text[7:] # Remove '```json'
            if raw_text.endswith('```'):
                raw_text = raw_text[:-3] # Remove '```'
        
        # Tenta carregar o JSON
        parsed_response = json.loads(raw_text)
        print(f"DEBUG (backend): JSON parseado para frontend: {parsed_response}") # Log para depuração
        return parsed_response

    except json.JSONDecodeError as e:
        print(f"ERRO (backend): Falha ao parsear JSON da IA. Texto bruto: '{raw_text}'. Erro: {e}")
        # Retorna uma mensagem de erro estruturada para o frontend
        return {"error": "A IA gerou uma resposta JSON inválida. Tente novamente ou ajuste a solicitação."}
    except Exception as e:
        print(f"ERRO (backend): Erro inesperado ao gerar conteúdo da IA: {e}")
        return {"error": f"Erro interno ao se comunicar com a IA: {str(e)}"}

# Criando a Rota da API
@app.route('/sugestao_passeio', methods=['POST'])
def make_sugestao_passeio():
    try:
        dados = request.get_json()

        if not dados or not isinstance(dados, dict):
            return jsonify({'error': 'Requisição JSON inválida. Esperava um dicionário.'}), 400

        cidade = dados.get('cidade')
        perfil = dados.get('perfil')

        if not cidade or not perfil:
            return jsonify({'error': 'Cidade e perfil do viajante são campos obrigatórios.'}), 400

        response_from_ai = criar_sugestao_passeio(cidade, perfil)

        # Se a função criar_sugestao_passeio já retornou um erro, passamos ele adiante
        if "error" in response_from_ai:
            return jsonify(response_from_ai), 500 # Ou um código apropriado, ex: 422 Unprocessable Entity

        return jsonify(response_from_ai), 200

    except Exception as e:
        print(f"Um erro interno ocorreu na API: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)