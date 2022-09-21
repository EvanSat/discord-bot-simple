# from typing import Optional

import discord
import os
import random
from dotenv import load_dotenv


def message_help(message):
    return message.channel.send('Commands include:\n'
                                '\"hello\" - responds with a greeting\n'
                                '\"bye\" - responds with a farewell\n'
                                '\"~d#\" - a dice roll with a number of input sides (replace \'#\' as the '
                                'desired number of sides\n'
                                '\"help\" - prints out bot commands with details')


def dice_roll(user_message, message):
    d_roll = None
    if user_message[1].lower() == "d" and user_message[2] is not None:
        d_roll = random.randint(1, int(user_message[2:]))
        print(f'Dice roll: {d_roll}')
    return message.channel.send(f'{d_roll}')


def discord_bot():
    load_dotenv('.env')  # Allows access to the .env TOKEN
    BOT_TOKEN = os.getenv("TOKEN")
    client = discord.Client()

    @client.event
    async def on_ready():
        print("We have logged in as {0.user}".format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:  # Doesn't allow bot to respond to itself
            return
        username = str(message.author).split('#')[0]
        # username_at = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel.name)

        print(f'{username}: {user_message} ({channel})')

        if message.channel.name == 'bot-commands':  # Name of specific response channel
            if user_message.lower() == 'hello':
                await message.channel.send(f'Hello @{username}')
            elif user_message.lower() == 'bye':
                await message.channel.send(f'Good bye {username}')
            elif user_message[0] == '~':
                await dice_roll(user_message, message)
            if user_message.lower() == 'help':
                await message_help(message)

            return

    client.run(BOT_TOKEN)


if __name__ == '__main__':
    discord_bot()
