# 1C_TASK4

Чилилова Аминат Ахмедовна
Задача №4 / Системное программирование


__Запуск:__
1) Запустить Server.py.
2) Запустить несколько экземпляров Сlient.py, указав адрес сервера.

__Эксперимент:__
1) В консоли Server доступны следующие команды:
   1.1) start - начало нового эксперимента
   
   1.2) leaderboard - просмотр таблицы лидеров на сервере
   1.3) stop - завершения работы сервера
   1.4) waiting - просмотра списка ожидающих ответов
   
3) В консолях Сlient доступны следующие команды:
   guess - ввод попытки (затем предполагаемое число)
   history - просмотр истории попыток в данном эксперименте
   disconnect - отключиться от эксперимента


__Примечания (дороботки):__
Таблица лидеров хранится в памяти сервера и не сохраняется между запусками. Планировалось подкрутить sqlite3, но не хватило времени.
