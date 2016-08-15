from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *
from main.utils import nlp

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def handle_todo(current_user, text, processed_text):

    fbid = current_user.fbid
    
    if nlp.user_is_in_complete_todo_state(processed_text, current_user):
        # Subtract one since the numbering starts at 1
        index_to_complete = int(processed_text) - 1

        todo_list = todo_list = ToDoTask.objects.filter(user=current_user, completed=False).order_by('id')

        if index_to_complete >= len(todo_list):
            # Error
            incorrect_todo_index_message = 'Please try again and enter a valid todo number'
            send_api_helper.send_basic_text_message(current_user.fbid, incorrect_todo_index_message)
            message_log.log_message('incorrect_todo_index_message', current_user, incorrect_todo_index_message, None)

        else:
            todo_to_complete = todo_list[index_to_complete]
            todo_to_complete.completed = True
            todo_to_complete.save()

            # Log response
            message_log.log_message('complete_todo_response', current_user, processed_text, None)

            # Send message and log it
            send_todo_list(current_user)
    elif nlp.user_is_in_todo_listening_state(current_user):
        # Log response
        message_log.log_message('add_todo_response', current_user, text, None)

        # Create todo
        add_todo_message = text

        todo = ToDoTask(text=add_todo_message, user=current_user)
        todo.save()

        # Send message telling them that we created the todo
        add_todo_message = 'Your todos:\n' + generate_todo_list_string(current_user)
        send_api_helper.send_basic_text_message(fbid,add_todo_message)
        message_log.log_message('add_todo_message', current_user, add_todo_message, None)
    elif processed_text == 'add todo':
         # Log response
        message_log.log_message('add_todo_trigger_response', current_user, text, None)

        # Send message telling them that we are listening (and log)
        add_todo_trigger_message = 'Tell me what you want to add to your todo list:'
        send_api_helper.send_basic_text_message(current_user.fbid,add_todo_trigger_message)

        message_log.log_message('add_todo_trigger_message', current_user, add_todo_trigger_message, None)

    elif processed_text.startswith('add todo'):
        # Log response
        message_log.log_message('add_todo_response', current_user, text, None)

        # Create todo
        add_todo_message = text.replace('add todo', '').strip()

        todo = ToDoTask(text=add_todo_message, user=current_user)
        todo.save()

        # Send message telling them that we created the todo
        add_todo_message = 'Your todos:\n' + generate_todo_list_string(current_user)
        send_api_helper.send_basic_text_message(fbid,add_todo_message)
        message_log.log_message('add_todo_message', current_user, add_todo_message, None)


    elif processed_text == 'todo':
        # Log response
        message_log.log_message('show_todo_response', current_user, text, None)

        send_todo_list(current_user)

        # # Send todo list inline
        # todo_list_message = generate_todo_list_string(current_user)
        # send_api_helper.send_basic_text_message(fbid, todo_list_message)
        # message_log.log_message('todo_list_message', current_user, todo_list_message, None)

    

def send_todo_list(current_user):
    # Send link to todo list
    show_todo_message = generate_todo_list_string(current_user) + "\nReply with the corresponding number to complete a task."
    send_api_helper.send_button_message(current_user.fbid, show_todo_message, [
            {
                'type': 'web_url',
                'url': BASE_HEROKU_URL + '/users/'+current_user.fbid+'/todo',
                'title': 'View your todo list'
            }
        ])
    message_log.log_message('show_todo_message', current_user, show_todo_message, None)


def generate_todo_list_string(current_user):
    return_string = ''

    todo_list = ToDoTask.objects.filter(user=current_user, completed=False).order_by('id')

    if len(todo_list) == 0:
        return_string = "You're done with everything!"
    else:
        count = 1
        for todo in todo_list:
            return_string += str(count) + ') ' + todo.text + '\n'
            count += 1

    return return_string







