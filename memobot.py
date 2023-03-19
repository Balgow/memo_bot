import json
from collections import defaultdict
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

token = "Token"

class MemoBot:
    def __init__(self, token):
        self.bot = TeleBot(token)
        
        self.action = ''
        self.input = ''
        self.balgyn_chat_id = 'your_chat_id'

    def start(self, message):
        print(self.get_categories())
        try:
            print("*** Memo has been started ***")
            self.bot.send_message(message.chat.id, "Hello, Mommy and Daddy. How can I help you today?")
            self.all_content_pretty(message)
        except:
            self.bot.send_message(message.chat.id, "I got crashed. Try again")
            self.all_content_pretty(message)

    def set_categories(self, categories):
        with open('data.json', 'w') as f:
            json.dump(categories, f)

    def get_categories(self):
        f = open('data.json')
        data = json.load(f)
        f.close()
        return data
    

    def add_category(self,message):
        try:
            self.action = 'add'
            self.bot.send_message(message.chat.id, "Please enter a category name:")
        except:
            self.bot.send_message(message.chat.id, "I got crashed. Try again")
            self.all_content_pretty(message)

    def delete_category(self, message):
        try:
            self.action = 'delete'
                    
            markup = InlineKeyboardMarkup()
            for key in self.get_categories():
                markup.row(InlineKeyboardButton(text=key, callback_data=key), InlineKeyboardButton(text="🗑", callback_data="^"+key))
            markup.row(InlineKeyboardButton(text='🚫Cancel', callback_data="back_to_menu"))

            self.bot.send_message(message.chat.id, 'Choose category that need to be deleted', reply_markup=markup)
        except:
            self.bot.send_message(message.chat.id, "I got crashed. Try again")
            self.all_content_pretty(message)

    def all_content_json(self, message):
        try:
            self.bot.send_message(message.chat.id, json.dumps(self.get_categories())) 
        except:
            self.bot.send_message(message.chat.id, "I got crashed. Try again")
            self.all_content_pretty(message)
    
    def all_content_pretty(self, message, return_need = False):
        try:
            self.action = ''
            self.input = ''

            markup = InlineKeyboardMarkup()
            for key in self.get_categories():
                markup.row(InlineKeyboardButton(text=key, callback_data=key))
            markup.row(InlineKeyboardButton(text='🔙', callback_data="back_to_menu"), InlineKeyboardButton(text='➕', callback_data="add"), InlineKeyboardButton(text='➖', callback_data="delete"))
            
            if return_need:
                return markup
            
            self.bot.send_message(message.chat.id, 'Choose needed category', reply_markup=markup)
        except:
            self.bot.send_message(message.chat.id, "I got crashed. Try again")
            self.all_content_pretty(message)

    def query_handler(self, call):
        try:
            message = call.message
            data = call.data

            

            if self.action == 'add':
                if data == 'back_to_menu':
                    self.bot.edit_message_reply_markup(message.chat.id, call.message.message_id, reply_markup = self.all_content_pretty(message, return_need = True))
                    return
                
                if data[0] == "^":
                    self.action = ''
                    data = data[1:]
                    
                    categories = self.get_categories()
                    sub_categories = categories

                    if data:
                        for key in data.split('^'):
                            sub_categories = sub_categories[key]
                    
                    sub_categories[self.input] = {}

                    self.set_categories(categories)

                    self.bot.send_message(message.chat.id, "Following information is for Balgowski(Just in case)")
                    self.all_content_json(message)

                    self.bot.send_message(message.chat.id, f'Category "{self.input}" was added')
                    self.input = ''
                    self.bot.edit_message_reply_markup(message.chat.id, call.message.message_id, reply_markup= self.all_content_pretty(message, return_need = True))
                    self.bot.send_message(self.balgyn_chat_id, json.dumps(self.get_categories()))
                    self.all_content_pretty(message)

                else:
                    sub_categories = self.get_categories()
                    for key in data.split('^'):
                        sub_categories = sub_categories[key]
                    markup = InlineKeyboardMarkup()
                    markup.row(InlineKeyboardButton(text="⬇️", callback_data='^'+data))
                    for key in sub_categories:
                        markup.row(InlineKeyboardButton(text=key, callback_data=data+"^"+key))
                    markup.row(InlineKeyboardButton(text='🚫Cancel', callback_data="back_to_menu"))

                    self.bot.edit_message_reply_markup(message.chat.id, call.message.message_id, reply_markup = markup)
                    
            elif self.action == 'delete':
                if data == 'back_to_menu':
                    self.bot.edit_message_reply_markup(message.chat.id, call.message.message_id, reply_markup = self.all_content_pretty(message, return_need = True))
                    return
                
                if data[0] == "^":
                    self.action = ''
                    data = data[1:]

                    self.bot.send_message(message.chat.id, "Following information is for Balgowski(Just in case)")
                    self.all_content_json(message)
                    self.bot.send_message(self.balgyn_chat_id, json.dumps(self.get_categories()))
                    categories = self.get_categories()
                    sub_categories = categories

                    if '^' in data:
                        deleting_category, data = data[data.rindex('^')+1:], data[:data.rindex('^')]
                        for key in data.split('^'):
                            sub_categories = sub_categories[key]
                    else:
                        deleting_category = data

                    

                    del sub_categories[deleting_category]
                    self.set_categories(categories)
                    
                    self.bot.send_message(message.chat.id, f'Category "{deleting_category}" was deleted')
                    
                    self.bot.edit_message_reply_markup(message.chat.id, call.message.message_id, reply_markup= self.all_content_pretty(message, return_need = True))
                    
                    self.all_content_pretty(message)


                else:
                    sub_categories = self.get_categories()
                    for key in data.split('^'):
                        sub_categories = sub_categories[key]
                    markup = InlineKeyboardMarkup()
                    for key in sub_categories:
                        markup.row(InlineKeyboardButton(text=key, callback_data=data+'^'+key), InlineKeyboardButton(text="🗑", callback_data="^"+data+'^'+key))
                    markup.row(InlineKeyboardButton(text='🚫Cancel', callback_data="back_to_menu"))

                    self.bot.edit_message_reply_markup(message.chat.id, call.message.message_id, reply_markup= markup)
            else:  
                if data == "back_to_menu":
                    self.all_content_pretty(message)
                elif data == 'add':
                    self.add_category(message)
                elif data == 'delete':
                    self.delete_category(message)
                    
                else:
                    markup = InlineKeyboardMarkup()
                    
                    sub_categories = self.get_categories()
                    for key in data.split('^'):
                        sub_categories = sub_categories[key]
                    for key in sub_categories:
                        markup.row(InlineKeyboardButton(text=key, callback_data=data+'^'+key))

                    markup.row(InlineKeyboardButton(text='🔙', callback_data="back_to_menu"), InlineKeyboardButton(text='➕', callback_data="add"), InlineKeyboardButton(text='➖', callback_data="delete"))
            
                    self.bot.send_message(message.chat.id, 'Choose needed category', reply_markup=markup)
        except:
            self.bot.send_message(message.chat.id, "I got crashed. Try again")
            self.all_content_pretty(message)
            

    def echo(self, message):
        try:
            if self.action == 'add':
                self.input = message.text

                markup = InlineKeyboardMarkup()
                markup.row(InlineKeyboardButton(text="⬇️", callback_data='^'))
                for key in self.get_categories():
                    markup.row(InlineKeyboardButton(text=key, callback_data=key))
                markup.row(InlineKeyboardButton(text='🚫Cancel', callback_data="back_to_menu"))
                
                self.bot.send_message(message.chat.id, 'Choose place where you want to add a category', reply_markup=markup) 
        except:
            self.bot.send_message(message.chat.id, "I got crashed. Try again")
            self.all_content_pretty(message)
        

            
    
    def send_help(self, message):
        try:
            output = '\n\n'.join([
                '*For my little princess*',
                '/start - Start Memo', 
                '/add_category - Add Category to Memo', 
                '/delete_category - Delete Category from Memo', 
                '/all_content_pretty - Display Menu of Memo',
                '*For Balgowski*',
                '/all_content_json - Display Json of Menu'])
            self.bot.send_message(message.chat.id, output)
        except:
            self.bot.send_message(message.chat.id, "I got crashed. Try again")
            self.all_content_pretty(message)





    def run(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.start(message)

        @self.bot.message_handler(commands=['add_category'])
        def add_category(message):
            self.add_category(message)

        @self.bot.message_handler(commands=['delete_category'])
        def delete_category(message):
            self.delete_category(message)

        @self.bot.message_handler(commands=['all_content_json'])
        def all_content_json(message):
            self.all_content_json(message)

        @self.bot.message_handler(commands=['all_content_pretty'])
        def all_content_pretty(message):
            self.all_content_pretty(message)
        
        @self.bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):
            self.query_handler(call)

        @self.bot.message_handler(commands=['help'])
        def send_help(message):
            self.send_help(message)

        @self.bot.message_handler(func=lambda message: True)
        def echo(message):
            self.echo(message)

        
        
        self.bot.polling(none_stop = True)
    


memo = MemoBot(token)
memo.run()

