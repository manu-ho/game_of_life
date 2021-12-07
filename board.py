import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import logic

UI_BOARD_SIZE = (8, 6)
UI_BOARD_OFFSET = 0.25
UI_BOARD_CELL_COLORS = [(0,0,0,0.4), (0,0.9,1,0.7)]

'''
UI front-end implementation
'''
class Board:
    def __init__(self):
        # Create figure and axes
        self.fig, self.ax = plt.subplots(figsize=UI_BOARD_SIZE)
        # Board background color
        self.ax.set_facecolor((0,0,0,0.15))
        # Hiding axes
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        # Scale axes
        self.ax.set_xlim([0,1])
        self.ax.set_ylim([0,1])
        self.ax.set_aspect('equal', adjustable='box')

        # Board cells
        self.patches = []

        # Last board state - needed for differential update of board
        self.last_state = None

        # Connect to UI for mouse click event
        connection_id = self.fig.canvas.mpl_connect('button_press_event', self.on_click_cell)
        self.on_click_event_handler = None

        # Generation label
        self.lbl_generation = None

        # Next generation button
        axnext = plt.axes([0.45, 0.9, 0.2, 0.075])
        self.bnext = plt.Button(axnext, 'Next', color=(0, 1, 0.7, 0.7), hovercolor=(0, 1, 0.7, 1))
        self.bnext.label.set_fontsize(16)
        self.bnext.on_clicked(self.on_click_btn_next)

        # Reset button
        axreset = plt.axes([0.25, 0.9, 0.1, 0.075])
        self.breset = plt.Button(axreset, 'Reset', color=(1, 0.2, 0, 0.7), hovercolor=(1, 0.2, 0, 1))
        self.breset.label.set_fontsize(16)
        self.breset.on_clicked(self.on_click_btn_reset)

    def on_click_btn_next(self, event):
        if self.on_click_event_handler is None:
            raise ValueError
        self.on_click_event_handler(logic.EVENT_NEXT_CLICK)

    def on_click_btn_reset(self, event):
        if self.on_click_event_handler is None:
            raise ValueError
        self.on_click_event_handler(logic.EVENT_RESET_CLICK)

    def on_click_cell(self, event):
        if not event.inaxes == self.ax:
            return
        # Left mouse button click to change cell state
        if event.button == 1:
            x = int(np.floor((event.xdata - self.cell_margin[0]) / self.cell_width))
            y = int(np.floor((event.ydata - self.cell_margin[1]) / self.cell_height))
            if self.on_click_event_handler is None:
                raise ValueError
            self.on_click_event_handler(logic.EVENT_CELL_CLICK, data=(x, y))

    def set_click_event_handler(self, handler):
        self.on_click_event_handler = handler

    def redraw_board(self, state):
        # Update cell size and margin
        self.cell_width = 1. / state.shape[0]
        self.cell_height = 1. / state.shape[1]
        self.cell_margin = (self.cell_width * 0.05, self.cell_height * 0.05)

        # Remove all previously drawn patches
        [p.remove() for p in reversed(self.ax.patches)]

        # Add new patches
        for x in range(state.shape[0]):
            for y in range(state.shape[1]):
                rect = patches.Rectangle((x*self.cell_height + self.cell_margin[1], y*self.cell_width + self.cell_margin[0]),
                            self.cell_width*0.9, self.cell_height*0.9,
                            fill=True, facecolor=UI_BOARD_CELL_COLORS[state[x, y]])
                self.ax.add_patch(rect)
        self.patches = self.ax.patches
        
        # Update last state
        self.last_state = state.copy()

        plt.show()
    
    def redraw_ui_elements(self, generation=None):
        # UI elements, status, buttons
        if not generation is None:
            if not self.lbl_generation is None:
                self.lbl_generation.remove()

            self.lbl_generation = self.ax.annotate('%d' % generation,
                color='k', weight='bold', fontsize=16, ha='center', va='center',
                xy=(0.95, 1.08), xycoords=self.ax.transAxes, annotation_clip=False)
    
    def redraw(self, state, generation=None):
        # Redraw game board
        self.redraw_board(state)

        # UI elements, status, buttons
        if not generation is None:
            self.redraw_ui_elements(generation)
    
    def update(self, state, generation=None):
        # Redraw entire board if state dimension has changed
        if self.last_state is None or state.size != self.last_state.size:
            self.redraw(state, generation)
        
        # Update only those cells, that have changed since last state
        diff = np.subtract(state, self.last_state)
        print('diff = {}'.format(diff))
        changed_idx = list(zip(*diff.nonzero()))
        print('Cells at {} changed.'.format(changed_idx))
        for xy in changed_idx:
            self.patches[xy[0] * state.shape[0] + xy[1]].set_facecolor(UI_BOARD_CELL_COLORS[state[xy[0], xy[1]]])

        # Update last state
        self.last_state = state.copy()
        
        # UI elements, status, buttons
        if not generation is None:
            self.redraw_ui_elements(generation)

        plt.show()

