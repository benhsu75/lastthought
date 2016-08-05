
def is_onboarding_domain(current_user, text):
    return current_user.state == 0

def is_goals_domain(current_user, text):

    last_message = Message.objects.filter(user=current_user).order_by('-created_at')[0]

    if('goals' in text):
        return True
    elif(last_message.message_type == 6):
        return True
    else:
        return False

def is_logs_domain(current_user, text):
    # TODO by cathy
    x = 1

def is_todo_domain(current_user, text):
    return 'todo' in text
