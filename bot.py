import discord
import random
from discord.ext import commands
import handychatter


async def send_message(message, user_message, bot):
    try:
        response = handychatter.get_true_response(user_message)
        await message.channel.send(response)
        await bot.process_commands(message)

    except Exception as e:
        logs = open("logs.txt", "a")
        logs.write(f"\"{user_message}\",\n")
        logs.close()
        print(e)


def run_discord_bot():
    token = 'API-token-here'
    my_guild = discord.Object(id='server-id')
    papa_id = 'user-id'

    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix="/", intents=intents)

    @bot.command()
    async def sync(ctx):
        print("sync command")
        if ctx.author.id == papa_id:
            await bot.tree.sync()
            await ctx.send('Dad! :hand_with_index_finger_and_thumb_crossed:')
        else:
            await ctx.send('Not my dada :index_pointing_at_the_viewer:')
    @bot.tree.command(name='bang', description='gestures frenzy', guild=my_guild)
    async def bang(interaction):
        responses = [':middle_finger:', ':index_pointing_at_the_viewer:', ':leftwards_hand:', ':call_me:', ':thumbsup:',
                     ':thumbsdown:', ':punch:', ':fist:', ':fingers_crossed:', ':fingers_crossed:', ':v:',
                     ':hand_with_index_finger_and_thumb_crossed:', ':love_you_gesture:', ':metal:', ':ok_hand:',
                     ':pinched_fingers:', ':pinching_hand:', ':palm_down_hand:', ':palm_up_hand:', ':point_left:',
                     ':point_right:', ':point_up_2:', ':point_down:', ':point_up:', ':raised_back_of_hand:',
                     ':hand_splayed:', ':vulcan:', ':wave:', ':call_me:', ':left_facing_fist:', ':right_facing_fist:',
                     ':rightwards_hand:', ':foot:']
        mail = ''
        for i in range(random.randint(2, 4)):
            mail += responses[random.randint(0, len(responses)-1)]
        await interaction.response.send_message(mail)

    @bot.event
    async def on_ready():
        print(f'{bot.user} gtg!')
        for server in bot.guilds:
            await bot.tree.sync(guild=discord.Object(id=server.id))

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        user_message = str(message.content)

        print(f"{user_message}")

        await send_message(message, user_message, bot)

    bot.run(token)
