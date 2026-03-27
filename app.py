import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações (Pegando das variáveis de ambiente do Render)
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'meu_robo_vendedor_123')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')

@app.route('/')
def index():
    return "Robô Dinho Ferramentas está ONLINE! 🚀"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. Verificação do Webhook (Quando você salva na Meta)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFIED ✅")
            return challenge, 200
        else:
            return 'Token de verificação inválido', 403

    # 2. Recebimento de Mensagens (Quando alguém manda um "Oi")
    if request.method == 'POST':
        data = request.get_json()
        print(f"MENSAGEM RECEBIDA: {data}") # Isso vai aparecer no log do Render!
        
        # Aqui o robô processa a mensagem
        if data.get('object') == 'instagram' or data.get('object') == 'page':
            # O robô vai ler e responder aqui (lógica simplificada para teste)
            return 'EVENT_RECEIVED', 200
        
        return 'Objeto não suportado', 404

if __name__ == '__main__':
    # O Render exige que o robô rode na porta definida pela variável PORT
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
