# echo-telegram-redirect

Echo is a telegram redirect service for redirecting and manipulating telegram
messages both from telegram itself or whatsapp.

## Environment Variables

In order to run, you'll need to create a `.env` file with the following keys:
```
TELEGRAM_API_ID // Get your API ID from my.telegram.org
TELEGRAM_API_HASH // Get your API hash from my.telegram.org
TELEGRAM_BOT_TOKEN // Get the bot token by creating a bot with @botfather
TELEGRAM_RECIPIENT_CHAT_ID // For whatsapp to telegram redirect, we need to fixate a chat ID which the bot is an admin
MONGO_URL // Mongo Cluster URI/URL
```

## Telegram to Telegram

Upon running the script, selecting Telegram and loggin in to your Telegram account vida code sent, you'll be prompted
to select the "from" chats and "to" chat. It will be based on your account's chats.

Also, there is a special parameter which can sanitize messages. More type of sanitizations can be added in the future.

## Whatsapp to Telegram

The "to" chat will not be made based on a login via code as were made in Telegram to Telegram function. Instead, you'll
need to create a bot via @botfather, add it into the "to" chat as an admin and find out the chat's ID.

In the future we will be providing a more easy way to find this ID.

As mentioned before, create environment variables for the bot token and recipient (to) chat id.

Upon running the script and selecting Whatsapp, you'll receive a QR Code for logging in into your account.
Your whatsapp account will be used to select the "from" chat only.

After selecting the from chat and setting the recipient (to) inside the environment variables, we'll be ready ro go.

## MongoDB Database

We are keeping a MongoDB database for debug and log purposes, saving on it the messages sent in both methods and also
the errors we are catching in the process.

## Duplicate Key Error

In order to avoid this duplicated key error, if you want to run two Echo
instances simultaneously, you need to delete session files from the branch and
then run again.
