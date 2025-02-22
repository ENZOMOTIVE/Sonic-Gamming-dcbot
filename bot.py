import discord
from discord.ext import commands
from pymongo import MongoClient
from twilio.rest import Client

import random

import os
from dotenv import load_dotenv

# Load Environment
load_dotenv()

 
print(f"MONGO_URI: {os.getenv('MONGO_URI')}")
print(f"TWILIO_SID: {os.getenv('TWILIO_SID')}")
print(f"TWILIO_PHONE: {os.getenv('TWILIO_PHONE')}")
print(f"BOT_TOKEN: {'Loaded' if os.getenv('BOT_TOKEN') else 'Not Loaded'}")

#define intents
intents = discord.Intents.default()
intents.messages = True #For reading messages

# Create Bot instance
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree #Tree for the slash commands


#setup the mongodb database

MONGO_URI= os.getenv('MONGO_URI') # MongoDB url from the dotenv files
#MONGO_URI = "mongodb+srv://enzo:enzo@sonic.3psdw.mongodb.net/?retryWrites=true&w=majority&appName=Sonic"

client = MongoClient(MONGO_URI)
db = client["discord_bot"] # database name
users = db["kyc_users"] # Collection

# TWILIO Credentials Setup
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")

# Initialize Twilio Client
twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

#OTP Temporary storage for Verification
otp_storage = {} # Temporary stores OTPs for comparision

#TWILIO Connection check 
if TWILIO_AUTH_TOKEN :
   print("✅ Twillio_AUTH_TOKEN connection loaded successfully.")
else: 
   print("❌ Failed to load TWILIO_AUTH_TOEN Check your .env file.")

if TWILIO_SID :
   print("✅ Twillio SID connection loaded successfully.")
else: 
   print("❌ Failed to load TWILIO_SID Check your .env file.")   

if TWILIO_PHONE :
    print("✅ TWILIO_PHONE connection loaded successfully.")
else: 
   print("❌ Failed to load TWILIO_PHONE Check your .env file.")

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

# Verify the user through SMS Verification Twilio
@bot.tree.command(name="verify", description="Verify your account via phone number")
async def verify(interaction: discord.Interaction):
    await interaction.response.send_message("Check your DMs for Verification", ephemeral=True)

    try:
        #Send DM to user
        dm_channel = await interaction.user.create_dm()
        await dm_channel.send("Please provide your phone number for verification")

        def check_phone(msg):
            return msg.author == interaction.user and isinstance(msg.channel, discord.DMChannel)

        phone_msg = await bot.wait_for("message", check=check_phone, timeout=60)
        phone_number = phone_msg.content.strip()

        #Generate OTP and store it temporarily
        otp = str(random.randint(100000,999999))
        otp_storage[interaction.user.id] = otp #Store OTP with user ID

        #Send OTP via Twilio
        twilio_client.messages.create(
            body=f"Your OTP for verification is: {otp}",
            from_=TWILIO_PHONE,
            to=phone_number
        )

        await dm_channel.send("OTP sent! Please reply with the OTP your received")

        def check_otp(msg):
            return(
                msg.author == interaction.user
                and isinstance(msg.channel, discord.DMChannel)
                and msg.content == otp_storage.get(interaction.user.id) #Compare OTP
            )

        await bot.wait_for("message", check=check_otp, timeout=120)

        # Remove OTP from memory after use
        del otp_storage[interaction.user.id]
        await dm_channel.send("Verification Successfull!")

    except Exception as e:
        print(f"Error during verification {e}")
        await dm_channel.send("Verification failed. Please try again")

# Whatsapp Send SMS
@bot.tree.command(name="watsapp", description="Send a WhatsApp message")
async def verify(interaction: discord.Interaction):

    await interaction.response.send_message("Check your WhatsApp!")

    try:
        # Send WhatsApp message
        message = twilio_client.messages.create(
            from_="whatsapp:+14155238886",
            to="whatsapp:+918658663855",
           
            body="Congratulations You just won 1000000$. Contact Aayushman to Redeem the funds!"
        )

        # Follow-up message with success confirmation
        await interaction.followup.send(f"Message sent successfully! SID: {message.sid}")

    except Exception as e:
        # Handle errors
        await interaction.followup.send(f"Failed to send message: {str(e)}")
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