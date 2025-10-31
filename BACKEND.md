Структура БД проекта So_Buy. Версия MVP:
    Модель CustomUser(Пользователь) (Кастомная модель наследуется от встроенной модели AbstractUser):
        Поля:
            email(Электронная почта)
            phone (Номер телефона)
            balance (количество денег на счёте)
    Модель SellerProfile(Продавец) (Модель наследуемая от кастомной модели User)
        Поля:
            user (связь с таблицей User с помощью OneToOneField)
            company_name (название компании)
            logo (логотип)
    # Так как модель Buyer пока что не имеет своих уникальных полей она будет реализована в модели Transaction в виде поля buyer которое ссылается на кастомную модель User 
    Модель Product(Товар)
        Поля:
            seller (связь с таблицей Seller через ForeignKey)
            name (Название товара)
            price (Цена)
            images (Изображение)
            description (Описание)
            total_amount (Общее количество товара)
    Модель Transaction(Транзакция)
        Поля:
            seller (связь с таблицей Seller)
            buyer (ссылка на модель User через OneToOneField)
            product (связь с таблицей Product)
            quantity_of_goods_purchased (количество покупаемого товара)
            transaction_status (Статус транзакции)


