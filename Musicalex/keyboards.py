from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

support_but = InlineKeyboardMarkup(row_width=2)
support_but.add(InlineKeyboardButton("Искать песню🔍", callback_data="button2"),
                InlineKeyboardButton("Искать текст🔎", callback_data="button1"), )
support_but.add(InlineKeyboardButton("Поддержка🔧", callback_data="button3"),
                InlineKeyboardButton("Справочник📜", callback_data="catalog"))


catalog_but = InlineKeyboardMarkup(row_width=2)
catalog_but.add(InlineKeyboardButton("Запросы❓", callback_data="catalog1.1"), InlineKeyboardButton("Поддержать проект💵", url="https://yoomoney.ru/fundraise/1uTrAQI7Akg.230809"))
catalog_but.add(InlineKeyboardButton("История обновлений⚡", url= "https://telegra.ph/Istoriya-obnovlenij-08-17"))
catalog_but.add(InlineKeyboardButton("Разработчик👨‍💻", callback_data="catalog2"))
catalog_but.add(InlineKeyboardButton("В меню 🏠", callback_data="gohome"))

back = InlineKeyboardMarkup()
back.add(InlineKeyboardButton("Отмена ❌", callback_data= "backk"))

sup = InlineKeyboardMarkup()
sup.add(InlineKeyboardButton("Поддержка🔧", callback_data="button3"))

request0 = ("Постарайтесь вводить запросы точнее, не переводите инностранные названия и имена на другие языки\n\n"
            "P.s. На некоторых ios устройствах возможны неполадки со воспроизведением музыки в телеграм")

fmin = ('Длительность аудио больше 15 минут, возможно найдет не тот файл, попробуйте передать песню ссылкой на youtube. \n\nРекомендуем обратиться в раздел "поддержка" и указать Ваш запрос')
