# VOSK Micro
Пример использования _vosk_ с микрофоном.\
___Примечание:___ дополнительного реализована проверка непристойных слов.

## Установка
Установка зависимостей:
```commandline
pip install -r requirements.txt
```
Загрузка моделей:
```commandline
wget https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
unzip vosk-model-small-ru-0.22.zip -d model
```

## Запуск

```commandline
python3 main.py
```
