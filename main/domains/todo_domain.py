from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *


BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def handle_todo(current_user, text):
    if('add todo' in text):
        # Create todo
        todo_text = text.replace('add todo', '')

        todo = ToDoTask(text=todo_text, user=current_user)
        todo.save()

        # Send message telling them that we created the todo
        send_api_helper.send_basic_text_message(fbid,'"'+todo_text+'" added to your to do list!')
    elif('todo' in text):
        send_api_helper.send_button_message(fbid, "Your todo list:", [
                {
                    'type': 'web_url',
                    'url': BASE_HEROKU_URL + '/users/'+fbid+'/todo',
                    'title': 'To Do List'
                }
            ])