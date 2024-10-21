import os
from aiogram import Bot
from openpyxl import load_workbook
from add_basket_data import *
from private import *
import kbds
from datetime import datetime
from dotenv import load_dotenv
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext

load_dotenv()

basket_router=Router()



@basket_router.callback_query(F.data.startswith("basket_"))
async def basket(callback:types.CallbackQuery):
    user_id=int(callback.from_user.id)
    a = await get_basket(user_id)

    if a and a[0]["product"]:

        q=a[0]["quantity"]
        await show_basket(callback, a, 0,quan=int(q))
    else:
        await callback.answer("Корзина пустая")

@basket_router.callback_query(F.data.startswith("buy_"))
async def buy(callback:types.CallbackQuery):

    number = int(callback.data.split('_')[-1])
    user_id=int(callback.from_user.id)
    prod= await one_product(number)
    data={
        "user":int(callback.from_user.id),
        "product_id":number,
        "quantity": 1

    }

    logger.info(f"Пользователь {callback.from_user.id} добавил товар {prod[0]['name']} в корзину")
    await add_basket(data)
    await callback.answer(f"Товар ({prod[0]['name']}) добавлен")



@basket_router.callback_query(F.data.startswith("del_"))
async def delete(callback:types.CallbackQuery):
    basket_id, index = map(int, callback.data.split('_')[1:])
    user_id = int(callback.from_user.id)


    a = await get_basket(user_id)


    if index < 0 or index >= len(a):
        await callback.answer("Некорректный индекс товара.", show_alert=True)
        return


    data = {
        "product_id": a[index]["product"],
    }


    await del_basket(user_id, data)


    updated_basket = await get_basket(user_id)


    if updated_basket:

        if index >= len(updated_basket):
            index = len(updated_basket) - 1

        await show_basket(callback, updated_basket, 0, updated_basket[index]["quantity"])
    else:
        from private import backhome
        await backhome(callback)
        # b = await banner("basket")
        #
        # btns = {
        #     "К подкатегориям ↩️": "category_1",
        # }
        # media = InputMediaPhoto(
        #     media=b[0]["photo"],
        #     caption="Корзина пустая"
        # )
        # await callback.message.edit_media(
        #     media=media,
        #     reply_markup=ikbds.get_callback_btns(btns, size_1=1)
        # )




@basket_router.callback_query(F.data.startswith("forvbasket_"))
async def next_product_basket(callback: types.CallbackQuery):
    basket_id, index = map(int, callback.data.split('_')[1:])



    user_id = int(callback.from_user.id)
    a = await get_basket(user_id)


    if index < len(a):

        if a and a[index]["id"]:

            q = a[index]["quantity"]

            await show_basket(callback, a, index,quan=int(q))
    else:
        await callback.answer("Это был последний товар.", show_alert=True)

@basket_router.callback_query(F.data.startswith("backbasket_"))
async def previous_product_basket(callback: types.CallbackQuery):

    subcategory_id, index = map(int, callback.data.split('_')[1:])

    user_id = int(callback.from_user.id)
    a = await get_basket(user_id)



    if index >= 0:

        if a and a[index]["id"]:

            q = a[index]["quantity"]
            await show_basket(callback, a, index, quan=int(q))
    else:
        await callback.answer("Это был первый товар.", show_alert=True)

@basket_router.callback_query(F.data.startswith("plus_"))
async def plus(callback: types.CallbackQuery):
    user_id = int(callback.from_user.id)
    id, index = map(int, callback.data.split('_')[1:])



    a = await get_basket(user_id)
    data = {
        "product_id": a[index]["product"],
        "plus": True,

    }

    await plusminus_basket(user_id, data)
    await show_basket(callback, a, index,quan=a[index]["quantity"]+1)


@basket_router.callback_query(F.data.startswith("minus_"))
async def minus(callback: types.CallbackQuery):
    user_id = int(callback.from_user.id)
    id, index = map(int, callback.data.split('_')[1:])
    a = await get_basket(user_id)
    data = {
        "product_id":a[index]["product"],
        "minus": True,

    }

    a= await get_basket(user_id)

    if a[index]["quantity"]>1:
        await plusminus_basket(user_id, data)
        await show_basket(callback, a, index, quan=a[index]["quantity"] - 1)






async def show_basket(callback: types.CallbackQuery, bask_products, index,quan=0):
    current_product = bask_products[index]


    btns = {

    }

    btns["-"] = f"minus_{callback.data.split('_')[1]}_{index}"
    btns["+"] = f"plus_{callback.data.split('_')[1]}_{index}"

    if index > 0:
        btns["Назад ⬅️"] = f"backbasket_{callback.data.split('_')[1]}_{index - 1}"



    if index + 1 < len(bask_products):
        btns["Вперед ➡️"] = f"forvbasket_{callback.data.split('_')[1]}_{index + 1}"



    btns[f"Оплатить ({len(bask_products)} товара)"] = f"pay_"
    btns["Удалить 🗑️"] = f"del_{callback.data.split('_')[1]}_{index}"
    btns["К категориям ↩️"] = f"catalog"

    reply_markup = ikbds.get_callback_btns(btns,size_1=2)

    media = InputMediaPhoto(
        media=f"https://emirmagalov13.pythonanywhere.com{current_product['product_photo']}",
        caption=f"Товар: {current_product['product_name']}\nЦена:{float(current_product['product_price'])*quan}\nКол-во: {quan}"
    )
    await callback.message.edit_media(media=media, reply_markup=reply_markup)


from fsm_add_adress import AddData

@basket_router.callback_query(F.data.startswith("pay_"))
async def pay(callback: types.CallbackQuery,bot:Bot,state:FSMContext):
    await callback.message.delete()
    user_id = int(callback.from_user.id)
    a = await get_basket(user_id)
    total_price = 0
    total_name = []
    for i in a:
        p_name = i["product_name"]
        p_quan = i["quantity"]
        p_price = float(i["product_price"]) * int(p_quan)
        total_name.append(p_name)
        total_price += p_price
    await callback.message.answer(f"Оплата товара ({','.join(total_name)}) на сумму {total_price} Руб.")
    await callback.message.answer("Как тебя зовут?",reply_markup=kbds.cancel.as_markup(resize_keyboard=True))
    await state.set_state(AddData.name)


    # await bot.send_invoice(
    #     chat_id=user_id,
    #     title=",".join(total_name),
    #     description=f"Опалта товаров на сумму {total_price}",
    #     payload=",".join(total_name),
    #     provider_token=os.getenv("YOOTOKEN"),
    #     currency=os.getenv("CURRENCY"),
    #     start_parameter="test",
    #     prices=[LabeledPrice(label="Zakaz", amount=100*100)]
    #
    # )


