import discord
from discord.ext import commands

#define intents
intents = discord.Intents.default()
intents.message = True ## For reading messages

# Create Bot instance
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree #Tree for the slash commands

# Track Lending and Borrowing
@bot.event
async def on_ready():
    await tree.sync()  # Sync commands to Discord
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="lend", description="Lend money to another user")
async def lend(interaction: discord.Interaction, member: discord.Member, amount: int ):
    # Commands to lend money

@bot.tree.command(name="borrow", description="Borrow Money")
async def borrow(interaction: discord.Interaction, discord.Interaction, member: discord.Member, amount: int):
    #Commands to borrow money

@bot.tree.command(name="findLender", description="find People who are willing to lend money")
async def findLender(interacction: discord.Interaction, discord.Interaction)
# This will use AI to find people who are willing to lend money


 #Run the bot
 bot.run("Your_BOT_token")   

## We can use Twillio like AI can use Twillio to notify you through watsapp if the server sees any possible lender or something.
