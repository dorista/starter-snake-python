import os
import random
import sys
import cherrypy
from collections import namedtuple


games = {}
#   games = {Board1, Board2, ...}


# TODO: use BFS algorithm to avoid being cornered by finding path to own tail. Can also use to find closest path to nearest food
# ???: sets or lists?


class Board():
    gid = 0 # TODO: getters/setters
    turn = 1
    width = 11
    height = 11
    head = tuple()
    body = list()
    length = 1
    health = 90
    foods = list()
    sneks = {
        'sid': {
            'head': tuple(),
            'body': list(),
            'length': 1,
#            'tail': tuple()
        },
    },
    heatmap = {}


class Battlesnake(object):
    @cherrypy.expose
    def index(self):
        return 'Baby Blep licked you!'

    @cherrypy.expose
    def ping(self):
        return

    def create_board(data: dict):
        games[data['game']['id']] = {
#            'turn' = data['turn'],
            'width' = data['board']['width'],
            'height' = data['board']['height']
#            'head' = tuple((data['you']['body'][0]['x'], data['you']['body'][0]['y'])),
#            'body' = list(tuple((body['x'], body['y'])) for body in data['you']['body']),
#            'length' = 1,
#            'health' = data['you']['health'],
#            'foods' = list(tuple((food['x'], food['y'])) for food in data['board']['food']),
        }
        print(games) # DEBUG

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        create_board(cherrypy.request.json)
        return {
            'color': '#FFFFFF',
            'headType': 'bwc-rudolph',
            'tailType': 'bwc-ice-skate'
        }

    def update_board(data: dict, gid: str):
        games[gid]['turn'] = data['turn']
        games[gid]['health'] = data['you']['health']
        games[gid]['body'] = list(tuple((body['x'], body['y'])) for body in data['you']['body'])
        games[gid]['head'] = games[gid]['body'][0]
        games[gid]['length'] = len(games[gid]['body'])
        games[gid]['foods'] = list(tuple((food['x'], food['y'])) for food in data['board']['food'])
        games[gid]['sneks'] = {
            snek['id']: {
                'body': list(tuple((body['x'], body['y'])) for body in snek['body']),
                'head': tuple((snek['body'][0]['x'], snek['body'][0]['y'])),
                'length': len(snek['body'])
#                'tail': tuple()
            } for snek in data['board']['snakes']
        }
        games[gid]['heatmap'] = {}

    def in_bounds(pos: tuple, gid: str) -> bool:
        return 0 <= pos[0] < games[gid][width] and 0 <= pos[1] < games[gid][height]

    def is_valid(move: tuple, gid: str) -> bool:
        if move not in games[gid]['body']:
            for snek in games[gid]['sneks'].values():
                if move in snek['body']:
                    break
            else:
                return true
        return false

    def check_ahead(move: tuple, gid: str) -> int:
        pass #TODO: check all three directions, not including head pos

    def distance(pos1: tuple, pos2: tuple) -> int:
        return abs(pos2[0]-pos1[0])+abs(pos2[1]-pos[1])

    def check_moves(gid) -> dict:
        moves = {}
        curr_pos = games[gid]['head']

        # check up
        up = tuple((curr_pos[0], curr_pos[1] - 1))
        if in_bounds(up, gid) and is_valid(up, gid):
#            moves.append('up')
            moves['up'] = check_ahead(up, gid)

        # check down
        down = tuple((curr_pos[0], curr_pos[1] + 1))
        if in_bounds(down, gid) and is_valid(down, gid):
#            moves.append('down')
            moves['down'] = check_ahead(down, gid)
        
        # check left
        left = tuple((curr_pos[0] - 1, curr_pos[1]))
        if in_bounds(left, gid) and is_valid(left, gid):
#            moves.append('left')
            moves['left'] = check_ahead(left, gid)

        # check right
        right = tuple((curr_pos[0] + 1, curr_pos[1]))
        if in_bounds(right, gid) and is_valid(right, gid):
#            moves.append('right')
            moves['right'] = check_ahead(right, gid)

        # TODO: chase down food and eat it!
            # note for adjacent to enemy snake head: if opponent is same length or longer, include move but make it last resort if all other moves not possible
                # if two or more possible moves are both enemy snake heads and last resort or attacking, choose randomly
	# TODO: revamp score/heatmap to eval next spot's danger by possible moves from that new spot:
	    # 0: all three future moves from new spot are available
	    # 1: two of three future moves
	    # 2: one of three future moves
	    # 3: none of future moves available
	    # 7: avoid completely, snake's body
	    # +1 if new spot is adjacent to enemy snake's head
	    # if no moves possible: target snake tail or head if no tail or if other snake is weaker

        return moves

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        data = cherrypy.request.json
        gid = data['game']['id']
        update_board(data, gid)

        print(f"head at {games[gid]['head'][0]}:{games[gid]['head'][1]}")
        possible_moves = check_moves(gid)
        print(f"Possible moves: {possible_moves}")

        move = random.choice(possible_moves)
        print(f"Move chosen: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        del games[cherrypy.request.json["game"]["id"]]
        print('GG')
        return


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({
        'server.socket_port': int(os.environ.get('PORT', '8008')),
        'server.socket_host': '0.0.0.0'
    })
    print('Baby Blep is now slithering')
    cherrypy.quickstart(server)

