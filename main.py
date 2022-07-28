import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputMediaDocument

app = telebot.TeleBot('5449636806:AAFoXz0_5Pgb-LdbHG8mpgBLUoNOlrYrP8g')

class Data(object):
    def __init__(self) -> None:
        self.data:dict={}
        self.i_obj2=0
        self.i_obj1=0
    def add(self,data:dict) -> None:
        self.data.update(data)
    def obj(self,num):
        if num==1:self.i_obj1+=1
        else: self.i_obj2+=1

data:object=Data()

def keyboard(keyboard:list):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    markup.add(*[KeyboardButton(x) for x in keyboard])
    return markup


@app.message_handler()
def main(m):
    if m.text=='/start':
        app.send_message(m.chat.id,'Ваш регион Москва?', reply_markup=keyboard(['Москва', 'Выбрать другой']))
        app.register_next_step_handler(m,region)

def region_another(m):
    data.add({'region':m.text})
    app.register_next_step_handler(app.send_message(m.chat.id, 'Выберите тип объекта', reply_markup=keyboard(['Объект или мульти сплит-система', 'Бытовые кондиционеры'])),type_object)

def region(m):
    if m.text=='Москва':
        regions=['Центральный','Северный','Северо-Восточный','Восточный','Юго-Восточный','Южный','Юго-Западный','Западный','Северо-Западный','Зеленоградский','Новомосковский','Троицкий']
        app.register_next_step_handler(app.send_message(m.chat.id, 'Выберите район', reply_markup=keyboard(regions)),region_moscow)
    if m.text=='Выбрать другой':
        regions=['test1','test2']
        app.register_next_step_handler(app.send_message(m.chat.id, 'Введите город'),region_another)

def region_moscow(m):
    data.add({'region': 'Москва - '+m.text})
    app.register_next_step_handler(app.send_message(m.chat.id, 'Выберите тип объекта', reply_markup=keyboard(['Объект или мульти сплит-система', 'Бытовые кондиционеры'])),type_object)

def type_object(m):
    if m.text=='Бытовые кондиционеры':
        app.register_next_step_handler(app.send_message(m.chat.id, f'Модель {data.i_obj2+1}-го кондиционера', reply_markup=keyboard(['07','09','12','18','24'])),model_obj2)
    else: app.register_next_step_handler(app.send_message(m.chat.id, f'Опишите задачу и бюджет'),info_obj1)

def model_obj2(m):
    if not data.i_obj2:data.add({'obj2': [{'model': m.text}]})
    else: data.data['obj2'].append({'model': m.text})
    app.register_next_step_handler(app.send_message(m.chat.id, f'Стандартный прайс?', reply_markup=keyboard(['Да', 'Нет'])),setup_obj2)

def setup_obj2(m):
    if m.text=='Нет':app.register_next_step_handler(app.send_message(m.chat.id, f'Опишите доп. работы'), info_obj2)
    else:
        data.data['obj2'][data.i_obj2].update({'work_info': 'Стандарт'})
        app.register_next_step_handler(app.send_message(m.chat.id, f'Стандартная цена?', reply_markup=keyboard(['Да', 'Нет'])),info_obj2)

def info_obj2(m):
    if m.text=='Нет':
        data.data['obj2'][data.i_obj2].update({'work_info': m.text})
        app.register_next_step_handler(app.send_message(m.chat.id, f'Введите сумму за монтаж'), price_obj2)
    elif m.text=='Да':
        app.register_next_step_handler(app.send_message(m.chat.id, f'Добавить {data.i_obj2+1}-й?', reply_markup=keyboard(['Да','Нет'])), add_obj2)
        data.data['obj2'][data.i_obj2].update({'work_price': 'Стандарт'})

def price_obj2(m):
    data.data['obj2'][data.i_obj2].update({'work_price': m.text})
    app.register_next_step_handler(app.send_message(m.chat.id, f'Добавить {data.i_obj2+2}-й?', reply_markup=keyboard(['Да','Нет'])), add_obj2)

def add_obj2(m):
    if m.text=='Да':
        data.obj(2)
        app.register_next_step_handler(app.send_message(m.chat.id, f'Модель {data.i_obj2+1} кондиционера', reply_markup=keyboard(['07','09','12','18','24'])),model_obj2)
    else:
        app.register_next_step_handler(app.send_message(m.chat.id, f'Введите контактные данные (контакт и имя)'),contact_obj2)

def info_obj1(m):
    if not data.i_obj2:data.add({'obj1': [{'info': m.text}]})
    else: data.data['obj1'].append({'info': m.text})
    app.register_next_step_handler(app.send_message(m.chat.id, f'Добавить файл?', reply_markup=keyboard(['Да','Нет'])), file_obj1)

def file_obj1(m):
    if m.text=='Нет':
        app.register_next_step_handler(app.send_message(m.chat.id, f'Введите контактные данные (контакт и имя)'),contact_obj1)
    else:
        app.register_next_step_handler(app.send_message(m.chat.id, f'Отправте файл'),filed_obj1)

def filed_obj1(m):
    if not data.i_obj1:data.data['obj1'][0].update({'files': [app.download_file(app.get_file(m.document.file_id).file_path)]})
    else:data.data['obj1'][0]['files'].append(app.download_file(app.get_file(m.document.file_id).file_path))
    data.obj(1)
    app.register_next_step_handler(app.send_message(m.chat.id, f'Добавить еще один файл?', reply_markup=keyboard(['Да','Нет'])), file_obj1)


def contact_obj1(m):
    data.data['obj1'][0].update({'contacts': m.text})
    if not data.i_obj1:
        app.send_message(-629408312, 
                        f'''
Регион - {data.data["region"]}
Объект или мульти сплит-система
Информация - {data.data['obj1'][0]["info"]}

Контакты - {data.data["obj1"][0]["contacts"]}
'''
                )
    if data.i_obj1:
        app.send_media_group(-629408312, [InputMediaDocument(data.data["obj1"][0]["files"][i], caption=f'''
Регион - {data.data["region"]}
Объект или мульти сплит-система
Информация - {data.data['obj1'][0]["info"]}

Контакты - {data.data["obj1"][0]["contacts"]}
''') if not i else InputMediaDocument(data.data["obj1"][0]["files"][i]) for i in range(len(data.data["obj1"][0]["files"]))])
    app.send_message(m.chat.id, 'Публикация отправлена, чтобы создать новый запрос введите /start')

def contact_obj2(m):
    data.data['obj2'][0].update({'contacts': m.text})
    app.send_message(m.chat.id, 'Публикация отправлена, чтобы создать новый запрос введите /start')
    
    for i in data.data['obj2']:
        app.send_message(-629408312, 
                        f'''
Регион - {data.data["region"]}
Модель кондиционера - {i["model"]}
Информация - {i["work_info"]}
Цена - {i["work_price"]}

Контакты - {data.data["obj2"][0]["contacts"]}
'''
                )


app.infinity_polling()