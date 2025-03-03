from src.core.game import ChronosGame

if __name__ == "__main__":
    try:
        game = ChronosGame()
        game.run()
    except Exception as e:
        print(f"Game failed to start: {e}")