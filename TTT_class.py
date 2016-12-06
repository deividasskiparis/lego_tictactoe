import random
import tkinter as tk
import cv2
import numpy as np


def nothing(x):
    pass

class TTT(tk.Frame):

    def __init__(self, master=None):

        # CV variables
        self.grids = []
        self.grid_height = 0
        self.grid_delta = 0
        self.thresh = 0
        self.lower_T = 0
        self.higher_T = 0
        self.cap = cv2.VideoCapture(1)

        print(self.cap.isOpened())

        self.next_player_move = tk.IntVar()

        self.root = master
        self.root.minsize(width=666, height=666)
        super().__init__(master)
        # self.pack()
        self.create_widgets()
        self.starts = ''
        self.turn = ''
        self.theBoard = ['_'] * 9
        self.stop_game()
        self.lbl_board_print()

    def reset(self):

        self.theBoard = ['_'] * 9
        self.playerLetter, self.computerLetter = 'X', 'O'
        self.turn = self.whoGoesFirst()
        self.starts = self.turn
        print('The ' + self.turn + ' will go first.')
        self.gameIsPlaying = True
        self.lbl_board_print()
        self.next_player_move.set(0)
        self.next_move()


    def stop_game(self):
        self.gameIsPlaying = False

    def create_widgets(self):


        tk.Label(self.master, text="Your move").grid(row=0, column=1, sticky=tk.W)

        e1 = tk.Entry(self.master,textvariable=self.next_player_move, width=2)


        e1.grid(row=0, column=2)

        self.next_player_move.set(0)

        self.new_game = tk.Button(self.root, text="New Game", fg="red" ,command=self.reset).grid(row=0,column=0)
        self.quit = tk.Button(self.root, text="Next Move" ,command=self.next_move).grid(row=0,column=3)
        self.calib = tk.Button(self.root, text="Calibrate" ,command=self.calibrate).grid(row=1,column=0)

        self.lbl_board_var1 = tk.StringVar()
        self.lbl_board_var2 = tk.StringVar()
        self.lbl_board_var3 = tk.StringVar()
        self.lbl_board_var4 = tk.StringVar()
        self.lbl_board_var5 = tk.StringVar()
        self.lbl_board_var6 = tk.StringVar()
        self.lbl_board_var7 = tk.StringVar()
        self.lbl_board_var8 = tk.StringVar()
        self.lbl_board_var9 = tk.StringVar()

        lbl_board_grid_row = 3
        lbl_board_grid_col = 4
        lbl_font_size = 20
        self.lbl_board1 = tk.Label(self.root, textvariable=self.lbl_board_var1, relief=tk.RAISED, font=("Helvetica", lbl_font_size)).grid(row=lbl_board_grid_row+2, column=lbl_board_grid_col,sticky=tk.W)
        self.lbl_board2 = tk.Label(self.root, textvariable=self.lbl_board_var2, relief=tk.RAISED, font=("Helvetica", lbl_font_size)).grid(row=lbl_board_grid_row+2, column=lbl_board_grid_col+1,sticky=tk.W)
        self.lbl_board3 = tk.Label(self.root, textvariable=self.lbl_board_var3, relief=tk.RAISED, font=("Helvetica", lbl_font_size)).grid(row=lbl_board_grid_row+2, column=lbl_board_grid_col+2,sticky=tk.W)
        self.lbl_board4 = tk.Label(self.root, textvariable=self.lbl_board_var4, relief=tk.RAISED, font=("Helvetica", lbl_font_size)).grid(row=lbl_board_grid_row+1, column=lbl_board_grid_col,sticky=tk.W)
        self.lbl_board5 = tk.Label(self.root, textvariable=self.lbl_board_var5, relief=tk.RAISED, font=("Helvetica", lbl_font_size)).grid(row=lbl_board_grid_row+1, column=lbl_board_grid_col+1,sticky=tk.W)
        self.lbl_board6 = tk.Label(self.root, textvariable=self.lbl_board_var6, relief=tk.RAISED, font=("Helvetica", lbl_font_size)).grid(row=lbl_board_grid_row+1, column=lbl_board_grid_col+2,sticky=tk.W)
        self.lbl_board7 = tk.Label(self.root, textvariable=self.lbl_board_var7, relief=tk.RAISED, font=("Helvetica", lbl_font_size)).grid(row=lbl_board_grid_row, column=lbl_board_grid_col,sticky=tk.W)
        self.lbl_board8 = tk.Label(self.root, textvariable=self.lbl_board_var8, relief=tk.RAISED, font=("Helvetica", lbl_font_size)).grid(row=lbl_board_grid_row, column=lbl_board_grid_col+1,sticky=tk.W)
        self.lbl_board9 = tk.Label(self.root, textvariable=self.lbl_board_var9, relief=tk.RAISED, font=("Helvetica", lbl_font_size)).grid(row=lbl_board_grid_row, column=lbl_board_grid_col+2,sticky=tk.W)

    def lbl_board_print(self):

        self.lbl_board_var1.set(self.theBoard[0])
        self.lbl_board_var2.set(self.theBoard[1])
        self.lbl_board_var3.set(self.theBoard[2])
        self.lbl_board_var4.set(self.theBoard[3])
        self.lbl_board_var5.set(self.theBoard[4])
        self.lbl_board_var6.set(self.theBoard[5])
        self.lbl_board_var7.set(self.theBoard[6])
        self.lbl_board_var8.set(self.theBoard[7])
        self.lbl_board_var9.set(self.theBoard[8])

        self.root.update_idletasks()

    def drawBoard(self, board):

        # This function prints out the board that it was passed.

        # "board" is a list of 10 strings representing the board (ignore index 0)

        print('   |   |')

        print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])

        print('   |   |')

        print('-----------')

        print('   |   |')

        print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])

        print('   |   |')

        print('-----------')

        print('   |   |')

        print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])

        print('   |   |')

    def inputPlayerLetter(self):
        # Lets the player type which letter they want to be.
        # Returns a list with the player's letter as the first item, and the computer's letter as the second.

        letter = ''

        while not (letter == 'X' or letter == 'O'):
            print('Do you want to be X or O?')

            letter = input().upper()

        # The first element in the list is the player's letter, the second is the computer's letter.

        if letter == 'X':

            return ['X', 'O']

        else:

            return ['O', 'X']

    def whoGoesFirst(self):

        # Randomly choose the player who goes first.

        if random.randint(0, 1) == 0:

            return 'computer'

        else:

            return 'player'

    def playAgain(self):

        # This function returns True if the player wants to play again, otherwise it returns False.

        print('Do you want to play again? (yes or no)')

        return input().lower().startswith('y')

    def makeMove(self, board, letter, move):

        board[move] = letter

    def isWinner(self, bo, le):

        # Given a board and a player's letter, this function returns True if that player has won.

        # We use bo instead of board and le instead of letter so we don't have to type as much.

        return ((bo[6] == le and bo[7] == le and bo[8] == le) or  # across the top

                (bo[3] == le and bo[4] == le and bo[5] == le) or  # across the middle

                (bo[0] == le and bo[1] == le and bo[2] == le) or  # across the bottom

                (bo[6] == le and bo[3] == le and bo[0] == le) or  # down the left side

                (bo[7] == le and bo[4] == le and bo[1] == le) or  # down the middle

                (bo[8] == le and bo[5] == le and bo[2] == le) or  # down the right side

                (bo[6] == le and bo[4] == le and bo[2] == le) or  # diagonal

                (bo[8] == le and bo[4] == le and bo[0] == le))  # diagonal

    def getBoardCopy(self, board):

        # Make a duplicate of the board list and return it the duplicate.

        dupeBoard = []

        for i in board:
            dupeBoard.append(i)

        return dupeBoard

    def isSpaceFree(self, board, move):

        # Return true if the passed move is free on the passed board.

        return board[move] == '_'

    def getPlayerMove(self, board):

        # Let the player type in their move.

        move = ' '

        while move not in '1 2 3 4 5 6 7 8 9'.split() or not self.isSpaceFree(board, int(move)):
            print('What is your next move? (1-9)')

            move = input()

        return int(move)

    def chooseRandomMoveFromList(self, board, movesList):

        # Returns a valid move from the passed list on the passed board.

        # Returns None if there is no valid move.

        possibleMoves = []

        for i in movesList:

            if self.isSpaceFree(board, i):
                possibleMoves.append(i)

        if len(possibleMoves) != 0:

            return random.choice(possibleMoves)

        else:

            return None

    def getComputerMove(self, board, computerLetter):

        # Given a board and the computer's letter, determine where to move and return that move.

        if computerLetter == 'X':

            playerLetter = 'O'

        else:

            playerLetter = 'X'

        # Here is our algorithm for our Tic Tac Toe AI:

        # First, check if we can win in the next move

        for i in range(1, 10):

            copy = self.getBoardCopy(board)

            if self.isSpaceFree(copy, i):

                self.makeMove(copy, computerLetter, i)

                if self.isWinner(copy, computerLetter):
                    return i

        # Check if the player could win on their next move, and block them.

        for i in range(1, 10):

            copy = self.getBoardCopy(board)

            if self.isSpaceFree(copy, i):

                self.makeMove(copy, playerLetter, i)

                if self.isWinner(copy, playerLetter):
                    return i

        # Try to take one of the corners, if they are free.

        move = self.chooseRandomMoveFromList(board, [1, 3, 7, 9])

        if move != None:
            return move

        # Try to take the center, if it is free.

        if self.isSpaceFree(board, 5):
            return 5

        # Move on one of the sides.

        return self.chooseRandomMoveFromList(board, [2, 4, 6, 8])

    def getComputerMove2(self, board, P1, P2):

        best_move_score = -9999
        best_move_idx = -9999

        for idx in range(9):
            if board[idx] == '_':
                board[idx] = P1 # Try test move.
                score_for_this_move = -(self.negamax(board, P2, P1))
                board[idx] = '_' # Put back test move.

                if score_for_this_move >= best_move_score:
                    best_move_score = score_for_this_move
                    best_move_idx = idx

        return best_move_idx

    def negamax(self, board, P1, P2):

        best_move_score = -9999


        if self.isWinner(board, P1):
            return 1000

        elif self.isWinner(board, P2):
            return -1000

        for idx in range(9):
            if board[idx] == '_':
                board[idx] = P1 # Try test move.

                score_for_this_move = -(self.negamax(board, P2, P1))
                board[idx] = '_' # Put back test move.
                if score_for_this_move >= best_move_score:
                    best_move_score = score_for_this_move

        if best_move_score == -9999 or best_move_score == 0:
            return 0
        elif best_move_score < 0:
            return best_move_score + 1
        elif best_move_score > 0:
            return best_move_score - 1

    def isBoardFull(self, board):

        # Return True if every space on the board has been taken. Otherwise return False.

        for i in range(9):

            if self.isSpaceFree(board, i):
                return False

        return True

    # Unused
    def play(self):
        print('Welcome to Tic Tac Toe!')

        while True:

            # Reset the board

            self.theBoard = ['_'] * 9

            playerLetter, computerLetter = self.inputPlayerLetter()

            turn = self.whoGoesFirst()

            print('The ' + turn + ' will go first.')

            gameIsPlaying = True

            while gameIsPlaying:

                if turn == 'player':

                    # Player's turn.

                    self.drawBoard(self.theBoard)

                    move = self.getPlayerMove(self.theBoard)

                    self.makeMove(self.theBoard, playerLetter, move)

                    if self.isWinner(self.theBoard, playerLetter):

                        self.drawBoard(self.theBoard)

                        print('Hooray! You have won the game!')

                        gameIsPlaying = False

                    else:

                        if self.isBoardFull(self.theBoard):

                            self.drawBoard(self.theBoard)

                            print('The game is a tie!')

                            break

                        else:

                            turn = 'computer'

                else:

                    # Computer's turn.

                    move = self.getComputerMove2(self.theBoard, computerLetter, playerLetter)

                    self.makeMove(self.theBoard, computerLetter, move)

                    if self.isWinner(self.theBoard, computerLetter):

                        self.drawBoard(self.theBoard)

                        print('The computer has beaten you! You lose.')

                        gameIsPlaying = False

                    else:

                        if self.isBoardFull(self.theBoard):

                            self.drawBoard(self.theBoard)

                            print('The game is a tie!')

                            break

                        else:

                            turn = 'player'

            if not self.playAgain():
                break

    def next_move(self):
        if not self.gameIsPlaying:
            return

        j = 0
        while (j < 10):
            _, frm = self.cap.read()
            j += 1

        self.theBoard = self.get_real_board(frm)
        n_xs = self.theBoard.count('X')
        n_os = self.theBoard.count('O')
        print("X = " + str(n_xs) + ", O = " + str(n_os))

        if self.turn == 'player':
            # Player's turn.

            # try:
            #     move = self.next_player_move.get()
            #     if move > 9 or move < 1:
            #         raise("Value error")
            #     if not self.isSpaceFree(self.theBoard, move):
            #         raise("Value error")
            # except:
            #     print("Invalid move! Enter value between 1-9")
            #     return
            #
            # self.makeMove(self.theBoard, self.playerLetter, move)



            if (self.starts =='computer' and n_xs < n_os):  # The move has not been made
                print("Symbol was not drawn by the robot yet")
                return
            if (self.starts =='player' and n_xs == n_os):
                print("Player did not draw a symbol yet")
                return
            elif (self.starts =='player' and n_xs < n_os) or (self.starts =='computer' and n_xs > n_os):
                print("Something went wrong")
                return


            if self.isWinner(self.theBoard, self.playerLetter):
                print('Hooray! You have won the game!')
                self.stop_game()

            else:

                if self.isBoardFull(self.theBoard):
                    print('The game is a tie!')

                    self.stop_game()
                else:

                    self.turn = 'computer'

        if self.turn == 'computer':
            # Computer's turn.

            if (self.starts == 'computer' and n_xs < n_os) or (self.starts == 'player' and n_xs == n_os):  # The move has not been made
                print("Player did not draw yet")
                return
            elif (self.starts =='player' and n_xs < n_os) or (self.starts =='computer' and n_xs > n_os):
                print("Something went wrong")
                return

            move = self.getComputerMove2(self.theBoard, self.computerLetter, self.playerLetter)

            self.makeMove(self.theBoard, self.computerLetter, move)

            if self.isWinner(self.theBoard, self.computerLetter):

                print('The computer has beaten you! You lose.')

                self.stop_game()

            else:

                if self.isBoardFull(self.theBoard):

                    print('The game is a tie!')
                    self.stop_game()

                else:

                    self.turn = 'player'

        self.lbl_board_print()

    def calibrate(self):


        f_W = int(self.cap.get(3))
        f_H = int(self.cap.get(4))
        f_Size = (f_H, f_W)

        print(str(f_W) + ', ' + str(f_H))

        cv2.namedWindow("frame")

        cv2.createTrackbar('Height', 'frame', 97, 500, nothing)
        cv2.createTrackbar('Delta', 'frame', 20, 200, nothing)
        cv2.createTrackbar('TH', 'frame', 87, 255, nothing)
        cv2.createTrackbar('Rec_Lower', 'frame', 50, 1000, nothing)
        cv2.createTrackbar('Rec_Higher', 'frame', 2000, 5000, nothing)

        while (True):

            ret, frame = self.cap.read()

            self.grid_height = cv2.getTrackbarPos('Height', 'frame')
            self.grid_delta = cv2.getTrackbarPos('Delta', 'frame')
            self.thresh = cv2.getTrackbarPos('TH', 'frame')
            self.lower_T = cv2.getTrackbarPos('Rec_Lower', 'frame')
            self.higher_T = cv2.getTrackbarPos('Rec_Higher', 'frame')
            self.grids = self.set_grids(f_H, f_W, self.grid_height, self.grid_delta)

            bw = np.zeros(f_Size, dtype=np.uint8)
            gray = np.zeros(f_Size, dtype=np.uint8)

            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, gray)
            cv2.threshold(gray, self.thresh, 255, cv2.THRESH_BINARY_INV, bw)
            for g in self.grids:
                cv2.rectangle(bw, g[0], g[1], 255)
            cv2.imshow('frame', bw)

            wt = cv2.waitKey(1)
            if wt & 0xFF == 98: # 'b'oard
                current_board = self.get_real_board(frame)
                print(current_board)
            if wt & 0xFF == 27: # 'ESC'
                print ("Calibration complete")

                cv2.destroyWindow('frame')
                return

    def get_real_board(self, img):

        f_Size = (img.shape[0], img.shape[1])

        bw = np.zeros(f_Size, dtype=np.uint8)
        gray = np.zeros(f_Size, dtype=np.uint8)

        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY, gray)
        cv2.threshold(gray, self.thresh, 255, cv2.THRESH_BINARY_INV, bw)

        board = []
        for grid in self.grids:
            # Get all the contours in the ROI
            y0 = grid[0][1]
            y1 = grid[1][1]

            x0 = grid[0][0]
            x1 = grid[1][0]

            roi = bw[grid[0][1]:grid[1][1], grid[0][0]:grid[1][0]]
            _image, _contours, _hierarchy = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            max_area = 0
            max_id = 0

            # Get max area contour
            for cnt in _contours:
                if len(cnt) < 1:
                    continue
                this_area = cv2.contourArea(cnt)
                if this_area >= max_area:
                    max_area = this_area

            # Classify
            if max_area < self.lower_T:
                board.append('_')

            elif max_area > self.higher_T:
                board.append('O')

            else:
                board.append('X')
        return board

    class Rectangle():
        def __init__(self, pt1, pt2):
            self.pnts = [pt1, pt2]

        def __getitem__(self, item):
            return self.pnts[item]

        def area(self):
            l1 = abs(self.pnts[0][0] - self.pnts[1][0])
            l2 = abs(self.pnts[0][1] - self.pnts[1][1])
            return l1 * l2

    def set_grids(self, frame_H, frame_W, height, delta):
        grids = []

        mid_x = frame_W / 2
        mid_y = frame_H / 2

        r1_p1 = (int(mid_x - 1.5 * height - delta), int(mid_y - 1.5 * height - delta))
        r1_p2 = (r1_p1[0] + height, r1_p1[1] + height)

        r2_p1 = (int(mid_x - 0.5 * height), int(mid_y - 1.5 * height - delta))
        r2_p2 = (r2_p1[0] + height, r2_p1[1] + height)

        r3_p1 = (int(mid_x + 0.5 * height + delta), int(mid_y - 1.5 * height - delta))
        r3_p2 = (r3_p1[0] + height, r3_p1[1] + height)

        r4_p1 = (int(mid_x - 1.5 * height - delta), int(mid_y - 0.5 * height))
        r4_p2 = (r4_p1[0] + height, r4_p1[1] + height)

        r5_p1 = (int(mid_x - 0.5 * height), int(mid_y - 0.5 * height))
        r5_p2 = (r5_p1[0] + height, r5_p1[1] + height)

        r6_p1 = (int(mid_x + 0.5 * height + delta), int(mid_y - 0.5 * height))
        r6_p2 = (r6_p1[0] + height, r6_p1[1] + height)

        r7_p1 = (int(mid_x - 1.5 * height - delta), int(mid_y + 0.5 * height + delta))
        r7_p2 = (r7_p1[0] + height, r7_p1[1] + height)

        r8_p1 = (int(mid_x - 0.5 * height), int(mid_y + 0.5 * height + delta))
        r8_p2 = (r8_p1[0] + height, r8_p1[1] + height)

        r9_p1 = (int(mid_x + 0.5 * height + delta), int(mid_y + 0.5 * height + delta))
        r9_p2 = (r9_p1[0] + height, r9_p1[1] + height)

        grids.append(self.Rectangle(r7_p1, r7_p2))
        grids.append(self.Rectangle(r8_p1, r8_p2))
        grids.append(self.Rectangle(r9_p1, r9_p2))

        grids.append(self.Rectangle(r4_p1, r4_p2))
        grids.append(self.Rectangle(r5_p1, r5_p2))
        grids.append(self.Rectangle(r6_p1, r6_p2))

        grids.append(self.Rectangle(r1_p1, r1_p2))
        grids.append(self.Rectangle(r2_p1, r2_p2))
        grids.append(self.Rectangle(r3_p1, r3_p2))

        return grids
