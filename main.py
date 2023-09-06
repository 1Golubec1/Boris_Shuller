import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import time
import sqlite3
from _config_ import *
from functions import FUNCTIONS
from move_bot import MOVE_BOT
from func_bj import  FUNCS_BJ
from func_durack import FUNC_DURACK
import json
import datetime
# --------------------------------------------------------------------------
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
func = FUNCTIONS()
funcs_bj = FUNCS_BJ
mv_bt = MOVE_BOT
func_dr = FUNC_DURACK
connect = sqlite3.connect(name_baz)
cursor = connect.cursor()
# ['1084337847', '899364641', '716753284']
# f = json.load(open("players.json", "r", encoding="UTF-8"))
# id_nm = []
# for i in f.keys():
#     id_nm.append((i, f[i]["NAME"]))


def move_pl_bj(user_id):
    deck_cards_bj = func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_black_jack"))
    name = func.get_variable(connect, user_id, "choose_ryka").replace("\'", "")
    ryka_pl_bj = func.create_list_deck_cards(func.get_variable(connect, user_id, name))
    ryka_pl_bj.append(deck_cards_bj.pop(0))
    func.save_info(connect, user_id, func.get_variable(connect, user_id, "choose_ryka").replace("\'", ""),str(ryka_pl_bj))
    func.save_info(connect, user_id, "deck_black_jack", str(deck_cards_bj))
    if funcs_bj.check_victory(connect, user_id,func.get_variable(connect, user_id, "choose_ryka").replace("\'", "")) == 2:
        func.save_info(connect, user_id, "state", "BEG_MOVE_PL_JB")
    if funcs_bj.check_victory(connect, user_id,func.get_variable(connect, user_id, "choose_ryka").replace("\'", "")) == 1:
        return True

def Generation_Nik_Name():
    name = open("Name.txt", "r", encoding="UTF-8").read().split("\n")
    adje = open("Adjectives.txt", "r", encoding="UTF-8").read().split("\n")
    niks = func.check_nik(connect)
    nik = random.choice(adje) + "_" + random.choice(name)
    if nik not in niks:
        return nik
    else:
        return Generation_Nik_Name()


