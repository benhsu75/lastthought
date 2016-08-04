from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *


BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def handle_todo(current_user, text):

    fbid = current_user.fbid
    
    if('add todo' in text):
        # Log response
        message_log.log_message('add_todo_response', current_user, text, None)

        # Create todo
        add_todo_message = text.replace('add todo', '')

        todo = ToDoTask(text=add_todo_message, user=current_user)
        todo.save()

        # Send message telling them that we created the todo
        send_api_helper.send_basic_text_message(fbid,'"'+add_todo_message+'" added to your to do list!')
        message_log.log_message('add_todo_message', current_user, add_todo_message, None)


    elif('todo' in text):
        # Log response
        message_log.log_message('show_todo_response', current_user, text, None)

        show_todo_message = "Your todo list:"
        send_api_helper.send_button_message(fbid, show_todo_message, [
                {
                    'type': 'web_url',
                    'url': BASE_HEROKU_URL + '/users/'+fbid+'/todo',
                    'title': 'To Do List'
                }
            ])
        message_log.log_message('show_todo_message', current_user, show_todo_message, None)