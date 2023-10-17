from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from lyricsgenius import Genius
from dotenv import load_dotenv
import keyboards as kl
import urllib.request
import asyncio
import shutil
import yt_dlp
import uuid
import bd
import re
import os



load_dotenv()
bot = Bot(os.getenv("Token1"))
dp = Dispatcher(bot=bot, storage=MemoryStorage())
genius = Genius(os.getenv('genius_token'))

async def on_startup(_):
    await bd.sq_start()


class ButtonState(StatesGroup):
    waiting_for_message = State()
    button1_pressed = State()
    catalog_pressed = State()
    support_pressed = State()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await bd.cmd_start_db(message.from_user.id,
                          fname=message.from_user.first_name,
                          username=message.from_user.username)
    await message.answer(f"Здравствуй, {message.from_user.first_name.title()}, меня зовут Алекс, чем займемся?",
                         reply_markup=kl.support_but)

@dp.message_handler(commands=["search_song"])
async def search_song(message: types.Message):
    await ButtonState.waiting_for_message.set()
    await message.answer(os.getenv("but_2"), reply_markup=kl.back)

@dp.message_handler(commands=["search_text"])
async def search_text(message: types.Message):
    await ButtonState.button1_pressed.set()
    await message.answer(os.getenv("but_1"), reply_markup=kl.back)

@dp.message_handler(commands=["support"])
async def search_song(message: types.Message):
    await ButtonState.support_pressed.set()
    await message.answer(os.getenv("but_3"), reply_markup=kl.back)

@dp.message_handler(commands=["cancel"], state=[ButtonState.support_pressed, ButtonState.waiting_for_message, ButtonState.button1_pressed,
                           ButtonState.catalog_pressed])
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Здравствуй, {message.from_user.first_name.title()}, меня зовут Алекс, чем займемся?",
                         reply_markup=kl.support_but)

@dp.message_handler(commands=['send_broadcast'])
async def send_broadcast_command(message: types.Message):
    if message.from_user.id == 6419978055:
        await message.reply("Введите текст сообщения для рассылки:")
        await ButtonState.waiting_for_message.set()


@dp.callback_query_handler()
async def callback_keyboard1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "button1":
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=os.getenv("but_1"), reply_markup=kl.back)
        await ButtonState.button1_pressed.set()
    elif callback_query.data == "button2":
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=os.getenv("but_2"), reply_markup=kl.back)
        await ButtonState.waiting_for_message.set()
    elif callback_query.data == "button3":
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=os.getenv("but_3"), reply_markup=kl.back)
        await ButtonState.support_pressed.set()
    elif callback_query.data == "catalog":
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=os.getenv("but_4"),
                                    reply_markup=kl.catalog_but)
        await ButtonState.catalog_pressed.set()


@dp.callback_query_handler(state=ButtonState.catalog_pressed)
async def handle_catalog_buttons(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "catalog1.1":
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=kl.request0)
        await state.finish()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"Здравствуй, {callback_query.from_user.first_name.title()}, меня зовут Алекс, чем займемся?",
                               reply_markup=kl.support_but)
    elif callback_query.data == "catalog2":
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=f"Разработчиком и модератором данного бота является [Исмаил](https://t.me/laotzzu)\n"
                                         "Если у вас есть предложения по улучшению бота - пишите\nЕсли у бота возникли проблемы воспользуйтесь кнопкой Поддержка",
                                    parse_mode="MARKDOWN")
        await bot.answer_callback_query(callback_query.id)
        await state.finish()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"Здравствуй, {callback_query.from_user.first_name.title()}, меня зовут Алекс, чем займемся?",
                               reply_markup=kl.support_but)
    elif callback_query.data == "gohome":
        await state.finish()
        user_name = callback_query.from_user.first_name.title()
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=f"Здравствуй, {user_name}, меня зовут Алекс, чем займемся?",
                                    reply_markup=kl.support_but)


@dp.callback_query_handler(lambda callback_query: callback_query.data == "backk", state=[ButtonState.support_pressed, ButtonState.waiting_for_message,
                                  ButtonState.button1_pressed])
async def cancel_support(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_name = callback_query.from_user.first_name.title()
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text=f"Здравствуй, {user_name}, меня зовут Алекс, чем займемся?",
                                reply_markup=kl.support_but)


@dp.message_handler(state=ButtonState.button1_pressed)
async def get_lyrics(message: types.Message, state: FSMContext):
    try:
        lines = message.text.split(' - ')
        if len(lines) == 2:
            artist_name = lines[0]
            song_title = lines[1]
            song = genius.search_song(song_title, artist_name)
            if song is not None:
                lyrics = song.lyrics.replace("You might also like", "").strip()
                lyrics_lines = lyrics.split("\n")
                cleaned_lines = lyrics_lines[1:]
                cleaned_lyrics = ""
                for line in cleaned_lines:
                    if line.startswith("["):
                        cleaned_lyrics += "\n\n" + line
                    else:
                        cleaned_lyrics += "\n" + line
                cleaned_lyrics = cleaned_lyrics.strip()
                last_line_pattern = r"(?:\d+)?Embed$"
                cleaned_lyrics = re.sub(last_line_pattern, "", cleaned_lyrics)
                cleaned_lyrics = cleaned_lyrics.strip()
                song_title = f"Текст песни {artist_name.title()} - {song.title}:\n"
                output_text = f"{song_title}\n{cleaned_lyrics}"
                max_message_length = 4096
                if len(output_text) <= max_message_length:
                    keyboard = InlineKeyboardMarkup()
                    lyrics_url = song.url
                    lyrics_button = InlineKeyboardButton("Перейти к тексту", url=lyrics_url)
                    keyboard.add(lyrics_button)
                    await send_message_with_pagination(message.chat.id, output_text, reply_markup=keyboard)
                else:
                    messages = []
                    while len(output_text) > 0:
                        if len(output_text) <= max_message_length:
                            messages.append(output_text)
                            break
                        split_index = output_text[:max_message_length].rfind('\n\n')
                        if split_index == -1:
                            split_index = max_message_length
                        messages.append(output_text[:split_index].strip())
                        output_text = output_text[split_index:].strip()
                    for index, message_text in enumerate(messages):
                        if index == len(messages) - 1:
                            keyboard = InlineKeyboardMarkup()
                            lyrics_url = song.url
                            lyrics_button = InlineKeyboardButton("Перейти к тексту", url=lyrics_url)
                            keyboard.add(lyrics_button)
                            await send_message_with_pagination(message.chat.id, message_text, reply_markup=keyboard)
                        else:
                            await send_message_with_pagination(message.chat.id, message_text)
                            await state.finish()
                await state.finish()
                await cmd_start(message)
            else:
                await message.answer(os.getenv("search_text1"), reply_markup=kl.back)
        else:
            await message.answer(os.getenv("search_text2"), reply_markup=kl.back)
    except Exception as e:
        await message.answer(os.getenv("search_text3"), reply_markup=kl.sup)
        print(e)


