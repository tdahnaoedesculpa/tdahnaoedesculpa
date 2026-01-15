"""
🧠 SERVIDOR TDAH - Backend Simples
Execute: python backend/server.py
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

# Dados em memória (simula banco de dados)
depoimentos = [
    {
        "id": 1,
        "nome": "SuperFocado",
        "mensagem": "Descobri que meu hiperfoco é um superpoder!",
        "data": "Hoje",
        "likes": 42,
        "liked": False,
        "avatar": "🚀"
    },
    {
        "id": 2,
        "nome": "MenteCriativa", 
        "mensagem": "Aceitar meu TDAH foi libertador!",
        "data": "Ontem",
        "likes": 38,
        "liked": True,
        "avatar": "🎨"
    }
]

usuarios = {
    "demo": {
        "username": "demo",
        "xp": 1250,
        "nivel": 5,
        "streak": 7,
        "avatar": "🧠"
    }
}

# ================ ROTAS DA API ================

@app.route('/')
def home():
    return jsonify({"message": "API TDAH funcionando!"})

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "status": "online",
        "message": "API TDAH funcionando!",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/depoimentos', methods=['GET'])
def get_depoimentos():
    return jsonify(depoimentos)

@app.route('/api/depoimentos', methods=['POST'])
def criar_depoimento():
    try:
        data = request.json
        novo_depoimento = {
            "id": len(depoimentos) + 1,
            "nome": data.get('nome', 'Anônimo'),
            "mensagem": data.get('mensagem', ''),
            "data": "Agora mesmo",
            "likes": 0,
            "liked": False,
            "avatar": "👤"
        }
        depoimentos.insert(0, novo_depoimento)  # Adiciona no início
        
        # Atualiza XP do usuário
        usuarios["demo"]["xp"] += 100
        
        return jsonify({
            "success": True,
            "message": "Depoimento criado!",
            "depoimento": novo_depoimento,
            "xp_ganho": 100
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/depoimentos/<int:depoimento_id>/like', methods=['POST'])
def curtir_depoimento(depoimento_id):
    # Encontra o depoimento
    for dep in depoimentos:
        if dep["id"] == depoimento_id:
            if dep["liked"]:
                dep["likes"] -= 1
                dep["liked"] = False
                acao = "unliked"
                xp = 0
            else:
                dep["likes"] += 1
                dep["liked"] = True
                acao = "liked"
                xp = 10
                usuarios["demo"]["xp"] += xp
            
            return jsonify({
                "success": True,
                "acao": acao,
                "likes": dep["likes"],
                "xp_ganho": xp
            })
    
    return jsonify({"error": "Depoimento não encontrado"}), 404

@app.route('/api/usuario/<username>', methods=['GET'])
def get_usuario(username):
    if username in usuarios:
        return jsonify(usuarios[username])
    else:
        # Cria novo usuário
        usuarios[username] = {
            "username": username,
            "xp": 100,
            "nivel": 1,
            "streak": 1,
            "avatar": "🧠"
        }
        return jsonify(usuarios[username])

@app.route('/api/usuario/<username>/xp', methods=['POST'])
def add_xp(username):
    data = request.json
    xp = data.get('xp', 10)
    
    if username in usuarios:
        usuarios[username]["xp"] += xp
        
        # Verifica level up
        novo_nivel = usuarios[username]["xp"] // 500 + 1
        level_up = novo_nivel > usuarios[username]["nivel"]
        
        if level_up:
            usuarios[username]["nivel"] = novo_nivel
        
        return jsonify({
            "success": True,
            "xp_total": usuarios[username]["xp"],
            "level_up": level_up,
            "novo_nivel": novo_nivel if level_up else usuarios[username]["nivel"]
        })
    
    return jsonify({"error": "Usuário não encontrado"}), 404

@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    return jsonify({
        "total_usuarios": len(usuarios),
        "total_depoimentos": len(depoimentos),
        "total_likes": sum(d["likes"] for d in depoimentos),
        "comunidade_ativa": True
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🧠 SERVIDOR TDAH INICIANDO...")
    print("="*50)
    print("\n📍 Endpoints disponíveis:")
    print("   • http://localhost:5000/api/status")
    print("   • http://localhost:5000/api/depoimentos")
    print("   • http://localhost:5000/api/usuario/demo")
    print("\n⚡ Acesse seu site em: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)