from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *


BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def handle_todo(current_user, text, processed_text):

    fbid = current_user.fbid
    
    if('add todo' in processed_text):
        # Log response
        message_log.log_message('add_todo_response', current_user, text, None)

        # Create todo
        add_todo_message = text.replace('add todo', '').strip()

        todo = ToDoTask(text=add_todo_message, user=current_user)
        todo.save()

        # Send message telling them that we created the todo
        add_todo_message = '"'+add_todo_message+'" added to your to do list!'
        send_api_helper.send_basic_text_message(fbid,add_todo_message)
        message_log.log_message('add_todo_message', current_user, add_todo_message, None)


    elif('todo' in processed_text):
        # Log response
        message_log.log_message('show_todo_response', current_user, text, None)

        # Send link to todo list
        show_todo_message = ""
        send_api_helper.send_button_message(fbid, show_todo_message, [
                {
                    'type': 'web_url',
                    'url': BASE_HEROKU_URL + '/users/'+fbid+'/todo',
                    'title': 'View your todo list'
                }
            ])
        message_log.log_message('show_todo_message', current_user, show_todo_message, None)

        # Send todo list inline
        todo_list_message = generate_todo_list_string(current_user)
        send_api_helper.send_basic_text_message(fbid, todo_list_message)
        message_log.log_message('todo_list_message', current_user, todo_list_message, None)

def generate_todo_list_string(current_user):
    return_string = ''

    todo_list = ToDoTask.objects.filter(user=current_user, completed=False)

    if len(todo_list) == 0:
        return_string = "You're done with everything!"
    else:
        count = 0
        for todo in todo_list:
            return_string += str(count) + ') ' + todo.text + '\n'
            count += 1

    return return_string







