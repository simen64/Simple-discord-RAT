# Simple-discord-RAT
A simple remote shell through Discord written in Python

## maintenance
I will not be maintaining this project any further, it was a proof of concept. And the developing process was not really fun at all.

## Dependencies
- Python with required libraries (see Getting started)
- Linux or Windows (This was originally made for linux, but i have tried getting functionality over to Windows so expect some bugs)

## Getting started

To get started with this RAT, you'll need to follow these steps:

1. Clone the repository to your local machine or just download the file.

3. Install the required dependencies using `pip`:  
`pip install discord.py python-dotenv requests`

4. Set up a Discord Bot:
- Go to the [Discord Developer Portal](https://discord.com/developers/applications).
- Click "New Application" and give it a name (e.g., "RAT Bot").
- Navigate to the "Bot" section
- Under the "Token" section, reset your token, then click "Copy" to copy your bot token.
- Paste the bot token into the `.env` file as `DISCORD_TOKEN`.
- Scroll down and enable the `Message Content Intent` switch
- Save your changes
- Navigate to the OAuth2 page, then URL Generator
- Select the `bot` scope
- Enable the required permissions like: `Send messages`, `Attach files`, `Read messages`, `Read message history` `Embed Links`, and others you might need.
- Copy the URL at the bottom, paste it in your browser and add the bot to a server **WITH ONLY YOU IN**

2. Create a `.env` file in the root directory of the project and add your Discord bot token as follows:  
   DISCORD_TOKEN=your-bot-token-here

5. Run the RAT either using `python Simple-Discord-RAT.py` in terminal, or running it in an IDE

## Usage

- After starting the RAT, you can use Discord messages to interact with the target machine.
- Commands should be prefixed with `!`. For example, `!help` will display the help screen.
- You can execute shell commands by sending a message with a `!` prefix (e.g., `!ls`).
- Use `!upload` to upload a file to the target machine and `!download` to download a file from the target machine.
- You can use `cd (path)` to go to a directory, this is OS independent and is the only way of switchind directories. You can also use `cd ..`

## Security
- **Keep your `.env` file secure:** Ensure that your `.env` file containing the Discord bot token is not exposed or shared publicly.
- **Make sure you are the only one in the discord server with the bot for the RAT**, anyone in the discord server has access to running commands.
- **Use responsibly:** Only use this tool on systems for which you have proper authorization. I have no responsibility in illegal actions done with this program. It is made for purely educational purposes.
- **Be aware of limitations:** This RAT doesn't grant admin privileges on the target machine and may have limitations.
