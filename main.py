import os
import telebot
import base64
import cryptography
from cryptography.fernet import Fernet


#---------------Custom Exceptions---------------#
class KeyError(Exception):
    pass

#---------------api-key import from env file---------------#
API_KEY = os.getenv('API_KEY')


#---------------bot initialized---------------#
bot = telebot.TeleBot(API_KEY)


#---------------Global variables---------------#
p_key = None
key = None
mode = None


#---------------function to encode---------------#
def Encode(key,message):
    enc=[]
    if len(message) == 0:
        raise Exception("No message found!")
    if key is None:
        raise KeyError()
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
        
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def encrypt_file(file_path):
    global p_key
    if p_key is None:
        raise KeyError("Encryption key not set!")

    with open(file_path, 'rb') as file:
        data = file.read()

    f = Fernet(p_key)
    encrypted_data = f.encrypt(data)

    enc_file_path = "enc_"+file_path

    with open(enc_file_path, 'wb') as file:
        file.write(encrypted_data)
    os.remove(file_path)


#---------------function to decode---------------#
def Decode(key,message):
    dec=[]
    if len(message) == 0:
        raise Exception("No message found!")
    if key is None:
        raise KeyError()
    message = base64.urlsafe_b64decode(message).decode()
    for i in range(len(message)):
        key_c = key[i % len(key)]
        dec.append(chr((256 + ord(message[i])- ord(key_c)) % 256))
        
    return "".join(dec)


def decrypt_file(file_path):
    global p_key
    if p_key is None:
        raise KeyError("Encryption key not set!")

    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    f = Fernet(p_key)
    decrypted_data = f.decrypt(encrypted_data)

    dec_file_path = "dec_"+file_path

    with open(dec_file_path, 'wb') as file:
        file.write(decrypted_data)
    os.remove(file_path)


#---------------message handlers -> replys to users messages---------------#
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Genarate your Private key using /generate')


@bot.message_handler(commands=['generate'])
def generate(message):
    global p_key, key
    p_key = Fernet.generate_key()
    key = p_key.decode()
    bot.send_message(message.chat.id, 'Your private key is: '+"`"+ key +"`", parse_mode='MarkdownV2')
    

@bot.message_handler(commands=['set'])
def set(message):
    global p_key , key
    bot.send_message(message.chat.id,'Private Key set to: ' + message.text[5::])
    key = message.text[5::]
    p_key = key.encode()


@bot.message_handler(commands=['encode'])
def encode(message):
    bot.send_message(message.chat.id, "Encryption mode on!")
    global mode
    mode = 0


@bot.message_handler(commands=['decode'])
def decode(message):
    bot.send_message(message.chat.id, "Decryption mode on!")
    global mode
    mode = 1


@bot.message_handler()
def handle_text(message):
    global key, mode
    
    if mode is None:
        bot.send_message(message.chat.id, 'Please activate encryption or decryption mode first using /encode or /decode command.')
        return
    
    if mode == 0:
        try:
            bot.send_message(message.chat.id, 'Here is your encoded message: ' + "`" + Encode(key, message.text) + "`", parse_mode='MarkdownV2')
        except KeyError:
            bot.send_message(message.chat.id, 'Private key not set!')
        except Exception:
            bot.send_message(message.chat.id, 'No message found!')

    elif mode == 1:
        try:
            bot.send_message(message.chat.id, 'Here is your decoded message: ' + Decode(key, message.text))
        except KeyError:
            bot.send_message(message.chat.id, 'Private key not set!')
        except Exception:
            bot.send_message(message.chat.id, 'No message found!')
        except binascii.Error:
            bot.send_message(message.chat.id, 'Private key not set!')


@bot.message_handler(content_types=['voice', 'audio', 'photo', 'document'])
def handle_file(message):
    if mode is None:
        bot.send_message(message.chat.id, 'Please activate encryption or decryption mode first using /encode or /decode command.')
        return
    elif 'voice' in message.content_type:
        process_file(message, message.voice.file_id, ".mp3")
    elif 'audio' in message.content_type:
        process_file(message, message.audio.file_id, ".mp3")
    elif 'photo' in message.content_type:
        process_file(message, message.photo[3].file_id, ".jpg")
    elif 'document' in message.content_type:
        process_file(message, message.document.file_id, ".jpg")


def process_file(message, file_id, file_extension):
    global mode
    file_suffix = 1
    file_name = message.from_user.username + file_extension
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    while os.path.isfile(file_name):
        file_name = message.from_user.username + "_" + str(file_suffix) + file_extension
        file_suffix += 1

    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    if mode == 0:
        try:
            encrypt_file(file_name)
            encrypted_file_name = "enc_" + file_name
            with open(encrypted_file_name, 'rb') as doc:
                bot.send_document(message.chat.id, doc)
            os.remove(encrypted_file_name)
        except Exception:
            bot.send_message(message.chat.id, "Key is not set!")

    elif mode == 1:
        try:
            decrypt_file(file_name)
            decrypted_file_name = "dec_" + file_name
            with open(decrypted_file_name, 'rb') as doc:
                bot.send_document(message.chat.id, doc)
            os.remove(decrypted_file_name)
        except cryptography.fernet.InvalidToken:
            bot.send_message(message.chat.id, "Not an encrypted file, switch to /encode mode!")
            os.remove(file_name)
        except KeyError:
            bot.send_message(message.chat.id, "Key is not set!")
            os.remove(file_name)


bot.infinity_polling()