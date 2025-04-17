import threading
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

game_thread = None

@app.route('/start-game')
def starting_game():
    global game_thread

    # If thread is alive, don't restart
    if game_thread and game_thread.is_alive():
        return "Game is already running!", 400

    def run_game():
        from Demo import start_game
        start_game()

    game_thread = threading.Thread(target=run_game)
    game_thread.start()

    return "Game started"

if __name__ == '__main__':
    app.run(debug=True)
