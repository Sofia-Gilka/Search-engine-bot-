from flask import Flask, render_template, request, jsonify
from search_engine import prompt

app = Flask(__name__)

# Глобальные переменные для хранения состояния
current_query = ""  # Последний поисковый запрос
current_results = []  # Кеш результатов
current_index = 0     # Текущий индекс результата

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def handle_command():
    global current_query, current_results, current_index
    
    user_input = request.form['user_input'].strip()
    response = ""
    
    if user_input == '/start':
        response = "Привет! Я - бот-помощник. Ты можешь задать мне вопрос, а я подберу тебе нужный материал.\n Используй:\n/ask - поиск\n/another - следующий результат\n/help - помощь"
        
    elif user_input == '/help':
        response = "Команды:\n/start - начать\n/ask - поиск\n/another - следующий результат.\n Если всё очень плохо - обращайтесь к gpt или @sofia_sophie_sofya :)"
        
    elif user_input.startswith('/ask'):
        query = user_input[4:].strip()
        if not query:
            response = "Введите запрос после /ask"
        else:
            try:
                # Сохраняем запрос и сбрасываем индекс
                current_query = query
                current_index = 0
                
                # Получаем первый результат (i=0)
                response = prompt(query, i=current_index)
                
                # Сохраняем результат в кеш (опционально)
                current_results.append(response)
            except Exception as e:
                response = f"Ошибка поиска: {str(e)}"
                
    elif user_input == '/another':
        if not current_query:
            response = "Сначала выполните поиск (/ask запрос)"
        else:
            try:
                # Увеличиваем индекс и получаем следующий результат
                current_index += 1
                response = prompt(current_query, i=current_index)
                current_results.append(response)
            except IndexError:
                response = "Больше результатов нет!"
                current_index = 0  # Сбрасываем индекс
            except Exception as e:
                response = f"Ошибка: {str(e)}"
                current_index = 0
                
    else:
        response = "Неизвестная команда. Введите /help"
        
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)