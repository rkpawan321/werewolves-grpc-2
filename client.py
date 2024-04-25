import grpc
import werewolves_pb2
import werewolves_pb2_grpc
import threading
import time

def listen_for_messages(stub, username):
    try:
        print("Listening for messages...")
        my_role = None
        for message in stub.ReceiveMessages(werewolves_pb2.PlayerInfo(username=username)):
            print("Server message:", message.message)

            # Assign role based on the initial message
            if 'You are a' in message.message:
                my_role = 'werewolf' if 'werewolf' in message.message else 'villager'
                print(f"Your role is: {my_role}")

            # Process voting messages
            if 'please vote' in message.message.lower() and my_role:
                if 'werewolves' in message.message.lower() and my_role == 'werewolf':
                    votee = input("You are a werewolf. Enter the username to eat: ")
                    stub.Vote(werewolves_pb2.VoteRequest(voter=username, votee=votee))
                elif 'cast your vote' in message.message.lower():
                    votee = input("Enter the username to eliminate: ")
                    stub.Vote(werewolves_pb2.VoteRequest(voter=username, votee=votee))

    except grpc.RpcError as e:
        print(f"An RPC error occurred: {e.details()}")
        print('Status code:', e.code())
    except Exception as e:
        print(f"An error occurred: {e}")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = werewolves_pb2_grpc.WerewolvesGameStub(channel)
        username = input("Enter your username to connect: ")
        response = stub.Connect(werewolves_pb2.PlayerInfo(username=username))
        print("Server response:", response.message)

        # Create a thread to listen for messages continuously
        listener_thread = threading.Thread(target=listen_for_messages, args=(stub, username))
        listener_thread.daemon = True  # Set as a daemon so it doesn't prevent the program from exiting
        listener_thread.start()

        # Keep the main thread alive to listen for keyboard interrupts
        try:
            while True:
                time.sleep(1)  # Sleep to reduce CPU usage
        except KeyboardInterrupt:
            print("Exiting client...")

def receive_messages(username):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = werewolves_pb2_grpc.WerewolvesGameStub(channel)
        try:
            for message in stub.ReceiveMessages(werewolves_pb2.MessageRequest(username=username)):
                print(f"Received: {message.message}")
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")


if __name__ == '__main__':
    run()
