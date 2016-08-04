from main.models import Message

# WE MUST FOLLOW THIS
# If it ends in 'message' it is sent TO the user
# If it ends in 'response' it is sent FROM the user

# 0 - welcome_message
# 1 - ask_for_name_message
# 2 - name_response
# 3 - nice_to_meet_message
# 4 - learn_more_message
# 5 - goals_trigger_message
# 6 - goal_prompt_message
# 7 - goal_response
# 8 - misunderstood_message
# 9 - misunderstood_response
# 10 - show_todo_message
# 11 - add_todo_message

# Mapping a message_key to the message_type that we store in the Message object
message_mapping = {
  'welcome_message' : 0,
  'ask_for_name_message' : 1,
  'name_response' : 2,
  'nice_to_meet_message' : 3,
  'learn_more_message' : 4,
  'goals_trigger_message' : 5,
  'goal_prompt_message' : 6,  
  'goal_response' : 7,
  'misunderstood_response' : 9,
  'show_todo_message' : 10,
  'add_todo_message' : 11,
}

def log_message(message_key, user, text, data):
  # Validate that message_key is valid
  if message_key not in message_mapping:
      return False

  # Determine if sent_to_user
  if 'message' in message_key:
      sent_to_user = True
  else:
      sent_to_user = False

  message_type = message_mapping[message_key]
  m = Message(user=user, sent_to_user=sent_to_user, message_type=message_type)
  m.save()

  # Add any extra data depending on message_type
  if(message_type == 5):
      m.goal_in_reference = data['goal']
      m.save()
  elif(message_type == 6):
      m.goal_in_reference = data['goal']
      m.save()
  elif(message_type == 7):
      m.goal_in_reference = data['goal']
      m.save()

  return True
