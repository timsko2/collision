import discord
from dotenv import load_dotenv
import os

load_dotenv()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Ne pas répondre à soi-même pour éviter les boucles infinies
        if message.author == self.user:
            return
        
        print(f'Message from {message.author}: {message.content}')
        
        # Répondre à un message spécifique
        if message.content.lower() == 'bonjour':
            await message.channel.send(f'Salut {message.author.mention}!')
        
        # Répondre par une réaction
        if 'python' in message.content.lower():
            await message.add_reaction('🐍')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

if DISCORD_TOKEN is None:
    print("Erreur: Le token Discord n'a pas été trouvé dans le fichier .env")
else:
    client.run(DISCORD_TOKEN)
