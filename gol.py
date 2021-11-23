from logging import log
from logic import GameLogic
from board import Board


def main():
    board = Board()
    logic = GameLogic(board, size=(16,16))
    
    logic.start_game()


if __name__ == '__main__':
    main()