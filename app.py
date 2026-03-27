import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configurações do Google Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Configurações do WhatsApp e Verificação
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "5511982677974")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "meu_robo_vendedor_123")

# Instruções de Personalidade do Vendedor
SYSTEM_PROMPT = f"""
Você é um vendedor de elite de ferramentas para construção civil. Seu foco é vender: 
1. Riscadeiras profissionais.
2. Serras de mármore potentes.
3. Kits de ferramentas completos.

Sua personalidade:
- Educado, técnico e muito persuasivo.
- Responde dúvidas sobre preços, formas de pagamento (PIX, Cartão, Boleto) e localização (loja física e entregas).
- Se o cliente perguntar o preço, dê uma estimativa, mas diga que tem "condições especiais exclusivas para quem chama no WhatsApp".
- Seu objetivo principal é capturar o número de WhatsApp do cliente ou fazer ele clicar no seu link: https://wa.me/{WHATSAPP_NUMBER}
- Se o cliente mandar o número dele, confirme que um consultor entrará em contato em minutos.
- Nunca saia do personagem. Você é o vendedor da loja.
"""

@app.route('/webhook', methods=['GET'] )
def verify():
    # Verificação exigida pela Meta (Facebook/Instagram)
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return 'Token de verificação inválido', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Lógica simplificada para processar mensagens do Instagram
    try:
        if data.get('object') == 'instagram':
            for entry in data.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    if messaging_event.get('message'):
                        sender_id = messaging_event['sender']['id']
                        message_text = messaging_event['message'].get('text')
                        
                        if message_text:
                            # Gerar resposta usando IA do Google Gemini
                            chat = model.start_chat(history=[])
                            full_prompt = f"{SYSTEM_PROMPT}\n\nCliente diz: {message_text}\n\nResponda como o vendedor:"
                            response = chat.send_message(full_prompt)
                            
                            # Aqui você integraria com a API de envio da Meta
                            # Por enquanto, o log mostrará a resposta ideal
                            print(f"Resposta para {sender_id}: {response.text}")
                            
            return 'EVENT_RECEIVED', 200
    except Exception as e:
        print(f"Erro no processamento: {e}")
        
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000)
