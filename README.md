# Описание #
Скрипт для мониторинга показателей удачи на пуле

# Установка #
1. Получить скрипт из репозитория
```bash
git clone 
```
2. Создать файл конфигурации
```bash
cp ./connections.template.py ./connections.py
```
# Настройка #
1. Уставить необходимые пакеты
```bash
pip3 install -r requirements.txt
```
2. Заполнить файл с параметрами для подключения ко всем серверам.
```
connections.py
```
# Использование #
1. Выполнить скрипт
```
python3 ./main.py
```