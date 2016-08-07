from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *
from main.utils import nlp

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def handle_todo(current_user, text, processed_text):

    fbid = current_user.fbid
    
    if 'add todo' in processed_text:
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


    elif 'todo' in processed_text:
        # Log response
        message_log.log_message('show_todo_response', current_user, text, None)

        send_todo_list(current_user)

        # # Send todo list inline
        # todo_list_message = generate_todo_list_string(current_user)
        # send_api_helper.send_basic_text_message(fbid, todo_list_message)
        # message_log.log_message('todo_list_message', current_user, todo_list_message, None)

    elif nlp.user_is_in_complete_todo_state(processed_text, current_user):
        # Subtract one since the numbering starts at 1
        index_to_complete = int(processed_text) - 1

        todo_list = todo_list = ToDoTask.objects.filter(user=current_user, completed=False).order_by('id')

        if index_to_complete >= len(todo_list):
            # Error
            # TODO
            x = 1
        else:
            todo_to_complete = todo_list[index_to_complete]
            todo_to_complete.completed = True
            todo_to_complete.save()

            # Log response
            message_log.log_message('complete_todo_response', current_user, processed_text, None)

            # Send message and log it
            send_todo_list(current_user)

def send_todo_list(current_user):
    # Send link to todo list
    show_todo_message = generate_todo_list_string(current_user) + "\n\nReply with the corresponding number to complete a task."
    send_api_helper.send_button_message(fbid, show_todo_message, [
            {
                'type': 'web_url',
                'url': BASE_HEROKU_URL + '/users/'+fbid+'/todo',
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







