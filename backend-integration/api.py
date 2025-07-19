from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv, set_key
from Backend.Chatbot import ChatBot
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.model import FirstLayerDMM
from Backend.Automation import Automation
import asyncio

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    
    if not username or not email:
        return jsonify({'error': 'Username and email are required'}), 400
    
    # Update .env file with username
    try:
        set_key('.env', 'Username', username)
        return jsonify({
            'success': True,
            'user': {
                'username': username,
                'email': email
            }
        })
    except Exception as e:
        return jsonify({'error': 'Failed to update user settings'}), 500

@app.route('/api/chat/send', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        # Process message through the existing AI pipeline
        decision = FirstLayerDMM(message)
        
        # Check if it's a general query or requires real-time search
        if any(d.startswith('general') for d in decision):
            response = ChatBot(message)
        elif any(d.startswith('realtime') for d in decision):
            response = RealtimeSearchEngine(message)
        else:
            # Handle automation tasks
            asyncio.run(Automation(decision))
            response = "Task executed successfully."
        
        return jsonify({
            'success': True,
            'response': response,
            'decision': decision
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    try:
        with open('Data/ChatLog.json', 'r', encoding='utf-8') as f:
            chat_log = json.load(f)
        
        # Convert to frontend format
        messages = []
        for entry in chat_log:
            messages.append({
                'id': str(len(messages)),
                'role': entry['role'],
                'content': entry['content'],
                'timestamp': '2024-01-01T00:00:00Z'  # You might want to add timestamps to your chat log
            })
        
        return jsonify({
            'success': True,
            'messages': messages
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/clear', methods=['POST'])
def clear_chat_history():
    try:
        with open('Data/ChatLog.json', 'w', encoding='utf-8') as f:
            json.dump([], f)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    try:
        # Read status from the existing status file
        with open('Frontend/Files/Status.data', 'r', encoding='utf-8') as f:
            status = f.read().strip()
        
        return jsonify({
            'success': True,
            'status': status,
            'isListening': status == 'Listening...',
            'isThinking': status == 'Thinking...',
            'isAnswering': status == 'Answering...'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)