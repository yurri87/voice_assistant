# -*- coding: utf-8 -*-

import os
import random
import speech_recognition

# Установка кодировки вывода в консоль
import sys
sys.stdout.reconfigure(encoding='utf-8')

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка'],
        'play_music': ['включить музыку', 'дискотека'],
        'exit': ['выход', 'стоп', 'завершить']
    }
}


def listen_command():
    """Функция будет возвращать распознанную команду"""
    
    try:
        with speech_recognition.Microphone() as mic:
            print("Слушаю...")
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            print("Распознаю...")
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
            print(f"Распознано: {query}")
        return query
    except speech_recognition.UnknownValueError:
        print("Не удалось распознать речь")
        return 'Damn... Не понял что ты сказал :/'
    except speech_recognition.RequestError as e:
        print(f"Ошибка сервиса распознавания речи; {e}")
        return "Ошибка сервиса распознавания речи"


def greeting():
    """Функция приветствия"""
    
    return 'Привет нищеброд!'


def create_task():
    """Создать задачу в списке дел"""
    
    print('Что добавим в список дел?')
    
    query = listen_command()
        
    with open('todo-list.txt', 'a', encoding='utf-8') as file:
        file.write(f'❗️ {query}\n')
        
    return f'Задача {query} добавлена в todo-list!'


def play_music():
    """Воспроизвести случайный mp3 файл"""
    
    files = os.listdir('music')
    random_file = f'music\\{random.choice(files)}'
    os.system(f'start "" "{random_file}"')
    
    return f'Танцуем под {os.path.basename(random_file)} 🔊🔊🔊'


def main():
    print("Программа слушает. Скажите команду...")
    while True:
        try:
            query = listen_command()
            
            if query in commands_dict['commands']['exit']:
                print("Программа завершается. До свидания!")
                break
            
            command_found = False
            for k, v in commands_dict['commands'].items():
                if query in v:
                    result = globals()[k]()
                    print(result)
                    command_found = True
                    break
            
            if not command_found:
                print("Команда не распознана. Попробуйте еще раз.")
            
            print("\nГотов к следующей команде...")
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем. До свидания!")
            break

if __name__ == '__main__':
    main()
