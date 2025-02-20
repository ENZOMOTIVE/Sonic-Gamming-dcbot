import discord
from discord.ext import commands
from pymongo import MongoClient

import os
from dotenv import load_dotenv

# Load Environment
load_dotenv()

#define intents
intents = discord.Intents.default()
intents.messages = True #For reading messages

# Create Bot instance
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree #Tree for the slash commands


#setup the mongodb database

MONGO_URI= os.getenv('MONGO_URI') # MongoDB url from the dotenv files
client = MongoClient(MONGO_URI)
db = client["discord_bot"] # database name
users = db["kyc_users"] # Collection


# MongoDB Connection check
if MONGO_URI:
   print("✅ MongoDB connection string loaded successfully.")
else: 
   print("❌ Failed to load MongoDB connection string. Check your .env file.")

#DISCORD BOT CONNECTION CHECK

# Event: Bot Ready
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync slash commands with Discord
    print(f"✅ Logged in as {bot.user.name} and bot is now online!")   


# Track Lending and Borrowing
@bot.event
async def on_ready():
    await tree.sync()  # Sync commands to Discord
    print(f"Logged in as {bot.user}")

# Slash Command: Lend Money
@bot.tree.command(name="lend", description="Lend money to another user")
async def lend(interaction: discord.Interaction, member: discord.Member, amount: int):
    await interaction.response.send_message(f"💰 You are lending {amount} coins to {member.mention}.")
    print(f"Lending {amount} to {member.name}")

# Slash Command: Borrow Money
@bot.tree.command(name="borrow", description="Borrow Money")
async def borrow(interaction: discord.Interaction, member: discord.Member, amount: int):
    await interaction.response.send_message(f"🤑 You are borrowing {amount} coins from {member.mention}.")
    print(f"Borrowing {amount} from {member.name}")

# Slash Command: Find Lender (AI Placeholder)
@bot.tree.command(name="findlender", description="Find people willing to lend money")
async def findLender(interaction: discord.Interaction):
    await interaction.response.send_message("🤖 AI is searching for potential lenders...")
    print("AI is searching for lenders")
# This will use AI to find people who are willing to lend money

# Run the bot
bot.run(os.getenv("BOT_TOKEN"))   

## We can use Twillio like AI can use Twillio to notify you through watsapp if the server sees any possible lender or something.
## For KYC we can  use a model So user types in his things 