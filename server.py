import os
import random
import sys
import cherrypy
from collections import namedtuple


games = {}


class Battlesnake(object):
    @cherrypy.expose
    def index(self):
        return 'Baby Blep licked you!'

    @cherrypy.expose
    def ping(self):
        return

    def create_board(data: dict):
        games[data['game']['id']] = {
            'turn' = data['turn'],
            'width' = data['board']['width'],
            'height' = data['board']['height'],
            'head' = tuple((data['you']['body'][0]['x'], data['you']['body'][0]['y'])),
            'body' = set(tuple((body['x'], body['y'])) for body in data['you']['body']),
            'health' = data['you']['health'],
            'foods' = set(tuple((food['x'], food['y'])) for food in data['board']['food']),
            'sneks' = set(tuple((snek['x'], snek['y'])) for enemy in data['board']['snakes'] for snek in enemy['body']) 
            # TODO: 'snek_heads' (as dict) minus our head + also track length of other sneks
            # TODO: change sets to lists?
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
        games[gid]['head'] = tuple((data['you']['body'][0]['x'], data['you']['body'][0]['y'])) 
        games[gid]['body'] = set(tuple((body['x'], body['y'])) for body in data['you']['body'])
        games[gid]['foods'] = set(tuple((food['x'], food['y'])) for food in data['board']['food'])
        games[gid]['sneks'] = set(tuple((snek['x'], snek['y'])) for enemy in data['board']['snakes'] for snek in enemy['body'])
        # TODO: change sets to lists?

    def in_bounds(pos: tuple, gid: str):
        return 0 <= pos[0] < games[gid][width] and 0 <= pos[1] < games[gid][height]

    def check_moves(gid) -> list:
        moves = []
        curr_pos = games[gid]['head']

        # check up
        up = tuple((curr_pos[0], curr_pos[1] - 1))
        if in_bounds(up, gid) and up not in games[gid]['sneks'] and up not in games[gid]['body']:
            moves.append('up')

        # check down
        down = tuple((curr_pos[0], curr_pos[1] + 1))
        if in_bounds(down, gid) and down not in games[gid]['sneks'] and down not in games[gid]['body']:
            moves.append('down')
        
        # check left
        left = tuple((curr_pos[0] - 1, curr_pos[1]))
        if in_bounds(left, gid) and left not in games[gid]['sneks'] and left not in games[gid]['body']:
            moves.append('left')

        # check right
        right = tuple((curr_pos[0] + 1, curr_pos[1]))
        if in_bounds(right, gid) and right not in games[gid]['sneks'] and right not in games[gid]['body']:
            moves.append('right')

        # TODO: chase down food and eat it!
        # TODO: 5 levels of heatmap, higher levels take precedence, dict of coords, replaces random move choice, 1-4 can be in possible moves:
            # 0: safe move, nobody in position or nearby
            # 1: edge of the map, slight caution
            # 2: any snake tail, potentially moved next turn unless they eat something
            # 3: the adjacent position to any snake's body
            # 4: spot adjacent to an opponent's head, identify opponent and if shorter, eat it!
            # 5: BIG NONO, any snake's body or head, DON'T EVER MOVE HERE, take risk and go to pos with heat 4
            # dict = {0: {(1, 1), ...}, 1: ..., 2: ..., 3: ..., 4: ..., 5: ...}
            # note for heat 4: if opponent is same length or longer, include move but make it last resort if all other moves not possible
                # if two or more possible moves are heat 4 and last resort or attacking, choose randomly

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

