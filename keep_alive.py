from flask import Flask
from threading import Thread


# Create a webserver so that repl wont kill after closing tab
# Only work for repl.it server afaik
# Make an uptime robot to ping to your server to keep the server active
# Full guide here: https://repl.it/talk/learn/Hosting-discordpy-bots-with-replit/11008
app = Flask('')

@app.route('/')
def main():
	return("I'm alive!!!")


def run():
	app.run(host='0.0.0.0', port='8080')


def keep_alive():
	server = Thread(target=run)
	server.start()
