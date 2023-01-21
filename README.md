# PostgreSQL-Avia-Client

Клиент для администрирования PostgreSQL базы данных авиабилетов с возможностью авторизации, введения произвольного SQL-запроса, редактирования поля БД, добавления строки, выгрузки таблицы в CSV формат c удобным пользовательским интерфейсом

Файл sign.py и файл sign.ui отвечает за мозги и вид страницы подключения базы данных

![image-20230121183726051](C:\Users\maks-\AppData\Roaming\Typora\typora-user-images\image-20230121183726051.png)

Файл interface.py главная страница клиента, встречающая окном, где можно ввести произвольный SQL запрос, либо выбрать шаблон из кнопок сверху

![image-20230121184127308](C:\Users\maks-\AppData\Roaming\Typora\typora-user-images\image-20230121184127308.png)

Также клиент предоставляет функцию просмотра отдельных таблиц базы данных

![image-20230121184211041](C:\Users\maks-\AppData\Roaming\Typora\typora-user-images\image-20230121184211041.png)

Где присутствуют кнопки сохранения изменений ![image-20230121184325011](C:\Users\maks-\AppData\Roaming\Typora\typora-user-images\image-20230121184325011.png), обновления таблицы ![image-20230121184338720](C:\Users\maks-\AppData\Roaming\Typora\typora-user-images\image-20230121184338720.png), выгрузка таблицы в CSV формат ![image-20230121184347874](C:\Users\maks-\AppData\Roaming\Typora\typora-user-images\image-20230121184347874.png), операция вставки строки ![image-20230121184356661](C:\Users\maks-\AppData\Roaming\Typora\typora-user-images\image-20230121184356661.png)