@dp.message_handler(commands=['check_pl'])
async def check_pll(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id in ADMINS:
        func.save_info(connect, user_id, "state", "SEARCH")
        await message.answer("Пришлите id пользователя, чтобы начать поиск")
@dp.message_handler(commands=['change_info'])
async def change_info(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id in ADMINS:
        func.save_info(connect, user_id, "state", "CHANGE")
        await message.answer("Выберите действие", reply_markup=change_info_kb)

@dp.message_handler(commands=['admin_command'])
async def admin_command(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id in ADMINS:
        await message.answer("/check_pl - проверка наличия id пользователя\n/change_info - изменить информацию ползователя\n/send_mes - для отправки сообщения")

@dp.message_handler(commands=['send_mes'])
async def sen_mess(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id in ADMINS:
        ms = str(open('Mess',"r",encoding="UTF-8").read())
        await message.answer(f"Текст, для рассылки: {ms}",reply_markup=ch_ms)
        func.save_info(connect, user_id, "state", "send_mes")

@dp.message_handler(commands=['contact'])
async def cont(message: types.Message):
    await message.answer(
        "Связаться с разработчиками можно по следующим ссылкам (отвечаем на конструктивные и понятные сообщения, голосовые не будут прослушаны, спам – неприемлем):")
    await message.answer("https://t.me/G0lubec")
    await message.answer("https://t.me/Snailid")

@dp.message_handler(commands=['up_balance'])
async def rep_sh(message: types.Message):
    user_id = str(message.from_user.id)
    now = datetime.datetime.now()
    day = now.day
    if func.get_variable(connect, user_id, "day_cash") != str(day):
        await message.answer(f"Баланс в BlackJack повысился на 50\nТеперь он равен {float(func.get_variable(connect, user_id, 'rating_bj'))+50}.")
        cash = float(func.get_variable(connect, user_id, 'rating_bj'))+50
        func.save_info(connect, user_id, "rating_bj", cash)
        func.save_info(connect, user_id, "day_cash", str(day))
    else:
        await message.answer("Вы сегодня уже пополняли баланс.")

@dp.message_handler(commands=['set_pl'])
async def get_player(message: types.Message):
    if func.get_variable(connect, message.from_user.id, "id") == '1084337847':
        # print(func.GET_PLAYERS(connect))
        for i in [('899364641', 'Преисполненный_Физик'), ('801914089', 'iris0_o'), ('1969876530', 'Erny_Schwarz'), ('1425477866', 'meowmeow01'), ('1631348467', 'GoluAny'), ('804674317', 'Серо-арахисовый_Компрессор'), ('905857249', 'Гробовой_Крыс'), ('234736473', 'Поразительный_Полководец'), ('456022925', 'unique_vlados'), ('788916599', 'dgeaniusd'), ('1561691029', 'Болезный_Гоблин'), ('1582442781', 'GryLdy'), ('870871569', 'Призрачный_Царь'), ('5607638958', 'volno2343'), ('1418792611', 'Звероподобный_Парламентер'), ('710637673', 'ssppooppss'), ('5290973513', 'Забытый_Факториал'), ('5703956237', 'Оптический_Парламентер'), ('180624767', 'Электронный_Жираф'), ('5042800976', 'Alex_Pauluss'), ('442892113', 'iskorkaaaaaaa'), ('371319883', 'banannawork')]:
            func.add_old_players(connect, cursor, i[0], i[1])
@dp.message_handler(commands=['cou_cards'])
async def cou_card(message: types.Message):
    user_id = str(message.from_user.id)
    if func.get_variable(connect, user_id, "state") == "BEG_MOVE_BOT" or func.get_variable(connect, user_id, "state") == "OTBIV" or func.get_variable(connect, user_id, "state") == "BEG_MOVE_PL":
        await message.answer(f"Колличество кард в колоде: {str(len(func.create_list_deck_cards(func.get_variable(connect,  message.from_user.id, 'deck_cards'))))}")
    else:
        await message.answer("Вы сейчас не играете в Дурака ♦️.")

@dp.message_handler(commands=['send_obnv'])
async def send_obn(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        id = func.send_message(connect)
        for i in id:
            try:
                func.save_info(connect, i, "state", "START")
                await bot.send_message(i,MS, reply_markup=main_menu)
            except:
                continue
    else:
        await message.answer("У вас нет доступа!")

@dp.message_handler(commands=['trump_card'])
async def kozar(message: types.Message):
    user_id = str(message.from_user.id)
    if func.get_variable(connect, user_id, "state") == "BEG_MOVE_BOT" or func.get_variable(connect, user_id,"state") == "OTBIV":
        await message.answer(f'Козырь: {func.get_variable(connect,str(message.from_user.id), "kozar")}')
    else:
        await message.answer("Вы сейчас не играете в Дурака ♦️.")
@dp.message_handler(commands=['start'])
async def start_menu(message: types.Message):
    user_id = str(message.from_user.id)
    func.Connect(cursor, connect)
    nik = str(message.from_user.username)
    if func.check_pl(cursor, user_id, connect):
        if nik != "None":
            func.save_info(connect, user_id, "state", "REG")
            nik2 = Generation_Nik_Name()
            func.save_info(connect, user_id, "prop_nik", nik2)
            await message.answer(f"Ваше текущие имя: {nik}, не хотите поменять его на '{nik2}'?",
                                 reply_markup=gen_nik_kb)

        if nik == "None":
            nikk = Generation_Nik_Name()
            func.save_info(connect, user_id, "name",nik)
            await message.answer(
                f"Так как мы не смогли найти ваше имя в Telegram (возможно вы его не задали), вам было автоматически присвоено следующие имя: '{nikk}'.")
            await message.answer(f"{Krasota} {Vstyplenie1}", reply_markup=main_menu)
            await message.answer(f"{Update}")


    else:
        await message.answer(f"{Krasota} {Vstyplenie1}", reply_markup=main_menu)
        await message.answer(f"{Update}")


@dp.message_handler()
async def Game(message: types.Message):
    players = func.get_players()
    user_id = str(message.from_user.id)

    # ----------------------------------------------------------------Для техподдержки--------------------------------------------------------------------------
    if message.text == "Изменить информацию" and func.get_variable(connect, user_id, "state") == "CHANGE":
        await message.answer("Вам нужен список названий столбцов?",reply_markup=choice_kb)
        func.save_info(connect, user_id, "state", "CHOICE_CH")

    if (message.text == "Да" or message.text == "Нет") and func.get_variable(connect, user_id, "state") == "CHOICE_CH":
        if message.text == "Да":
            await message.answer(func.get_name_st())
        await message.answer("Пример написания изменений:\nid пользователя, название столбца, новые данные\nЕсли нужно изменить информацию в нескольких столбцах, то поставьте ';' после написанной вами цифры",reply_markup=types.ReplyKeyboardRemove())
        func.save_info(connect, user_id, "state", "CHANGE_INFO")


    if func.get_variable(connect, user_id, "state") == "CHANGE_INFO" and message.text != "Да" and message.text != "Нет":
        if ";" in message.text:
            new_info = list(map(lambda x: x.split(","),message.text.split(";")))
            for inf in new_info:
                try:
                    func.save_info(connect, inf[0], inf[1],inf[2])
                    await message.answer("Данные успешно изменены", reply_markup=main_menu)
                    func.save_info(connect, user_id, "state", "START")
                except:
                    await message.answer("Произошла ошибка")
        else:
            new_info = message.text.split(",")
            try:
                func.save_info(connect, new_info[0],new_info[1],new_info[2])
                await message.answer("Данные успешно изменены", reply_markup=main_menu)
                func.save_info(connect,user_id, "state", "START")
            except:
                await message.answer("Произошла ошибка")

    if message.text == "Сбросить информацию" and func.get_variable(connect, user_id, "state") == "CHANGE":
        await message.answer("Введите id пользователя", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Чтобы сбросить информацию нескольких пользователей пропишите ';' после 'id'")
        func.save_info(connect, user_id, "state", "RESET_INFO")

    if message.text.replace(";","").isdigit() and func.get_variable(connect, user_id, "state") == "RESET_INFO":
        if ";" not in message.text:
            reset = func.reset_info(connect, message.text)
            if reset == "Данные обнулены":
                await message.answer(reset, reply_markup=main_menu)
                func.save_info(connect, user_id, "state", "START")
            if reset == 1:
                await message.answer("Такого пользователя нету")
        else:
            list_id = message.text.split(";")
            for id in list_id:
                reset = func.reset_info(connect, id)
                if reset == "Данные обнулены":
                    await message.answer(f"Данные пользователя с id ({id}) обнулены", reply_markup=main_menu)
                    func.save_info(connect, user_id, "state", "START")
                if type(reset) == int:
                    await message.answer("Такого пользователя нету")


    if message.text and func.get_variable(connect, user_id, "state") == "SEARCH":
        result_func = func.search_info(connect, message.text)
        if type(result_func) == str:
            await message.answer(result_func, reply_markup=main_menu)
        else:
            await message.answer("Этот пользователь не найден", reply_markup=main_menu)
        func.save_info(connect, user_id, "state", "START")

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------Техподдержка авто--------------------------------------------------------------------------------------------
    if str(message.chat.id) == CHAT_ID and message.text.split()[0] == "Борис":
        ms = message.text.split()
        if ms[1] == "проверить_id":
            result_fn = func.search_info(connect, ms[2])
            if type(result_fn) == str:
                await Bot(token=TOKEN).send_message(CHAT_ID,"Пользователь найден")
            else:
                await Bot(token=TOKEN).send_message(CHAT_ID,"Пользователь не найден")
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if message.text == "Изменить" and func.get_variable(connect, user_id, "state") == "REG":
        nik2 = func.get_variable(connect, user_id, "prop_nik")
        func.save_info(connect, user_id, "name", nik2)
        func.save_info(connect, user_id, "state", "START")
        await message.answer(f"Теперь ваше имя: {nik2}")
        await message.answer(f"{Krasota} {Vstyplenie1}", reply_markup=main_menu)
        await message.answer(f"{Update}")

    if message.text == "Оставить мое имя" and func.get_variable(connect, user_id, "state") == "REG":
        func.save_info(connect, user_id, "state", "START")
        func.save_info(connect, user_id, "name", str(message.from_user.username))
        await message.answer(f"{Krasota} {Vstyplenie1}", reply_markup=main_menu)
        await message.answer(f"{Update}")

    if message.text == "Изменить текст" and func.get_variable(connect, user_id, "state") == "send_mes":
        await message.answer("Введите текст")
        func.save_info(connect, user_id, "state", "chage_text")

    if message.text != "Изменить текст" and func.get_variable(connect, user_id, "state") == "chage_text":
        ms = open("Mess", "w", encoding="UTF-8")
        ms.write(message.text)
        ms.close()
        mss = open("Mess","r",encoding="UTF-8")
        ms = str(mss.read())
        await message.answer(f"Текст для рассылки:\n{ms}",reply_markup=send_ms_kb)
        mss.close()
        func.save_info(connect, user_id, "state","send_mes")

    if message.text == "Сделать рассылку" and func.get_variable(connect, user_id, "state") == "send_mes":
        id = func.send_message(connect)
        mss = open("Mess","r",encoding="UTF-8")
        ms = mss.read()
        for i in id:
            try:
                func.save_info(connect, i, "state", "START")
                await Bot(token=TOKEN).send_message(i,ms, reply_markup=main_menu)
            except:
                continue
        mss.close()

    if message.text == "Не менять текст" and func.get_variable(connect,user_id, "state") == "send_mes":
        await message.answer("Выберите действие", reply_markup=send_ms_kb)

    if message.text == "Выйти"  and func.get_variable(connect,user_id, "state") == "send_mes":
        func.save_info(connect, user_id, "state","START")
        await message.answer("Вы оказались в главном меню", reply_markup=main_menu)

    # # ----------------------------------21------------------------------------- #
    if func.get_variable(connect, user_id, "state") == "START" and (message.text == "Сыграть в 21🃏"):
        func.save_info(connect, user_id, "ryka_pl_bj", str([]))
        func.save_info(connect, user_id, "state", "21")
        await message.answer(pravila_txt, reply_markup=rules_kb)

    if func.get_variable(connect, user_id, "state") == "21" and (message.text == "Правила📋"):
        await message.answer(rules_21_txt, reply_markup=vb_kb)


    if (message.text == "Играть 🎮" and func.get_variable(connect, user_id, "state") == "21") or (message.text == "Сыграть еще раз 🃏" and func.get_variable(connect,user_id, "state") == "START"):
        func.save_info(connect, user_id, "deck_cards_21",str(func.create_cards()))
        func.save_info(connect, user_id, "ruka_cards_21", "[]")
        func.save_info(connect, user_id, "balance", 0)
        func.save_info(connect, user_id, "sum_bot", 0)
        func.save_info(connect, user_id, "state", "CARDS")
        await message.answer(f"{NachaloK}", reply_markup=vibor)

    # ----------------------------------Ход игрока------------------------------#
    if message.text == "Взять карту" and (func.get_variable(connect, user_id, "state") == "CARDS" or func.get_variable(connect, user_id, "state") == "MOVE"):
        ruka_cards = func.create_list_deck_cards(func.get_variable(connect, user_id, "ruka_cards_21"))
        deck_card = func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards_21"))
        x1 = deck_card.pop()
        ruka_cards.append(x1)
        func.save_info(connect, user_id, "ruka_cards_21", str(ruka_cards))
        func.save_info(connect, user_id, "deck_cards_21", deck_card)
        await message.answer(f'Вы взяли: {x1}')
        user_id = str(message.from_user.id)
        sum_pl = int(func.get_variable(connect, user_id, "balance"))
        if x1[3:] == "Туз" and (sum_pl + int(func.convert_1_card(x1)[:-3])) <= 21:
            sum_pl += int(func.convert_1_card(x1)[:-3])
        elif x1[3:] == "Туз" and (sum_pl + int(func.convert_1_card(x1)[:-3])) > 21:
            sum_pl += 1
        if x1[3:] != "Туз":
            sum_pl += int(func.convert_1_card(x1)[:-3])
        func.save_info(connect, user_id, "balance", sum_pl)

        if func.get_variable(connect, user_id, "balance") == 21:
            func.save_info(connect, user_id, "vin_line_cards", func.get_variable(connect, user_id, "vin_line_cards")*1.15)
            func.save_info(connect, user_id, "rating_cards", round(func.get_variable(connect, user_id, "rating_cards") + (2 * func.get_variable(connect, user_id, "vin_line_cards")), 3))

            await message.answer(
                f'Вы победили набрав 21 очко, в колоде остались следующие карты: {", ".join(func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards_21")))}\n\n📈Ваш текущий рейтинг: {func.get_variable(connect, user_id, "rating_cards")}',
                reply_markup=vibor2)
            sum_pl = 0
            func.save_info(connect, user_id, "balance", sum_pl)
            func.save_info(connect, user_id, "state", "START")

        elif func.get_variable(connect, user_id, "balance") > 21:

            if func.get_variable(connect, user_id, "rating_cards") - (2 * func.get_variable(connect, user_id, "vin_line_cards")) >= 0:
                func.save_info(connect, user_id, "rating_cards", round(
                    func.get_variable(connect, user_id, "rating_cards") - (2 * func.get_variable(connect, user_id, "vin_line_cards")), 3))
            else:
                func.save_info(connect, user_id, "rating_cards", 0)
            func.save_info(connect, user_id, "vin_line_cards", 1)
            if func.get_variable(connect, user_id, "rating_cards") >= 1000:
                func.save_info(connect, user_id, "rating_cards", 0)
                func.save_info(connect, user_id, "vin_line_cards", 1)

            await message.answer(
                f'Вы проиграли набрав больше 21, в колоде остались следующие карты: {", ".join(func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards_21")))}\n\n📉Ваш текущий рейтинг: {func.get_variable(connect, user_id, "rating_cards")}',
                reply_markup=vibor2)
            sum_pl = 0
            sum_player = str(sum_pl)
            func.save_info(connect, user_id, "balance", sum_player)
            sumbot = 0
            func.save_info(connect, user_id, "sum_bot", sumbot)
            func.save_info(connect, user_id, "state", "START")
        else:
            func.save_info(connect, user_id, "state", "MOVE")
            await message.answer(
                f"Карты в вашей руке: {', '.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'ruka_cards_21')))}, желаете добрать еще одну карту?",
                reply_markup=vibor)
    if message.text == "Ну нахер этого Бориса!"  and (func.get_variable(connect, user_id, 'state') == "START"):
        func.save_info(connect, user_id, "state", "START")
        await message.answer(f"Борис доволен игрой.", reply_markup=cards_kb)

    # -----------------------------Конец хода игрока и начало хода Бориса---------------------------------#
    if message.text == "Спасовать" and func.get_variable(connect, user_id, "state") != "MOVE_PL_BJ" and func.create_list_pole(func.get_variable(connect, user_id, "ryka_pl_bj")) == []:
        if func.get_variable(connect, user_id, "balance") > 0:
            await message.answer(f"{Konec}", reply_markup=types.ReplyKeyboardRemove())
            func.save_info(connect, user_id, "state", "MOVE_BOT")
        elif func.get_variable(connect, user_id, "balance") == 0:
            await message.answer(
                f"Видимо вы решили, что Бориса не зря прозвали Шулером и просто сдались - ожидаемо.",reply_markup=vibor2)
            func.save_info(connect, user_id, "state", "START", )

        while func.get_variable(connect, user_id, "STATE") == "MOVE_BOT":
            if func.get_variable(connect, user_id, "sum_bot") <= random.randint(14, 16):
                deck_card = func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards_21"))
                x2 = deck_card.pop()
                sumbota = func.get_variable(connect, user_id, "sum_bot")
                sumbota += int(func.convert_1_card(x2)[:-3])
                func.save_info(connect, user_id, "sum_bot", sumbota)
                if func.get_variable(connect, user_id, "sum_bot") == 21:
                    if func.get_variable(connect, user_id, "rating_cards") - (2 * func.get_variable(connect, user_id, "vin_line_cards")) >= 0:
                        func.save_info(connect, user_id, "rating_cards", round(
                            func.get_variable(connect, user_id, "rating_cards") - (
                                        2 * func.get_variable(connect, user_id, "vin_line_cards")), 3))
                    else:
                        func.save_info(connect, user_id, "rating_cards", 0)
                    func.save_info(connect, user_id, "vin_line_cards", 1)
                    await message.answer(
                        f'Победил Борис, сразу же набрав 21 очко.\nВ колоде остались следующие карты: {", ".join(func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards_21")))} {func.get_variable(connect, user_id, "sum_bot")}\n\n📉Ваш текущий рейтинг: {func.get_variable(connect, user_id, "rating_cards")}',
                        reply_markup=vibor2)
                    func.save_info(connect, user_id, "state", "START")
                    func.save_info(connect, user_id, "balance", 0)
                    func.save_info(connect, user_id, "sum_bot", 0)
                    break
                elif func.get_variable(connect, user_id, "sum_bot") >= 16 or func.get_variable(connect, user_id, "balance") == 0:
                    if func.get_variable(connect, user_id, "balance") == 0:
                        if func.get_variable(connect, user_id, "rating_cards")  - (2 * func.get_variable(connect, user_id, "vin_line_cards")) >= 0:
                            func.save_info(connect, user_id, "rating_cards", round(
                                func.get_variable(connect, user_id, "rating_cards") - (
                                        2 * func.get_variable(connect, user_id, "vin_line_cards")), 3))
                        else:
                            func.save_info(connect, user_id, "rating_cards", 0)
                        func.save_info(connect,user_id, "vin_line_cards", 1)
                        if func.get_variable(connect, user_id, "rating_cards") >= 1000:
                            func.save_info(connect, user_id, "rating_cards", 0)
                            func.save_info(connect, user_id, "vin_line_cards", 1)
                        await message.answer(f'«Ты проиграл, не сделав и хода - жалкая попытка», - Борис ликует.\nВ колоде остались следующие карты: {",".join(func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards_21")))}.\n\nСумма, набранная Борисом: {func.get_variable(connect, user_id, "sum_bot")}.\nВаша сумма: {func.get_variable(connect, user_id, "balance")}\n\n📊Ваш текущий рейтинг: {func.get_variable(connect, user_id, "rating_cards")}',reply_markup=vibor2)
                        func.save_info(connect, user_id, "state", "START")
                        func.save_info(connect, user_id, "sum_bot", 0)
                        if message.text == "Ну нахер этого Бориса!" and (func.get_variable(connect, user_id, 'state') == "START"):
                            await message.answer(f"Борис доволен игрой.", reply_markup=cards_kb)
                        break
                    break

    # # ----------------------------------Проверки на победу-----------------------------------#
    if func.get_variable(connect, user_id, "sum_bot") >= 16 and (func.get_variable(connect, user_id, 'state') == "CARDS" or  func.get_variable(connect, user_id, 'state') == "MOVE" or func.get_variable(connect, user_id, 'state') =="MOVE_BOT"):
        user_id = str(message.from_user.id)
        if func.get_variable(connect,user_id, 'balance') < 21 and func.get_variable(connect, user_id, "sum_bot") < 21:
            if func.get_variable(connect, user_id, "balance") == func.get_variable(connect, user_id, "sum_bot"):
                if func.get_variable(connect, user_id, "rating_cards") - (2 * func.get_variable(connect, user_id, "vin_line_cards")) >= 0:
                    func.save_info(connect, user_id, "rating_cards", round(func.get_variable(connect, user_id, "rating_cards") - (2 * func.get_variable(connect, user_id, "vin_line_cards"))))
                else:
                    func.save_info(connect, user_id, "rating_cards", 0)
                func.save_info(connect, user_id, "vin_line_cards", 1)
                await message.answer(
                    f'В проиграли, набрав столько же очков, сколько и Борис.\nВ колоде остались следующие карты: {", ".join(func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards_21")))}.\n\nСумма, набранная Борисом: {func.get_variable(connect, user_id,"sum_bot")}.\nВаша сумма: {func.get_variable(connect, user_id, "balance")}\n\n📈Ваш текущий рейтинг: {func.get_variable(connect, user_id, "rating_cards")}',
                    reply_markup=vibor2)
                func.save_info(connect, user_id, "state", "START")
                func.save_info(connect, user_id, "sum_bot", 0)
                func.save_info(connect, user_id, "balance", 0)
            if message.text == "Ну нахер этого Бориса!" and (func.get_variable(connect, user_id, 'state') == "START"):
                func.save_info(connect, user_id, "sum_bot", 0)
                await message.answer(f"Борис доволен игрой.", reply_markup=cards_kb)
            elif func.get_variable(connect, user_id, "balance") > func.get_variable(connect, user_id, "sum_bot"):

                func.save_info(connect, user_id, "vin_line_cards", func.get_variable(connect, user_id, "vin_line_cards")*1.15)
                func.save_info(connect, user_id, "rating_cards", round(func.get_variable(connect, user_id, "rating_cards") + (2*func.get_variable(connect, user_id, "vin_line_cards")),3))
                if func.get_variable(connect, user_id, "rating_cards") >= 1000:
                    func.save_info(connect, user_id, "rating_cards", 0)
                    func.save_info(connect, user_id, "vin_line_cards", 1)

                await message.answer(
                    f'Вы победили, набрав больше очков, чем Борис.\nВ колоде остались следующие карты: {", ".join(func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards_21")))}.\n\nСумма, набранная Борисом: {func.get_variable(connect, user_id, "sum_bot")}.\nВаша сумма: {func.get_variable(connect, user_id, "balance")}\n\n📈Ваш текущий рейтинг: {func.get_variable(connect, user_id, "rating_cards")}',
                    reply_markup=vibor2)
                func.save_info(connect, user_id, "state", "START")
                func.save_info(connect, user_id, "sum_bot", 0)
                func.save_info(connect, user_id, "balance", 0)
                if message.text == "Ну нахер этого Бориса!" and (func.get_variable(connect, user_id, 'state') == "START"):
                    func.save_info(connect, user_id, "state", "START")
                    await message.answer(f"Борис доволен игрой.", reply_markup=cards_kb)
            elif func.get_variable(connect, user_id, "balance") < func.get_variable(connect, user_id, "sum_bot"):
                if func.get_variable(connect, user_id, "rating_cards") - (2 * func.get_variable(connect, user_id, "vin_line_cards")) >= 0:
                    func.save_info(connect, user_id, "rating_cards", round(func.get_variable(connect, user_id, "rating_cards") - (2 * func.get_variable(connect, user_id, "vin_line_cards"))))
                else:
                    func.save_info(connect, user_id, "rating_cards", 0)
                func.save_info(connect, user_id, "vin_line_cards", 1)

                await message.answer(
                    f'Вы проиграли набрав очков меньше, чем Борис! (Он торжествует, хоть и не мог ожидать чего-либо другого помимо триумфа).\nВ колоде остались следующие карты: {", ".join(func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards_21")))}.\n\nСумма, набранная Борисом: {func.get_variable(connect, user_id, "sum_bot")}.\nВаша сумма: {func.get_variable(connect, user_id, "balance")}\n\n📉Ваш текущий рейтинг: {func.get_variable(connect, user_id, "rating_cards")}',
                    reply_markup=vibor2)
                func.save_info(connect, user_id, "state", "START")
                func.save_info(connect, user_id, "sum_bot", 0)
                func.save_info(connect, user_id, "balance", 0)
                if message.text == "Ну нахер этого Бориса!" and (func.get_variable(connect, user_id, 'state') == "START"):
                    await message.answer(f"Борис доволен игрой.", reply_markup=cards_kb)
        else:
            func.save_info(connect, user_id, "state", "START")
            func.save_info(connect, user_id, "vin_line_cards", 1.15*func.get_variable(connect, user_id, "vin_line_cards"))
            func.save_info(connect, user_id, "rating_cards", round(func.get_variable(connect, user_id, "rating_cards") + (2* func.get_variable(connect, user_id, "vin_line_cards")), 3))
            if  func.get_variable(connect, user_id, "rating_cards") >= 1000:
                func.save_info(connect, user_id, "rating_cards", 0)
                func.save_info(connect, user_id, "vin_line_cards", 1)

            func.save_players(players)

            await message.answer(
                f'Вы победили, так как Борис поверил в себя и набрал больше 21 очка.\nВ колоде остались следующие карты: {", ".join(func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards_21")))}\n\n📈Ваш текущий рейтинг: {func.get_variable(connect, user_id,  "rating_cards")}',
                reply_markup=vibor2)
            func.save_info(connect, user_id, "balance", 0)
            func.save_info(connect, user_id, "state", "START")

    # # -----------------------------------Кости--------------------------------------- #

    if message.text == "Партия в кости 🎲" and (func.get_variable(connect, user_id, 'state') != "CARDS" or  func.get_variable(connect, user_id, 'state') != "MOVE" or func.get_variable(connect, user_id, 'state') !="MOVE_BOT"):
        await message.answer(begin_dice)
        user_id = str(message.from_user.id)
        func.save_info(connect, user_id, "state", "DICE_PR")
        await message.answer(pravila_txt, reply_markup=rules_kb)

    if message.text == "Правила📋" and func.get_variable(connect, user_id, 'state') == "DICE_PR":
        await message.answer(rules_bones, reply_markup=vb_kb)


    if message.text == "Играть 🎮" and func.get_variable(connect, user_id, 'state') == "DICE_PR":
        func.save_info(connect, user_id, "balance", 50)
        func.save_info(connect, user_id, "state", "dice")
        func.save_info(connect, user_id, "sum_bot", 50)

    if func.get_variable(connect, user_id, "state") == "dice" and func.get_variable(connect, user_id, "balance") > 0 and func.get_variable(connect, user_id, "sum_bot") > 0:
        await message.answer("Введите число от 2 до 12:", reply_markup=exit_kb)
        func.save_info(connect, user_id, "state", "dice1")

    user_id = str(message.from_user.id)

    if func.get_variable(connect, user_id, "state") == "dice1" and message.text.isdigit():
        user_id = str(message.from_user.id)
        num_player = message.text
        func.save_info(connect, user_id, "num", int(num_player))
        if func.get_variable(connect, user_id, "num") >= 2 and func.get_variable(connect, user_id, "num") <= 12:
            await message.answer(f'Введите сумму ставки, не превышающию: {func.get_variable(connect, user_id, "balance")}')
            func.save_info(connect, user_id, "state", "SUM")
        elif func.get_variable(connect, user_id, "num") < 2 or func.get_variable(connect, user_id, "num") > 12:
            func.save_info(connect, user_id, "state", "dice1")
            await message.answer(
                "❗Вы ввели число, которое не соответствует требованиям игры.\nВведите другое число от 2 до 12 включительно❗")


    elif ("," in message.text or "." in message.text) and func.get_variable(connect, user_id, "state") == "SUM":
        await message.answer("❗Введите целое число❗")

    elif message.text.isdigit() and func.get_variable(connect, user_id, "state") == "SUM" and func.get_variable(connect, user_id, "balance") >= 0:
        user_id = str(message.from_user.id)
        bet_player = int(message.text)
        if "," not in str(bet_player) or "." not in str(bet_player):
            func.save_info(connect, user_id, "bet", bet_player)
            func.save_info(connect, user_id, "state", "CHECK")
            if func.get_variable(connect, user_id, "bet") > func.get_variable(connect, user_id, "balance") and func.get_variable(connect, user_id, "state") == "CHECK":
                func.save_info(connect, user_id, "state", "dice1")
                await message.answer("❗Ошибка, ваша ставка больше вашей суммы, введите другугю ставку❗")

    if( func.get_variable(connect, user_id, "bet") <= func.get_variable(connect, user_id, "balance")) and func.get_variable(connect, user_id, "state") == "CHECK":
        w = int(func.get_variable(connect, user_id, "bet") * 0.5)
        w1 = int(func.get_variable(connect, user_id, "bet") * 0.6)
        w2 = int(func.get_variable(connect, user_id, "bet") * 0.2)
        w3 = int(func.get_variable(connect, user_id, "bet") * 0.8)
        w4 = 0
        ww = [w, w1, w2, w3, w4, abs(w3 - w), abs(w1 - w2), abs(w1 - w), abs(w3 - w1), abs(w3 - w2)]
        chs = random.choice(ww)
        bot = random.randint(2, 12)
        func.save_info(connect, user_id, "num_bot", bot)
        if int(chs) <=func.get_variable(connect, user_id, "sum_bot"):
            func.save_info(connect, user_id, "bet_bot", int(chs))
        else:
            bot_stafka = chs / 2
            func.save_info(connect, user_id, "bet_bot", bot_stafka)

        q1 = random.randint(1, 6)
        q2 = random.randint(1, 6)
        if abs(bot - (q1 + q2)) < (abs(func.get_variable(connect, user_id, "num") - (q1 + q2))):
            await message.answer(
                f"Вы проиграли: \n Ваше число = {func.get_variable(connect, user_id, 'num')} \n Число Бориса = {func.get_variable(connect, user_id, 'num_bot')} \n Выпавшие число = {q1 + q2}")
            user_id = str(message.from_user.id)
            func.save_info(connect, user_id, "balance", func.get_variable(connect, user_id, "balance") - func.get_variable(connect, user_id, "bet"))
            func.save_info(connect, user_id, "sum_bot", func.get_variable(connect, user_id, "sum_bot") + (func.get_variable(connect, user_id, "bet") - int(func.get_variable(connect, user_id, "bet")*0.08)))
            await message.answer(
                f"Ваш счет = {func.get_variable(connect, user_id, 'balance')} \n Счет Бориса = {func.get_variable(connect, user_id, 'sum_bot')} \n Ставка Бориса = {func.get_variable(connect, user_id, 'bet_bot')}")
            func.save_info(connect, user_id, "state", "dice1")
            if func.get_variable(connect, user_id, 'balance') <= 0:
                func.save_info(connect, user_id, "state", "end")
            else:
                await message.answer("Введите число от 2 до 12:")
        if abs(bot - (q1 + q2)) > abs(func.get_variable(connect, user_id, 'num') - (q1 + q2)):
            await message.answer(
                f"Вы победили: \n Ваше число = {func.get_variable(connect, user_id, 'num')} \n Число Бориса = {func.get_variable(connect, user_id, 'num_bot')} \n Выпавшие число = {q1 + q2}", )
            user_id = str(message.from_user.id)
            func.save_info(connect, user_id, "balance", func.get_variable(connect, user_id, "balance")+(func.get_variable(connect, user_id, "bet_bot") - int(func.get_variable(connect, user_id, "bet_bot")*0.1)))
            func.save_info(connect, user_id, "sum_bot", func.get_variable(connect, user_id, "sum_bot") - (func.get_variable(connect, user_id, "bet_bot") + (func.get_variable(connect, user_id, "bet_bot") /100 * 20)))
            await message.answer(
                f"Ваш счет = {func.get_variable(connect, user_id, 'balance')} \n Счет Бориса = {func.get_variable(connect, user_id, 'sum_bot')} \n Ставка бота = {func.get_variable(connect, user_id, 'bet_bot')}")
            state[user_id] = "PART"
            func.save_info(connect, user_id, "state", "dice1")
            await message.answer("Введите число от 2 до 12:")
        elif func.get_variable(connect, user_id, 'num_bot') == func.get_variable(connect, user_id, 'num'):
            user_id = str(message.from_user.id)
            await message.answer(
                f"Ничья: \n Ваше число = {func.get_variable(connect, user_id, 'num')} \n Число Бориса = {func.get_variable(connect, user_id, 'num_bot')} \n Выпавшие число = {q1 + q2} \n Ваш счет = {func.get_variable(connect, user_id, 'balance')} \n Счет Бориса = {func.get_variable(connect, user_id, 'sum_bot')} \n Ставка Бориса = {func.get_variable(connect, user_id, 'bet_bot')}")
            state[user_id] = "PART"
            func.save_info(connect, user_id, "state", "dice1")
            await message.answer("Введите число от 2 до 12:")


        if func.get_variable(connect, user_id, 'balance') <= 0:
            if func.get_variable(connect, user_id, 'sum_bot') < 20 and func.get_variable(connect, user_id, 'rating_dice') - func.get_variable(connect, user_id, 'sum_bot') >= 0:
                func.save_info(connect, user_id, "rating_dice", func.get_variable(connect, user_id, "rating_dice") - func.get_variable(connect, user_id, "sum_bot")*1.5)
            if func.get_variable(connect, user_id, 'rating_dice') - func.get_variable(connect, user_id, 'sum_bot') >= 0:
                func.save_info(connect, user_id, "rating_dice",func.get_variable(connect, user_id, "rating_dice") - func.get_variable(connect, user_id,"sum_bot"))
            else:
                func.save_info(connect, user_id, "rating_dice",0)
            await message.answer(f'{lost_dice}\n\n📉Ваш текущий рейтинг: {func.get_variable(connect, user_id, "rating_dice")}')
            func.save_info(connect, user_id, "state", "end")

        user_id = str(message.from_user.id)

        if func.get_variable(connect, user_id, 'sum_bot') <= 0:
            func.save_info(connect, user_id, "rating_dice", func.get_variable(connect, user_id, "rating_dice") + func.get_variable(connect, user_id, "balance"))
            await message.answer(f"{vin_dice}\n\n📈Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_dice')}")
            func.save_info(connect, user_id, "state", "end")

    # # ----------------------------------------Крестики нолики---------------------------------------
    if  message.text == "Сыграть в К/Н ❌⭕" and (func.get_variable(connect, user_id, 'state') != "CARDS" or  func.get_variable(connect, user_id, 'state') != "MOVE" or func.get_variable(connect, user_id, 'state') !="MOVE_BOT"):
        s = [i for i in range(8)]
        random.shuffle(s)
        tr = s.pop(0)
        func.save_info(connect, user_id, "num_fun_move_bot", str([s,tr,0]))
        func.save_info(connect, user_id, "state","CROSS/ZERO_PR")
        await message.answer(pravila_txt, reply_markup=rules_kb)

    if message.text == "Правила📋" and func.get_variable(connect,user_id, "state") == "CROSS/ZERO_PR":
        await message.answer(rules_zerocross, reply_markup=vb_kb)

    if (message.text == "Играть 🎮" and func.get_variable(connect,user_id, "state") == "CROSS/ZERO_PR") or  (message.text == "Сыграть еще раз ❌⭕" and func.get_variable(connect,user_id, "state") == "START"):
        func.save_info(connect, user_id, "filter_ls_bot_vin", str([]))
        func.save_info(connect, user_id, "filter_interf_pl", str([]))
        s = [i for i in range(8)]
        random.shuffle(s)
        tr = s.pop(0)
        func.save_info(connect, user_id, "num_fun_move_bot", str([s,tr,0]))
        func.save_info(connect,user_id, "pole_cross_zero", str(func.gen_pole_cross_zero()))
        func.save_info(connect, user_id, 'state', 'CROSS/ZERO_PR')
        func.save_info(connect, user_id, "state", "CROSS/ZERO")
        await message.answer("Выберите, чем будете играть", reply_markup=sign_kb)

    elif message.text == "❌" and func.get_variable(connect,user_id, "state") == "CROSS/ZERO":
        func.save_info(connect,user_id, "sign", "❌")
        func.save_info(connect,user_id, "sign_bot", "⭕")
        func.save_info(connect,user_id, "state", "CHOICE")
    elif message.text == "⭕" and func.get_variable(connect,user_id, "state") == "CROSS/ZERO":
        func.save_info(connect,user_id, "sign", "⭕")
        func.save_info(connect,user_id, "sign_bot", "❌")
        func.save_info(connect,user_id, "state", "CHOICE")
    if func.get_variable(connect,user_id, "state") == "CHOICE":
        func.save_info(connect,user_id, "state", "END_MT")
        await message.answer( func.messege_pole(func.get_variable(connect,user_id, "pole_cross_zero")),reply_markup=types.ReplyKeyboardRemove())
        mv_bt.motion_bot_cross__zero(connect,user_id)
        time.sleep(1)
        await message.answer(func.messege_pole(func.get_variable(connect,user_id, "pole_cross_zero")), reply_markup=ex_pe_kb)


    # -------------------------ход_игрока----------------------

    if message.text.isdigit() and func.get_variable(connect,user_id, "state") == "PLAY_CROSS/ZERO" and (message.text in ["1","2","3","4","5","6","7","8","9"]):
        pos = int(message.text)
        pole = func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))
        func.save_info(connect,user_id, 'motoin_pl_cross_zero', pos)
        if pole[(pos-1)//3][(pos-1)%3] == "🔲":
            pole[(pos-1)//3][(pos-1)%3] = func.get_variable(connect,user_id, "sign")
            func.save_info(connect,user_id, "pole_cross_zero", str(pole))
            func.save_info(connect,user_id, "state", "END_MT")
            await message.answer(func.messege_pole(func.get_variable(connect,user_id, "pole_cross_zero")))
        else:
            await message.answer("Эта клетка уже занята")

    if message.text.isdigit() and func.get_variable(connect,user_id, "state") == "PLAY_CROSS/ZERO" and (message.text not in ["1","2","3","4","5","6","7","8","9"]):
        await message.answer("❗️ Данное действие спровоцирует выход за пределы поля, что недопустимо, пожалуйста, выберете другую цифру ❗️")

    # ------------------------ход_бота---------------------------
    if func.get_variable(connect,user_id, "state") == "END_MT":
        mv_bt.motion_bot_cross__zero(connect,user_id)
        func.save_info(connect,user_id, "state", "PLAY_CROSS/ZERO")
        await message.answer(func.messege_pole(func.get_variable(connect,user_id, "pole_cross_zero")), reply_markup=ex_pe_kb)

    # -------------------------------------------------проверки побед игрока---------------------------------------------------

    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and (func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0].count(func.get_variable(connect,user_id, "sign")) == 3 or
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1].count(func.get_variable(connect,user_id, "sign")) == 3 or
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2].count(func.get_variable(connect,user_id, "sign")) == 3):
        func.save_info(connect,user_id, "state", "START")
        func.save_info(connect, user_id,"rating_cr_zr",round((func.get_variable(connect, user_id, "rating_cr_zr")//10)/10 + func.get_variable(connect, user_id, "rating_cr_zr"),3))
        await message.answer(f"{vin_tic_tac}\n\n📈Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}", reply_markup=vib_tic)
    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0][0] == func.get_variable(connect,user_id, "sign") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1][0] == func.get_variable(connect,user_id, "sign") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2][0] == func.get_variable(connect,user_id, "sign"):
        func.save_info(connect,user_id, "state", "START")
        func.save_info(connect, user_id, "rating_cr_zr", round(abs((func.get_variable(connect, user_id, "rating_cr_zr") // 10) / 10) + func.get_variable(connect, user_id,"rating_cr_zr"), 3))
        await message.answer(
            f"{vin_tic_tac}\n\n📈Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}",
            reply_markup=vib_tic)
    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0][1] == func.get_variable(connect,user_id, "sign") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1][1] == func.get_variable(connect,user_id, "sign") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2][1] == func.get_variable(connect,user_id, "sign"):
        func.save_info(connect,user_id, "state", "START")
        func.save_info(connect, user_id, "rating_cr_zr", round(abs((func.get_variable(connect, user_id, "rating_cr_zr") // 10) / 10) + func.get_variable(connect, user_id,"rating_cr_zr"), 3))
        await message.answer(
            f"{vin_tic_tac}\n\n📈Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}",
            reply_markup=vib_tic)
    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0][2] == func.get_variable(connect,user_id, "sign") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1][2] == func.get_variable(connect,user_id, "sign") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2][2] == func.get_variable(connect,user_id, "sign"):
        func.save_info(connect, user_id, "state", "START")
        func.save_info(connect, user_id, "rating_cr_zr", round(abs((func.get_variable(connect, user_id, "rating_cr_zr") // 10) / 10) + func.get_variable(connect, user_id,"rating_cr_zr"), 3))
        await message.answer(
            f"{vin_tic_tac}\n\n📈Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}",
            reply_markup=vib_tic)
    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0][0] == func.get_variable(connect,user_id, "sign") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1][1] == func.get_variable(connect,user_id, "sign") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2][2] == func.get_variable(connect,user_id, "sign"):
        func.save_info(connect,user_id, "state", "START")
        func.save_info(connect, user_id, "rating_cr_zr", round(abs((func.get_variable(connect, user_id, "rating_cr_zr") // 10) / 10) + func.get_variable(connect, user_id,"rating_cr_zr"), 3))
        await message.answer(
            f"{vin_tic_tac}\n\n📈Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}",
            reply_markup=vib_tic)
    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0][2] == func.get_variable(connect,user_id, "sign") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1][1] == func.get_variable(connect,user_id, "sign") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2][0] == func.get_variable(connect,user_id, "sign"):
        func.save_info(connect,user_id, "state", "START")
        func.save_info(connect, user_id, "rating_cr_zr", round(abs((func.get_variable(connect, user_id, "rating_cr_zr") // 10) / 10) + func.get_variable(connect, user_id,"rating_cr_zr"), 3))
        await message.answer(
            f"{vin_tic_tac}\n\n📈Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}",
            reply_markup=vib_tic)

    # ------------------------------------------------проверки побед бота-----------------------------------------------

    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and (func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0].count(func.get_variable(connect,user_id, "sign_bot")) == 3 or
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1].count(
                    func.get_variable(connect,user_id, "sign_bot")) == 3 or
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2].count(
                    func.get_variable(connect,user_id, "sign_bot")) == 3):
        func.save_info(connect,user_id, "state", "START")
        func.save_info(connect, user_id, "rating_cr_zr", round(func.get_variable(connect, user_id, "rating_cr_zr") - (abs(2 * (func.get_variable(connect, user_id, "rating_cr_zr") // 10) / 10)), 3))
        await message.answer(f"{lost_tic_tac}\n\n📉Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}", reply_markup=vib_tic)
    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0][0] == func.get_variable(connect,user_id, "sign_bot") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1][0] == func.get_variable(connect,user_id, "sign_bot") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2][0] == func.get_variable(connect,user_id, "sign_bot"):
        func.save_info(connect,user_id, "state", "START")
        func.save_info(connect, user_id, "rating_cr_zr", round(func.get_variable(connect, user_id, "rating_cr_zr") - (abs(2 * (func.get_variable(connect, user_id, "rating_cr_zr") // 10) / 10)), 3))
        await message.answer(
            f"{lost_tic_tac}\n\n📉Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}",
            reply_markup=vib_tic)
    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0][1] == func.get_variable(connect,user_id, "sign_bot") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1][1] == func.get_variable(connect,user_id, "sign_bot") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2][1] == func.get_variable(connect,user_id, "sign_bot"):
        func.save_info(connect, user_id, "state", "START")
        func.save_info(connect, user_id, "rating_cr_zr", round(func.get_variable(connect, user_id, "rating_cr_zr") - (abs(2 * (func.get_variable(connect, user_id, "rating_cr_zr") // 10) / 10)), 3))
        await message.answer( f"{lost_tic_tac}\n\n📉Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}",reply_markup=vib_tic)
    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0][2] == func.get_variable(connect,user_id, "sign_bot") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1][2] == func.get_variable(connect,user_id, "sign_bot") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2][2] == func.get_variable(connect,user_id, "sign_bot"):
        func.save_info(connect,user_id, "state", "START")
        func.save_info(connect, user_id, "rating_cr_zr", round(func.get_variable(connect, user_id, "rating_cr_zr") - (abs(2 * (func.get_variable(connect, user_id, "rating_cr_zr") // 10) / 10)), 3))
        await message.answer(f"{lost_tic_tac}\n\n📉Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}",
            reply_markup=vib_tic)
    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0][0] == func.get_variable(connect,user_id, "sign_bot") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1][1] == func.get_variable(connect,user_id, "sign_bot") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2][2] == func.get_variable(connect,user_id, "sign_bot"):
        func.save_info(connect,user_id, "state", "START")
        func.save_info(connect, user_id, "rating_cr_zr", round(func.get_variable(connect, user_id, "rating_cr_zr") - (abs(2 * (func.get_variable(connect, user_id, "rating_cr_zr") // 10) / 10)), 3))
        await message.answer(
            f"{lost_tic_tac}\n\n📉Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}",
            reply_markup=vib_tic)
    if (func.get_variable(connect, user_id, "state") == "END_MT" or func.get_variable(connect, user_id, "state") == "PLAY_CROSS/ZERO") and func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[0][2] == func.get_variable(connect,user_id, "sign_bot") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1][1] == func.get_variable(connect,user_id, "sign_bot") and \
            func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2][0] == func.get_variable(connect,user_id, "sign_bot"):
        func.save_info(connect,user_id, "state", "START")
        func.save_info(connect, user_id, "rating_cr_zr", round(func.get_variable(connect, user_id, "rating_cr_zr") - (abs(2 * (func.get_variable(connect, user_id, "rating_cr_zr") // 10) / 10)), 3))
        await message.answer(
            f"{lost_tic_tac}\n\n📉Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}",
            reply_markup=vib_tic)
    if (func.get_variable(connect,user_id, "state") == "PLAY_CROSS/ZERO" or func.get_variable(connect,user_id, "state") == "END_MT") and "🔲" not in func.create_list_pole(func.get_variable(connect, user_id, "pole_cross_zero"))[0] and  "🔲" not in func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[1] and  "🔲" not in func.create_list_pole(func.get_variable(connect,user_id, "pole_cross_zero"))[2]:
        func.save_info(connect,user_id, "state", "START")
        await message.answer(f"{darw_tic_tac}\n\n📊Ваш текущий рейтинг: {func.get_variable(connect, user_id, 'rating_cr_zr')}", reply_markup=vib_tic)

    #

    # ------------------------------дурак------------------------------------------------
    if message.text == "Сыграть в Дурака ♦️" and func.get_variable(connect, user_id, 'state') == "START":
        func.save_info(connect, user_id, "state", "DURAK_NCH")
        await message.answer(pravila_txt, reply_markup=rules_kb)

    if message.text == "Правила📋" and func.get_variable(connect, user_id, 'state') == "DURAK_NCH":
        await message.answer(rules_durak, reply_markup=vb_kb)

    if message.text == "Играть 🎮" and (func.get_variable(connect, user_id, 'state') == "DURAK_NCH"):
        func.save_info(connect, user_id, "deck_cards", str(func.gen_deck()))
        func.save_info(connect, user_id, "state", "BEGDURACK")

    if message.text == "Сыграть ещё одну партию" and (func.get_variable(connect, user_id, 'state') != "CARDS" or  func.get_variable(connect, user_id, 'state') != "MOVE" or func.get_variable(connect, user_id, 'state') !="MOVE_BOT"):
        func.save_info(connect, user_id, "deck_cards", str(func.gen_deck()))
        func.save_info(connect, user_id, "state", "BEGDURACK")


    if func.get_variable(connect, user_id, "state") == "BEGDURACK":
        func.save_info(connect, user_id, "pl_deck_cards", str([]))
        func.save_info(connect, user_id, "bot_deck_cards", str([]))
        func.save_info(connect, user_id, "opponent_cards", str([]))
        func.save_info(connect, user_id, "recapture_bt", str([]))
        kozar = func.gen_kozar()
        func.save_info(connect, user_id, "kozar", kozar)
        func.save_info(connect, user_id, "kozar_ch", func.convert_kozar(kozar))
        deck_cards = func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards"))
        coloda = ReplyKeyboardMarkup(resize_keyboard=True)
        exit = KeyboardButton("Выйти в меню игр")
        for i in range(1, 13, 2):
            deck_pl_cards = func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards"))
            deck_bot_cards = func.create_list_deck_cards(func.get_variable(connect, user_id, "bot_deck_cards"))
            deck_pl_cards.append(deck_cards[i])
            deck_bot_cards.append(deck_cards[i-1])
            knopka = KeyboardButton(deck_pl_cards[-1])
            deck_cards.pop(i)
            deck_cards.pop(i-1)
            func.save_info(connect, user_id, "deck_cards", str(deck_cards))
            func.save_info(connect, user_id, "pl_deck_cards", str(deck_pl_cards))
            func.save_info(connect, user_id, "bot_deck_cards", str(deck_bot_cards))
            coloda.add(knopka)
        coloda.add(exit)
        func.save_info(connect, user_id, "state", "BEG_MOVE_PL")
        await message.answer(f"{kozar_txt} {kozar}.", reply_markup=coloda)
        await message.answer("Ваш ход")

    if message.text in func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards")) and func.get_variable(connect, user_id, "state") == "BEG_MOVE_PL":
        opponent_cards = func.create_list_deck_cards(func.get_variable(connect, user_id, "opponent_cards"))
        pl_deck_cards = func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards"))
        if opponent_cards == []:
            opponent_cards.append(message.text)
            pl_deck_cards.remove(message.text)
            func.save_info(connect, user_id, "pl_deck_cards", str(pl_deck_cards))
            func.save_info(connect, user_id, "opponent_cards", str(opponent_cards))
            end = KeyboardButton("Закончить ход")
            ryka = ReplyKeyboardMarkup(resize_keyboard=True)
            ryka.add(end)
            for cards in func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards")):
                ryka.add(cards)
            ryka.add("Выйти в меню игр")
            await message.answer("Ход продолжается", reply_markup=ryka)
        elif opponent_cards != []:
            if message.text[2:] == opponent_cards[0][2:]:
                opponent_cards.append(message.text)
                pl_deck_cards.remove(message.text)
                func.save_info(connect, user_id, "pl_deck_cards", str(pl_deck_cards))
                func.save_info(connect, user_id, "opponent_cards", str(opponent_cards))
                end = KeyboardButton("Закончить ход")
                ryka = ReplyKeyboardMarkup(resize_keyboard=True)
                ryka.add(end)
                for cards in func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards")):
                    ryka.add(cards)
                ryka.add("Выйти в меню игр")
                await message.answer("Ход продолжается", reply_markup=ryka)
            else:
                await message.answer("Вы не можете выставить эту карту")

    # ----------------------------------Отбитие бота-----------------------------------------

    if message.text == "Закончить ход" and func.get_variable(connect, user_id, "state") == "BEG_MOVE_PL":
        await message.answer("Считаные секунды требуются Борису на размышления",reply_markup=types.ReplyKeyboardRemove())
        if func_dr.recapture_bot(connect,user_id) == 4:
            await message.answer(f"Неразумный ход, Борис с легкостью бьет вашу карту: [{','.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'recapture_bt')))}]")
            func.save_info(connect, user_id, "recapture_bt", str([]))
            if func_dr.add_cards(connect,user_id, "pl_deck_cards") != []:
                await message.answer(f"Вы вытащили: [{','.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'result')))}]")
            func_dr.add_cards(connect,user_id, "bot_deck_cards")
            func.save_info(connect, user_id, "state", "BEG_MOVE_BOT")

        if func_dr.recapture_bot(connect,user_id) == 3:
            await message.answer("Ваш противник взял карту")
            opponent_cards = func.create_list_deck_cards(func.get_variable(connect, user_id, "opponent_cards"))
            opponent_cards.clear()
            func.save_info(connect, user_id, "opponent_cards", str(opponent_cards))
            if func_dr.add_cards(connect,user_id, "pl_deck_cards") != []:
                await message.answer(f"Вы вытащили: [{','.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'result')))}]")
            end = KeyboardButton("Закончить ход")
            coloda = ReplyKeyboardMarkup(resize_keyboard=True)
            exit = KeyboardButton("Выйти в меню игр")
            coloda.add(end)
            for card in func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards")):
                cards = KeyboardButton(card)
                coloda.add(cards)
            coloda.add(exit)
            await message.answer("Ваш ход", reply_markup=coloda)


    if func.get_variable(connect, user_id, "state") == "OTBIV" and message.text in func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards")):
        if func_dr.recapture(connect,user_id, message.text) == 1:
            if len(func.create_list_deck_cards(func.get_variable(connect, user_id, "opponent_cards"))) == 0:
                if func_dr.add_cards(connect,user_id, "pl_deck_cards") != []:
                    await message.answer(f"Вы вытащили: [{','.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'result')))}]")
                coloda = ReplyKeyboardMarkup(resize_keyboard=True)
                exit = KeyboardButton("Выйти в меню игр")
                for cards in func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards")):
                    card = KeyboardButton(cards)
                    coloda.add(card)
                coloda.add(exit)
                await message.answer("Ваш ход", reply_markup=coloda)
                func.save_info(connect, user_id, "state", "BEG_MOVE_PL")
            if len(func.create_list_deck_cards(func.get_variable(connect, user_id, "opponent_cards"))) > 0:
                coloda = ReplyKeyboardMarkup(resize_keyboard=True)
                exit = KeyboardButton("Выйти в меню игр")
                for cards in func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards")):
                    card = KeyboardButton(cards)
                    coloda.add(card)
                coloda.add(exit)
                await message.answer("Вы прродолажете отбиваться", reply_markup=coloda)
        else:
            await message.answer("Вы не можете побить этой картой")


    if func.get_variable(connect, user_id, "state") == "OTBIV" and message.text == "Взять карту":
        deck_pl_cards = func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards"))
        deck_pl_cards += func.create_list_deck_cards(func.get_variable(connect, user_id, "opponent_cards"))
        func.save_info(connect, user_id,"pl_deck_cards" ,str(deck_pl_cards))
        func.save_info(connect, user_id, "state", "BEG_MOVE_BOT")

    if func.get_variable(connect, user_id, "state") == "BEG_MOVE_BOT" and  len(func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards"))) != 0:
        func_dr.move_bot_durak(connect,user_id)
        func_dr.add_cards(connect,user_id, "bot_deck_cards")
        func.save_info(connect, user_id, "state", "OTBIV")
        coloda = ReplyKeyboardMarkup(resize_keyboard=True)
        exit = KeyboardButton("Выйти в меню игр")
        end = KeyboardButton("Закончить ход")
        take_card = KeyboardButton("Взять карту")
        coloda.add(end)
        for cards in func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards")):
            card_ = KeyboardButton(cards)
            coloda.add(card_)
        coloda.add(take_card)
        coloda.add(exit)
        await message.answer(f"Борис настолько самоуверенно выставляет \n[{','.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'opponent_cards')))}]\n, что начинает казаться будто он уже точно знает, чем окончиться партия.", reply_markup=coloda)

    if len(func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_cards"))) == 0 and (func.get_variable(connect, user_id, "state") == "OTBIV" or func.get_variable(connect, user_id, "state") == "BEG_MOVE_BOT" or func.get_variable(connect, user_id, "state") == "BEG_MOVE_PL"):
        if len(func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards"))) == 0 or func.create_list_deck_cards(func.get_variable(connect, user_id, "pl_deck_cards")) == []:
            func.save_info(connect, user_id, "state", "START")
            func.save_info(connect, user_id, "rating_durak", abs(float(func.get_variable(connect, user_id, "rating_durak")))*0.15+float(func.get_variable(connect, user_id, 'rating_durak')))
            await message.answer(f"Сегодня в дураках Борис – вы победили.\n\n ваш рейтинг:📈 {func.get_variable(connect, user_id, 'rating_durak')}", reply_markup=ver_durack)
        if len(func.create_list_deck_cards(func.get_variable(connect, user_id, "bot_deck_cards"))) == 0:
            func.save_info(connect, user_id, "state", "START")
            func.save_info(connect, user_id, "rating_durak", float(func.get_variable(connect, user_id, "rating_durak"))-abs(float(func.get_variable(connect, user_id, "rating_durak"))*0.30))
            await message.answer(f"Дурак остался дураком – вы проиграли.\n\n ваш рейтинг:📉 {func.get_variable(connect, user_id, 'rating_durak')}", reply_markup=ver_durack)


    #----------------------------------Black jack-------------------------------

    if message.text == "Сыграть в BlackJack 💰"and func.get_variable(connect, user_id, "state") == "START":
        func.save_info(connect, user_id, "state", "BLACK_JACK")
        await message.answer(pravila_txt, reply_markup=rules_kb)
    if message.text == "Правила📋" and func.get_variable(connect, user_id, "state") == "BLACK_JACK":
        await message.answer(rules_bj,reply_markup=vb_kb)

    if (message.text == "Играть 🎮" and func.get_variable(connect, user_id, "state") == "BLACK_JACK") or (message.text == "Сыграть еще раз 💰" and func.get_variable(connect, user_id, 'state') == "START"):
        func.save_info(connect, user_id, "state", "STAVKA_SYKA")
        await message.answer(f"{stavka_1_bj}{func.get_variable(connect, user_id, 'rating_bj')}{stavka_2_bj}",reply_markup=types.ReplyKeyboardRemove())


    if message.text and func.get_variable(connect, user_id, "state") == "STAVKA_SYKA":
        try:
            if float(message.text.replace(",",".")) <= float(func.get_variable(connect, user_id, "rating_bj")) and float(func.get_variable(connect, user_id, "rating_bj")) >= 0:
                print(float(message.text.replace(",",".")))
                func.save_info(connect, user_id, "stavka", float(message.text.replace(",",".")))
                func.save_info(connect, user_id, "state", "START_BLACK_JACK")
                deck_cards_bj = func.gen_deck() + func.gen_deck()
                func.save_info(connect, user_id, "dop_ryka_bj", "[]")
                func.save_info(connect, user_id, "open_dop_ryka", " ")
                func.save_info(connect, user_id, "choose_ryka", '\'ryka_pl_bj\'')
                func.save_info(connect, user_id, "deck_black_jack", str(deck_cards_bj))
                await message.answer(begin_bj,reply_markup=ver_durack)
            elif float(func.get_variable(connect, user_id, "rating_bj")) < 0:
                await message.answer("У вас отрицательный счет", reply_markup=cards_kb)
                func.save_info(connect, user_id, "state", "START")
            elif float(message.text.replace(",",".")) > float(func.get_variable(connect, user_id, "rating_bj")):
                await message.answer("Ваша ставка больше вышего счета")
        except:
            await message.answer("Введите число")

    if func.get_variable(connect, user_id, "state") == "START_BLACK_JACK":
        ryka_pl_bj = []
        deck_cards_bj = func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_black_jack"))
        ryka_bot_bj = []
        ryka_pl_bj.append(deck_cards_bj.pop(0))
        text_otp = ''
        text_otp += f"Вам выпала: {ryka_pl_bj[-1]}\n-------------------------\n"
        ryka_bot_bj.append(deck_cards_bj.pop(0))
        text_otp += f'Борису выпала: {ryka_bot_bj[-1]}\n-------------------------\n'
        ryka_pl_bj.append(deck_cards_bj.pop(0))
        text_otp +=f'Вам выпала: {ryka_pl_bj[-1]}\n-------------------------\n'
        text_otp +=f"Последняя карта – закрытая, мягко ложиться на стол, - игра началась."
        await message.answer(text_otp)
        ryka_bot_bj.append(deck_cards_bj.pop(0))
        func.save_info(connect, user_id, "ryka_pl_bj", str(ryka_pl_bj))
        func.save_info(connect, user_id, "ryka_bot_bj", str(ryka_bot_bj))
        func.save_info(connect, user_id, "deck_cards", str(deck_cards_bj))

        if "Туз" in func.get_variable(connect, user_id, "ryka_pl_bj"):
            if funcs_bj.check_victory(connect, user_id, "ryka_pl_bj") == "BJ":
                rating = float(func.get_variable(connect, user_id, "rating_bj"))
                func.save_info(connect, user_id, "rating_bj", round(rating+float(func.get_variable(connect, user_id,"stavka"))*1.875,2))
                func.save_info(connect, user_id, "state", "START")
                await message.answer(f"Вы победили, благодарите судьбу, - у вас BlackJack.\n\n📈 {func.get_variable(connect, user_id, 'rating_bj')} (+{float(func.get_variable(connect, user_id, 'stavka'))*1.875})", reply_markup=vd_bj_kb)
            else:
                await message.answer("У вас нет BlackJack-а.")
                func.save_info(connect, user_id, "state", "BEG_MOVE_PL_JB_")

        elif "Туз" in func.get_variable(connect, user_id, "ryka_bot_bj"):
            if funcs_bj.check_victory(connect, user_id, "ryka_pl_bj") == "BJ":
                rating = float(func.get_variable(connect, user_id, "rating_bj"))
                func.save_info(connect, user_id, "rating_bj",round(rating - float(func.get_variable(connect, user_id, "stavka")) * 2, 2))
                func.save_info(connect, user_id, "state", "START")
                await message.answer(f"У Бориса BlackJack.\n\n📉 {func.get_variable(connect, user_id, 'rating_bj')} (-{float(func.get_variable(connect, user_id, 'stavka')) * 2})",reply_markup=vd_bj_kb)
            else:
                await message.answer("У Бориса нет BlackJack-а.")
                func.save_info(connect, user_id, "state", "BEG_MOVE_PL_JB_")

        else:
            func.save_info(connect, user_id, "state", "BEG_MOVE_PL_JB_")


    if message.text == "Взять карту" and func.get_variable(connect, user_id, "state") == "MOVE_PL_JB":
        deck_cards_bj = func.create_list_deck_cards(func.get_variable(connect, user_id, "deck_black_jack"))
        await message.answer(f"Вы ватащили: {deck_cards_bj[0]}")

        if func.get_variable(connect,user_id, "open_dop_ryka") == "open":
            await message.answer("Выберите руку, в которую хотите взять карту.", reply_markup=ryka_kb)
        else:
            if move_pl_bj(user_id):
                rating = float(func.get_variable(connect, user_id, "rating_bj"))
                func.save_info(connect, user_id, "rating_bj",round(rating - (float(func.get_variable(connect, user_id, "stavka"))) * 1.35, 2))
                await message.answer(f"Вы проиграли, набрав больше 21, будьте сдержаннее в следующей раз.\n\n📉 {func.get_variable(connect, user_id, 'rating_bj')} (-{float(func.get_variable(connect, user_id, 'stavka')) * 1.35})", reply_markup=vd_bj_kb)
                func.save_info(connect, user_id, "ryka_pl_bj", str([]))
                func.save_info(connect, user_id, "state", "START")

    if message.text == "Основная" and func.get_variable(connect, user_id, "state") == "MOVE_PL_JB" and func.get_variable(connect,user_id, "open_dop_ryka") == "open":
        func.save_info(connect, user_id, "choose_ryka", "\'ryka_pl_bj\'")
        if move_pl_bj(user_id):
            rating = float(func.get_variable(connect, user_id, "rating_bj"))
            func.save_info(connect, user_id, "rating_bj",round(rating - (float(func.get_variable(connect, user_id, "stavka"))) * 1.35, 2))
            func.save_info(connect, user_id, "ryka_pl_bj", func.get_variable(connect, user_id, "dop_ryka_bj"))
            func.save_info(connect, user_id, "dop_ryka_bj", str([]))
            func.save_info(connect, user_id, "open_dop_ryka", "close")
            await message.answer(f"Вы проиграли, набрав больше 21, будьте сдержаннее в следующей раз.\n\n📉 {func.get_variable(connect, user_id, 'rating_bj')} (-{float(func.get_variable(connect, user_id, 'stavka')) * 1.35})", reply_markup=vd_bj_kb)
            func.save_info(connect, user_id, "state", "BEG_MOVE_PL_JB_")

    if func.get_variable(connect, user_id, "state") == "MOVE_PL_JB" and funcs_bj.sum_card(connect, user_id, "ryka_pl_bj") == 21:
        rating = float(func.get_variable(connect, user_id, "rating_bj"))
        func.save_info(connect, user_id, "rating_bj",round(rating + float(func.get_variable(connect, user_id, "stavka")) * 1.5, 2))
        await message.answer(f"Вы победили, набрав 21 очко.\n\n📈 {func.get_variable(connect, user_id, 'rating_bj')} (+{float(func.get_variable(connect, user_id, 'stavka')) * 1.5})", reply_markup=vd_bj_kb)
        if func.get_variable(connect, user_id, "open_dop_ryka") == "open":
            func.save_info(connect, user_id, "state", "BEG_MOVE_PL_JB_")
            func.save_info(connect, user_id ,"open_dop_ryka", "close")
            func.save_info(connect, user_id,"ryka_pl_bj",func.get_variable(connect, user_id, "dop_ryka_bj"))
            func.save_info(connect, user_id, "dop_ryka_bj", str([]))
        else:
            func.save_info(connect, user_id, "ryka_pl_bj", str([]))
            func.save_info(connect, user_id, "state", "START")

    if message.text == "Дополнительная" and func.get_variable(connect, user_id, "state") == "MOVE_PL_JB" and func.get_variable(connect,user_id, "open_dop_ryka") == "open":
        func.save_info(connect, user_id, "choose_ryka", "\'dop_ryka_bj\'")
        if move_pl_bj(user_id):
            rating = float(func.get_variable(connect, user_id, "rating_bj"))
            func.save_info(connect, user_id, "rating_bj",round(rating - (float(func.get_variable(connect, user_id, "stavka"))) * 1.35, 2))
            func.save_info(connect, user_id, "dop_ryka_bj", str([]))
            func.save_info(connect, user_id, "open_dop_ryka", "close")
            await message.answer(f"Вы проиграли, набрав больше 21, будьте сдержаннее в следующей раз.\n\n📉 {func.get_variable(connect, user_id, 'rating_bj')} (-{float(func.get_variable(connect, user_id, 'stavka')) * 1.35})", reply_markup=vd_bj_kb)
            func.save_info(connect, user_id, "state", "BEG_MOVE_PL_JB_")

    if func.get_variable(connect, user_id, "state") == "MOVE_PL_JB" and message.text == "Спасовать":
        ryka_bot_bj = func.create_list_deck_cards(func.get_variable(connect, user_id, "ryka_bot_bj"))
        await message.answer(f"Закрытая карта Бориса: {ryka_bot_bj[-1]}")
        funcs_bj.move_bot_bj(connect, user_id)
        if len(func.create_list_deck_cards(func.get_variable(connect, user_id, "ryka_bot_bj"))) > 2:
            await message.answer(f"Борис вытащил: {func.create_list_deck_cards(func.get_variable(connect, user_id, 'ryka_bot_bj'))[-1]}")

    # ---------------------------------------------
    if func.get_variable(connect, user_id, "state") == "BEG_MOVE_PL_JB_":
        ryka_pl_bj = func.create_list_deck_cards(func.get_variable(connect, user_id, "ryka_pl_bj"))
        if len(ryka_pl_bj) >= 2 and ryka_pl_bj[0][2:] == ryka_pl_bj[1][2:] and func.get_variable(connect, user_id,"open_dop_ryka") != "close" and float(func.get_variable(connect, user_id, "rating_bj")) >= 2*float(func.get_variable(connect, user_id, "stavka")):
            await message.answer("Вам выпали карты одинакого напиманала, у вас есть возможность использовать вторую руку.", reply_markup=split_kb)
            func.save_info(connect, user_id, "state", "CHOOSE_SPLIT")
        else:
            if func.get_variable(connect, user_id, "open_dop_ryka") == "open":
                await message.answer(f"Ваша основная рука: {','.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'ryka_pl_bj')))}",reply_markup=vibor)
                await message.answer(f"Ваша дполнительная рука: {','.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'dop_ryka_bj')))}")
            else:
                await message.answer(f"Ваша рука: {','.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'ryka_pl_bj')))}",reply_markup=vibor)
            func.save_info(connect, user_id, "state", "MOVE_PL_JB")

    if func.get_variable(connect, user_id, "state") == "CHOOSE_SPLIT" and message.text == "Не играть сплит":
        func.save_info(connect, user_id, "state", "BEG_MOVE_PL_JB_")
        func.save_info(connect, user_id, "open_dop_ryka", "close")

    if func.get_variable(connect, user_id, "state") == "CHOOSE_SPLIT" and message.text == "Играть сплит":
        ryka_pl_bj = func.create_list_deck_cards(func.get_variable(connect, user_id, "ryka_pl_bj"))
        dop_ryka_bj = func.create_list_deck_cards(func.get_variable(connect, user_id, "dop_ryka_bj"))
        dop_ryka_bj.append(ryka_pl_bj.pop(0))
        func.save_info(connect, user_id, "ryka_pl_bj", str(ryka_pl_bj))
        func.save_info(connect, user_id, "dop_ryka_bj", str(dop_ryka_bj))
        func.save_info(connect, user_id, "open_dop_ryka", "open")
        func.save_info(connect, user_id, "state", "BEG_MOVE_PL_JB_")

    if func.get_variable(connect, user_id, "state") == "BEG_MOVE_PL_JB":
        if func.get_variable(connect,user_id, "open_dop_ryka") == "open":
            await message.answer(f"Ваша дополнительная рука: {','.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'dop_ryka_bj')))}")
            await message.answer(f"Ваша основная рука: {','.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'ryka_pl_bj')))}", reply_markup=vibor)
        else:
            await message.answer(f"Ваша рука: {','.join(func.create_list_deck_cards(func.get_variable(connect, user_id, 'ryka_pl_bj')))}",reply_markup=vibor)
        func.save_info(connect, user_id, "state", "MOVE_PL_JB")

    if funcs_bj.sum_card(connect, user_id, "ryka_bot_bj") > 21:
        rating = float(func.get_variable(connect, user_id, "rating_bj"))
        func.save_info(connect, user_id, "rating_bj",round(rating + float(func.get_variable(connect, user_id, "stavka")) * 1.5, 2))
        await message.answer(f"Борис перебрал карт и вы победили, так как он набрал более 21.\n\n📈 {func.get_variable(connect, user_id, 'rating_bj')} (+{float(func.get_variable(connect, user_id, 'stavka')) * 1.5})", reply_markup=vd_bj_kb)
        func.save_info(connect, user_id, "ryka_pl_bj", str([]))
        func.save_info(connect, user_id, "state", "START")

    if func.get_variable(connect, user_id, "state") == "END_GAME_BJ":
        if func.get_variable(connect,user_id, "open_dop_ryka") == "open":
        # Проверки с двумя руками:

            if (funcs_bj.sum_card(connect, user_id, "ryka_bot_bj") >= funcs_bj.sum_card(connect, user_id, "ryka_pl_bj")) and (funcs_bj.sum_card(connect, user_id, "ryka_bot_bj") >= funcs_bj.sum_card(connect, user_id, "dop_ryka_bj")):
                rating = float(func.get_variable(connect, user_id, "rating_bj"))
                func.save_info(connect, user_id, "rating_bj",round(rating - float(func.get_variable(connect, user_id, "stavka")) * 3, 2))
                await message.answer(f"Сокрушительно поражение. Обе ваши руки проигрышные. Печально, что еще тут скажешь.\n\n📉 {func.get_variable(connect, user_id, 'rating_bj')} (-{float(func.get_variable(connect, user_id, 'stavka')) * 3})",reply_markup=vd_bj_kb)
                func.save_info(connect, user_id, "state", "START")

            if (funcs_bj.sum_card(connect, user_id, "ryka_bot_bj") >= funcs_bj.sum_card(connect, user_id, "ryka_pl_bj")) and (funcs_bj.sum_card(connect, user_id, "ryka_bot_bj") < funcs_bj.sum_card(connect, user_id, "dop_ryka_bj")):
                rating = float(func.get_variable(connect, user_id, "rating_bj"))
                func.save_info(connect, user_id, "rating_bj", round(rating + float(func.get_variable(connect, user_id, "stavka")) * 1.5, 2))
                rating = float(func.get_variable(connect, user_id, "rating_bj"))
                func.save_info(connect, user_id, "rating_bj",round(rating - float(func.get_variable(connect, user_id, "stavka")) * 1.35, 2))
                func.save_info(connect, user_id, "open_dop_ryka", "close")
                func.save_info(connect, user_id, "dop_ryka_bj", str([]))
                await message.answer(f"Можно это назвать успехом или поражение? Скорее это полу-успех. Ваша дополнительна рука - победила, а основная рука - проиграла.\n\n📈 {func.get_variable(connect, user_id, 'rating_bj')} (+{(float(func.get_variable(connect, user_id, 'stavka')) * 1.5) - (float(func.get_variable(connect, user_id, 'stavka')) * 1.35)})",reply_markup=vd_bj_kb)
                func.save_info(connect, user_id, "state","START")

            if (funcs_bj.sum_card(connect, user_id, "ryka_bot_bj") < funcs_bj.sum_card(connect, user_id, "ryka_pl_bj")) and (funcs_bj.sum_card(connect, user_id, "ryka_bot_bj") >= funcs_bj.sum_card(connect, user_id, "dop_ryka_bj")):
                rating = float(func.get_variable(connect, user_id, "rating_bj"))
                func.save_info(connect, user_id, "rating_bj",round(rating + float(func.get_variable(connect, user_id, "stavka")) * 1.5, 2))
                rating = float(func.get_variable(connect, user_id, "rating_bj"))
                func.save_info(connect, user_id, "rating_bj",round(rating - float(func.get_variable(connect, user_id, "stavka")) * 1.35, 2))
                func.save_info(connect, user_id, "ryka_pl_bj", func.get_variable(connect, user_id, "dop_ryka_bj"))
                func.save_info(connect, user_id, "dop_ryka_bj", str([]))
                func.save_info(connect, user_id, "open_dop_ryka", "close")
                await message.answer(f"Можно это назвать успехом или поражение? Скорее это полу-успех. Ваша основная рука - победила, а дополнительна рука - проиграла.\n\n📈 {func.get_variable(connect, user_id, 'rating_bj')} (+{(float(func.get_variable(connect, user_id, 'stavka')) * 1.5) - (float(func.get_variable(connect, user_id, 'stavka')) * 1.35)})",reply_markup=vd_bj_kb)
                func.save_info(connect, user_id, "state", "START")

            if (funcs_bj.sum_card(connect, user_id, "ryka_bot_bj") < funcs_bj.sum_card(connect, user_id, "ryka_pl_bj")) and (funcs_bj.sum_card(connect, user_id, "ryka_bot_bj") < funcs_bj.sum_card(connect, user_id, "dop_ryka_bj")):
                rating = float(func.get_variable(connect, user_id, "rating_bj"))
                func.save_info(connect, user_id, "rating_bj",round(rating + float(func.get_variable(connect, user_id, "stavka")) * 3, 2))
                await message.answer(f"Вы победили обоими руками! Удивительно, правда?\n\n📈 {func.get_variable(connect, user_id, 'rating_bj')} (+{float(func.get_variable(connect, user_id, 'stavka')) * 3})",reply_markup=vd_bj_kb)
                func.save_info(connect, user_id, "state", "START")

        # Проверки с одной рукой:

        else:
            if funcs_bj.sum_card(connect, user_id, "ryka_bot_bj") >= funcs_bj.sum_card(connect, user_id,"ryka_pl_bj") and func.get_variable(connect, user_id, "open_dop_ryka") != "open":
                rating = float(func.get_variable(connect, user_id, "rating_bj"))
                func.save_info(connect, user_id, "rating_bj",round(rating - float(func.get_variable(connect, user_id, "stavka")) * 1.35, 2))
                await message.answer(f"Вы проиграли, так как набрали очков меньше, чем Борис.\n\n📉 {func.get_variable(connect, user_id, 'rating_bj')} (-{float(func.get_variable(connect, user_id, 'stavka')) * 1.35})",reply_markup=vd_bj_kb)
                func.save_info(connect, user_id, "state", "START")

            if funcs_bj.sum_card(connect, user_id, "ryka_bot_bj") < funcs_bj.sum_card(connect, user_id,"ryka_pl_bj") and func.get_variable(connect, user_id, "open_dop_ryka") != "open":
                rating = float(func.get_variable(connect, user_id, "rating_bj"))
                func.save_info(connect, user_id, "rating_bj",round(rating + float(func.get_variable(connect, user_id, "stavka")) * 1.5, 2))
                await message.answer(f"Вы победили, набрав больше очков чем Борис.\n\n📈 {func.get_variable(connect, user_id, 'rating_bj')} (+{float(func.get_variable(connect, user_id, 'stavka')) * 1.5})",reply_markup=vd_bj_kb)
                func.save_info(connect, user_id, "state", "START")
    # -------------------------------------------------------------------------------------------------------------------------------------------------

    if message.text == "Карточные игры" and func.get_variable(connect, user_id, "state") == "START":
        await message.answer("Здесь вы можете сыграть с Борисом в карточные игры.", reply_markup=cards_kb)

    if message.text == "Другие игры" and func.get_variable(connect, user_id, "state") == "START":
        await message.answer("Здесь вы можете сыграть в классические игры Бориса.", reply_markup=games)

    if message.text == "Выйти в меню игр" and (func.get_variable(connect, user_id, 'state') != "CARDS" or  func.get_variable(connect, user_id, 'state') != "MOVE" or func.get_variable(connect, user_id, 'state') !="MOVE_BOT"):
        func.save_info(connect, user_id, "state", "START")
        await message.answer(f"Борис доволен игрой.", reply_markup=games_kb)

    if message.text == "Сыграть с Борисом" and func.get_variable(connect, user_id, "state") == "START":
        await message.answer("💬Какую игру выбираешь?", reply_markup=games_kb)

    if message.text == "Другое" and func.get_variable(connect, user_id, "state") == "START":
        await message.answer(
            "Здесь вы можете дать Борису уверенность в завтрашнем дне, а также рассказать о багах или своих предложениях насчет дальнейшего развития бота.",
            reply_markup=add_menu)

    if message.text == "Выйти в главное меню" and (func.get_variable(connect, user_id, 'state') != "CARDS" or  func.get_variable(connect, user_id, 'state') != "MOVE" or func.get_variable(connect, user_id, 'state') !="MOVE_BOT"):
        func.save_info(connect, user_id, "state", "START")
        await message.answer("Вы попали в начальное меню.", reply_markup=main_menu)

    if message.text == "Связаться с нами" and func.get_variable(connect, user_id, "state") == "START":
        await message.answer(
            "Связаться с разработчиками можно по следующим ссылкам (отвечаем на конструктивные и понятные сообщения, голосовые не будут прослушаны, спам – неприемлем):")
        await message.answer("https://t.me/G0lubec")
        await message.answer("https://t.me/Snailid", reply_markup=exit_kb)

    if message.text == "Пожертвовать средства 💳" and func.get_variable(connect, user_id, "state") == "START":
        await message.answer(
            "Да, конечно, без проблем, мой друг, вот номер карты, на которую можно сбросить червонец-другой: 4377723767674546",
            reply_markup=donat_kb)

    if message.text == "Выйти в меню игр." and (func.get_variable(connect, user_id, 'state') != "CARDS" or  func.get_variable(connect, user_id, 'state') != "MOVE" or func.get_variable(connect, user_id, 'state') !="MOVE_BOT"):
        func.save_info(connect, user_id, "state", "START")
        await message.answer(f"Вы вернулись в меню игр.", reply_markup=games_kb)

    if message.text == 'Сегодня я на мели' and func.get_variable(connect, user_id, "state") == "START":
        await message.answer("Вы попали в начальное меню", reply_markup=main_menu)

    if message.text == "Рейтинг" and func.get_variable(connect, user_id, "state") == "START":
        await message.answer("🏅 Лучшие игроки сезона 🏅")
        top_cr = func.RATING_CARDS(connect)
        await message.answer(f'Двадцать одно\n\n{top_cr}\n🎖Ваш рейтинг, {func.get_variable(connect, user_id, "name")}: {func.get_variable(connect, user_id, "rating_cards")}')
        top_dice = func.RATING_DICE(connect)
        await message.answer(f'Кости\n\n{"".join(top_dice)}\n🎖Ваш рейтинг, {func.get_variable(connect, user_id, "name")}: {func.get_variable(connect, user_id, "rating_dice")}')
        top_cr_zr = func.RATING_CR_ZR(connect)
        await message.answer(f'Крестики-нолики\n\n{top_cr_zr}\n🎖Ваш рейтинг, {func.get_variable(connect, user_id, "name")}: {func.get_variable(connect, user_id, "rating_cr_zr")}\n\n')
        top_durak = func.RATING_DURAK(connect)
        await message.answer(f'Дурак\n\n{top_durak}\n🎖Ваш рейтинг, {func.get_variable(connect, user_id, "name")}: {func.get_variable(connect, user_id, "rating_durak")}\n\n')
        top_bj = func.RATING_BJ(connect)
        await message.answer(f'BlackJack\n\n{top_bj}\n🎖Ваш рейтинг, {func.get_variable(connect, user_id, "name")}: {func.get_variable(connect, user_id, "rating_bj")}\n\n{rating_mes}')

if __name__ == "__main__":
    connect = sqlite3.connect(name_baz + ".db")
    cursor = connect.cursor()
    executor.start_polling(dp)
