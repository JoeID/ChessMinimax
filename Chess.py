import random
from tkinter import *
from itertools import product
import copy
import time


class View:
    def __init__(self):

        self.user_color = self.user_mode = self.user_moves = self.calc_counter = self.turn_counter = self.moves_without_take = 0
        self.game_state = "start/mid-game"
        self.dark = self.light = ""
        self.move_list = []

        def save():
            self.user_color = chosen_color.get()
            self.user_mode = chosen_mode.get()
            self.user_moves = int(chosen_move.get())
            board_color = chosen_board.get()
            if board_color == "gray":
                self.dark = "#AAAAAA"
                self.light = "#FFFFFF"
            elif board_color == "blue":
                self.dark = "#70809A"
                self.light = "#CCCFE0"
            elif board_color == "green":
                self.dark = "#86A666"
                self.light = "#FFFFDD"
            elif board_color == "brown":
                self.dark = "#B58863"
                self.light = "#F0D9B5"
            elif board_color == "red":
                self.dark = "#962414"
                self.light = "#E3AE8C"
            elif board_color == "violet":
                self.dark = "#d82bb3"
                self.light = "#E89DD8"

            presentation.quit()

            self.Board.pack(side=LEFT)
            self.Function_panel.pack(side=RIGHT)

        presentation = Tk()
        presentation.title("Kundéchecs")

        self.Chess = Toplevel(presentation)
        self.Board = Canvas(self.Chess, width=17 / 2 * self.CASE_WIDTH, height=17 / 2 * self.CASE_WIDTH, bg="#EEEEEE")
        self.Function_panel = Canvas(self.Chess, width=5 / 2 * self.CASE_WIDTH, height=17 / 2 * self.CASE_WIDTH,
                                     bg="#EEEEEE")
        self.stat_panel = self.Function_panel.create_text(0, 0, text="")

        instructions = LabelFrame(presentation, text="Please choose the AI's configuration")
        instructions.pack()

        color = Frame(instructions)
        color.pack(side=LEFT, padx=15, pady=15)
        Label(color, text="Your color").pack()
        chosen_color = StringVar(color)
        chosen_color.set("white")
        color_list = OptionMenu(color, chosen_color, "white", "black")
        color_list.pack()

        mode = Frame(instructions)
        mode.pack(side=LEFT, padx=15, pady=15)
        Label(mode, text="Game mode").pack()
        chosen_mode = StringVar(mode)
        chosen_mode.set("AI")
        mode_list = OptionMenu(mode, chosen_mode, "random", "value", "AI")
        mode_list.pack()

        moves = Frame(instructions)
        moves.pack(side=LEFT, padx=15, pady=15)
        Label(moves, text="Moves to calculate").pack()
        chosen_move = StringVar(moves)
        chosen_move.set("2")
        moves_list = OptionMenu(moves, chosen_move, "1", "2", "3", "4")
        moves_list.pack()

        board = Frame(instructions)
        board.pack(side=LEFT, padx=15, pady=15)
        Label(board, text="Board color").pack()
        chosen_board = StringVar(board)
        chosen_board.set("brown")
        board_list = OptionMenu(board, chosen_board, "brown", "blue", "gray", "green", "red", "violet")
        board_list.pack()

        validate = Button(presentation, text="Save and play", command=save, relief=FLAT)
        validate.pack(side=BOTTOM)

        presentation.mainloop()

    CASE_WIDTH = 80
    DOT_WIDTH = 0.4 * CASE_WIDTH
    # so that the dots are in the center of the cases
    DOT_ADJUSTMENT = (CASE_WIDTH - DOT_WIDTH) / 2
    ALPHABET = "abcdefgh"

    def get_user_conf(self):
        return [self.user_color, self.user_mode, self.user_moves]

    def update(self):  # update the chessboard
        self.Board.delete("all")
        self.Board.images = []

        for x in range(8):
            text = self.ALPHABET[x] if human_player.color == "white" else self.ALPHABET[7 - x]
            self.Board.create_text((x + 1 / 2) * self.CASE_WIDTH, (8 + 1 / 4) * self.CASE_WIDTH,
                                   text=text, font="Arial 16 bold")
        for y in range(8):
            text = str(8 - y) if human_player.color == "white" else str(y + 1)
            self.Board.create_text((8 + 1 / 4) * self.CASE_WIDTH, (y + 1 / 2) * self.CASE_WIDTH,
                                   text=text, font="Arial 16 bold")

        for x in range(8):
            for y in range(8):
                # draw the board
                if (x + y) % 2 == 1:
                    self.Board.create_rectangle(
                        (x * self.CASE_WIDTH, y * self.CASE_WIDTH,
                         (x + 1) * self.CASE_WIDTH, (y + 1) * self.CASE_WIDTH),
                        fill=self.dark, width=0)
                else:
                    self.Board.create_rectangle(
                        (x * self.CASE_WIDTH, y * self.CASE_WIDTH,
                         (x + 1) * self.CASE_WIDTH, (y + 1) * self.CASE_WIDTH),
                        fill=self.light, width=0)

        if self.move_list:
            try:
                moving = self.move_list[-1][2]
            except IndexError:
                moving = self.move_list[-1][0]
            pattern = r"[abcdefgh][12345678]"
            # reverse the list if the human plays black
            alphabet = self.ALPHABET if human_player.color == "white" else self.ALPHABET[::-1]

            if moving != "O-O-O" and moving != "O-O":
                first = moving[0:3]
                second = moving[3:]

                oldXY = re.search(pattern, first).group()
                newXY = re.search(pattern, second).group()
                oldX, oldY = oldXY
                newX, newY = newXY

                oldX = alphabet.index(oldX)
                oldY = 7-int(oldY)+1 if human_player.color == "white" else int(oldY)-1
                newX = alphabet.index(newX)
                newY = 7-int(newY)+1 if human_player.color == "white" else int(newY)-1

                self.show_moving(oldX, oldY, newX, newY)

        for x in range(8):
            for y in range(8):
                # draw the pieces
                if Pieces.pieces_list[x][y] != "nothing":
                    piece = PhotoImage(file=Pieces.pieces_list[x][y] + ".png")
                    self.Board.create_image((x + 1 / 2) * self.CASE_WIDTH, (y + 1 / 2) * self.CASE_WIDTH,
                                            image=piece)
                    # to keep trace of the images so that the garbage collector doesn't erase them
                    self.Board.images.append(piece)

        human_kingX, human_kingY = human_player.get_position_of_king(Pieces.pieces_list)
        AI_kingX, AI_kingY = AI_player.get_position_of_king(Pieces.pieces_list)

        if human_player.is_threatened(human_kingX, human_kingY, Pieces.pieces_list):
            threatened = PhotoImage(file="checked " + human_player.color + " king.png")
            self.Board.create_image((human_kingX + 1 / 2) * self.CASE_WIDTH, (human_kingY + 1 / 2) * self.CASE_WIDTH,
                                    image=threatened)
            self.Board.images.append(threatened)

        elif AI_player.is_threatened(AI_kingX, AI_kingY, Pieces.pieces_list):
            threatened = PhotoImage(file="checked " + AI_player.color + " king.png")
            self.Board.create_image((AI_kingX + 1 / 2) * self.CASE_WIDTH, (AI_kingY + 1 / 2) * self.CASE_WIDTH,
                                    image=threatened)
            self.Board.images.append(threatened)

        if self.game_state == "start/mid-game":
            total_ai_pieces = 0
            for x in range(8):
                for y in range(8):
                    if Pieces.pieces_list[x][y] != "nothing":
                        color, type = Pieces.pieces_list[x][y].split()
                        if color == AI_player.color:
                            if type == "pawn":
                                total_ai_pieces += Pieces.PAWN_VALUE
                            elif type == "knight":
                                total_ai_pieces += Pieces.KNIGHT_VALUE
                            elif type == "bishop":
                                total_ai_pieces += Pieces.BISHOP_VALUE
                            elif type == "queen":
                                total_ai_pieces += Pieces.QUEEN_VALUE
                            elif type == "rook":
                                total_ai_pieces += Pieces.ROOK_VALUE
                            else:
                                continue
            if total_ai_pieces <= Pieces.QUEEN_VALUE + Pieces.ROOK_VALUE:
                self.game_state = "endgame"

    def show_possible_plays(self, possible_plays):
        if possible_plays is not None:
            for i in range(2, len(possible_plays)):
                # extract the coordinates of the possible plays
                x = possible_plays[i][0]
                y = possible_plays[i][1]

                dot_color = "#32FF32"
                self.Board.create_oval(
                    (x * self.CASE_WIDTH + self.DOT_ADJUSTMENT, y * self.CASE_WIDTH + self.DOT_ADJUSTMENT,  # x0, y0
                     (x + 1) * self.CASE_WIDTH - self.DOT_ADJUSTMENT, (y + 1) * self.CASE_WIDTH - self.DOT_ADJUSTMENT),
                    # x1, y1
                    fill=dot_color, width=0)

    def show_victory(self, winner):

        if winner == "human":
            self.Board.create_text(4 * self.CASE_WIDTH, 4 * self.CASE_WIDTH,
                                   text="YOU WON", font="Arial 50 bold", fill="#32FF32")
            self.Board.create_text(4 * self.CASE_WIDTH, 9 / 2 * self.CASE_WIDTH,
                                   text="checkmate", font="Arial 25", fill="#32FF32")

        elif winner == "AI":
            self.Board.create_text(4 * self.CASE_WIDTH, 4 * self.CASE_WIDTH,
                                   text="YOU LOST", font="Arial 50 bold", fill="#F40E0E")
            self.Board.create_text(4 * self.CASE_WIDTH, 9 / 2 * self.CASE_WIDTH,
                                   text="checkmate", font="Arial 25", fill="#F40E0E")

        elif winner == "draw":
            self.Board.create_text(4 * self.CASE_WIDTH, 4 * self.CASE_WIDTH,
                                   text="DRAW", font="Arial 50 bold", fill="#D90EF4")
            self.Board.create_text(4 * self.CASE_WIDTH, 9 / 2 * self.CASE_WIDTH,
                                   text="stalemate", font="Arial 25", fill="#D90EF4")
        AI_player.can_play = human_player.can_play = False

    def show_moving(self, oldX, oldY, newX, newY):
        self.Board.moving = []
        moving = PhotoImage(file="moving piece.png", width=self.CASE_WIDTH, height=self.CASE_WIDTH)
        self.Board.create_image((oldX + 1 / 2) * self.CASE_WIDTH, (oldY + 1 / 2) * self.CASE_WIDTH, image=moving)
        self.Board.create_image((newX + 1 / 2) * self.CASE_WIDTH, (newY + 1 / 2) * self.CASE_WIDTH, image=moving)
        self.Board.moving.append(moving)

    def show_progression(self, percentage):
        print(percentage)
        self.Board.create_rectangle(0, 0, percentage * 8 * self.CASE_WIDTH / 100, 5, fill="#32FF32", width=0)

    def show_stats(self):
        self.Function_panel.delete(self.stat_panel)

        AI_possible_plays = AI_player.get_list_possible_plays(Pieces.pieces_list)
        human_possible_plays = human_player.get_list_possible_plays(Pieces.pieces_list)

        AI_mobility = AI_player.get_mobility(Pieces.pieces_list, human_possible_plays)
        human_mobility = human_player.get_mobility(Pieces.pieces_list, AI_possible_plays)

        current_reward = AI_player.reward(Pieces.pieces_list, AI_mobility-human_mobility)
        output_text = "Moves calculated : " + str(self.calc_counter) + \
                      "\nMoves without action : " + str(self.moves_without_take) + \
                      "\nCurrent AI reward : " + str(current_reward)

        self.stat_panel = self.Function_panel.create_text(5 / 4 * self.CASE_WIDTH, 1 / 2 * self.CASE_WIDTH,
                                                          text=output_text, font="Arial 11")

    def algebraic_notation(self, type, oldX, oldY, newX, newY, old_target_case, event):
        winner = "nobody"
        if type == "king" and abs(oldX - newX) == 2:  # if the king castled
            # small castle
            if (newX - oldX == 2 and AI_player.color == "black") or (newX - oldX == -2 and AI_player.color == "white"):
                text = "O-O"
            else:  # big castle
                text = "O-O-O"
        else:
            old_caseX = self.ALPHABET[oldX] if human_player.color == "white" else self.ALPHABET[7 - oldX]
            old_caseY = str(8 - oldY) if human_player.color == "white" else str(oldY + 1)
            new_caseX = self.ALPHABET[newX] if human_player.color == "white" else self.ALPHABET[7 - newX]
            new_caseY = str(8 - newY) if human_player.color == "white" else str(newY + 1)
            promotion = ""

            if type == "pawn":
                piece = ""
                if newY == 0 or newY == 7:
                    promotion = "Q"
            elif type == "knight":
                piece = "N"
            elif type == "bishop":
                piece = "B"
            elif type == "queen":
                piece = "Q"
            elif type == "rook":
                piece = "R"
            else:  # if the piece is a king
                piece = "K"

            moving = "-" if old_target_case == "nothing" else "x"

            if event == "check":
                event = "+"
            elif event == "AI" or event == "human":
                winner = event
                event = "#"
            elif event == "draw":
                winner = event
                event = "="
            else:
                event = ""

            text = piece + old_caseX + old_caseY + moving + new_caseX + new_caseY + promotion + event
        if not self.move_list:
            self.move_list.append([text, AI_player.copy(Pieces.pieces_list)])
        elif len(self.move_list[-1]) == 4:
            self.move_list.append([text, AI_player.copy(Pieces.pieces_list)])
        else:
            self.move_list[-1].append(text)
            self.move_list[-1].append(AI_player.copy(Pieces.pieces_list))

        self.show_moving_list()

        if event != "#" and event != "=":  # because you cannot cancel a move if you or your opponent is checkmated
            cancel = Button(self.Function_panel, command=self.cancel_turn, text="Cancel last turn", relief=RAISED)
            self.Function_panel.create_window(5 / 4 * self.CASE_WIDTH, 7 * self.CASE_WIDTH, window=cancel)
        self.update()
        if winner == "draw" or winner == "human" or winner == "AI":
            self.show_victory(winner)

    def show_moving_list(self):
        self.Function_panel.delete("all")
        if not self.move_list:
            return None
        x = 11
        for i in range(len(self.move_list) - 1, len(self.move_list) - 13, -1):
            if i < 0:
                break
            # output the algebric notation of the moves
            self.Function_panel.create_text(1/8*self.CASE_WIDTH, (2+x/3)*self.CASE_WIDTH+10, text=str(i+1), font="Arial 11")
            self.Function_panel.create_text(3/4 * self.CASE_WIDTH, (2+x/3)*self.CASE_WIDTH+10,
                                            text=self.move_list[i][0], font="Arial 13")
            if len(self.move_list[i]) == 4:
                self.Function_panel.create_text(7 / 4 * self.CASE_WIDTH, (2 + x / 3) * self.CASE_WIDTH + 10,
                                                text=self.move_list[i][2], font="Arial 13")
            x -= 1

        # create the border and the button
        self.Function_panel.create_rectangle(1 / 4 * self.CASE_WIDTH, 2 * self.CASE_WIDTH - 7,
                                             9 / 4 * self.CASE_WIDTH, 6 * self.CASE_WIDTH + 3, fill="", width=2)
        self.Function_panel.create_text(5 / 4 * self.CASE_WIDTH, 7 / 4 * self.CASE_WIDTH,
                                        text="WHITE      BLACK", font="Arial 12 bold")
        cancel = Button(self.Function_panel, command=self.cancel_turn, text="Cancel last turn", relief=RAISED)
        self.Function_panel.create_window(5 / 4 * self.CASE_WIDTH, 7 * self.CASE_WIDTH, window=cancel)

    def cancel_turn(self):
        if AI_player.color == "white" and self.turn_counter == 1:
            return None
        try:
            del self.move_list[-1]
            if AI_player.color == "black":
                restore_index = 3
            else:
                restore_index = 1
                del self.move_list[-1][2:]
            Pieces.pieces_list = copy.deepcopy(self.move_list[-1][restore_index])
            self.update()
            self.show_moving_list()
            self.turn_counter -= 1
        except IndexError:
            self.turn_counter -= 1
            Pieces.pieces_list = [
                ['black rook', 'black pawn', 'nothing', 'nothing', 'nothing', 'nothing', 'white pawn', 'white rook'],
                ['black knight', 'black pawn', 'nothing', 'nothing', 'nothing', 'nothing', 'white pawn',
                 'white knight'],
                ['black bishop', 'black pawn', 'nothing', 'nothing', 'nothing', 'nothing', 'white pawn',
                 'white bishop'],
                ['black queen', 'black pawn', 'nothing', 'nothing', 'nothing', 'nothing', 'white pawn', 'white queen'],
                ['black king', 'black pawn', 'nothing', 'nothing', 'nothing', 'nothing', 'white pawn', 'white king'],
                ['black bishop', 'black pawn', 'nothing', 'nothing', 'nothing', 'nothing', 'white pawn',
                 'white bishop'],
                ['black knight', 'black pawn', 'nothing', 'nothing', 'nothing', 'nothing', 'white pawn',
                 'white knight'],
                ['black rook', 'black pawn', 'nothing', 'nothing', 'nothing', 'nothing', 'white pawn', 'white rook']]
            self.update()
            self.show_moving_list()
            self.turn_counter -= 1
        self.focus_rectangle = self.Board.create_rectangle(0, 0, 0, 0, fill="", width=4, outline="yellow")


