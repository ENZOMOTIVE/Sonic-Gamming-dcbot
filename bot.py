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

MONGO_URI= os.getenv('MONGO_URL') # MongoDB urls
client = MongoClient(MONGO_URI)
db = client["discord_bot"] # database name
users = db["kyc_users"] # Collection
lending_offers = db["lending_offers"] # Collection for lending offers
loans = db["loans"] #Collection for active loans

collateral_data = {
     "user_123": {"collateral": "ETH", "value": 1000},  
     "user_456": {"collateral": "BTC", "value": 5000},
}

# TWILIO Credentials Setup
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
TWILIO_WHATSAPP=os.getenv('TWILIO_WHATSAPP')
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



# Verification KYC view
class VerificationView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=50) # 60 second timeout
        self.user = user
        self.choice = None

    @discord.ui.button(label="WhatsApp", style=discord.ButtonStyle.green)
    async def whatsapp_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "whatsapp"
        self.stop() #Ends the interaction allowing to proceed in the main function

    @discord.ui.button(label="SMS", style=discord.ButtonStyle.blurple)
    async def sms_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "sms"
        self.stop()

# Whatsapp Notification
async def send_whatsapp_notification(phone_number, message):
    try:
        twilio_client.messages.create(
            body=message,
            from_="whatsapp:+14155238886",
            to=f"whatsapp:{phone_number}",
        )
        print("Whatsapp notification sent to {phone_number}.")
    except Exception as e:
        print(f"Failed to send Whatsapp Notification: {e}")    


# Verify the user through SMS Verification Twilio
@bot.tree.command(name="verify", description="Verify your account via phone number")
async def verify(interaction: discord.Interaction):
    await interaction.response.defer()

    await interaction.followup.send("Check your DMs for Verification", view=VerificationView(interaction.user), ephemeral=True)

    view = VerificationView(interaction.user)
   

    await interaction.followup.send("Please choose Whatsapp or SMS:", view=view, ephemeral=True)
    
    #Wait for the user to select an option
    await view.wait()

    if view.choice is None:
       
        await interaction.followup.send("Verification timed out. Please try again", ephemeral=True)

    #Send DM to user
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send("Please provide your phone number for verification")

    def check_phone(msg):
        return msg.author == interaction.user and isinstance(msg.channel, discord.DMChannel)

    try:
        phone_msg = await bot.wait_for("message", check=check_phone, timeout=60)
        phone_number = phone_msg.content.strip()

         #Generate OTP and store it temporarily
        otp = str(random.randint(100000,999999))
        otp_storage[interaction.user.id] = otp #Store OTP with user ID

        #Send OTP based on User's choice
        if view.choice == "whatsapp":
            twilio_client.messages.create(
                body=f"Your OTP for Verification is : {otp}",
                from_="whatsapp:+14155238886",
                to=f"whatsapp:{phone_number}"
            )
            await dm_channel.send("OTP send via WhatsApp")
        else:

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

@bot.tree.command(name="lend",  description="Offer to lend money")
async def lend(interaction: discord.Interaction, amount: int, interest: float, period: int):
    offer = {
        "lender_id": interaction.user.id,
        "amount": amount,
        "interest": interest,
        "period": period,
        "status": "active",
    }
    lending_offers.insert_one(offer)

    #Send Confirmation message
    await interaction.response.send_message(
         f"✅ You have offered to lend **{amount} coins** at **{interest}%** interest for **{period} days**."
    )

    #notify the user
    phone_number="+918658663855"
    message=(
        f"🚀 New Lending Offer!\n"
        f"Amount: {amount} coins\n"
        f"Interest: {interest}%\n"
        f"Period: {period} days\n"
        f"Contact the lender for more details."
    )
    await send_whatsapp_notification(phone_number, message)


# Command: Borrow
@bot.tree.command(name="borrow", description="Request to borrow money")
async def borrow(interaction: discord.Interaction, amount: int, period: int):
    user_id = str(interaction.user.id)
    collateral = collateral_data.get(user_id, {})

    if not collateral:
        await interaction.response.response.send_message(" ❌ You need to provide collateral to borrow. Use `/add_collateral` to add collateral.")
        return
    
    # Find matching lending offer
    offer = lending_offers.find_one({"amount":{"$gte": amount}, "status": "ative"})

    if not offer:
        await interaction.response.send_message("❌ No matching lending offers found. Try again later")
        return
    
    # Create a loan agreement
    loan = {
        "borrower_id": interaction.user.id,
        "lender_id": offer["lender_id"],
        "amount": amount,
        "interest": offer["interest"],
        "period": period,
        "collateral": collateral,
        "status": "active",
    }
    loans.insert_one(loan)

    # Update the lending offer status
    lending_offers.update_one({"_id": offer["_id"]}, {"$set": {"status": "fulfilled"}})

    # Notify both parties
    await interaction.response.send_message(
        f"✅ Your loan request for **{amount} coins** has been approved! You have **{period} days** to repay."
    )
    lender = await bot.fetch_user(offer["lender_id"])
    await lender.send(
        f"📩 Your lending offer has been accepted! {interaction.user.name} has borrowed **{amount} coins**."
    )



# Command: View Offers
@bot.tree.command(name="view_offers", description="View active lending offers")
async def view_offers(interaction: discord.Interaction):
    # Fetch all active lending offers
    active_offers = lending_offers.find({"status": "active"})

    if not active_offers:
        await interaction.response.send_message("❌ No active lending offers found.")
        return

    # Format the offers into a message
    offers_message = "**Active Lending Offers:**\n"
    for offer in active_offers:
        offers_message += (
            f"- **{offer['amount']} coins** at **{offer['interest']}%** interest for **{offer['period']} days**\n"
        )

    await interaction.response.send_message(offers_message)

# Command: Add Collateral (Dummy Implementation)
@bot.tree.command(name="add_collateral", description="Add collateral for borrowing")
async def add_collateral(interaction: discord.Interaction, asset: str, value: float):
    # Save collateral data (dummy logic for now)
    user_id = str(interaction.user.id)
    collateral_data[user_id] = {"collateral": asset, "value": value}

    await interaction.response.send_message(
        f"✅ Added **{asset}** worth **{value} coins** as collateral."
    )

# This will use AI to find people who are willing to lend money

# Run the bot
bot.run(os.getenv("BOT_TOKEN"))   

## We can use Twillio like AI can use Twillio to notify you through watsapp if the server sees any possible lender or something.
## For KYC we can  use a model So user types in his things 

# Note --  We can use AI to rate user's behaviour in the ecosystem
# Risk Assessment: AI evaluates a borrower’s credibility based on past loans, transaction history, and community feedback.