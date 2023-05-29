from discord import Intents
from discord import Client
import asyncio
import yaml

from colors import Colors
from folder_scanner import FolderScanner
from log_uploader import LogUploader

# Create a bot instance and set command prefix
intents = Intents.default()

# Create a client instance
client = Client(intents=intents)

# Function for asynchronous console input
async def async_input(prompt):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, input, prompt)

# Function to handle console input
async def console_input():
    # Wait until the bot is ready
    await client.wait_until_ready()
    
    print(Colors.GREEN + f'Logged in as {client.user.name} ({client.user.id})' + Colors.RESET)

    while True:
        command = await async_input('> ')

        if command == 'exit':
            await client.close()
            break

        # Extracting command and parameters from the input
        parts = command.split(' ')
        command_name = parts[0]
        parameters = parts[1:]

        # Process the command and parameters
        print(f'Command: {command_name}, Parameters: {parameters}')

        if command_name == 'scan':
            scanner = FolderScanner()
            found_files = scanner.scan(parameters[0])
            for file in found_files:
                print(file)

        if command_name == 'upload':            
            uploader = LogUploader()
            uploader.upload(parameters[0])

# Load the bot token from a YAML file
def load_bot_token():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
        return config['bot_token']

# Run the bot with the loaded bot token
async def run_bot():
    bot_token = load_bot_token()
    await client.start(bot_token)

# Start the bot and console input listener concurrently
loop = asyncio.get_event_loop()
tasks = asyncio.gather(run_bot(), console_input())
loop.run_until_complete(tasks)
