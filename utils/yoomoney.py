from __main__ import *
import threading
import time
import random
from yoomoney import Client
from yoomoney import Quickpay

token = yoomoney_token
client = Client(token)

def accept_payment(message, type_of_buy, cost, type_of_own='update'):

    def payment_with_timeout(url, timeout=120.0):
        result = [None]  # используем список вместо прямого значения, чтобы иметь возможность изменить его в любом потоке

        def check_payment(label):
            # Проверяем историю операции
            history = client.operation_history(label=label)
            for operation in history.operations:
                if operation.status == "success":
                    result[0] = True
                else:
                    result[0] = False

        language_code = groups[message.chat.id].lang_code

        markup = types.InlineKeyboardMarkup()
        temp_button = types.InlineKeyboardButton(
            text=templates[language_code]["pay.txt"],
            url=url,
        )
        markup.add(temp_button)
        bot.send_message(
            message.chat.id,
            templates[language_code]["info_about_buy.txt"].format(type_of_buy=type_of_buy, cost=cost),
            reply_markup = markup,
            parse_mode = "HTML"
        )
        print(label)

        start_time = time.time()

        # Запускаем таймеры, пока не истечет общее время ожидания
        while time.time() - start_time < timeout and result[0] is None:
            timer = threading.Timer(2.0, lambda: check_payment(label))
            timer.start()
            timer.join()

        if result[0] is None:
            result[0] = False

        if result[0]:
            if type_of_own=='update':
                if type_of_buy=="You buy USER subscription":
                    groups[message.chat.id].add_new_user(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, 'USER', 300)
                    groups[message.chat.id].load_subscription(message.chat.id)
                    groups[message.chat.id].track_sub(message.chat.id, new=True)

                elif type_of_buy=="You buy SMALL BUSINESS subscription":
                    groups[message.chat.id].add_new_user(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, 'SMALL BUSINESS', 700)
                    groups[message.chat.id].load_subscription(message.chat.id)
                    groups[message.chat.id].track_sub(message.chat.id, new=True)

                elif type_of_buy=="You buy BIG BUSINESS subscription":
                    groups[message.chat.id].add_new_user(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, 'BIG BUSINESS', 1000)
                    groups[message.chat.id].load_subscription(message.chat.id)
                    groups[message.chat.id].track_sub(message.chat.id, new=True)

                for group_id in groups[message.chat.id].id_groups:
                        groups[group_id].subscription = groups[message.chat.id].subscription
                        groups[group_id].permissions[groups[group_id].subscription]["messages_limit"] = groups[message.chat.id].permissions[groups[message.chat.id].subscription]["messages_limit"]
                        groups[group_id].permissions[groups[group_id].subscription]["dynamic_gen_permission"] = groups[message.chat.id].permissions[groups[message.chat.id].subscription]["dynamic_gen_permission"]
                        groups[group_id].permissions[groups[group_id].subscription]["voice_output_permission"] = groups[message.chat.id].permissions[groups[message.chat.id].subscription]["voice_output_permission"]
            elif type_of_own=='extend':
                groups[message.chat.id].extend_sub(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
                groups[message.chat.id].track_sub(message.chat.id, new=True)
            elif type_of_own=='more_messages':
                groups[message.chat.id].add_purchase_of_messages(
                    message.chat.id,
                    val
                )
                groups[message.chat.id].messages_limit = groups[message.chat.id].groups[message.chat.id].messages_limit + val

                for group in groups[message.chat.id].id_groups:
                    groups[group].messages_limit = groups[message.chat.id].messages_limit

                bot.send_message(
                    message.chat.id,
                    templates[language_code]["new_messages.txt"],
                    parse_mode="HTML",
        )
        else:
            bot.send_message(message.chat.id, groups[message.chat.id].templates[language_code]["buy_was_canceled.txt"])



    # Генерация случайного 8-значного числа для label
    label = random.randint(10000000, 99999999)


    # Создание формы оплаты
    quickpay = Quickpay(
        receiver="4100118270605528",
        quickpay_form="shop",
        targets="Buy product",
        paymentType="SB",
        sum=2,           #cost
        label=label,
    )

    # Вызов функции с передачей ссылки
    threading.Thread(target=payment_with_timeout, args=(quickpay.redirected_url, 120.0)).start()


def support(message, cost):
    # Создание формы оплаты

    def payment_with_timeout(url, timeout=300.0):
        result = [None]  # используем список вместо прямого значения, чтобы иметь возможность изменить его в любом потоке

        def check_payment(label):
            # Проверяем историю операции
            history = client.operation_history(label=label)
            for operation in history.operations:
                if operation.status == "success":
                    result[0] = True
                else:
                    result[0] = False

        language_code = groups[message.chat.id].lang_code

        markup = types.InlineKeyboardMarkup()
        temp_button = types.InlineKeyboardButton(
            text=templates[language_code]["pay.txt"],
            url=url,
        )
        markup.add(temp_button)
        bot.send_message(
            message.chat.id,
            templates[language_code]["info_about_support.txt"].format(cost=cost),
            reply_markup = markup,
            parse_mode = "HTML"
        )
        print(label)

        start_time = time.time()

        # Запускаем таймеры, пока не истечет общее время ожидания
        while time.time() - start_time < timeout and result[0] is None:
            timer = threading.Timer(2.0, lambda: check_payment(label))
            timer.start()
            timer.join()

        if result[0] is None:
            result[0] = False

        return result[0]

    # Генерация случайного 8-значного числа для label
    label = random.randint(10000000, 99999999)


    # Создание формы оплаты
    quickpay = Quickpay(
        receiver="4100118270605528",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        sum=cost,
        label=label,
    )

    # Вызов функции с передачей ссылки
    res = payment_with_timeout(quickpay.redirected_url)
    return res