class Pieces:
    pieces_list = [[], [], [], [], [], [], [], []]  # store every single piece

    PIECE_WIDTH = int(0.9 * View.CASE_WIDTH)
    PIECE_MARGIN = (View.CASE_WIDTH - PIECE_WIDTH) / 2

    QUEEN_VALUE = 8.8
    ROOK_VALUE = 5.1
    PAWN_VALUE = 1.0
    BISHOP_VALUE = 3.33
    KNIGHT_VALUE = 3.2

    MOBILITY_BONUS = [[[-62, -81], [-53, -56], [-12, -30], [-4, -14], [3, 8], [13, 15], [22, 23], [28, 27], [33, 33]],
                      # for the knights

                      [[-48, -59], [-20, -23], [16, -3], [26, 13], [38, 24], [51, 42], [55, 54], [63, 57], [63, 65],
                       [68, 73], [81, 78], [81, 86], [91, 88], [98, 97]],  # for the bishops

                      [[-58, -76], [-27, -18], [-15, 28], [-10, 55], [-5, 69], [-2, 82], [9, 112], [16, 118], [30, 132],
                       [29, 142], [32, 155], [38, 165], [46, 166], [48, 169], [58, 171]],  # for the rooks

                      [[-39, -36], [-21, -15], [3, 8], [3, 18], [14, 34], [22, 54], [28, 61], [41, 73], [43, 79],
                       [48, 92], [56, 94], [60, 104], [60, 113], [66, 120], [67, 123], [70, 126], [71, 133], [73, 136],
                       [79, 140], [88, 143], [88, 148], [99, 166], [102, 170], [102, 175], [106, 184], [109, 191],
                       [113, 206], [116, 212]]]  # for the queen

    def __init__(self):
        top_color = "black" if human_player.color == "white" else "white"
        bottom_color = "white" if human_player.color == "white" else "black"

        for x in range(8):
            for y in range(8):
                if y == 1:  # create the top pawns
                    self.pieces_list[x].append(top_color + " pawn")

                elif y == 6:  # create the bottom pawns
                    self.pieces_list[x].append(bottom_color + " pawn")

                elif y == 0:  # create the other top pieces
                    if x == 0 or x == 7:
                        self.pieces_list[x].append(top_color + " rook")
                    if x == 1 or x == 6:
                        self.pieces_list[x].append(top_color + " knight")
                    if x == 2 or x == 5:
                        self.pieces_list[x].append(top_color + " bishop")
                    if x == 3 and top_color == "black" or x == 4 and top_color == "white":
                        self.pieces_list[x].append(top_color + " queen")
                    if x == 4 and top_color == "black" or x == 3 and top_color == "white":
                        self.pieces_list[x].append(top_color + " king")

                elif y == 7:  # create the other bottom pieces
                    if x == 0 or x == 7:
                        self.pieces_list[x].append(bottom_color + " rook")
                    if x == 1 or x == 6:
                        self.pieces_list[x].append(bottom_color + " knight")
                    if x == 2 or x == 5:
                        self.pieces_list[x].append(bottom_color + " bishop")
                    if x == 4 and bottom_color == "black" or x == 3 and bottom_color == "white":
                        self.pieces_list[x].append(bottom_color + " queen")
                    if x == 3 and bottom_color == "black" or x == 4 and bottom_color == "white":
                        self.pieces_list[x].append(bottom_color + " king")

                else:

                    self.pieces_list[x].append("nothing")  # if the case is empty


