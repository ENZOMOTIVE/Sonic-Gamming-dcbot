# Crypto Lending Discord Bot

A Discord bot that facilitates peer-to-peer crypto lending on the Sonic blockchain with integrated KYC verification, AI-powered risk assessment, and automated notifications.

## Features

### Core Functionality
- **Wallet Integration**: Connect and manage your Sonic blockchain wallet
- **Lending System**: Create and manage lending offers with customizable terms
- **Borrowing System**: Request loans with collateral backing
- **Smart Contract Integration**: Interact with the Sonic blockchain for secure transactions

### Security & Verification
- **KYC Verification**: Two-factor authentication via WhatsApp or SMS using Twilio
- **AI Risk Assessment**: OpenAI-powered analysis of user lending history and behavior
- **Collateral Management**: Track and manage crypto collateral for loans

### AI-Powered Features
- **Intelligent Support**: GPT-4 powered assistance for user queries
- **Risk Analysis**: Automated assessment of borrower creditworthiness
- **Loan Recommendations**: AI-driven suggestions for optimal lending matches

### Communication
- **Multi-Channel Notifications**: Updates via Discord, WhatsApp, and SMS
- **Real-time Alerts**: Instant notifications for lending offers and loan status changes
- **Interactive Commands**: User-friendly slash commands for all operations

## Technical Stack
- **Blockchain**: Sonic Network (Testnet)
- **Database**: MongoDB
- **AI Integration**: OpenAI GPT-4
- **Communication**: Twilio API (SMS & WhatsApp)
- **Bot Framework**: Discord.py

## Environment Variables
Create a `.env` file with the following variables:

```ini
BOT_TOKEN=your_discord_bot_token
MONGO_URL=your_mongodb_connection_string
OPENAI_API_KEY=your_openai_api_key
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE=your_twilio_phone_number
TWILIO_WHATSAPP=your_twilio_whatsapp_number
```

## Installation

### Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

### Install required packages:
```bash
pip install -r requirements.txt
```

### Set up environment variables in `.env` file

### Run the bot:
```bash
python main.py
```

## Available Commands

### Wallet Management
```bash
/connect_wallet <address>  # Connect your Sonic wallet
/balance  # Check your wallet balance
/connect_testnet  # Get Sonic testnet connection details
```

### Lending & Borrowing
```bash
/lend <amount> <interest> <period>  # Create a lending offer
/borrow <amount> <period>  # Request a loan
/view_offers  # View active lending offers
/add_collateral <asset> <value>  # Add collateral for borrowing
```

### Security & Verification
```bash
/verify  # Complete KYC verification
/assess_risk_ai  # Get AI risk assessment
/recommend_loan  # Receive AI-powered loan recommendations
/support <message>  # Get AI assistance for queries
```

## Security Considerations
- All sensitive data is stored in MongoDB with appropriate security measures.
- KYC verification is required for lending and borrowing.
- AI risk assessment helps prevent fraudulent activities.
- Collateral requirements protect lenders.
- All blockchain transactions are verified on the Sonic network.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[Add your license information here]
