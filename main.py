import inquirer
import subprocess

questions = [
    inquirer.List('source_app',
          message="Which app do you want to get the messages from?",
          choices=['Telegram', 'Whatsapp'])
]

answers = inquirer.prompt(questions)

if answers['source_app'] == 'Telegram':
    exec(open('./src/telegram.py').read())
elif answers['source_app'] == 'Whatsapp':
    subprocess.run(['node', './src/whatsapp.js'])