class Player:

    def __init__(self, color, config=None, mode="default", moves_ahead=1):
        self.is_a_right_piece = False
        # check if the selected piece is the same color as the
        # player. For the moment, it is false because no piece is selected
        self.is_a_right_place = False
        # check if the selected piece can be played at a given place
        # For the moment, it is false because no piece is selected
        if color == "white":
            self.can_play = True
        else:
            self.can_play = False

        self.color = color
        self.mode = mode
        self.moves_ahead = moves_ahead
        self.max_moves_ahead = moves_ahead + 2
        self.max_reward = 1
        self.king_moved = self.left_rook_moved = self.right_rook_moved = False  # used to check if a player can castle

        if config is not None:
            self.VALUE_WEIGHT, self.MOBILITY_WEIGHT, self.PAWN_WEIGHT = config

    def get_position_of_king(self, chessboard):
        for x in range(8):
            for y in range(8):
                if chessboard[x][y] == self.color + " king":
                    return [x, y]

    def get_list_possible_plays(self, chessboard, PseudoLegalMoves=False):

        list_possible_plays = []
        pattern = self.color

        kingX, kingY = self.get_position_of_king(chessboard)

        # it appends the list of possible plays for each piece the player has
        for y in range(7, -1, -1):
            for x in range(8):

                if re.match(pattern, chessboard[x][y]):

                    possible_plays = self.get_list_plays_of_piece(x, y, chessboard, kingX, kingY, PseudoLegalMoves)

                    if possible_plays is not None:
                        list_possible_plays.append(possible_plays)

        return list_possible_plays

    def is_not_in_check(self, chessboard, oldX, oldY, newX, newY, kingX, kingY):

        backup = chessboard[newX][newY]

        color, piece = chessboard[oldX][oldY].split()
        chessboard[oldX][oldY] = "nothing"
        chessboard[newX][newY] = color + " " + piece

        if piece == "king":
            if not self.is_threatened(newX, newY, chessboard):
                chessboard[oldX][oldY] = color + " " + piece
                chessboard[newX][newY] = backup
                return True
            else:
                chessboard[oldX][oldY] = color + " " + piece
                chessboard[newX][newY] = backup
                return False

        if not self.is_threatened(kingX, kingY, chessboard):
            chessboard[oldX][oldY] = color + " " + piece
            chessboard[newX][newY] = backup
            return True
        else:
            chessboard[oldX][oldY] = color + " " + piece
            chessboard[newX][newY] = backup
            return False

    def get_list_plays_of_piece(self, x, y, chessboard, kingX, kingY, PseudoLegalMoves):

        # stores first the name of the piece
        list_play_of_piece = [[x, y], chessboard[x][y]]

        color, type = chessboard[x][y].split(None)
        oldX = x
        oldY = y

        if type == "pawn":

            newX = x
            newY = (y - 1) if color == human_player.color else (y + 1)
            newnewY = (y - 2) if color == human_player.color else (y + 2)

            # the following lines verify if the pawn can be moved right
            # ahead
            if chessboard[newX][newY] == "nothing" and \
                    (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY)):
                list_play_of_piece.append([newX, newY])

            # if the human pawn has never moved and can move 2 cases right
            # ahead
            if color == human_player.color and y == 6 and chessboard[newX][newnewY] == "nothing" \
                    and chessboard[newX][newY] == "nothing" \
                    and (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newnewY, kingX, kingY)):
                list_play_of_piece.append([newX, newnewY])

            # if the AI pawn has never moved and can move 2 cases right
            # ahead
            if color == AI_player.color and y == 1 and chessboard[newX][newnewY] == "nothing" and \
                    chessboard[newX][newY] == "nothing" and \
                    (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newnewY, kingX, kingY)):
                list_play_of_piece.append([newX, newnewY])

            # the following lines verify if the pawn can attack
            newX = x - 1
            if newX in range(8) and chessboard[newX][newY] != "nothing" and \
                    re.match(color, chessboard[newX][newY]) is None and \
                    (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY)):
                # the line just above verifies if the newX is in the chess
                # board, if the case corresponding is occupied and not by an
                # allied piece
                list_play_of_piece.append([newX, newY])

            newX = x + 1
            if newX in range(8) and chessboard[newX][newY] != "nothing" and \
                    re.match(color, chessboard[newX][newY]) is None and \
                    (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY)):
                # the line just above verifies if the newX is in the chess
                # board, if the case corresponding is occupied and not by an
                # allied piece
                list_play_of_piece.append([newX, newY])

                ####################################################################

        elif type == "rook":

            for i in range(oldX + 1, 8):
                # if there is nothing or an enemy on the cases at the right of
                # the piece
                if re.match(color, chessboard[i][y]) is None and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, i, y, kingX, kingY)):
                    list_play_of_piece.append([i, y])
                if chessboard[i][y] != "nothing":
                    break

            for i in range(oldX - 1, -1, -1):
                # if there is nothing or an enemy on the cases at the left of
                # the piece
                if re.match(color, chessboard[i][y]) is None and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, i, y, kingX, kingY)):
                    list_play_of_piece.append([i, y])
                if chessboard[i][y] != "nothing":
                    break

            for i in range(oldY + 1, 8):
                # if there is nothing or an enemy on the cases on the bottom
                # of the piece
                if re.match(color, chessboard[x][i]) is None and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, x, i, kingX, kingY)):
                    list_play_of_piece.append([x, i])
                if chessboard[x][i] != "nothing":
                    break

            for i in range(oldY - 1, -1, -1):
                # if there is nothing or an enemy on the cases on the top of
                # the piece
                if re.match(color, chessboard[x][i]) is None and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, x, i, kingX, kingY)):
                    list_play_of_piece.append([x, i])
                if chessboard[x][i] != "nothing":
                    break

                    #######################################################

        elif type == "knight":
            for a in range(-2, +3):
                for b in range(-2, +3):
                    if abs(a) + abs(b) == 3 and (x + a) in range(8) and (y + b) in range(8) and \
                            re.match(color, chessboard[x + a][y + b]) is None and \
                            (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, x+a, y+b, kingX, kingY)):
                        list_play_of_piece.append([x + a, y + b])

                    #######################################################

        elif type == "bishop":
            for i in range(1, 8):
                newX = x + i
                newY = y + i
                if newX in range(8) and newY in range(8):
                    # if there is nothing or an enemy on the cases at the
                    # down-right of the piece
                    if re.match(color, chessboard[newX][newY]) is None and \
                            (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY)):
                        list_play_of_piece.append([newX, newY])
                    if chessboard[newX][newY] != "nothing":
                        break

            for i in range(1, 8):
                newX = x + i
                newY = y - i
                if newX in range(8) and newY in range(8):
                    # if there is nothing or an enemy on the cases at the
                    # up-right of the piece
                    if re.match(color, chessboard[newX][newY]) is None and \
                            (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY)):
                        list_play_of_piece.append([newX, newY])
                    if chessboard[newX][newY] != "nothing":
                        break

            for i in range(1, 8):
                newX = x - i
                newY = y + i
                if newX in range(8) and newY in range(8):
                    # if there is nothing or an enemy on the cases at the
                    # down-left of the piece
                    if re.match(color, chessboard[newX][newY]) is None and \
                            (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY)):
                        list_play_of_piece.append([newX, newY])
                    if chessboard[newX][newY] != "nothing":
                        break

            for i in range(1, 8):
                newX = x - i
                newY = y - i
                if newX in range(8) and newY in range(8):
                    # if there is nothing or an enemy on the cases at the
                    # up-left of the piece
                    if re.match(color, chessboard[newX][newY]) is None and \
                            (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY)):
                        list_play_of_piece.append([newX, newY])
                    if chessboard[newX][newY] != "nothing":
                        break

                ###########################################################

        elif type == "queen":
            for i in range(oldX + 1, 8):
                # if there is nothing or an enemy on the cases at the right of
                # the piece
                if re.match(color, chessboard[i][y]) is None and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, i, y, kingX, kingY)):
                    list_play_of_piece.append([i, y])
                if chessboard[i][y] != "nothing":
                    break

            for i in range(oldX - 1, -1, -1):
                # if there is nothing or an enemy on the cases at the left of
                # the piece
                if re.match(color, chessboard[i][y]) is None and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, i, y, kingX, kingY)):
                    list_play_of_piece.append([i, y])
                if chessboard[i][y] != "nothing":
                    break

            for i in range(oldY + 1, 8):
                # if there is nothing or an enemy on the cases on the bottom
                # of the piece
                if re.match(color, chessboard[x][i]) is None and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, x, i, kingX, kingY)):
                    list_play_of_piece.append([x, i])
                if chessboard[x][i] != "nothing":
                    break

            for i in range(oldY - 1, -1, -1):
                # if there is nothing or an enemy on the cases on the top of
                # the piece
                if re.match(color, chessboard[x][i]) is None and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, x, i, kingX, kingY)):
                    list_play_of_piece.append([x, i])
                if chessboard[x][i] != "nothing":
                    break

            for i in range(1, 8):
                newX = x + i
                newY = y + i
                if newX in range(8) and newY in range(8):
                    # if there is nothing or an enemy on the cases at the
                    # down-right of the piece
                    if re.match(color, chessboard[newX][newY]) is None and \
                            (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY)):
                        list_play_of_piece.append([newX, newY])
                    if chessboard[newX][newY] != "nothing":
                        break

            for i in range(1, 8):
                newX = x + i
                newY = y - i
                if newX in range(8) and newY in range(8):
                    # if there is nothing or an enemy on the cases at the
                    # up-right of the piece
                    if re.match(color, chessboard[newX][newY]) is None and \
                            (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY)):
                        list_play_of_piece.append([newX, newY])
                    if chessboard[newX][newY] != "nothing":
                        break

            for i in range(1, 8):
                newX = x - i
                newY = y + i
                if newX in range(8) and newY in range(8):
                    # if there is nothing or an enemy on the cases at the
                    # down-left of the piece
                    if re.match(color, chessboard[newX][newY]) is None and \
                            (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY)):
                        list_play_of_piece.append([newX, newY])
                    if chessboard[newX][newY] != "nothing":
                        break

            for i in range(1, 8):
                newX = x - i
                newY = y - i
                if newX in range(8) and newY in range(8):
                    # if there is nothing or an enemy on the cases at the
                    # up-left of the piece
                    if re.match(color, chessboard[newX][newY]) is None and \
                            (PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY)):
                        list_play_of_piece.append([newX, newY])
                    if chessboard[newX][newY] != "nothing":
                        break

            ###############################################################

        elif type == "king":
            for a in range(-1, 2):
                for b in range(-1, 2):
                    newX = oldX + a
                    newY = oldY + b
                    if abs(a) + abs(b) != 0 and newX in range(8) and newY in range(8) and \
                            re.match(self.color, chessboard[newX][newY]) is None:
                        # check if the coordinates a and b of the movement of the
                        # king are good and if the targeted case is no occupied by
                        # an allied piece

                        if PseudoLegalMoves or self.is_not_in_check(chessboard, oldX, oldY, newX, newY, kingX, kingY):
                            list_play_of_piece.append([newX, newY])

            # check if the king can castle

            # if the position of the king hasn't changed
            if not self.king_moved and (oldX == 3 or oldX == 4) and not self.is_threatened(oldX, oldY, chessboard):

                if not self.left_rook_moved and chessboard[0][oldY] == self.color + " rook":
                    for i in range(oldX - 1, 0, -1):
                        # check the left castling
                        if chessboard[i][oldY] != "nothing" or (i >= 1 and self.is_threatened(i, oldY, chessboard)):
                            break
                    else:
                        list_play_of_piece.append([oldX - 2, oldY])

                if not self.right_rook_moved and chessboard[7][oldY] == self.color + " rook":
                    for i in range(oldX + 1, 7):
                        # check the right castling
                        if chessboard[i][oldY] != "nothing" or self.is_threatened(i, oldY, chessboard):
                            break
                    else:
                        list_play_of_piece.append([oldX + 2, oldY])

        # if the list is not composed of just the name of the piece
        if list_play_of_piece != [[x, y], chessboard[x][y]]:
            return list_play_of_piece
        else:
            return None

    def is_threatened(self, caseX, caseY, chessboard):
        enemy_color = "white" if self.color == "black" else "black"

        # first of all verify if a pawn is threatening the case

        enemy_pawnY = caseY - 1 if self.color == human_player.color else caseY + 1

        if caseX + 1 in range(8) and enemy_pawnY in range(8) and \
                chessboard[caseX + 1][enemy_pawnY] == enemy_color + " pawn":
            return True
        if caseX - 1 in range(8) and enemy_pawnY in range(8) and \
                chessboard[caseX - 1][enemy_pawnY] == enemy_color + " pawn":
            return True

        # then verify if a king is threatening the case

        for x in range(-1, 2):
            for y in range(-1, 2):
                if abs(x) + abs(y) != 0 and caseX + x in range(8) and caseY + y in range(8):
                    if chessboard[caseX + x][caseY + y] == enemy_color + " king":
                        return True

        # then verify if a knight is threatening the piece

        for x in range(-2, 3):
            for y in range(-2, 3):
                if caseX + x in range(8) and caseY + y in range(8) and abs(x) + abs(y) == 3:
                    if chessboard[caseX + x][caseY + y] == enemy_color + " knight":
                        return True

        # then verifing the sliding pieces

        for x in range(caseX + 1, 8):  # check the right
            if chessboard[x][caseY] == enemy_color + " rook" or \
                    chessboard[x][caseY] == enemy_color + " queen":
                return True
            if chessboard[x][caseY] != "nothing":
                break

        for x in range(caseX - 1, -1, -1):  # check the left
            if chessboard[x][caseY] == enemy_color + " rook" or \
                    chessboard[x][caseY] == enemy_color + " queen":
                return True
            if chessboard[x][caseY] != "nothing":
                break

        for y in range(caseY + 1, 8):  # check the bottom
            if chessboard[caseX][y] == enemy_color + " rook" or \
                    chessboard[caseX][y] == enemy_color + " queen":
                return True
            if chessboard[caseX][y] != "nothing":
                break

        for y in range(caseY - 1, -1, -1):  # check the top
            if chessboard[caseX][y] == enemy_color + " rook" or \
                    chessboard[caseX][y] == enemy_color + " queen":
                return True
            if chessboard[caseX][y] != "nothing":
                break

        ###################################

        for i in range(1, 8):  # check the bottom-right
            newX = caseX + i
            newY = caseY + i
            if newX in range(8) and newY in range(8):
                if (chessboard[newX][newY] == enemy_color + " bishop" or
                        chessboard[newX][newY] == enemy_color + " queen"):
                    return True
                if chessboard[newX][newY] != "nothing":
                    break

        for i in range(1, 8):  # check the top-right
            newX = caseX + i
            newY = caseY - i
            if newX in range(8) and newY in range(8):
                if (chessboard[newX][newY] == enemy_color + " bishop" or
                        chessboard[newX][newY] == enemy_color + " queen"):
                    return True
                if chessboard[newX][newY] != "nothing":
                    break

        for i in range(1, 8):  # check the bottom-left
            newX = caseX - i
            newY = caseY + i
            if newX in range(8) and newY in range(8):
                if (chessboard[newX][newY] == enemy_color + " bishop" or
                        chessboard[newX][newY] == enemy_color + " queen"):
                    return True
                if chessboard[newX][newY] != "nothing":
                    break

        for i in range(1, 8):  # check the top-left
            newX = caseX - i
            newY = caseY - i
            if newX in range(8) and newY in range(8):
                if (chessboard[newX][newY] == enemy_color + " bishop" or
                        chessboard[newX][newY] == enemy_color + " queen"):
                    return True
                if chessboard[newX][newY] != "nothing":
                    break

        return False

    @staticmethod
    def move_piece(oldX, oldY, newX, newY, chessboard):
        piece_to_move = chessboard[oldX][oldY]
        color, type = piece_to_move.split(None)
        piece_taken = True if chessboard[newX][newY] != 'nothing' else False

        if type == "pawn" and (newY == 0 or newY == 7):  # if the piece is a pawn which reached its last line
            chessboard[newX][newY] = color + " queen"
        elif type == "king" and newX - oldX == -2:  # if the king wants to castle at his left
            old_rookX = 0
            old_rookY = oldY
            new_rookX = newX + 1
            new_rookY = newY
            chessboard[old_rookX][old_rookY] = "nothing"
            chessboard[new_rookX][new_rookY] = color + " rook"
            chessboard[newX][newY] = piece_to_move
        elif type == "king" and newX - oldX == 2:  # if the king wants to castle at his right
            old_rookX = 7
            old_rookY = oldY
            new_rookX = newX - 1
            new_rookY = newY
            chessboard[old_rookX][old_rookY] = "nothing"
            chessboard[new_rookX][new_rookY] = color + " rook"
            chessboard[newX][newY] = piece_to_move
        else:
            chessboard[newX][newY] = piece_to_move

        chessboard[oldX][oldY] = "nothing"

        return piece_taken

    def get_mobility(self, chessboard, enemy_possible_plays, debug=False):
        enemy_attack_table = self.get_attack_table(enemy_possible_plays)
        enemy_color = "white" if self.color == "black" else "black"
        bonus_index = 0 if myView.game_state == "start/mid-game" else 1

        if self.color == AI_player.color:
            excluded_ranks = {1, 2}
            enemy_pawn_step = 1
        else:
            excluded_ranks = {5, 6}
            enemy_pawn_step = -1
        excluded_mobility_area = []
        for x in range(8):  # first defines the mobility area by excluding some squares :
            #  those occupied by pawns on ranks 2 & 3, or the queen, or the king, or defended by an ennemy pawn
            for y in range(8):

                if chessboard[x][y] == self.color + " pawn" and y in excluded_ranks:
                    excluded_mobility_area.append([x, y])
                    continue
                elif chessboard[x][y] == self.color + " king" or chessboard[x][y] == self.color + " queen":
                    excluded_mobility_area.append([x, y])
                    continue
                elif (x+1 in range(8) and y+enemy_pawn_step in range(8) and chessboard[x+1][y+enemy_pawn_step] == enemy_color + " pawn") \
                        or (x-1 in range(8) and y+enemy_pawn_step in range(8) and chessboard[x-1][y+enemy_pawn_step] == enemy_color + " pawn"):
                    excluded_mobility_area.append([x, y])
                    continue
        queen_mobility = bishops_mobility = knights_mobility = rooks_mobility = 0

        for x in range(8):
            for y in range(8):
                if chessboard[x][y] == "nothing":
                    continue
                else:
                    color, type = chessboard[x][y].split()

                if color == self.color:
                    if type == "king" or type == "pawn":
                        continue
                    elif type == "queen":
                        queen_mobility_score = 0
                        for a in range(x+1, 8):
                            A = "rook" in enemy_attack_table[a][y] \
                                    or "bishop" in enemy_attack_table[a][y] \
                                    or "knight" in enemy_attack_table[a][y]  # A : the case is attacked by an ennemy piece
                            B = re.match(color, chessboard[a][y])  # B : the piece on the case is ours
                            C = re.match(enemy_color, chessboard[a][y])  # C : the piece on the case is enemy's one
                            D = [a, y] in excluded_mobility_area  # D : the case is in excluded mobility area
                            if (A and not B and not C and not D) or (not A and not B and not C and D):  # if only A or only D
                                continue
                            elif (not A and B and not C and not D) or (not A and not B and C and not D):  # if only B or only C
                                queen_mobility_score += 1
                            elif not A and not B and not C and not D:
                                queen_mobility_score += 1
                                continue
                            break

                        for a in range(x-1, -1, -1):
                            A = "rook" in enemy_attack_table[a][y] \
                                    or "bishop" in enemy_attack_table[a][y] \
                                    or "knight" in enemy_attack_table[a][y]  # A : the case is attacked by an ennemy piece
                            B = re.match(color, chessboard[a][y])  # B : the piece on the case is ours
                            C = re.match(enemy_color, chessboard[a][y])  # C : the piece on the case is enemy's one
                            D = [a, y] in excluded_mobility_area  # D : the case is in excluded mobility area
                            if (A and not B and not C and not D) or (not A and not B and not C and D):  # if only A or only D
                                continue
                            elif (not A and B and not C and not D) or (not A and not B and C and not D):  # if only B or only C
                                queen_mobility_score += 1
                            elif not A and not B and not C and not D:
                                queen_mobility_score += 1
                                continue
                            break

                        for b in range(y+1, 8):
                            A = "rook" in enemy_attack_table[x][b] \
                                    or "bishop" in enemy_attack_table[x][b] \
                                    or "knight" in enemy_attack_table[x][b]  # A : the case is attacked by an ennemy piece
                            B = re.match(color, chessboard[x][b])  # B : the piece on the case is ours
                            C = re.match(enemy_color, chessboard[x][b])  # C : the piece on the case is enemy's one
                            D = [x, b] in excluded_mobility_area  # D : the case is in excluded mobility area
                            if (A and not B and not C and not D) or (not A and not B and not C and D):  # if only A or only D
                                continue
                            elif (not A and B and not C and not D) or (not A and not B and C and not D):  # if only B or only C
                                queen_mobility_score += 1
                            elif not A and not B and not C and not D:
                                queen_mobility_score += 1
                                continue
                            break

                        for b in range(y-1, -1, -1):
                            A = "rook" in enemy_attack_table[x][b] \
                                    or "bishop" in enemy_attack_table[x][b] \
                                    or "knight" in enemy_attack_table[x][b]  # A : the case is attacked by an ennemy piece
                            B = re.match(color, chessboard[x][b])  # B : the piece on the case is ours
                            C = re.match(enemy_color, chessboard[x][b])  # C : the piece on the case is enemy's one
                            D = [x, b] in excluded_mobility_area  # D : the case is in excluded mobility area
                            if (A and not B and not C and not D) or (not A and not B and not C and D):  # if only A or only D
                                continue
                            elif (not A and B and not C and not D) or (not A and not B and C and not D):  # if only B or only C
                                queen_mobility_score += 1
                            elif not A and not B and not C and not D:
                                queen_mobility_score += 1
                                continue
                            break

                        for a, b in product([-1, 1], repeat=2):
                            for i in range(1, 8):
                                newX = x + a*i
                                newY = y + b*i
                                if newX not in range(8) or newY not in range(8):
                                    break
                                A = "rook" in enemy_attack_table[newX][newY] \
                                        or "bishop" in enemy_attack_table[newX][newY] \
                                        or "knight" in enemy_attack_table[newX][newY]  # A : the case is attacked by an ennemy piece
                                B = re.match(color, chessboard[newX][newY])  # B : the piece on the case is ours
                                C = re.match(enemy_color, chessboard[newX][newY])  # C : the piece on the case is enemy's one
                                D = [newX, newY] in excluded_mobility_area  # D : the case is in excluded mobility area
                                if (A and not B and not C and not D) or (not A and not B and not C and D):  # if only A or only D
                                    continue
                                elif (not A and B and not C and not D) or (not A and not B and C and not D):  # if only B or only C
                                    queen_mobility_score += 1
                                elif not A and not B and not C and not D:
                                    queen_mobility_score += 1
                                    continue
                                break
                        queen_mobility += Pieces.MOBILITY_BONUS[3][queen_mobility_score][bonus_index]

                    elif type == "rook":
                        look_through = {"nothing", color + " rook", color + " queen"}
                        rook_mobility_score = 0

                        for a in range(x+1, 8):
                            A = chessboard[a][y] in look_through  # A : can look through
                            B = re.match(color, chessboard[a][y])  # B : is our piece
                            C = [a, y] in excluded_mobility_area  # is in excluded mobility area
                            if A and not C:
                                rook_mobility_score += 1
                                continue
                            elif B and not A and not C:
                                rook_mobility_score += 1
                            elif A and C:
                                continue
                            break

                        for a in range(x-1, -1, -1):
                            A = chessboard[a][y] in look_through  # A : can look through
                            B = re.match(color, chessboard[a][y])  # B : is our piece
                            C = [a, y] in excluded_mobility_area  # is in excluded mobility area
                            if A and not C:
                                rook_mobility_score += 1
                                continue
                            elif B and not A and not C:
                                rook_mobility_score += 1
                            elif A and C:
                                continue
                            break

                        for b in range(y+1, 8):
                            A = chessboard[x][b] in look_through  # A : can look through
                            B = re.match(color, chessboard[x][b])  # B : is our piece
                            C = [x, b] in excluded_mobility_area  # is in excluded mobility area
                            if A and not C:
                                rook_mobility_score += 1
                                continue
                            elif B and not A and not C:
                                rook_mobility_score += 1
                            elif A and C:
                                continue
                            break

                        for b in range(y-1, -1, -1):
                            A = chessboard[x][b] in look_through  # A : can look through
                            B = re.match(color, chessboard[x][b])  # B : is our piece
                            C = [x, b] in excluded_mobility_area  # is in excluded mobility area
                            if A and not C:
                                rook_mobility_score += 1
                                continue
                            elif B and not A and not C:
                                rook_mobility_score += 1
                            elif A and C:
                                continue
                            break
                        if debug:
                            print("rooks mobility score {}".format(rook_mobility_score))
                        rooks_mobility += Pieces.MOBILITY_BONUS[2][rook_mobility_score][bonus_index]

                    elif type == "bishop":
                        look_through = {"nothing", color + " queen", color + " bishop"}
                        bishop_mobility_score = 0

                        for a, b in product([-1, 1], repeat=2):
                            for i in range(1, 8):
                                newX = x + a * i
                                newY = y + b * i
                                if newX not in range(8) or newY not in range(8):
                                    break
                                A = chessboard[newX][newY] in look_through  # A : the bishop can look through the case
                                B = re.match(color, chessboard[newX][newY])  # B : the piece on the case is ours
                                C = [newX, newY] in excluded_mobility_area  # C : the case is in excluded mobility area
                                if A and not C:
                                    bishop_mobility_score += 1
                                    continue
                                elif not A and B and not C:
                                    bishop_mobility_score += 1
                                elif A and C:
                                    continue
                                break
                        bishops_mobility += Pieces.MOBILITY_BONUS[1][bishop_mobility_score][bonus_index]

                    elif type == "knight":
                        knight_mobility_score = 0
                        for a in range(-2, 3):
                            for b in range(-2, 3):
                                if abs(a) + abs(b) == 3 and x+a in range(8) and y+b in range(8):
                                    if [x+a, y+b] in excluded_mobility_area:
                                        continue
                                    elif re.match(enemy_color, chessboard[x+a][y+b]) is None:
                                        knight_mobility_score += 1
                        knights_mobility += Pieces.MOBILITY_BONUS[0][knight_mobility_score][bonus_index]
        mobility = knights_mobility + bishops_mobility + rooks_mobility + queen_mobility
        if debug:
            print("knights {} rooks {} bishops {} queen {}".format(knights_mobility, rooks_mobility, bishops_mobility, queen_mobility))
        return mobility

    @staticmethod
    def get_attack_table(possible_plays):
        attack_table = [[["none"] for i in range(8)] for j in range(8)]
        for a in range(len(possible_plays)):
            piece = possible_plays[a][1].split()[1]
            for b in range(2, len(possible_plays[a])):
                attackX = possible_plays[a][b][0]
                attackY = possible_plays[a][b][1]
                try:
                    if attack_table[attackX][attackY] == "none":
                        attack_table[attackX][attackY] = [piece]
                    else:
                        attack_table[attackX][attackY].append(piece)
                except IndexError as error:
                    print(error)
                    print(attackX, attackY)
                    print(possible_plays)
                    print(a, b)
        return attack_table

    def get_pawn_reward(self, chessboard):
        reward = cases_bf_passing = 0
        if self.color == human_player.color:
            step = -1
            board_edge = -1
        else:
            step = 1
            board_edge = 8
        enemy_color = "white" if self.color == "black" else "black"
        if myView.game_state == "start/mid-game":
            pawn_chains = []
            average_chain_length = 0
            passing_pawn_reward = 0
            total_chains = 0
            for y in range(board_edge-step*8, board_edge, step):
                for x in range(8):
                    if chessboard[x][y] == self.color + " pawn":
                        for i in range(y, board_edge, step):
                            if chessboard[x][i] == enemy_color + " pawn":
                                break
                        else:
                            cases_bf_passing += abs(board_edge-1-y)  # those lines are executed only if the for loop was not break
                            passing_pawn_reward += 1/cases_bf_passing
                        if [x, y] not in pawn_chains:
                            pawn_chains.append([x, y])
                            pawn_chains.append(1)
                            for direction in [1, -1]:
                                for i in range(1, 8):
                                    newX = x+i*direction
                                    newY = y+i*step
                                    if newX not in range(8) or newY not in range(8):
                                        break
                                    elif chessboard[newX][newY] != self.color + " pawn":
                                        break
                                    else:
                                        pawn_chains.insert(-1, [newX, newY])
                                        pawn_chains[-1] += 1
            for smth in pawn_chains:
                try:
                    average_chain_length += smth
                    total_chains += 1
                except TypeError:
                    continue
            try:
                average_chain_length = average_chain_length/(total_chains*8.0)  # to calculate the average and ensure it's a value btw 0 and 1
            except ZeroDivisionError:
                average_chain_length = 0.0
            passing_pawn_reward = passing_pawn_reward/8.0  # to ensure it's a value btw 0 and 1
            reward = (2*average_chain_length + passing_pawn_reward)/3
        else:  # endgame
            for x in range(8):
                for y in range(8):
                    if chessboard[x][y] == self.color + " pawn":
                        for i in range(y, board_edge, step):
                            if chessboard[x][i] == enemy_color + " pawn":
                                break
                        else:
                            cases_bf_passing += abs(board_edge-1-y)
                            reward += 1/cases_bf_passing
            reward = reward/8.0  # to ensure it's a value btw 0 and 1
        return reward


