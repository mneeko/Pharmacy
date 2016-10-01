# Проект онлайн-магазин

## Постановка задачи

*Цитата из wiki.cs.hse.ru:*

> Сервис состоит из: витрины/каталога товаров, разбитых по категориям; корзины, в которую пользователь может добавлять покупки; для электронных товаров реализована возможность скачать (или получить по почте) и оплата с помощью PayPal (наиболее простой для интеграции, для проекта достаточно показать работу с разработческим апи PayPal) или другими системами оплаты. Для неэлектронных товаров должна быть возможность указать их наличие, при покупке количество изменяется. В магазине могут быть промоакции: скидка при оформлении заказа по промокоду, скидка при заказе на определенную сумму, временная скидка на конкретную категорию товаров.

## Реализация критериев

#### Минимальная функциональность:

- [x] Витрина магазина с категориями
- [x] Корзина пользователя, в которую можно добавлять или удалять товары.
- [x] После оформления заказа, письмо с данными о заказе и пользователе отправляется на почту владельца магазина
- [x] Приложение защищено от инъекций к базе

#### На хорошо: 

- [x] Приложение работает с неэлектронными товарами, меняется количество доступного товара.
- [ ] Приложение защищено от XSS-атак.	

#### На отлично:

- [x] В приложении есть возможность оплатить с помощью сервисов онлайн-платежей.
      Сервис готов к запуску (по чеклисту выполнено все или почти все)

## Реализованные возможности

- Динамически изменяющийся каталог, где отображаются товары, отсортированные по категориям. Товар всегда можно положить в корзину прямо из каталога.
- На отдельной страничке товара даны более полные его характеристики. Оттуда также можно положить товар в корзину.
- Корзина,  в которой присутствует вся необходимая информация: список товаров, их количество, цена каждого товара и суммарная стоимость заказа. Также можно менять количество покупаемых товаров. Корзина сохраняется даже если пользователь закрыл браузер и потом вновь вернулся на сайт.
- Оплата производится при помощи системы онлайн-платежей PayPal. При этом если пользователь попытается купить товар в количестве, превосходящем имеющееся, этот товар будет исключен из корзины.

## Модели

В соответствии со стандартом Django, классы моделей, используемые в проекте, были реализованы в файле models.py:

- Category — категория товара
- Product — товар. Каждый товар может быть связан с одной или несколькими категориями. Количество товаров может меняться
- ProductImage — изображение товара *(не была задействована в проекте из-за технических сложностей)*
- SelectedProduct — товар, выбранный пользователем

Более подробно о моделях и их взаимосвязях можно узнать из файла [pharmacy-db](./schemes/pharmacy-db.png).

## Шаблоны

- base.html — оболочка для остальных страниц, содержащая верхнее меню, подключаемая при помощи `{% extends ... %}`
- cart.html — корзина пользователя
- catalogue.html — каталог товаров
- help.html — страничка со справкой для покупателя
- history.html — история заказов пользователя
- index.html — главная страница магазина
- item.html — страница конкретного товара
- payment.html — страница оплаты, содержащая ссылку на форму оплаты paypal
- registratiom/login.html — страница логина пользователя
- registratiom/registration_form.html — страница регистрации пользователя

## Работа бэкенда

Осуществляется при помощи стандартных способов фреймворка Django. Для получения обратной связи посланный пользователем запрос идентифицируется с паттерном внутри файла urls.py. Затем аргументы передаются на вход соответствующей функции в view.py, которая, обработав запрос, либо возвращает новую страницу, либо обновляет текущую.

Приведем пример. Пусть пользователь находится в каталоге и хочет выбрать категорию товаров 'Y' с slug 'x' и просмотреть товары, к ней относящиеся. Ссылка выглядит как `catalogue/x`.  Она удовлетворяет одному из паттернов в urls.py:

```python
url(r'^catalogue/(?P<slug>.*)$', CatalogueView.as_view(), name='catalogue')
```

Далее вызывается метод `get_context_data` класса `CatalogueView` из файла views.py:

```python
class CatalogueView(TemplateView):
    template_name = 'catalogue.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        if kwargs['slug']:
            category = get_object_or_404(Category, slug=kwargs['slug'])
            context['products'] = category.products.all()
        else:
            context['products'] = Product.objects.all()
        return context
```

Так как в данной ситуации slug был определен, выполняется условие if'а, выбирается категория, соответствующая данному slug'у, и передается список товаров, связанных с данной категорией. Если категория с таким slug'ом найдена не будет, вернется ошибка 404. Если же был совершен просто переход в каталог, в нем будут выведены все имеющиеся товары.