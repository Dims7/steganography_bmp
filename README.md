# Стеганография
Версия 1.0

Автор: Ларин Дмитрий КН-201

##Описание
Данное приложение позволяет зашифровывать текст в .bmp файл. 

##Требования для запуска
* Python версии 3.6

##Реализованные требования
* Стеганография типа LSB (+ указание параметров)
* Утилита для запаковки и распаковки данных
* Чексуммы
* Сохранение имени файла
* Не использовать готовый модуль работы с графическим форматом

##Состав файлов
* main.py - главный файл + обработчик аргументов командной строки
* converter.py - пакет, отвечающий за перевод целых чисел в байты и наоборот
* crypter.py - пакет, отвечающий за шифрование текста и создание хэша
* stegonography.py - главный пакет. Содержит методы для непосредственно шифровки и дешифровки из .bmp файла
* tests.py - пакет с модульными тестами

##Параметры запуска
Для запуска тестов можно использовать "python3.6 tests.py"

Для запуска самой программы необходимо прописать "python3.6 main.py" со следующими аргументами:
* -e	зашифровать сообщение
* -d	дешифровать сообщение
* -c	удалить зашифрованное сообщение, если оно есть (совместимо с -d -e)
* -f	после этого аргумента необходимо ввести путь к файлу
* -m	после этого аргумента необходимо ввести сообщение (совместимо с -e)
Порядок аргументов не важен.

Примеры запуска:
python3.6 main.py -f some.bmp -m "Some text" -e
python3.6 main.py -f some.bmp -m "Some text" -e -c
python3.6 main.py -f some.bmp -d
python3.6 main.py -f some.bmp -d -c
python3.6 main.py -f some.bmp -c

##Принцип работы
Программа находит начало массива пикселей .bmp файла. Сдвигает его и на оставшееся место вставляет зашифрованный текст + его хэш + его длину для последующей проверки на целостность. После изменяет поле с размером .bmp файла. По итогу получается внешне тот же самый .bmp файл с зашифрованные текстом.
Декодировщик смотрит на координаты начала массива пикселей.  После считывает длину кодированного сообщения. Потом считывает всё сообщение, сравнивает сообщение с его хэшом и если всё совпадает, то выводит закодированное сообщение.