class Engine(Player):

    def play_move(self, chessboard):

        possible_plays = self.get_list_possible_plays(chessboard)
        kingX, kingY = self.get_position_of_king(chessboard)
        event = "nothing"

        if not possible_plays:
            if self.is_threatened(kingX, kingY, chessboard):
                myView.show_victory("human")
                return None
            else:
                myView.show_victory("draw")
                return None

        index_1, index_2 = self.choose_index(chessboard, possible_plays)

        oldX, oldY = possible_plays[index_1][0]
        newX, newY = possible_plays[index_1][index_2]

        old_target_case = chessboard[newX][newY]
        piece_taken = self.move_piece(oldX, oldY, newX, newY, chessboard)
        type = chessboard[newX][newY].split()[1]

        if type == "rook":
            if oldX == 0:
                self.left_rook_moved = True
            elif oldX == 7:
                self.right_rook_moved = True
        elif type == "king":
            self.king_moved = True
        elif type == "pawn":
            piece_taken = True

        human_kingX, human_kingY = human_player.get_position_of_king(Pieces.pieces_list)

        self.can_play = False
        human_player.can_play = True

        if human_player.is_threatened(human_kingX, human_kingY, Pieces.pieces_list):
            event = "check"
        if not human_player.get_list_possible_plays(Pieces.pieces_list):

            if human_player.is_threatened(human_kingX, human_kingY, Pieces.pieces_list):
                event = "AI"
                piece_taken = None
            else:
                event = "draw"
                piece_taken = None

        elif myView.moves_without_take >= 50:
            event = "draw"
            piece_taken = None

        myView.algebraic_notation(type, oldX, oldY, newX, newY, old_target_case, event)

        return piece_taken

    def choose_index(self, chessboard, possible_plays):
        if self.mode == "random":

            # checks if the AI can put the human player checkmate

            checkmate_XY = self.checkmate_opponent(chessboard, possible_plays)

            if checkmate_XY is None:  # if the AI cannot put a checkmate

                index_1 = random.randint(0, len(possible_plays) - 1)
                index_2 = random.randint(2, len(possible_plays[index_1]) - 1)
                return [index_1, index_2]
            else:

                return checkmate_XY

        elif self.mode == "value" or self.mode == "AI":

            list_best_moves = self.minimax(possible_plays, self.moves_ahead, self.max_moves_ahead, True,
                                           -self.max_reward, self.max_reward,
                                           chessboard)

            # finally return the coordinates of the play to make in the list of possible plays
            if len(list_best_moves) == 1:

                [[index_1, index_2]] = list_best_moves
                return [index_1, index_2]

            else:
                rand = random.randint(0, len(list_best_moves) - 1)
                index_1, index_2 = list_best_moves[rand]
                return [index_1, index_2]

    def minimax(self, possible_plays, depth, max_depth, maximizingPlayer, alpha, beta, chessboard):
        # https://fr.wikipedia.org/wiki/Algorithme_minimax

        if depth == 0:
            self_possible_plays = self.get_list_possible_plays(chessboard, True)
            enemy_possible_plays = human_player.get_list_possible_plays(chessboard, True)

            self_mobility = self.get_mobility(chessboard, enemy_possible_plays)
            human_mobility = human_player.get_mobility(chessboard, self_possible_plays)
            return self.reward(chessboard, self_mobility - human_mobility)

        if maximizingPlayer:  # AI
            best_plays = []
            value = -self.max_reward
            human_kingX, human_kingY = human_player.get_position_of_king(chessboard)

            for a in range(len(possible_plays)):

                oldX, oldY = possible_plays[a][0]

                if depth == self.moves_ahead:
                    myView.show_progression(int(100 * a / len(possible_plays)))

                for b in range(2, len(possible_plays[a])):

                    new_chessboard = self.copy(chessboard)

                    newX, newY = possible_plays[a][b]
                    piece_taken = self.move_piece(oldX, oldY, newX, newY, new_chessboard)
                    enemy_possible_plays = human_player.get_list_possible_plays(new_chessboard)
                    if not enemy_possible_plays:
                        if human_player.is_threatened(human_kingX, human_kingY, new_chessboard):
                            if depth == self.moves_ahead:
                                return [[a, b]]
                            else:
                                return self.max_reward
                        else:  # in case of draw
                            if depth == self.moves_ahead:
                                value_test = 0
                            else:
                                return 0
                    else:
                        check = True if human_player.is_threatened(human_kingX, human_kingY, new_chessboard) else False
                        if ((piece_taken and depth == 1) or (check and max_depth >=3)) and max_depth >= 0:
                            value_test = self.minimax(enemy_possible_plays, depth, max_depth - 1, False, alpha, beta,
                                                      new_chessboard)
                        else:
                            value_test = self.minimax(enemy_possible_plays, depth - 1, max_depth - 1, False, alpha,
                                                      beta, new_chessboard)

                    if value_test > value:
                        value = value_test
                        if depth == self.moves_ahead:
                            best_plays = [[a, b]]

                    elif value_test == value and depth == self.moves_ahead:
                        best_plays.append([a, b])
                    if depth != self.moves_ahead:
                        alpha = max(alpha, value)
                        if alpha >= beta:
                            return value

            if depth == self.moves_ahead:
                return best_plays
            else:
                return value

        else:  # minimizingPlayer
            value = self.max_reward
            kingX, kingY = self.get_position_of_king(chessboard)
            for a in range(len(possible_plays)):

                oldX, oldY = possible_plays[a][0]
                for b in range(2, len(possible_plays[a])):

                    new_chessboard = self.copy(chessboard)

                    newX, newY = possible_plays[a][b]
                    piece_taken = human_player.move_piece(oldX, oldY, newX, newY, new_chessboard)
                    enemy_possible_plays = self.get_list_possible_plays(new_chessboard)

                    if not enemy_possible_plays:
                        if self.is_threatened(kingX, kingY, new_chessboard):
                            return -self.max_reward
                        else:  # in case of draw
                            return 0
                    else:
                        if piece_taken and depth == 1:
                            value = min(value,
                                        self.minimax(enemy_possible_plays, depth, max_depth - 1, True, alpha, beta,
                                                     new_chessboard))
                        else:
                            value = min(value,
                                        self.minimax(enemy_possible_plays, depth - 1, max_depth - 1, True, alpha, beta,
                                                     new_chessboard))

                    beta = min(beta, value)
                    if beta <= alpha:
                        return value

            return value

    def checkmate_opponent(self, chessboard, possible_plays):

        for a in range(len(possible_plays)):

            oldX, oldY = possible_plays[a][0]

            for b in range(2, len(possible_plays[a])):

                new_chessboard = self.copy(chessboard)

                newX, newY = possible_plays[a][b]
                self.move_piece(oldX, oldY, newX, newY, new_chessboard)
                human_kingX, human_kingY = human_player.get_position_of_king(new_chessboard)

                if not human_player.get_list_possible_plays(new_chessboard) and \
                        human_player.is_threatened(human_kingX, human_kingY, new_chessboard):
                    return [[a, b]]

        return None

    def reward(self, chessboard, mobility):

        ally_color = self.color
        enemy_color = "white" if self.color == "black" else "black"
        value_reward = reward = 0.0

        if self.mode == "value":
            for x in range(8):
                for y in range(8):

                    if chessboard[x][y] != "nothing":
                        piece_color, piece_type = chessboard[x][y].split(None)
                    else:
                        continue

                    if ally_color == piece_color:
                        if piece_type == "queen":
                            reward += Pieces.QUEEN_VALUE
                        elif piece_type == "rook":
                            reward += Pieces.ROOK_VALUE
                        elif piece_type == "bishop":
                            reward += Pieces.BISHOP_VALUE
                        elif piece_type == "knight":
                            reward += Pieces.KNIGHT_VALUE
                        elif piece_type == "pawn":
                            reward += Pieces.PAWN_VALUE

                    elif enemy_color == piece_color:
                        if piece_type == "queen":
                            reward -= Pieces.QUEEN_VALUE
                        elif piece_type == "rook":
                            reward -= Pieces.ROOK_VALUE
                        elif piece_type == "bishop":
                            reward -= Pieces.BISHOP_VALUE
                        elif piece_type == "knight":
                            reward -= Pieces.KNIGHT_VALUE
                        elif piece_type == "pawn":
                            reward -= Pieces.PAWN_VALUE

            return round(reward / 40.06, 3)
        elif self.mode == "AI":
            for x in range(8):
                for y in range(8):
                    if chessboard[x][y] != "nothing":
                        piece_color, piece_type = chessboard[x][y].split(None)
                    else:
                        continue

                    if ally_color == piece_color:
                        if piece_type == "queen":
                            value_reward += Pieces.QUEEN_VALUE
                        elif piece_type == "rook":
                            value_reward += Pieces.ROOK_VALUE
                        elif piece_type == "bishop":
                            value_reward += Pieces.BISHOP_VALUE
                        elif piece_type == "knight":
                            value_reward += Pieces.KNIGHT_VALUE
                        elif piece_type == "pawn":
                            value_reward += Pieces.PAWN_VALUE

                    elif enemy_color == piece_color:
                        if piece_type == "queen":
                            value_reward -= Pieces.QUEEN_VALUE
                        elif piece_type == "rook":
                            value_reward -= Pieces.ROOK_VALUE
                        elif piece_type == "bishop":
                            value_reward -= Pieces.BISHOP_VALUE
                        elif piece_type == "knight":
                            value_reward -= Pieces.KNIGHT_VALUE
                        elif piece_type == "pawn":
                            value_reward -= Pieces.PAWN_VALUE

            pawn_reward = self.get_pawn_reward(chessboard)-human_player.get_pawn_reward(chessboard)
            value_reward = value_reward / 40.06  # so that it's a value btw -1 and 1
            mobility_reward = mobility / 814.0  # so that it's a value btw -1 and 1
            reward = round((value_reward*self.VALUE_WEIGHT + mobility_reward*self.MOBILITY_WEIGHT) + pawn_reward*self.PAWN_WEIGHT/
                           (self.VALUE_WEIGHT + self.MOBILITY_WEIGHT + self.PAWN_WEIGHT),
                           3)
            myView.calc_counter += 1
            return reward

    def copy(self, chessboard):
        new_list = []
        for i in range(len(chessboard)):
            new_list.append(list(chessboard[i]))
        return new_list


