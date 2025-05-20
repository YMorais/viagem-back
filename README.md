## Status  
Projeto concluído!  

# API de Sugestões de Passeios 🗺️🚀  

## Descrição  
Este backend desenvolvido com Flask expõe uma API REST que utiliza a IA da Google (via Gemini) para gerar sugestões personalizadas de passeios a partir de uma cidade e de um perfil de viajante. A resposta retorna um JSON estruturado com título, introdução, locais, dicas e encerramento.

# Índice  
* [Status](#status)  
* [Funcionalidades](#funcionalidades)  
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Pré-Requisitos](#pré-requisitos)
* [Autores](#autores)  
* [Licença](#licença)  

## Funcionalidades  
- ✅ API REST com Flask  
- ✅ Recebe `cidade` e `perfil` como entrada  
- ✅ Gera roteiros detalhados usando IA  
- ✅ Trata erros de resposta inválida da IA  
- ✅ Suporte a CORS para conexão com frontend separado  

## Tecnologias Utilizadas  
**Linguagens/Frameworks:**  
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  
- ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)  
- ![dotenv](https://img.shields.io/badge/dotenv-3c3c3c?style=for-the-badge&logo=dotenv&logoColor=white)  

## Pré-Requisitos  
Antes de rodar o projeto, é necessário:  
- Ter o Python 3.x instalado  
- Ter o Pip instalado  
- Criar um arquivo `.env` com a variável `GOOGLE_API_KEY` contendo sua chave da API Gemini  
- Instalar as dependências com:  

## Autores
- Yasmim Bueno de Morais - [GitHub](https://github.com/YMorais/) - yasmim.morais.senai@gmail.com

## Licença  
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.