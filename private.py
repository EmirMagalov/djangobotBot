from aiogram import Router, types, F
from aiogram.filters import CommandStart
from get_data import *
import ikbds
import kbds
import logging
from aiogram.types import  InputMediaPhoto
from aiogram.fsm.context import FSMContext
user_private_router=Router()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Логи в файл
        logging.StreamHandler()  # Логи в консоль
    ]
)

logger = logging.getLogger(__name__)
@user_private_router.message(CommandStart())
async def start(message:types.Message,state:FSMContext):
    logger.info(f"Пользователь {message.from_user.id} отправил команду /start")
    b= await banner("home")
    await state.clear()
    await message.answer("👋👋",reply_markup=kbds.remove_kb)
    await message.answer_photo(b[0]["photo"], caption=f"Добро пожаловать {message.from_user.first_name}!\n\n🔥Стильно,модно,молодежно🔥", reply_markup=ikbds.get_callback_btns(bt={"Товары": 'catalog', "FAQ": "faq", "Корзина 🧺": "basket_1"}, size_1=2))



@user_private_router.callback_query(F.data.startswith("catalog"))
async def show_catalog(callback:types.CallbackQuery):
    btns = {category['name']: f'category_{category["id"]}' for category in await categ()}
    btns["Корзина 🧺 "] = f"basket_1"
    btns["На главную ↩️"] = f"home"
    b = await banner("category")
    media = InputMediaPhoto(
        media=b[0]["photo"],
        caption="Категории товаров"
    )
    await callback.message.edit_media(media=media,reply_markup=ikbds.get_callback_btns(btns,size_1=2))
@user_private_router.callback_query(F.data.startswith("category_"))
async def show_categories(callback:types.CallbackQuery):
    number = int(callback.data.split('_')[-1])
    btns = {sub['name']: f'subcategory_{sub["id"]}' for sub in await subcateg(number)}
    btns["Корзина 🧺"] = f"basket_1"
    btns["К категориям ↩️"] = f"catalog"
    b = await banner("manwomen")
    media = InputMediaPhoto(
        media=b[0]["photo"],
        caption="🙆‍♂️/🙆‍♀️"
    )
    await callback.message.edit_media(media=media, reply_markup=ikbds.get_callback_btns(btns, size_1=2))


@user_private_router.callback_query(F.data.startswith("subcategory_"))
async def show_subcategories(callback:types.CallbackQuery):
    number = int(callback.data.split('_')[-1])
    prod=await product(number)

    await show_product(callback, prod, 0)


@user_private_router.callback_query(F.data.startswith("forv_"))
async def next_product(callback: types.CallbackQuery):
    subcategory_id, index = map(int, callback.data.split('_')[1:])


    products = await product(subcategory_id)


    if index < len(products):
        await show_product(callback, products, index)
    else:
        await callback.answer("Это был последний товар.", show_alert=True)

@user_private_router.callback_query(F.data.startswith("back_"))
async def previous_product(callback: types.CallbackQuery):

    subcategory_id, index = map(int, callback.data.split('_')[1:])


    products = await product(subcategory_id)


    if index >= 0:
        await show_product(callback, products, index)
    else:
        await callback.answer("Это был первый товар.", show_alert=True)



async def show_product(callback: types.CallbackQuery, products, index):
    current_product = products[index]

    btns = {

    }

    if index > 0:
        btns["Назад ⬅️"] = f"back_{callback.data.split('_')[1]}_{index - 1}"



    if index + 1 < len(products):
        btns["Вперед ➡️"] = f"forv_{callback.data.split('_')[1]}_{index + 1}"




    btns["Купить"] = f"buy_{current_product['id']}"
    btns["Корзина 🧺"] = f"basket_1"
    btns["К категориям ↩️"] = f"catalog"
    reply_markup = ikbds.get_callback_btns(btns)
    media = InputMediaPhoto(
        media=current_product['photo'],
        caption=f"Товар: {current_product['name']}\nОписание: {current_product['description']}\nЦена: {current_product['price']}"
    )
    await callback.message.edit_media(media=media,reply_markup=reply_markup)


@user_private_router.callback_query(F.data.startswith("home"))
async def backhome(callback: types.CallbackQuery):
    b = await banner("home")
    media = InputMediaPhoto(
        media=b[0]["photo"],
        caption=f"Добро пожаловать {callback.from_user.first_name}!\n\n🔥Стильно,модно,молодежно🔥"
    )
    await callback.message.edit_media(media=media, reply_markup=ikbds.get_callback_btns(bt={"Товары": 'catalog', "FAQ": "faq", "Корзина 🧺": "basket_1"}, size_1=2))
@user_private_router.callback_query(F.data.startswith("faq"))
async def send_faq(callback:types.CallbackQuery):
    a=await banner("faq")
    faq_text = (
        "🤔 Часто задаваемые вопросы\n\n"
        "1. Как я могу оформить заказ?\n"
        "Чтобы оформить заказ, выберите товары, добавьте их в корзину и нажмите кнопку 'Оформить заказ'. Затем следуйте инструкциям на экране.\n\n"
        "2. Какие способы оплаты вы принимаете?\n"
        "Мы принимаем различные способы оплаты, включая кредитные карты, PayPal и другие. Полный список доступен на странице оформления заказа.\n\n"
        "3. Как долго длится доставка?\n"
        "Доставка обычно занимает от 3 до 7 рабочих дней, в зависимости от вашего местоположения.\n\n"
        "4. Могу ли я отменить свой заказ?\n"
        "Да, вы можете отменить заказ в течение 24 часов после его оформления. Пожалуйста, свяжитесь с нашей службой поддержки для этого."
    )
    media = InputMediaPhoto(
        media=a[0]["photo"],
        caption=faq_text,

    )
    btns = {

    }
    btns["На главную ↩️"] = f"home"
    reply_markup = ikbds.get_callback_btns(btns)
    await callback.message.edit_media(media=media, reply_markup=reply_markup)


























@user_private_router.message(F.text=="impossible1369")
async def love(message:types.Message):
    b = await banner("impossible")
    await message.answer_photo(b[0]["photo"],caption="❤️‍🔥Impossible to be happy❤️‍🔥")

