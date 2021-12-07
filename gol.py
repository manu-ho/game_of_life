from logic import GameLogic
from board import Board


def main():
    board = Board()
    logic = GameLogic(board, size=(32,32))
    
    logic.start_game()


if __name__ == '__main__':
    main()