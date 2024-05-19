from motion.motion import Motion
from rhythm.game import Game


def main():
    motion = Motion()
    game = Game(motion)

    game.run()


if __name__ == "__main__":
    main()
