import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações (Pegando das variáveis de ambiente do Render)
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'meu_robo_vendedor_123')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')

@app.route('/')
def index():
    return "Robô Dinho Ferramentas está ONLINE e PRONTO para responder! 🤖🚀"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. Verificação do Webhook (Meta)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        return 'Token inválido', 403

    # 2. Recebimento e Resposta de Mensagens
    if request.method == 'POST':
        data = request.get_json()
        print(f"--- NOVA MENSAGEM RECEBIDA ---")
        print(data)

        if data.get('object') == 'instagram':
            for entry in data.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    if messaging_event.get('message'):
                        sender_id = messaging_event['sender']['id']
                        message_text = messaging_event['message'].get('text')
                        
                        if message_text:
                            print(f"Enviando resposta para {sender_id}...")
                            enviar_resposta(sender_id, f"Olá! Eu sou o robô da Dinho Ferramentas. Recebi sua mensagem: '{message_text}'. Como posso te ajudar?")
        
        return 'EVENT_RECEIVED', 200

def enviar_resposta(recipient_id, text):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload )
    if response.status_code != 200:
        print(f"ERRO AO ENVIAR: {response.text}")
    else:
        print("RESPOSTA ENVIADA COM SUCESSO! ✅")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
