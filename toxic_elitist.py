from discord import Intents
from discord import Client
import asyncio
import yaml

from discord_embed_poster import DiscordEmbedPoster
from log_uploader import LogUploader
from logger import log_debug, log_error, log_info
from logs_collector import LogsCollector
from report_converter import ReportConverter
from report_parser import ReportParser

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
    
    log_info(f'Logged in as {client.user.name} ({client.user.id})')

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
        log_debug(f'Command: {command_name}, Parameters: {parameters}')

        if command_name == 'convert':
            converter = ReportConverter()
            converter.convert_links(parameters[0])

        if command_name == 'collect':
            arcdps_logs_path = load_arcdps_logs_path()
            logs_collector = LogsCollector(arcdps_logs_path, "./logs/")
            logs_collector.copy_files_by_datetime(parameters[0])

        if command_name == 'upload':            
            uploader = LogUploader()
            uploader.upload(parameters[0])

        if command_name == 'publish':            
            report_parser = ReportParser()
            parsed_reports = report_parser.parse_reports(parameters[0])
            
            channel_id = load_channel_id()
            embed_poster = DiscordEmbedPoster(client, channel_id)
            await embed_poster.post_embed_message(parsed_reports)

# Load the bot token from a YAML file
def load_bot_token():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
        return config['bot_token']

# Load the channel id from a YAML file
def load_channel_id():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
        return config['channel_id']
    
# Load the arcdps log files path from a YAML file
def load_arcdps_logs_path():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
        return config['arcdps_logs']

# Run the bot with the loaded bot token
async def run_bot():
    bot_token = load_bot_token()
    await client.start(bot_token)

# Start the bot and console input listener concurrently
try:
    loop = asyncio.get_event_loop()
    tasks = asyncio.gather(run_bot(), console_input())
    loop.run_until_complete(tasks)
except Exception as e:
    log_error(f"An unknown error occurred: {e}")
    input("Press Enter to exit...")
