import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    def index(self):
        # If you open your snake URL in a browser you should see this message.
        return "Baby Blep licked you!"

    @cherrypy.expose
    def ping(self):
        # The Battlesnake engine calls this function to make sure your snake is working.
        return

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json
        #gid = data["game"]["id"]
        #health = data["you"]["health"]
        #boardy = data["board"]["height"]
        #boardx = data["board"]["width"]
        return {
            "color": "#FFFFFF",
            "headType": "bwc-rudolph",
            "tailType": "bwc-ice-skate"
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        data = cherrypy.request.json
        #gid = data["game"]["id"]
        #health = data["you"]["health"]
        #boardy = data["board"]["height"]
        #boardx = data["board"]["width"]

        # TODO: Compute a random direction to move in
        possible_moves = ["up", "down", "left", "right"]
        move = random.choice(possible_moves)

        print(f"MOVE: {move}") # DEBUG
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        print(data) # DEBUG
        print("GG")
        return


if __name__ == "__main__":
    server = Battlesnake()
    # cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update({
        "server.socket_port": int(os.environ.get("PORT", "8008")),
        "server.socket_host": "0.0.0.0"
    })
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)

