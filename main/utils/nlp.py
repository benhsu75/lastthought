
def is_onboarding_domain(current_user, text):
    return current_user.state == 0

def is_goals_domain(current_user, text):
    if('goals' in text):
        return True
    else:
        return False

def is_logs_domain(current_user, text):
    # TODO by cathy
    x = 1

def is_todo_domain(current_user, text):
    return 'todo' in text
