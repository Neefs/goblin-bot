from quart import Quart, render_template, redirect, url_for
from quart_discord import DiscordOAuth2Session
from dotenv import load_dotenv
import os

load_dotenv(".env")
app = Quart(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DISCORD_CLIENT_ID"] = int(os.getenv("DISCORD_CLIENT_ID"))   # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")   # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback" 

discord = DiscordOAuth2Session(app)

@app.route('/')
async def home():
    return await render_template('index.html', test="helllllllll")

@app.route("/login")
async def login():
    return await discord.create_session()

@app.route("/callback")
async def callback():
	try:
		await discord.callback()
	except:
		return redirect(url_for("login"))

	user = await discord.fetch_user()
	return f"{user.name}" 






if __name__ == '__main__':
    app.run(debug=True)