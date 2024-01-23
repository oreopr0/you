import telebot
import requests
from telebot import types
from time import sleep
from datetime import datetime
import os

logo = '''
---------------------------------
'''

print(logo)

token = "6149645127:AAH6yTfAvHk6b3LAoKSENEXZgev4l5xBUVI"
Developer = "j_S_9"
bot = telebot.TeleBot(token)
is_bot_active = True

A = types.InlineKeyboardMarkup(row_width=2)
Ch = types.InlineKeyboardButton(text="𝘾𝙃𝘼𝙉𝙉𝙀𝙇", url="t.me/SpidrX")
Dev = types.InlineKeyboardButton(text="𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝙍", url="t.me/hack_onlaain")
A.add(Ch, Dev)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id, "https://t.me/SpidrX", caption="""
↯︙ 👋 مرحباً بك عزيزي في بوت GitHub X Bet لسحب المستودعات العامة الموجودة في موقع github.com ارسل اسم المستودع للبحث عن جميع الأدوات على سبيل المثال Hulk 🔰
""", parse_mode="markdown", reply_markup=A)

@bot.message_handler(func=lambda message: True)
def search(message):
    query = message.text
    try:
        projects = search_projects(query)
        if projects:
            for project in projects:
                download_project(project, message.chat.id)
        else:
            bot.send_photo(message.chat.id, "https://t.me/SpidrX", caption="""
↯︙ ♻️ عذراً عزيزي لم يتم البحث بنجاح عن المستودع يرجى التحقق من الاسم أو رابط الإحالة ❌
""", parse_mode="markdown", reply_markup=A)
    except Exception as e:
        print(f"Error: {str(e)}")
        bot.send_photo(message.chat.id, "https://t.me/SpidrX", caption="""
↯︙ حدثت مشكلة أثناء تنفيذ البحث. يرجى المحاولة مرة أخرى في وقت لاحق. ❌
""", parse_mode="markdown", reply_markup=A)

def search_projects(query):
    try:
        url = f"https://api.github.com/search/repositories?q={query}%20in:name"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        projects = data.get('items', [])
        return projects
    except Exception as e:
        print(f"Error in search_projects: {str(e)}")
        return []

def download_project(project, chat_id):
    try:
        Name = project.get('name')
        URL = project.get('html_url')
        Devs = project.get('owner', {}).get('login')
        ziplink = f"https://github.com/{Devs}/{Name}/archive/master.zip"
        response = requests.get(ziplink)
        response.raise_for_status()
        with open(f"{Name}.zip", 'wb') as file:
            file.write(response.content)

        # حصول على تاريخ آخر تعديل
        last_modified = datetime.fromtimestamp(os.path.getmtime(f"{Name}.zip"))

        # حصول على معلومات إضافية
        repo_info_url = f"https://api.github.com/repos/{Devs}/{Name}"
        repo_info_response = requests.get(repo_info_url)
        repo_info_response.raise_for_status()
        repo_info = repo_info_response.json()

        # الحصول على المعلومات
        stars = repo_info.get('stargazers_count', 0)
        forks = repo_info.get('forks_count', 0)
        watchers = repo_info.get('watchers_count', 0)

        bot.send_document(chat_id, open(f"{Name}.zip", 'rb'))
        bot.send_message(chat_id, f"اسم المشروع: {Name}\n"
                                  f"رابط المشروع: {URL}\n"
                                  f"اسم المستخدم: {Devs}\n"
                                  f"عدد النجوم: {stars}\n"
                                  f"عدد الفوركس: {forks}\n"
                                  f"عدد المراقبين: {watchers}\n"
                                  f"المشروع مفتوح المصدر\n"
                                  f"تاريخ آخر تعديل: {last_modified}\n"
                                  f"تاريخ النشر: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"Error in download_project: {str(e)}")
        bot.send_photo(chat_id, "https://t.me/SpidrX", caption=f"""
↯︙ حدثت مشكلة أثناء تحميل المستودع {Name}. يوجد تلف يرجى مراسلة :- {Developer}
""", parse_mode="markdown", reply_markup=A)

private = "\033[2;32m Running... /start"
print(private)
bot.polling(none_stop=True)
