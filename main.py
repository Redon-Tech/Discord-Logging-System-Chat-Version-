import discord # Import Discord
from discord.ext import commands # Import commands
import os # Import os
from quart import Quart, request # Import Quart
from time import time # Import time for ping command
from datetime import datetime

app = Quart(__name__) # Create app
bot = commands.Bot(command_prefix=".") # Create bot

@app.route("/") # Route index
async def index():
	return {
		"message" : "Ok"
	}
			

@bot.event # Make on_ready
async def on_ready():
  print("Bot ready")

class ExampleCommand(commands.Cog): # Cog for commands (I got this from https://replit.com/talk/learn/Discordpy-Discord-Bot-Web-Dashboard-Tutorial/131455)
	@commands.command() # Create command
	async def ping(self, ctx):
		start = time()
		message = await ctx.send(f"Pong :ping_pong:! **{bot.latency*100:,.0f} ms**")
		end = time()

		await message.edit(content=f"Pong :ping_pong:! **Latency: {bot.latency*100:,.0f} ms** | **Response Time {(end-start)*1000:,.0f} ms**")
	
	@commands.command()
	async def test(self, ctx):
		channel = discord.utils.get(bot.get_all_channels(), id=703389457453416458)
		await channel.send("Yes")

@app.route("/v1/send", methods=["POST"]) # Still WIP
async def send_message():
	try:
		messages = (await request.get_json())["message"]
	except:
		print("1")
		return {
		"errors": [
				{
					"code": 1,
					"message": "Couldn't get messages."
				}
			]
		}
	
	print(messages)

	try:
		channel = discord.utils.get(bot.get_all_channels(), id=703389457453416458)
		embed = discord.Embed(title="Messages Logged", colour=discord.Colour(0x159121), description=f"Logged {len(messages)} messages.", timestamp=datetime.utcnow())

		embed.set_footer(text="Made By: Redon Tech")
		for x in messages:
			data = x.split(":")
			embed.add_field(name=data[0], value=data[1], inline=False)

		await channel.send(embed=embed)
		return {
			"message" : "Ok"
		}
	except:
		print("2")
		return {
		"errors": [
				{
					"code": 2,
					"message": "Couldn't send message."
				}
			]
		}

def run(): # Run the Quart and bot instance
  bot.loop.create_task(app.run_task('0.0.0.0'))
  bot.add_cog(ExampleCommand(bot))
  bot.run(os.environ.get("token"))

if __name__ == "__main__":
  run() # Run everything