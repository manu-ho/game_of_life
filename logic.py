import numpy as np
import scipy.signal as sig

EVENT_CELL_CLICK    = 101
EVENT_NEXT_CLICK    = 102
EVENT_RESET_CLICK   = 103

'''
Game logic implementation - next state computation
'''
class GameLogic:
    def __init__(self, board, size=(16,16)):
        if board is None:
            raise ValueError
        self.board = board

        self.size = size
        self.state = None
        self.cnt_generation = 0

        self.reset_game()

        board.set_click_event_handler(self.on_click_handler)

    def reset_game(self):
        self.state = self.get_start_state(self.size)
        self.cnt_generation = 0

    def start_game(self):
        self.reset_game()
        self.refresh_board()

    @staticmethod
    def get_start_state(board_size):
        s = np.zeros(board_size, dtype=np.int8)
        s[5:8, 5] = 1
        return s

    def refresh_board(self):
        # self.board.draw(self.state, generation=self.cnt_generation)
        self.board.update(self.state, generation=self.cnt_generation)

    def on_click_handler(self, event, data=None):
        if event == EVENT_CELL_CLICK:
            self.state[data[0], data[1]] = (self.state[data[0], data[1]] + 1) % 2
            self.refresh_board()
        elif event == EVENT_NEXT_CLICK:
            self.next_generation()
            self.refresh_board()
        elif event == EVENT_RESET_CLICK:
            self.reset_game()
            self.refresh_board()
        else:
            print(event)
            raise NotImplementedError

    def next_generation(self):
        # First naive approach: use convolution-based approach.. let's see if this makes sense..
        kernel = np.ones((3,3), dtype=np.int8)
        kernel[1,1] = 0
        conv = sig.convolve2d(self.state, kernel, mode='same', boundary='fill', fillvalue=0)

        '''
        1 1 1
        1 0 1
        1 1 1
        '''

        # Compute next generation - implementation based on rules from wikipedia rules
        # https://de.wikipedia.org/wiki/Conways_Spiel_des_Lebens
        new_state = self.state.copy()
        for x in range(self.state.shape[0]):
            for y in range(self.state.shape[1]):
                if self.state[x, y] == 0:
                    if conv[x, y] == 3:
                        new_state[x, y] = 1  # rule 1 (wikipedia)
                else:
                    if conv[x, y] < 2:  # rule 2 (wikipedia)
                        new_state[x, y] = 0
                    elif conv[x, y] == 2 or conv[x, y] == 3:
                        new_state[x, y] = 1  # rule 3 (wikipedia)
                    elif conv[x, y] > 3:
                        new_state[x, y] = 0  # rule 4 (wikipedia)

        self.cnt_generation += 1
        self.state = new_state
