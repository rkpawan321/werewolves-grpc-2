import grpc
from concurrent import futures
import time
import random
import threading
from collections import defaultdict, deque
import werewolves_pb2
import werewolves_pb2_grpc
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WerewolvesGameServicer(werewolves_pb2_grpc.WerewolvesGameServicer):
    def __init__(self):
        self.players = {}  # username: {"role": None, "alive": True}
        self.state = "waiting for players"
        self.messages = defaultdict(deque)
        self.votes = {}
        self.lock = threading.Lock()
        self.game_active = False
        self.minimum_players = 4

    def Connect(self, request, context):
        with self.lock:
            if request.username in self.players:
                return werewolves_pb2.MessageResponse(message="Username already taken.")
            self.players[request.username] = {"role": None, "alive": True}
            logging.info(f"Player connected: {request.username}")
            if len(self.players) >= self.minimum_players and not self.game_active:
                threading.Thread(target=self.start_game).start()
            return werewolves_pb2.MessageResponse(message="You are connected!")

    def start_game(self):
        self.game_active = True
        logging.info("Game starting in 60 seconds...")
        time.sleep(60)  # Wait for 60 seconds after minimum players are connected
        self.assign_roles()
        while self.check_game_status():
            self.night_phase()
            self.day_phase()
        self.end_game()

    def assign_roles(self):
        usernames = list(self.players.keys())
        werewolf_count = max(1, len(usernames) // 4)
        werewolves = random.sample(usernames, werewolf_count)
        for username in usernames:
            role = "werewolf" if username in werewolves else "villager"
            self.players[username]['role'] = role
            self.messages[username].append(f"You are a {role}.")
            logging.info(f"{username} assigned role {role}")

    def night_phase(self):
        self.broadcast("Night begins, werewolves please vote whom to eat", "werewolf")
        logging.info("Night phase: Werewolves are voting.")
        time.sleep(60)  # Give werewolves 60 seconds to vote
        self.process_votes("night")

    def day_phase(self):
        self.broadcast("Day begins, all players vote who might be the werewolf")
        logging.info("Day phase: All players are voting.")
        time.sleep(60)  # Give all players 60 seconds to vote
        self.process_votes("day")

    def process_votes(self, phase):
        vote_counts = defaultdict(int)
        for voter, vote in self.votes.items():
            if self.players[voter]["alive"]:
                vote_counts[vote] += 1

        max_votes = max(vote_counts.values(), default=0)
        candidates = [player for player, count in vote_counts.items() if count == max_votes]
        logging.info(f"Votes processed: {vote_counts}")
        
        if len(candidates) == 1:
            eliminated_player = candidates[0]
            self.players[eliminated_player]["alive"] = False
            role = self.players[eliminated_player]["role"]
            message = f"{eliminated_player} eliminated, was a {role}."
            self.broadcast(message)
            logging.info(message)
        else:
            self.broadcast("No elimination this round due to a tie or no votes.")
            logging.info("No elimination due to tie or lack of votes.")

        self.votes.clear()

    def check_game_status(self):
        werewolves_alive = any(p['alive'] and p['role'] == 'werewolf' for p in self.players.values())
        villagers_alive = any(p['alive'] and p['role'] == 'villager' for p in self.players.values())
        game_continues = werewolves_alive and villagers_alive
        logging.info(f"Checking game status: Werewolves alive: {werewolves_alive}, Villagers alive: {villagers_alive}")
        return game_continues

    def end_game(self):
        werewolves_win = not any(p['alive'] and p['role'] == 'villager' for p in self.players.values())
        message = "Werewolves win!" if werewolves_win else "Villagers win!"
        self.broadcast(message)
        logging.info(message)
        self.game_active = False

    def broadcast(self, message, role=None):
        for username, player in self.players.items():
            if role is None or player['role'] == role:
                self.messages[username].append(message)

    def ReceiveMessages(self, request, context):
        username = request.username
        while self.messages[username]:
            msg = self.messages[username].popleft()
            yield werewolves_pb2.MessageResponse(message=msg)
            time.sleep(0.1)  # Reduce CPU usage

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    werewolves_pb2_grpc.add_WerewolvesGameServicer_to_server(WerewolvesGameServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
