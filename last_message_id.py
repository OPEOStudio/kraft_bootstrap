def getLastMessageId():
    try:
        file_handler = open('last_message_id.txt', 'r')
    except FileNotFoundError:
        return 0
    last_message_id = file_handler.read()
    file_handler.close()
    return int(last_message_id)

## Saves the last message ID
def saveLastMessageId(id):
    file_handler = open('last_message_id.txt', 'w+')
    file_handler.write(str(id))
    file_handler.close()