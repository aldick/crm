# CRM system

https://b24-7hgmkz.bitrix24.kz/stream/
	
## Что должно быть в нашем проекте:

- Канбан система для упорядочивание заказов
- CRM система
- Учет товароа в складе
- Аналитика

В верхней панели заказа логотип BalqaimaQ. Также вкладки:
* Заказы
* Контакты
	+ Клиенты
	+ Сотрудники
	+ Компании
* Склад
	* Учет товаров
	* Список товаров
+ Аналитика 
	+ Продажи(общий и каждого товара)
	+ Зарплата

## Канбан система для упорядочивание заказов

На главном экране будет стоять на канбан с несколькоми столбцами. Менеджер добавляет новый заказ с помощью кнопки "+ Создать заказ". Заказ появляется в первом столбце. Этот заказ отправляет в Telegram и после подготовки заказа фасовщик нажимает кнопку готово. После этого заказ переходит на следующий этап.

В каждом этапе есть общая сумма за этот этап. 

Каждый заказ имеет свое место в каком либо столбце. Каждый заказ можно перемещать из одного этапа к следующему. Данные можно отфильтровать по времени (Сегодня, Вчера, На этой неделе, В этом месяце, В этом году, Своя дата). Заказ можно перемещать вниз для удаление его из канбан системы. При удалении заказа нужно написать причину удалении для последующего анализа. 

При добавлении заказа должен происходиться поиск клиента по номеру телефона. Если такой клиент не существует, должна появиться форма для создание нового клиента. Также при добавлениие заказа можно выбрать тип заказа(онлайн или оффлайн) и в зависимости от выбора он переходит на первый или последний этап.

При нажатии на заказ, открывается детальная информация о данном заказе(модель заказа). При нажатии на кнопку редактировать, можно редактировать поля пользователь, тип оплаты, дата заказа, адрес заказа, этап заказа, отзыв клиента. тип заказа. При нажатии на кнопку назад вернуться на главную страницу.

Модель заказа:
- Номер заказа (Первичный ключ)
- Пользователь (Внешний ключ)
- Товары
- Тип оплаты
- Дата заказа
- Адрес заказа
- Этап заказа
- Отзыв клиента
- Тип заказа (Онлайн, Оффлайн)

## CRM система

На главном экране список всех пользователей

Кнопка "Создать пользователя" покажет форму для создание нового пользователя

Модель пользователя:
- Номер телефона клиента (Первчиный ключ)
- Имя пользователя
- Адрес пользователя
- Дата создания пользователя
- Заказы
- Тип пользователя (Клиент, Компания, Работник)

На странице детальной информации клиента должен быть его заказы и общая сумма заказов и отзыв клиента

## Учет товаров в складе

Фасовщик может добавить товары на склад через тг бота или сайт. При добавление товара на учет, будет писать имя работника который слепил данный продукт. В проекте будет учитываться количество созданного продукта каждым работником,
для учета количество работы и соответсвенно его зарплаты
Будет происходить учет количество товаров и при низком количестве товаров будет приходить уведомление. При появление нового заказа, количество товаров на складе будет уменьшаться.

Модель товара:
- Номер товара
- Имя товара
- Количество
- Цена
- Себестоимость
- Описание
- Фото товара

## Раздел Аналитики

Аналитика выводит информацию об текущем и других месяцах. Аналитика показывает общию сумму прибыли и количество заказов.

На главной странице должен выводиться два графика (гистораммы) количество заказов и общию сумму денег. Также круговая диаграмма с процентами продаж каждого продукта. 

Также она показывает количество затрат на работников, продукты, счета, цех,
и другие расходы. Кроме того, будет выводиться самые популярные позиции за этот месяц.

Аналитика количество товаров созданным каждым работником в виде графика с прошлыми месяцами.