class Human(Player):

    def play_move(self, pieceX, pieceY):
        if self.is_a_right_piece and self.can_play:

            color, type = Pieces.pieces_list[self.oldX][self.oldY].split(None)

            if self.oldX == pieceX and self.oldY == pieceY:
                self.is_a_right_place = False
                return [False, False]

            if self.list_of_plays_of_the_piece_to_move is not None:
                if [pieceX, pieceY] in self.list_of_plays_of_the_piece_to_move:
                    self.is_a_right_place = True

            if self.is_a_right_place:
                old_target_case = Pieces.pieces_list[pieceX][pieceY]
                piece_taken = self.move_piece(self.oldX, self.oldY, pieceX, pieceY, Pieces.pieces_list)

                self.is_a_right_piece = False
                self.is_a_right_place = False

                if type == "rook":
                    if self.oldX == 0:
                        self.left_rook_moved = True
                    elif self.oldX == 7:
                        self.right_rook_moved = True
                elif type == "king":
                    self.king_moved = True
                elif type == "pawn":
                    piece_taken = True

                self.can_play = False
                AI_player.can_play = True

                AI_kingX, AI_kingY = AI_player.get_position_of_king(Pieces.pieces_list)
                if not AI_player.get_list_possible_plays(Pieces.pieces_list):
                    if AI_player.is_threatened(AI_kingX, AI_kingY, Pieces.pieces_list):
                        event = "human"
                    else:
                        event = "draw"
                elif AI_player.is_threatened(AI_kingX, AI_kingY, Pieces.pieces_list):
                    event = "check"
                else:
                    event = ""

                myView.algebraic_notation(type, self.oldX, self.oldY, pieceX, pieceY, old_target_case, event)

                return [True, piece_taken]

            else:
                myView.update()
                return [False, False]
        return [False, False]

    def start_move(self, mouseX, mouseY):

        # to take the x and y positions of the piece targeted by the mouse
        pieceX = int(mouseX / View.CASE_WIDTH)
        pieceY = int(mouseY / View.CASE_WIDTH)

        pattern = self.color

        # to verify if the piece that the player is trying to move is the same
        # color as the player
        if re.match(pattern, Pieces.pieces_list[pieceX][pieceY]) is not None and self.can_play:
            self.piece_to_move = Pieces.pieces_list[pieceX][pieceY]
            self.oldX = pieceX
            self.oldY = pieceY

            kingX, kingY = self.get_position_of_king(Pieces.pieces_list)

            possible_plays = self.get_list_plays_of_piece(pieceX, pieceY, Pieces.pieces_list, kingX, kingY, False)
            myView.show_possible_plays(possible_plays)

            self.list_of_plays_of_the_piece_to_move = possible_plays

            self.is_a_right_piece = True


