import discord # Import Discord
from discord.ext import commands # Import commands
import os # Import os
from quart import Quart, request # Import Quart
from time import time # Import time for ping command

app = Quart(__name__) # Create app
bot = commands.Bot(command_prefix=".") # Create bot

@app.route("/") # Route index
async def index():
	return {
		"message" : "Ok"
	}

@app.route("/v1/send/<channel_id>", methods=["POST"])
async def send_message(channel_id):
	try:
		messages = (await request.get_json())["messages"]
	except:
		return {
		"errors": [
				{
					"code": 1,
					"message": "Couldn't get messages."
				}
			]
		}

	try:
		await channel_id.send(f"Yes {messages}")
	except:
		return {
		"errors": [
				{
					"code": 2,
					"message": "Couldn't send message."
				}
			]
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


def run(): # Run the Quart and bot instance
  bot.loop.create_task(app.run_task('0.0.0.0'))
  bot.add_cog(ExampleCommand(bot))
  bot.run(os.environ.get("token"))

if __name__ == "__main__":
  run() # Run everything