@dp.message_handler(state=ButtonState.waiting_for_message)
async def download_query(message: types.Message, state: FSMContext):
    query = message.text.strip()
    if query == "/start":
        await bot.send_message(chat_id=message.chat.id,
                               text="Пожалуйста, введите название песни, либо нажмите /cancel для отмены")
    else:
        await download_song(query, message.chat.id)
        await state.finish()
        await cmd_start(message)


@dp.message_handler(state=ButtonState.support_pressed, content_types='any')
async def support(message: types.Message, state: FSMContext):
    user_info = f"First Name: {message.from_user.first_name}\n"
    user_info += f"Username: @{message.from_user.username}\n"
    forwarded_text = f"Support Request:\n\n{user_info}\nwith text:\n\n{message.text}"
    await bot.send_message(os.getenv("My_Group_Token"), forwarded_text)
    await state.finish()
    await message.answer(os.getenv("supportt"))
    await cmd_start(message)


async def send_message_with_pagination(chat_id, text, reply_markup=None):
    max_message_length = 4096
    if len(text) <= max_message_length:
        await bot.send_message(chat_id, text, reply_markup=reply_markup)
    else:
        messages = []
        while len(text) > 0:
            if len(text) <= max_message_length:
                messages.append(text)
                break
            split_index = text[:max_message_length].rfind('\n\n')
            if split_index == -1:
                split_index = max_message_length
            messages.append(text[:split_index].strip())
            text = text[split_index:].strip()
        for index, message_text in enumerate(messages):
            await bot.send_message(chat_id, message_text, reply_markup=reply_markup if index == 0 else None)


async def download_song(query: str, chat_id: int):
    try:
        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': '%(title)s.%(ext)s', 'default_search': 'ytsearch'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            download_message = await bot.send_message(chat_id=chat_id, text=os.getenv("download"))
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                video = info['entries'][0]
            else:
                video = info
            title = video['title']
            clean_title = re.sub(r'[-—\/:*?"<>|_]', ' ', title)
            duration = video.get('duration', 0)
            if duration > 900:
                await bot.send_message(chat_id=chat_id, text=kl.fmin)
                return
            unique_id = str(uuid.uuid4())
            mp3_file = f"{unique_id}.mp3"
            ydl.download([video['webpage_url']])
            audio_file = f"{clean_title}.webm"
            destination_dir = "music/"
            destination = os.path.join(destination_dir, mp3_file)
            absolute_audio_path = os.path.abspath(audio_file)
            shutil.copyfile(absolute_audio_path, destination)
            thumbnail_url = video['thumbnail']
            thumbnail_file = f"{clean_title}.jpg"
            thumbnail_path = os.path.join(destination_dir, thumbnail_file)
            urllib.request.urlretrieve(thumbnail_url, thumbnail_path)
            absolute_path = os.path.abspath(destination)
            renamed_path = os.path.join(destination_dir, f"{clean_title}.mp3")
            os.rename(absolute_path, renamed_path)
            with open(renamed_path, "rb") as audio, open(thumbnail_path, "rb") as thumbnail:
                await bot.send_audio(chat_id=chat_id, audio=audio, thumb=thumbnail, title=clean_title,
                                                    caption=f"[Alex ♫](https://t.me/musicalext_bot)",
                                                    parse_mode="MARKDOWN")
                await bd.song_count(chat_id)
                await bot.delete_message(chat_id=chat_id, message_id=download_message.message_id)
    except Exception as e:
        await bot.send_message(chat_id=chat_id, text=os.getenv("error"), reply_markup=kl.back)
        print(e)
    os.remove(renamed_path)
    os.remove(thumbnail_path)
    os.remove(absolute_audio_path)


async def send_broadcast_message(message_text):
    sqcon = bd.sq.connect('trll.db')
    cur = sqcon.cursor()
    users = cur.execute("SELECT tg_id FROM accounts").fetchall()
    for user_id in users:
        user_id = user_id[0]
        try:
            await bot.send_message(user_id, message_text)
            await asyncio.sleep(0.05)
        except Exception as e:
            print(f"An error occurred while sending a message to user {user_id}: {e}")


@dp.message_handler(state=ButtonState.waiting_for_message)
async def process_broadcast_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_text'] = message.text
    await state.finish()
    await send_broadcast_message(data['message_text'])
    await message.answer("Рассылка выполнена.")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
