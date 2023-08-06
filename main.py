import discord
import random
from discord.ext import commands
from datetime import datetime
import os
import platform
from termcolor import colored
import asyncio
import psutil

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

TRANSCRIPT_CHANNEL_ID = 1137698768138010684
ID = 921530640510382100 #Guild ID
CATEGORY_ID = 1071925221214392392  #Category ID
SUPPORT_TEAM_ROLE_ID = [1067137048860958741]
EMOJI_ID = 937311948318572584 #Error Emoji
EMOJI_ID2 = 937311880836436009 #Success Emoji
async def statuschange():
    while True:
        membercount = len(bot.users)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Your DMs"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="My DMs"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Modmail"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Silly Development"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{membercount} Users"))
        await asyncio.sleep(60)
@bot.event
async def on_ready():
    bot.add_view(close())
    guild = bot.get_guild(ID)
    members = len(guild.members)
    python_version = platform.python_version()
    discord_version = discord.__version__
    total_gb = psutil.disk_usage('/').total / (1024.0 ** 3)
    memory_usage = psutil.virtual_memory().used
    memory_usage_gb = round(memory_usage / (1024 ** 3), 2)
    print(colored(f"╠{'═' * 43}╣", "blue"))
    print(colored(f"║{'':<14}Loading Bot... {'':<14}║", "blue"))
    await asyncio.sleep(0.5)
    print(colored(f"╠{'═' * 43}╣", "blue"))
    print(colored(f"║ {'Bot Name:':<20} {bot.user.name}#{bot.user.discriminator} {'║':<3}", "blue"))
    await asyncio.sleep(0.5)
    print(colored(f"║ {'Members:':<20} {members:<20}{'║':>2}", "blue"))
    await asyncio.sleep(0.5)
    print(colored(f"║ {'Python Version:':<20} {python_version:<20}{'║':>2}", "blue"))
    await asyncio.sleep(0.5)
    print(colored(f"║ {'Discord Version:':<20} {discord_version:<20}{'║':>2}", "blue"))
    await asyncio.sleep(0.5)
    print(colored(f"╠{'═' * 43}╣", "blue"))
    print(colored(f"║{'':<14}Bot is loaded! {'':<14}║", "blue"))
    print(colored(f"╠{'═' * 43}╣", "blue"))
    print(colored(f"║{'':<14}Time: {'0' if datetime.now().hour < 10 else ''}{datetime.now().hour}:{'0' if datetime.now().minute < 10 else ''}{datetime.now().minute}:{'0' if datetime.now().second < 10 else ''}{datetime.now().second} {'':<14}║", "blue"))
    print(colored(f"╠{'═' * 43}╣", "blue"))
    print(colored(f"║{'':<10} Listening to Messages {'':<10}║", "blue"))
    print(colored(f"╠{'═' * 43}╣", "blue"))
    await bot.loop.create_task(statuschange())
@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        print(colored(f"║{'':<2} Received Message From {message.author} {'':<2}║", "blue"))
        print(colored(f"╠{'═' * 43}╣", "blue"))
        guild = bot.get_guild(ID)
        member = guild.get_member(message.author.id)
        view = close()
        modmail_category = discord.utils.get(guild.categories, id=CATEGORY_ID)

        if modmail_category:
            channel = discord.utils.get(modmail_category.text_channels, name=str(message.author.id))
            if channel:
                message_embed = discord.Embed(
                    description=message.content,
                    color=0x6bbee3,
                    timestamp=datetime.now()
                )

                if message.author.avatar:
                    message_embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar.url)
                else:
                    message_embed.set_author(name=f"{message.author.name}#{message.author.discriminator}")

                emoji = bot.get_emoji(EMOJI_ID)
                emoji2 = bot.get_emoji(EMOJI_ID2)
                try:
                    await channel.send(embed=message_embed, view=view)
                    await message.add_reaction(emoji2)
                except:
                    await message.add_reaction(emoji)
                with open(f'temp/{channel.id}.txt', 'w+') as f:
                    f.writelines(f"[{datetime.now().month}/{datetime.now().day}/{datetime.now().year}  {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] : {message.author} -- {message.content}\n",)
                return

        modmail_channel = await guild.create_text_channel(name=str(message.author.id), category=modmail_category)
        start_embed_channel = discord.Embed(
            description=f"Hello Support Team, {message.author} Has Tried to Contact us. Please Respond to them.\n\n```{message.content}```",
            color=0x6bbee3
        )
        modmail_channel_content = ""
        for roleid in SUPPORT_TEAM_ROLE_ID:
            role = guild.get_role(roleid)
            modmail_channel_content+=f"<@&{role.id}>,"
        emoji = bot.get_emoji(EMOJI_ID)
        emoji2 = bot.get_emoji(EMOJI_ID2)
        await modmail_channel.send(modmail_channel_content,embed=start_embed_channel, view=view)
        await message.author.send(f"You have Started a Conversation with {guild.name}.")
        await message.add_reaction(emoji2)
        with open(f'temp/{modmail_channel.id}.txt', 'w+') as f:
            f.writelines(f"[{datetime.now().month}/{datetime.now().day}/{datetime.now().year}  {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] : {message.author} -- {message.content}\n")
    else:
        if isinstance(message.channel, discord.DMChannel):
            return
        if message.channel.category and message.channel.category.id == CATEGORY_ID and message.channel.name != 'transcripts':
            userid = message.channel.name
            try:
                user = bot.get_user(int(userid))
            except:
                return
            embed  = discord.Embed(
               description=message.content,
               color=0x6bbee3,
                timestamp=datetime.now()
            )
            if message.author.avatar:
                embed.set_author(name=message.author, icon_url=message.author.avatar.url)
            else:
                embed.set_author(name=message.author)
            emoji = bot.get_emoji(EMOJI_ID)
            emoji2 = bot.get_emoji(EMOJI_ID2)
            try:
                await user.send(embed=embed)
                await message.add_reaction(emoji2)
            except discord.Forbidden:
                err403 = discord.Embed(
                    description=f"I can't send messages to this user! <a:sendfailed:937311948318572584>",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=err403)
                await message.add_reaction(emoji)
            with open(f'temp/{message.channel.id}.txt', 'w+') as f:
                f.writelines(f"[{datetime.now().month}/{datetime.now().day}/{datetime.now().year}  {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}] : {message.author} -- {message.content}\n")

class close(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(style=discord.ButtonStyle.danger, label="Close", emoji="🔒",custom_id="buttons:close")
    async def close(self,interaction: discord.Interaction, button: discord.ui.Button):
        user = bot.get_user(int(interaction.channel.name))
        await interaction.channel.delete()
        transcript = discord.File(f'temp/{interaction.channel.id}.txt')
        channel = bot.get_channel(TRANSCRIPT_CHANNEL_ID)
        await channel.send(f"Closed by {interaction.user}",file=transcript)
        os.remove(f'temp/{interaction.channel.id}.txt')
        await user.send("This Conversation has been closed. If you need to contact us again, please send another message.")
import logging
bot.run("TOKEN",log_level=logging.ERROR)