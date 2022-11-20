import discord
from os import environ
from random import sample
from datetime import datetime
from pandas import read_csv
from discord.ext import commands

def write_log(logfile_path, content):
    logfile = open(logfile_path, "a")
    logfile.write(content)

intents = discord.Intents(messages=True, guilds=True, message_content=True)
SECRET_BOT_TOKEN = environ.get("SECRET_BOT_TOKEN")
thumbs_up_emoji = b'\\U0001f44d'
bot = commands.Bot(intents=intents, command_prefix='!')
lotted_lotteries = set()

@bot.command(name='loot')
async def loot(ctx, message_id: int):
    message = await ctx.fetch_message(message_id)

    if message_id not in lotted_lotteries:
        log_content = f"--------------------------------------------------\nMessage: '{message.clean_content}'\nAuthor: '{message.author}'\nMoment of script call: '{datetime.now()}'\n\nUsed coupon code(s):\n"

        coupon_codes = read_csv("coupon_codes.csv")['CODES']

        candidates = []
        for reaction in message.reactions:
            if reaction.emoji.encode('unicode-escape') == thumbs_up_emoji:
                async for user in reaction.users():
                    candidates.append(user)

        if len(candidates) < len(coupon_codes):
            winners = candidates
        else:
            winners = sample(candidates, len(coupon_codes))

        result_string = "The winners are:\n\n"
        for x, winner in enumerate(winners):
            await winner.send(f"You won! The code is '{coupon_codes[x]}'")
            log_content += f"'{coupon_codes[x]}' won by: {winner}\n"
            result_string += f"🏆 ***{winner}***\n"
        
        log_content += f"\nUnused coupon code(s):\n"
        for code in coupon_codes[len(winners):]:
            log_content += f"{code},"

        coupon_log_file = open("coupon_log.txt", "a")
        coupon_log_file.write(log_content)
        coupon_log_file.close()
        lotted_lotteries.add(message_id)

    else:
        result_string = "The lottery for this message is over already."

    
    await ctx.send(result_string)

bot.run(SECRET_BOT_TOKEN)