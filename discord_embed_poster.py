import discord
import datetime

class DiscordEmbedPoster:
    def __init__(self, client, channel_id):
        self.client = client
        self.channel_id = channel_id

    async def post_embed_message(self, content):
        channel = self.client.get_channel(self.channel_id)
        sorted_dps_reports = self.sort_dps_reports(content)
        embed = self.create_table_embed(sorted_dps_reports)
        await channel.send(embed=embed)

    def sort_dps_reports(self, dps_reports):
        sorted_dps_reports = sorted(dps_reports, key=lambda report: report['timestamp'])
        return sorted_dps_reports

    def create_table_embed(self, dps_reports):
        start_timestamp = dps_reports[0]['timestamp']

        last_report = dps_reports[-1]
        # Convert the Unix timestamp to a datetime object
        timestamp_dt = datetime.datetime.fromtimestamp(last_report['timestamp'])
        # Create a timedelta object with the duration in seconds
        duration_td = datetime.timedelta(seconds=last_report['duration'])
        # Add the duration to the timestamp
        end_timestamp_dt = timestamp_dt + duration_td
        # Convert the end timestamp back to a Unix timestamp
        end_timestamp = int(end_timestamp_dt.timestamp())

        embed = discord.Embed(
            title=f'<t:{start_timestamp}:D>',
            description=f'from <t:{start_timestamp}:T> to <t:{end_timestamp}:T>',
            color=discord.Color.blurple()
        )

        result_header = 'r'
        duration_header = 'duration'
        encounter_header = 'encounter'

        result_value = ''
        duration_value = ''
        encounter_value = ''

        for dps_report in dps_reports:
            success_emoji = '✅' if dps_report['success'] else '❌'
            duration_minutes = int(dps_report['duration'] / 60)
            duration_seconds = int(dps_report['duration'] % 60)
            encounter_link = f"[{dps_report['encounter']}]({dps_report['permalink']})"

            result_value += success_emoji + '\n'
            duration_value +=f"{duration_minutes:02d}m {duration_seconds:02d}s" + '\n'
            encounter_value += encounter_link + '\n'
        
        embed.add_field(
            name=result_header,
            value=result_value,
            inline=True
        )
        
        embed.add_field(
            name=duration_header,
            value=duration_value,
            inline=True
        )
        
        embed.add_field(
            name=encounter_header,
            value=encounter_value,
            inline=True
        )

        return embed
