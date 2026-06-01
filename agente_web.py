import os
from flask import Flask, request, jsonify, render_template_string
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
historico = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Meu Assistente IA</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial; max-width: 800px; margin: 40px auto; padding: 20px; }
        #chat { height: 500px; overflow-y: auto; border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 8px; }
        .user { background: #007bff; color: white; padding: 8px 12px; border-radius: 8px; margin: 5px 0; display: inline-block; float: right; clear: both; }
        .bot { background: #f1f1f1; padding: 8px 12px; border-radius: 8px; margin: 5px 0; display: inline-block; float: left; clear: both; }
        input { width: 80%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🤖 Meu Assistente IA</h1>
    <div id="chat"></div>
    <input id="msg" placeholder="Digite sua mensagem..." onkeypress="if(event.key=='Enter') enviar()">
    <button onclick="enviar()">Enviar</button>
    <script>
        async function enviar() {
            const msg = document.getElementById('msg').value;
            if (!msg) return;
            const chat = document.getElementById('chat');
            chat.innerHTML += '<div class="user">' + msg + '</div>';
            document.getElementById('msg').value = '';
            const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({mensagem: msg})});
            const data = await res.json();
            chat.innerHTML += '<div class="bot">' + data.resposta + '</div>';
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    dados = request.json
    historico.append({"role": "user", "content": dados['mensagem']})
    resposta = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        system="Você é um assistente prestativo. Responda sempre em português.",
        messages=historico
    )
    texto = resposta.content[0].text
    historico.append({"role": "assistant", "content": texto})
    return jsonify({"resposta": texto})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)