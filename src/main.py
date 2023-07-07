from quart import Quart, render_template, redirect, url_for, request
from quart_discord import DiscordOAuth2Session
from dotenv import load_dotenv
from bot.objects.bot import TicketBot
import os
import discord
import asyncio

DEBUG = True

load_dotenv(".env")
app = Quart(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DISCORD_CLIENT_ID"] = int(os.getenv("DISCORD_CLIENT_ID"))   # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")   # Discord client secret.
app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback" 

discord_oauth = DiscordOAuth2Session(app)
bot = TicketBot(prefix=";", intents=discord.Intents.all())

@app.before_serving
async def before():
    loop = asyncio.get_event_loop()
    loop.set_debug(DEBUG)
    loop.create_task(bot.start(app.config["DISCORD_BOT_TOKEN"]))

@app.route('/')
async def home():
    return await render_template('index.html', authorized = await discord_oauth.authorized)

@app.route("/login")
async def login():
    return await discord_oauth.create_session()

@app.route("/callback")
async def callback():
	try:
		await discord_oauth.callback()
	except:
		pass

	return redirect(url_for("dashboard"))

@app.route("/dashboard")
async def dashboard():
    if not await discord_oauth.authorized:
        return redirect(url_for("login"))
    
    user_guilds=await discord_oauth.fetch_guilds()
    
    shared_guilds = []

    for guild in user_guilds:
        if guild.id in [i.id for i in bot.guilds]:
            shared_guilds.append(guild.id)

    shared_guilds = [bot.get_guild(i) for i in shared_guilds]

    return await render_template('dashboard.html', shared_guilds=shared_guilds)

@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
    guild = bot.get_guild(guild_id)
    if not guild:
        return redirect(f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')
    return await render_template("dashboard_server.html", guild=guild, prefix=await bot.db.get_prefix(guild.id))

@app.route("/prefix_change", methods=["POST"])
async def prefix_change():
    form = await request.form
    gid = int(form["guild_id"])
    await bot.db.update_prefix(gid, form["prefix"])
    return redirect(url_for("dashboard_server", guild_id=gid))

     
    
    








if __name__ == '__main__':
    app.run(debug=True)