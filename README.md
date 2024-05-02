## Ссылка:

https://starbuzzand2.glitch.me/

## Файлы проекта:

- app.py - основной файл, из которого происходит запуск сайта
- папка templates содержит html файлы, которые отображают различные страницы
- папка static содержит:
  - 2 файла (starbuzz.css, styledform.css) с настройками стилей страниц
  - yandex_map.js - файл, отвечающий за отображение ближайших кофейн в виде яндекс карт в вкладке "Find store"
  - coffe.json - файл, содержащий информацию о кофе
  - папка images содержит все изображения, используемые на сайте

## Вкладки
/ - домашняя страница, на которой содержится вся информация о проходящих акциях и событиях

/ menu - страница, содержащая все напитки и еду, в качестве товаров, там расписаны их названия и краткая характеристика

/ recipes - на этой странице расположены ссылки на страницы с рецептами кофе, в виде стильных карточек с картинками и краткими описаниями

/ find a store - страница где можно указать ближайший к вам магазин, в который прийдет заказ, где его можно будет забрать или откуда будет происходить доставка

/ cart - страница корзины, в которой хранятся все добавленные в корзину товары и, в которой можно перейти на страницу оплаты товаров

/ profile - страница настройки своего профиля, где можно изменить свое имя, фамилию, номер телефона и почту, а также указать адрес проживания, по которому в дальнейшем будет происходить доставка

## Функционал
- Заказ доставки кофе и мучных продукций на дом
- Заказ кофе и мучных продукций в пункт выдачи
- Можно самостоятельно приготовить кофе по нашему рецепту, т.к. у нас все рецепты открыты для просмотра
- Возможность редактирования профиля
- Можно прочитать информацию про наше кафе и наше кофе

## Руководство по использованию

1) Для запуска сервера запустить файл app.py в терминале
2) Затем перейти по локальному ip (127.0.0.1:5000)
3) Для авторизации на сайте нажать "Join now", ввести необходимые данные и нажать кнопку "Login", далее войти в аккаунт
4) Для заказа кофе зайдите на вкладку "Menu", выберите подходящий товар и добавьте его в корзину
5) Затем оплатите заказ и ожидайте доставки

## Функционал админа

- Добавление адресов магазинов
- Добавление новых позиций в меню
