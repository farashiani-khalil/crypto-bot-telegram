from pyrogram import Client, filters
from bs4 import BeautifulSoup
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = Client(
    "my_bot",
    bot_token="lfwD9L8Koc"
)




##################################################################################################
def get_price_crypto():
    totel_result = requests.get("https://coinmarketcap.com/")
    suop = BeautifulSoup(totel_result.content, "html.parser")
    cmc = suop.find("div", class_='cmc-homepage')
    table = cmc.find("div", class_='tableWrapper___3utdq cmc-table-homepage-wrapper___22rL4')
    detail = table.find("table", class_="cmc-table cmc-table___11lFC cmc-table-homepage___2_guh")
    obj = detail.find("tbody")
    counter = 1
    information = {}
    for i in obj:
        crypto = i.text.split(sep='$')
        excoin = crypto[0].split(str(counter))
        coin = excoin[1]
        prices = crypto[1].split(sep='%')
        flag = 0
        counter2 = 0
        real_price = ''
        diff_24h_price = ''
        diff_7d_price = ''
        for i in prices[0]:
            if i == '.':
                flag = 1
            if flag == 1:
                counter2 += 1
            if counter2 <= 3:
                real_price += i
            else:
                diff_24h_price += i
        for i in prices[1]:
            diff_7d_price += i
    
        information[coin] = [real_price, diff_24h_price, diff_7d_price]
        counter += 1
        if counter > 10:
            break
    return information

##############################################################################################


@app.on_message(filters.command("cryptoprice"))
def crypto_get(client, message):
    try:
        x = get_price_crypto()
        msg = ''
        for i in x:
            msg += f"""
⏳{i}:              
price:{x[i][0]}               
24h%: {x[i][1]}              
7d%: {x[i][2]}
        """
        message.reply_text(msg)
    except:
        message.reply_text("یه مشکلی پیش اومده به آقای خدادوست یه پیامی بده درستش کنه /n @jezza1")

def crypto_job():
    try:
        x = get_price_crypto()
        msg = ''
        counter = 0
        for i in x:
            counter += 1
            msg += f"""
⏳{i}:              
price:{x[i][0]}               
24h%: {x[i][1]}              
7d%: {x[i][2]}
        """
            if counter == 4:
                break
        list_of_group_crypto = []
        f = open('group.txt', 'r')
        for i in f:
            string = i.replace("\n","") 
            list_of_group_crypto.append(string)
        f.close()
        for item in list_of_group_crypto:
            try:
                app.send_message(item ,msg)
            except:
                continue
    except:
        app.send_message(
            '-575083439',
            "یه مشکلی پیش اومده به آقای خدادوست یه پیامی بده درستش کنه /n @jezza1",
            )

######################################################################################################

@app.on_message(filters.command("addmygroup"))
def crypto_get(client, message):
    id_group = message.chat.id
    file_write = open('group.txt', 'a')
    file_read = open('group.txt', 'r')
    admin = []
    for item in app.iter_chat_members(str(id_group), filter="administrators"):
        if item.status == 'creator' or item.status == 'administrator':
            admin.append(item.user.id)
    if message.from_user.id in admin:
        if str(id_group) not in file_read:
            file_write.write(str(id_group))
            message.reply_text('گروهتو به لیستم اضافه کردم\n')
        else:
            message.reply_text('گروهت تو لیستم هست \n')
    else:
        message.reply_text('باید ادمین باشی تا بتونی از این دستور استفاده کنی \n')
    file_write.close()
    file_read.close()

###################################################################################################3
@app.on_message(filters.command("removemygroup"))
def crypto_get(client, message):
    id_group = message.chat.id
    file_write = open('group.txt', 'a')
    file_read = open('group.txt', 'r')
    admin = []
    for item in app.iter_chat_members(str(id_group), filter="administrators"):
        if item.status == 'creator' or item.status == 'administrator':
            admin.append(item.user.id)
    if message.from_user.id in admin:
        with open("group.txt", "r") as f:
            lines = f.readlines()
        with open("group.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != str(id_group):
                    f.write(line)
        message.reply_text('گروهتو از لیستم حذف کردم\n')
    else:
        message.reply_text('باید ادمین باشی تا بتونی از این دستور استفاده کنی \n')

######################################################################################################
@app.on_message(filters.command("help"))
def crypto_get(client, message):
    message.reply_text("""
این لیست دستوراتمه
/addmygroup
قیمت ارز دییتال رو هر یک ساعت توی گروهت میفرستم
/removemygroup
دیگه توی گروهت قیمت ارز دیجیتال رو نمیفرستم تا زمانی که مججد گروهت رو ادد کنی
/cryptoprice
قیمت و تغییرات ده تا ارز دیجیتال رو برات میفرستم
""")


scheduler = AsyncIOScheduler()

scheduler.add_job(crypto_job, "interval", seconds=30)

scheduler.start()
app.run()
