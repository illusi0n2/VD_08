from flask import Flask, render_template
import requests
from googletrans import Translator
from deep_translator import GoogleTranslator


app = Flask(__name__)

API_KEY = ('b8ukQeLwy35606xZPpm8RQ==evEhrdkd4nOI9FNA')
API_URL = 'https://api.api-ninjas.com/v1/quotes'

def translate_text(text, target_language='ru'):
    """Переводит текст на указанный язык"""
    try:
        translator = GoogleTranslator(source='auto', target=target_language)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return text  # Возвращаем оригинальный текст в случае ошибки


def get_random_quote():
    """Получает случайную цитату с API и переводит её"""
    try:
        headers = {'X-Api-Key': API_KEY}
        response = requests.get(API_URL, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data:
                quote_data = data[0]

                # Переводим цитату и автора на русский
                original_quote = quote_data['quote']
                original_author = quote_data['author']
                original_category = quote_data['category']

                translated_quote = translate_text(original_quote)
                translated_author = translate_text(original_author)
                translated_category = translate_text(original_category)

                return {
                    'translated_quote': translated_quote,
                    'translated_author': translated_author,
                    'translated_category': translated_category
                }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка API: {e}")
        return None


@app.route('/')
def index():
    """Главная страница с цитатой"""
    quote = get_random_quote()
    return render_template('index.html', quote=quote)


@app.route('/refresh')
def refresh_quote():
    """Обновление цитаты без перезагрузки страницы"""
    quote_data = get_random_quote()
    if quote_data:
        return {
            'quote': quote_data['quote'],
            'author': quote_data['author'],
            'category': quote_data['category']
        }
    return {'error': 'Не удалось загрузить цитату'}

if __name__ == '__main__':
    app.run(debug=True)