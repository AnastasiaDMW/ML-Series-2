# Sentiment Analysis API

API-сервис для анализа тональности русскоязычных комментариев с использованием модели
[blanchefort/rubert-base-cased-sentiment-rurewiews](https://huggingface.co/blanchefort/rubert-base-cased-sentiment-rurewiews)
(Hugging Face).

API позволяет:
- Анализировать один или несколько комментариев (в теле запроса)
- Загружать `.txt` или `.json` файлы с комментариями
- Получать сводку положительных и отрицательных отзывов

## **Запуск проекта**
### Клонировать репозиторий
```
git clone https://github.com/AnastasiaDMW/ML-Series-2.git
```
### Создать и активировать виртуальное окружение
```
# Windows
python -m venv venv
venv\Scripts\activate

# Linux, macOS
python3 -m venv venv
source venv/bin/activate
```
### Установить зависимости
```
pip install -r requirements.txt
```
### Запуск API
Из корня проекта (где находится папка /app) выполните:
```
python -m app.main
```
После запуска сервер будет доступен по адресу:
```
http://127.0.0.1:8000
```

## Доступные эндпоинты
| Метод | Путь                    | Описание                                      |
|-------|-------------------------|-----------------------------------------------|
| POST  | /api/analyze            | Анализ комментариев, переданных в теле запроса |
| POST  | /api/analyze/file       | Анализ комментариев из загруженного .txt или .json файла |

## Примеры запроса
### URL:
```
POST http://127.0.0.1:8000/api/analyze
```
### Тело:
```
{
  "comments": [
    "Мне понравилось видео!",
    "Это было ужасно, не делай так больше."
  ]
}
```
### Пример ответа:
```
{
  "positive": 1,
  "negative": 1,
  "positive_percent": 50.0,
  "negative_percent": 50.0,
  "results": [
    {"text": "Мне понравилось видео!", "label": "POSITIVE", "score": 0.981},
    {"text": "Это было ужасно, не делай так больше.", "label": "NEGATIVE", "score": 0.946}
  ]
}
```
## Пример загрузки файла в Postman
### Для .txt
```
POST http://127.0.0.1:8000/api/analyze/file
```
| Key | Type                           | Value                      |
|-------|------------------------------|----------------------------|
| file  | File            | data.txt                   |

## Swagger и ReDoc документация
После запуска API доступны автоматически:
- Swagger UI → http://127.0.0.1:8000/docs
- ReDoc → http://127.0.0.1:8000/redoc<br><br><br>

Автор: <b>*AnastasiaDMW*</b>

