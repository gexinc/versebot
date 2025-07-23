# packages
import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

#loads .env
load_dotenv()

# defines intents
intents = discord.Intents.default()
intents.message_content = True 

config = {
    "token": getenv("TOKEN"),
    "status": getenv("STATUS", "Bible Quotes"),
}

bot = commands.Bot(command_prefix="/", intents=intents)

#console stuff
@bot.event
async def on_ready():
    print(f"logged {bot.user} ({bot.user.id})")
    print(f"sharding: {bot.shard_count}")

    
    await bot.tree.sync()

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=config["status"]
        ),
    )

#hewwo parts
@bot.event
async def on_guild_join(guild):
    await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.timedelta(seconds=5))
    try:
        channel = guild.system_channel
        if channel:
            embed = discord.Embed(
                title="Hewwo :3",
                description="Im a cute robo-twink and I love God, if you want your inspiration for todayo pwease use /find",
            )
            embed.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/4/4e/Bible_opened.jpg"
            )
            embed.set_footer(
                text="God Bless",
                icon_url="https://upload.wikimedia.org/wikipedia/commons/9/9d/Christian_cross.svg",
            )
            await channel.send(embed=embed)
    except Exception as error:
        print(f"Unable to send welcome message: {error}")

#error handling
@bot.event
async def on_application_command_error(interaction, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await interaction.response.send_message(
            "Are you retarded, like OG?", ephemeral=True
        )
    elif isinstance(error, commands.CommandNotFound):
        await interaction.response.send_message(
            "You doing something that only devil would!", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"An error occurred: {error}", ephemeral=True
        )

# help
@bot.tree.command(
    name="help",
    description="God Will Always Listen"
)
async def help_command(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title="Help", description="Gyatt Bless")
    embed.add_field(name="Prefix", value="``/``", inline=False)
    embed.add_field(
        name="/findpic",
        value="Daily verses!!!\nExample: ``/findpic``",
        inline=False,
    )
    embed.set_thumbnail(
        url="https://upload.wikimedia.org/wikipedia/commons/4/4e/Bible_opened.jpg"
    )
    embed.set_footer(
        text="Hawk Tuah",
        icon_url="https://upload.wikimedia.org/wikipedia/commons/9/9d/Christian_cross.svg",
    )
    await interaction.followup.send(embed=embed)

# findpic
@bot.tree.command(
    name="findpic",
    description="Get a Bible verse image."
)
async def findpic(interaction: discord.Interaction):
    # first msg
    await interaction.response.send_message("hehe, amen and stuff")

    # img irl fetch
    def fetch_verse_image():
        url = "https://dailyverses.net/random-bible-verse-picture"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tag = soup.find('img', class_='bibleVerseImage')
            if img_tag and 'src' in img_tag.attrs:
                relative_src = img_tag['src']
                full_url = "https://dailyverses.net" + relative_src
                return full_url
        return None

    # placing irl
    img_url = fetch_verse_image()

    # post img or post error
    if img_url:
        await interaction.followup.send(content=img_url)
    else:
        await interaction.followup.send("sowwy, just can't :( )")

#running
bot.run(config["token"])