with open("coeffs.txt", "r") as coeffs:
    conf = []
    for line in coeffs:
        conf.append(float(line.split()[1]))

coeffs.close()
myView = View()  # instanciate the view with the chosen color for the board
# you can choose among : gray,red,green,blue,brown

human_color, AI_mode, depth = myView.get_user_conf()
human_player = Human(human_color)
AI_color = "white" if human_player.color == "black" else "black"

AI_player = Engine(AI_color, conf, AI_mode, depth)
# coeffs from left to right : value, table, mobility, king protection

myView.click_counter = 0
myView.calc_counter = 0


def onClick(event):
    myView.Board.delete(myView.focus_rectangle)
    myView.focus_rectangle = myView.Board.create_rectangle(0, 0, 0, 0, fill="", width=4, outline="yellow")
    # to ensure the user doesn't click out of the board
    if myView.click_counter == 0 and event.x < 8 * myView.CASE_WIDTH and event.y < 8 * myView.CASE_WIDTH:
        if human_player.can_play:
            human_player.start_move(event.x, event.y)
        myView.click_counter += 1
    else:
        if human_player.can_play:
            pieceX = int(event.x / View.CASE_WIDTH)
            pieceY = int(event.y / View.CASE_WIDTH)
            human_move = human_player.play_move(pieceX, pieceY)
            if human_move[0]:
                if human_move[1]:  # if a piece was taken
                    myView.moves_without_take = 0
                else:
                    myView.moves_without_take += 1

                myView.calc_counter = 0
                start_time = time.time()
                if AI_player.play_move(Pieces.pieces_list):  # if a piece was taken
                    myView.moves_without_take = 0
                else:
                    myView.moves_without_take += 1

                myView.turn_counter += 1
                myView.show_stats()
                moves_per_second = myView.calc_counter/(time.time() - start_time)
                print("moves per second", round(moves_per_second, 3))
        myView.click_counter = 0
    myView.focus_rectangle = myView.Board.create_rectangle(0, 0, 0, 0, fill="", width=4, outline="yellow")


def onOverlap(event):
    x = int(event.x / View.CASE_WIDTH)
    y = int(event.y / View.CASE_WIDTH)
    if x < 8 and y < 8:
        myView.Board.coords(myView.focus_rectangle, x * myView.CASE_WIDTH + 2, y * myView.CASE_WIDTH + 2,
                            (x + 1) * myView.CASE_WIDTH - 2, (y + 1) * myView.CASE_WIDTH - 2)


pieces = Pieces()
myView.update()
myView.focus_rectangle = myView.Board.create_rectangle(0, 0, 0, 0, fill="", width=4, outline="yellow")

if AI_player.can_play:
    AI_player.play_move(Pieces.pieces_list)
    myView.turn_counter += 1
    myView.show_stats()
    myView.focus_rectangle = myView.Board.create_rectangle(0, 0, 0, 0, fill="", width=4, outline="yellow")

myView.Board.bind("<Button-1>", onClick)
myView.Board.bind("<Motion>", onOverlap)

myView.Chess.mainloop()
