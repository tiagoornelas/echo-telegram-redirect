# echo-telegram-redirect

Echo is a telegram redirect service for redirecting and manipulating telegram
messages

## Environment Variables

In order to run, you'll need to create a `.env` file with the following keys:
```
TELEGRAM_API_ID
TELEGRAM_API_HASH
MONGO_URL
```
## Duplicate Key Error

In order to avoid this duplicated key error, if you want to run two Echo
instances simultaneously, you need to delete session files from the branch and
then run again.
