# coding: utf8

import random
from tkinter import *
from itertools import product
import time


class View:
    def __init__(self):

        self.user_color = self.user_mode = self.user_moves = self.calc_counter = self.turn_counter = self.moves_without_take = 0
        self.game_state = "start/mid-game"
        self.dark = self.light = ""
        self.move_list = []
        self.focus_rectangle = None

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
        self.Board = Canvas(self.Chess, width=8.5 * self.CASE_WIDTH, height=8.5 * self.CASE_WIDTH, bg="#EEEEEE")
        self.Function_panel = Canvas(self.Chess, width=2.5 * self.CASE_WIDTH, height=8.5 * self.CASE_WIDTH,
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
        mode_list = OptionMenu(mode, chosen_mode, "value", "AI")
        mode_list.pack()

        moves = Frame(instructions)
        moves.pack(side=LEFT, padx=15, pady=15)
        Label(moves, text="Moves to calculate").pack()
        chosen_move = StringVar(moves)
        chosen_move.set("2")
        moves_list = OptionMenu(moves, chosen_move, "2", "3", "4")
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

    def update(self, chessboard):  # update the chessboard
        self.Board.delete("all")
        self.Board.images = []
        all_pieces = "pnbrkqPNBRKQ"

        for x in range(8):  # draw the marks
            text = self.ALPHABET[x] if human_player.color == "white" else self.ALPHABET[7 - x]
            self.Board.create_text((x + 0.5) * self.CASE_WIDTH, (8 + 0.25) * self.CASE_WIDTH,
                                   text=text, font="Arial 16 bold")
        for y in range(8):
            text = str(8 - y) if human_player.color == "white" else str(y + 1)
            self.Board.create_text((8 + 0.25) * self.CASE_WIDTH, (y + 0.5) * self.CASE_WIDTH,
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

        for i in range(64):
            # draw the pieces
            if chessboard[i] != "o":
                piece = PhotoImage(file=Pieces.pieces_name[all_pieces.index(chessboard[i])] + ".png")
                self.Board.create_image((i%8 + 0.5) * self.CASE_WIDTH, (int(i/8) + 0.5) * self.CASE_WIDTH,
                                        image=piece)
                # to keep trace of the images so that the garbage collector doesn't erase them
                self.Board.images.append(piece)

        human_kingPos = human_player.get_position_of_king(chessboard)
        AI_kingPos = AI_player.get_position_of_king(chessboard)

        if human_player.is_threatened(human_kingPos, chessboard):
            threatened = PhotoImage(file="checked " + human_player.color + " king.png")
            self.Board.create_image((human_kingPos%8 + 0.5) * self.CASE_WIDTH, (int(human_kingPos/8) + 0.5) * self.CASE_WIDTH,
                                    image=threatened)
            self.Board.images.append(threatened)

        elif AI_player.is_threatened(AI_kingPos, chessboard):
            threatened = PhotoImage(file="checked " + AI_player.color + " king.png")
            self.Board.create_image((AI_kingPos%8 + 0.5) * self.CASE_WIDTH, (int(AI_kingPos/8) + 0.5) * self.CASE_WIDTH,
                                    image=threatened)
            self.Board.images.append(threatened)

        if self.game_state == "start/mid-game":
            total_ai_pieces = 0
            ai_pieces = AI_player.self_pieces
            for piece in Pieces.pieces_list:
                if piece == ai_pieces[0]:
                    total_ai_pieces += Pieces.PAWN_VALUE
                elif piece == ai_pieces[1]:
                    total_ai_pieces += Pieces.KNIGHT_VALUE
                elif piece == ai_pieces[2]:
                    total_ai_pieces += Pieces.BISHOP_VALUE
                elif piece == ai_pieces[5]:
                    total_ai_pieces += Pieces.QUEEN_VALUE
                elif piece == ai_pieces[3]:
                    total_ai_pieces += Pieces.ROOK_VALUE

            if total_ai_pieces <= Pieces.QUEEN_VALUE + Pieces.ROOK_VALUE:
                self.game_state = "endgame"
        self.Chess.update()

    def show_possible_plays(self, possible_plays):
        if possible_plays is not None:
            all_pieces = "pnbrkqPNBRKQ"
            pos = True
            dotPos = ""
            for i in possible_plays:
                if i == "|":
                    pos = False
                    continue
                if pos:
                    continue

                if i == "/":
                    # extract the coordinates of the possible plays
                    dotPos = int(dotPos)
                    x = dotPos%8
                    y = int(dotPos/8)

                    dot_color = "#32FF32"
                    self.Board.create_oval(
                        (x * self.CASE_WIDTH + self.DOT_ADJUSTMENT, y * self.CASE_WIDTH + self.DOT_ADJUSTMENT,  # x0, y0
                         (x + 1) * self.CASE_WIDTH - self.DOT_ADJUSTMENT, (y + 1) * self.CASE_WIDTH - self.DOT_ADJUSTMENT),
                        # x1, y1
                        fill=dot_color, width=0)
                    dotPos = ""

                elif i in all_pieces:
                    pos = True
                    continue
                else:
                    dotPos += i

    def show_victory(self, winner):

        if winner == "human":
            self.Board.create_text(4 * self.CASE_WIDTH, 4 * self.CASE_WIDTH,
                                   text="YOU WON", font="Arial 50 bold", fill="#32FF32")
            self.Board.create_text(4 * self.CASE_WIDTH, 4.5 * self.CASE_WIDTH,
                                   text="checkmate", font="Arial 25", fill="#32FF32")

        elif winner == "AI":
            self.Board.create_text(4 * self.CASE_WIDTH, 4 * self.CASE_WIDTH,
                                   text="YOU LOST", font="Arial 50 bold", fill="#F40E0E")
            self.Board.create_text(4 * self.CASE_WIDTH, 4.5 * self.CASE_WIDTH,
                                   text="checkmate", font="Arial 25", fill="#F40E0E")

        elif winner == "draw":
            self.Board.create_text(4 * self.CASE_WIDTH, 4 * self.CASE_WIDTH,
                                   text="DRAW", font="Arial 50 bold", fill="#D90EF4")
            self.Board.create_text(4 * self.CASE_WIDTH, 4.5 * self.CASE_WIDTH,
                                   text="stalemate", font="Arial 25", fill="#D90EF4")
        AI_player.can_play = human_player.can_play = False

    def show_moving(self, oldX, oldY, newX, newY):
        self.Board.moving = []
        moving = PhotoImage(file="moving piece.png", width=self.CASE_WIDTH, height=self.CASE_WIDTH)
        self.Board.create_image((oldX + 0.5) * self.CASE_WIDTH, (oldY + 0.5) * self.CASE_WIDTH, image=moving)
        self.Board.create_image((newX + 0.5) * self.CASE_WIDTH, (newY + 0.5) * self.CASE_WIDTH, image=moving)
        self.Board.moving.append(moving)

    def show_stats(self):
        self.Function_panel.delete(self.stat_panel)

        AI_possible_plays = AI_player.get_list_possible_plays(Pieces.pieces_list)
        human_possible_plays = human_player.get_list_possible_plays(Pieces.pieces_list)

        AI_mobility = AI_player.get_mobility(Pieces.pieces_list, human_possible_plays)
        human_mobility = human_player.get_mobility(Pieces.pieces_list, AI_possible_plays)

        current_reward = AI_player.reward(Pieces.pieces_list, AI_mobility-human_mobility)
        output_text = "Moves calculated : " + str(self.calc_counter) + \
                      "\nBoring moves : " + str(self.moves_without_take) + \
                      "\nCurrent AI reward : " + str(current_reward)

        self.stat_panel = self.Function_panel.create_text(self.CASE_WIDTH, 0.4 * self.CASE_WIDTH,
                                                          text=output_text, font="Arial 10")

    def algebraic_notation(self, piece, oldPos, newPos, old_target_case, event, chessboard):
        winner = "nobody"
        oldX = oldPos%8
        oldY = int(oldPos/8)
        newX = newPos%8
        newY = int(newPos/8)
        if piece in "kK" and abs(oldX - newX) == 2:  # if the king castled
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

            if piece in "pP":
                piece = ""
                if newY == 0 or newY == 7:
                    promotion = "Q"
            elif piece in "nN":
                piece = "N"
            elif piece in "bB":
                piece = "B"
            elif piece in "qQ":
                piece = "Q"
            elif piece in "rR":
                piece = "R"
            else:  # if the piece is a king
                piece = "K"

            moving = "-" if old_target_case == "o" else "x"

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
        if not self.move_list:  # move_list = [[text1, chessboard1, text2, chessboard2], [text3, chessboard3, text4, chessboard4]...]
            self.move_list.append([text, chessboard])
        elif len(self.move_list[-1]) == 4:
            self.move_list.append([text, chessboard])
        else:
            self.move_list[-1].append(text)
            self.move_list[-1].append(chessboard)

        self.show_moving_list()
        self.update(chessboard)

        if event != "#" and event != "=":  # because you cannot cancel a move if you or your opponent is checkmated
            cancel = Button(self.Function_panel, command=self.cancel_turn, text="Cancel last turn", relief=RAISED)
            self.Function_panel.create_window(1.25 * self.CASE_WIDTH, 6.5 * self.CASE_WIDTH, window=cancel)
        if winner == "draw" or winner == "human" or winner == "AI":
            self.show_victory(winner)

    def show_moving_list(self):
        self.Function_panel.shadows = []
        self.Function_panel.delete("all")
        pieces = "PNBRQ"
        names = ["pawn", "knight", "bishop", "rook", "queen"]

        if not self.move_list:
            return None
        x = 11
        for i in range(len(self.move_list) - 1, len(self.move_list) - 13, -1):
            if i < 0:
                break
            # output the algebraic notation of the moves
            self.Function_panel.create_text(0.125*self.CASE_WIDTH, (2+0.333*x)*self.CASE_WIDTH+10, text=str(i+1), font="Arial 11")
            self.Function_panel.create_text(0.75 * self.CASE_WIDTH, (2+0.333*x)*self.CASE_WIDTH+10,
                                            text=self.move_list[i][0], font="Arial 13")
            if len(self.move_list[i]) == 4:
                self.Function_panel.create_text(1.75 * self.CASE_WIDTH, (2 + 0.333*x) * self.CASE_WIDTH + 10,
                                                text=self.move_list[i][2], font="Arial 13")
            x -= 1

        # create the border and the button
        self.Function_panel.create_rectangle(0.25 * self.CASE_WIDTH, 2 * self.CASE_WIDTH - 7,
                                             2.25 * self.CASE_WIDTH, 6 * self.CASE_WIDTH + 3, fill="", width=2)
        self.Function_panel.create_text(1.25 * self.CASE_WIDTH, 1.75 * self.CASE_WIDTH,
                                        text="WHITE      BLACK", font="Arial 12 bold")

        for i in range(len(AI_player.pieces_lost)):
            a = AI_player.pieces_lost[i].upper()
            piece_to_draw = PhotoImage(file=names[pieces.index(a)] + " shadow.png")
            if i<=7:
                self.Function_panel.create_image(0.2*self.CASE_WIDTH+0.3*i*self.CASE_WIDTH, 7.25*self.CASE_WIDTH, image=piece_to_draw)
            else:
                self.Function_panel.create_image(0.2*self.CASE_WIDTH+0.3*i*self.CASE_WIDTH, 7.75*self.CASE_WIDTH, image=piece_to_draw)
            self.Function_panel.shadows.append(piece_to_draw)

        for i in range(len(human_player.pieces_lost)):
            a = human_player.pieces_lost[i].upper()
            piece_to_draw = PhotoImage(file=names[pieces.index(a)] + " shadow.png")
            if i<=7:
                self.Function_panel.create_image(0.2 * self.CASE_WIDTH + 0.3 * i * self.CASE_WIDTH, self.CASE_WIDTH, image=piece_to_draw)
            else:
                self.Function_panel.create_image(0.2 * self.CASE_WIDTH + 0.3 * i * self.CASE_WIDTH, 1.5*self.CASE_WIDTH, image=piece_to_draw)

            self.Function_panel.shadows.append(piece_to_draw)

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
            Pieces.pieces_list = self.move_list[-1][restore_index]
            self.update(Pieces.pieces_list)
            self.show_moving_list()
            self.turn_counter -= 1
        except IndexError:
            self.turn_counter -= 1
            Pieces.pieces_list = "rnbqkbnrppppppppooooooooooooooooooooooooooooooooPPPPPPPPRNBQKBNR"
            self.update(Pieces.pieces_list)
            self.show_moving_list()
            self.turn_counter -= 1
        self.focus_rectangle = self.Board.create_rectangle(0, 0, 0, 0, fill="", width=4, outline="yellow")

    def show_progression(self, percentage):
        self.Board.create_rectangle(0, 0, percentage/100.0*8*self.CASE_WIDTH, 0.1*self.CASE_WIDTH, width=0, fill="#32FF32")
        self.Chess.update()


class Game:
    pieces_list = ""  # store every single piece

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

    CHESSBOARD_INDEXES = set(range(64))
    CHESSBOARD_LENGTH = set(range(8))

    pieces_name = ["black pawn", "black knight", "black bishop", "black rook", "black king", "black queen",
                   "white pawn", "white knight", "white bishop", "white rook", "white king", "white queen"]

    def __init__(self):
        if human_player.color == "white":
            self.pieces_list = "rnbqkbnrppppppppooooooooooooooooooooooooooooooooPPPPPPPPRNBQKBNR"
        else:
            self.pieces_list = "RNBKQBNRPPPPPPPPoooooooooooooooooooooooooooooooopppppppprnbkqbnr"


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
            self.self_pieces = "PNBRKQ"
            self.enemy_pieces = "pnbrkq"
        else:
            self.can_play = False
            self.self_pieces = "pnbrkq"
            self.enemy_pieces = "PNBRKQ "

        self.color = color
        self.mode = mode
        self.moves_ahead = moves_ahead
        self.max_moves_ahead = moves_ahead + 4
        self.max_reward = 1
        self.king_moved = self.left_rook_moved = self.right_rook_moved = False  # used to check if a player can castle
        self.pieces_lost = []

        if config is not None:
            self.VALUE_WEIGHT, self.MOBILITY_WEIGHT, self.PAWN_WEIGHT = config

    def get_position_of_king(self, chessboard):
        king = self.self_pieces[4]
        return chessboard.index(king)

    def get_list_possible_plays(self, chessboard, PseudoLegalMoves=False):

        list_possible_plays = ""

        kingPos = chessboard.index(self.self_pieces[4])
        # it appends the list of possible plays for each piece the player has
        for i in range(64):
            if chessboard[i] in self.self_pieces:
                possible_plays = self.get_list_plays_of_piece(i, chessboard, kingPos, PseudoLegalMoves)
                if possible_plays is not None:
                    list_possible_plays += possible_plays

        if list_possible_plays != "":
            return list_possible_plays
        else:
            return None

    def is_not_in_check(self, chessboard, oldPos, newPos, kingPos):

        piece = chessboard[oldPos]
        new_chessboard = chessboard[:oldPos] + "o" + chessboard[oldPos+1:]
        new_chessboard = new_chessboard[:newPos] + piece + new_chessboard[newPos+1:]

        if piece in "kK":  # if the piece is a king
            if not self.is_threatened(newPos, new_chessboard):
                return True
            else:
                return False

        if not self.is_threatened(kingPos, new_chessboard):
            return True
        else:
            return False

    def get_list_plays_of_piece(self, Pos, chessboard, kingPos, PseudoLegalMoves):

        # stores first the name of the piece
        list_play_of_piece = chessboard[Pos] + str(Pos) + "|"

        piece = chessboard[Pos]
        oldPos = Pos
        oldX = oldPos % 8
        oldY = int(oldPos/8)
        step = -1 if self.color == human_player.color else 1

        if piece in "pP":

            newPos = oldPos + step*8
            # the following lines verify if the pawn can be moved right
            # ahead
            if chessboard[newPos] == "o" and (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                list_play_of_piece += str(newPos) + "/"

            # if the pawn has never moved and can move 2 cases right
            # ahead
            if ((oldY == 6 and step == -1) or (oldY == 1 and step == 1)) and \
                    chessboard[oldPos + step*16] == "o" and chessboard[newPos] == "o" and \
                    (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, oldPos+step*16, kingPos)):
                list_play_of_piece += str(oldPos+step*16) + "/"

            # the following lines verify if the pawn can attack
            for newX in [oldX-1, oldX+1]:
                newPos = (oldY + step)*8 + newX
                if newX in Pieces.CHESSBOARD_LENGTH and chessboard[newPos] != "o" and \
                        chessboard[newPos] not in self.self_pieces and (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                    list_play_of_piece += str(newPos) + "/"
                ####################################################################

        elif piece in "rR":

            for newPos in range(oldPos + 8, 64, 8):
                # if there is nothing or an enemy on the cases at the bottom of
                # the piece
                if chessboard[newPos] not in self.self_pieces and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                    list_play_of_piece += str(newPos) + "/"
                if chessboard[newPos] != "o":
                    break

            for newPos in range(oldPos - 8, -1, -8):
                # if there is nothing or an enemy on the cases at the right of
                # the top
                if chessboard[newPos] not in self.self_pieces and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                    list_play_of_piece += str(newPos) + "/"
                if chessboard[newPos] != "o":
                    break

            for newPos in range(oldPos-1, int(oldPos/8)*8-1, -1):
                # if there is nothing or an enemy on the cases at the left of
                # the piece
                if chessboard[newPos] not in self.self_pieces and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                    list_play_of_piece += str(newPos) + "/"
                if chessboard[newPos] != "o":
                    break

            for newPos in range(oldPos+1, (int(oldPos/8)+1)*8):
                # if there is nothing or an enemy on the cases at the right of
                # the piece
                if chessboard[newPos] not in self.self_pieces and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                    list_play_of_piece += str(newPos) + "/"
                if chessboard[newPos] != "o":
                    break

                    #######################################################

        elif piece in "nN":
            moving = {-6, -15, -17, -10, 6, 15, 17, 10}
            for move in moving:
                newPos = oldPos + move
                if newPos in Pieces.CHESSBOARD_INDEXES and newPos%8-oldPos%8 in {-2, -1, 1, 2} and chessboard[newPos] not in self.self_pieces and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                    list_play_of_piece += str(newPos) + "/"

                    #######################################################

        elif piece in "bB":
            oldX = oldPos%8
            oldY = int(oldPos/8)
            for a, b in product([-1, 1], repeat=2):
                for i in range(1, 8):
                    newX = oldX + a*i
                    newY = oldY + b*i
                    newPos = newY*8 + newX
                    if newX not in Pieces.CHESSBOARD_LENGTH or newY not in Pieces.CHESSBOARD_LENGTH:
                        break
                    if chessboard[newPos] not in self.self_pieces and \
                            (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                        list_play_of_piece += str(newPos) + "/"
                    if chessboard[newPos] != "o":
                        break

                ###########################################################

        elif piece in "qQ":
            for newPos in range(oldPos + 8, 64, 8):
                # if there is nothing or an enemy on the cases at the bottom of
                # the piece
                if chessboard[newPos] not in self.self_pieces and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                    list_play_of_piece += str(newPos) + "/"
                if chessboard[newPos] != "o":
                    break

            for newPos in range(oldPos - 8, -1, -8):
                # if there is nothing or an enemy on the cases at the right of
                # the top
                if chessboard[newPos] not in self.self_pieces and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                    list_play_of_piece += str(newPos) + "/"
                if chessboard[newPos] != "o":
                    break

            for newPos in range(oldPos - 1, int(oldPos / 8) * 8-1, -1):
                # if there is nothing or an enemy on the cases at the left of
                # the piece
                if chessboard[newPos] not in self.self_pieces and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                    list_play_of_piece += str(newPos) + "/"
                if chessboard[newPos] != "o":
                    break

            for newPos in range(oldPos + 1, (int(oldPos / 8) + 1) * 8):
                # if there is nothing or an enemy on the cases at the right of
                # the piece
                if chessboard[newPos] not in self.self_pieces and \
                        (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                    list_play_of_piece += str(newPos) + "/"
                if chessboard[newPos] != "o":
                    break

            oldX = oldPos%8
            oldY = int(oldPos/8)
            for a, b in product([-1, 1], repeat=2):
                for i in range(1, 8):
                    newX = oldX + a*i
                    newY = oldY + b*i
                    newPos = newY*8 + newX
                    if newX not in Pieces.CHESSBOARD_LENGTH or newY not in Pieces.CHESSBOARD_LENGTH:
                        break
                    if chessboard[newPos] not in self.self_pieces and \
                            (PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos)):
                        list_play_of_piece += str(newPos) + "/"
                    if chessboard[newPos] != "o":
                        break

            ###############################################################

        elif piece in "kK":
            for a in range(-1, 2):
                for b in range(-1, 2):
                    newX = oldX + a
                    newY = oldY + b
                    newPos = newY*8 + newX
                    if abs(a) + abs(b) != 0 and newX in Pieces.CHESSBOARD_LENGTH and newY in Pieces.CHESSBOARD_LENGTH and \
                            chessboard[newPos] not in self.self_pieces:
                        # check if the coordinates a and b of the movement of the
                        # king are good and if the targeted case is no occupied by
                        # an allied piece

                        if PseudoLegalMoves or self.is_not_in_check(chessboard, oldPos, newPos, kingPos):
                            list_play_of_piece += str(newPos) + "/"

            # check if the king can castle

            # if the position of the king hasn't changed
            if not self.king_moved and (oldX == 3 or oldX == 4) and not self.is_threatened(oldPos, chessboard):

                if not self.left_rook_moved and chessboard[oldY*8] == self.self_pieces[3]:
                    for i in range(oldPos-1, oldPos-3, -1):
                        # check the left castling
                        if chessboard[i] != "o" or self.is_threatened(i, chessboard):
                            break
                    else:
                        if chessboard[oldY*8+1] == "o":
                            newPos = oldY*8 + oldX - 2
                            list_play_of_piece += str(newPos) + "/"

                if not self.right_rook_moved and chessboard[oldY*8+7] == self.self_pieces[3]:
                    for i in range(oldPos+1, oldPos+3):
                        # check the right castling
                        if chessboard[i] != "o" or self.is_threatened(i, chessboard):
                            break
                    else:
                        if chessboard[oldY*8+6] == "o":
                            newPos = oldY*8 + oldX + 2
                            list_play_of_piece += str(newPos) + "/"

        # if the list is not composed of just the name of the piece and its coordinate
        if list_play_of_piece != chessboard[Pos] + str(Pos) + "|":
            return list_play_of_piece
        else:
            return None

    def is_threatened(self, case, chessboard):
        step = -1 if self.color == human_player.color else 1

        caseX = case % 8
        caseY = int(case/8)

        # first of all verify if a pawn is threatening the case

        if case+step*7 in Pieces.CHESSBOARD_INDEXES and int(case/8) != int((case+step*7)/8) and chessboard[case+step*7] == self.enemy_pieces[0]:
            return True
        if case+step*9 in Pieces.CHESSBOARD_INDEXES and abs(int(case/8) - int((case+step*9)/8)) == 1 and chessboard[case+step*9] == self.enemy_pieces[0]:
            return True

        # then verify if a king is threatening the case

        moving = [[0, 1],[0, -1],[1, 1],[1, 0],[1, -1],[-1, -1],[-1, 0],[-1, 1]]
        for x, y in moving:
            if caseX+x in Pieces.CHESSBOARD_LENGTH and caseY+y in Pieces.CHESSBOARD_LENGTH:
                if chessboard[(caseY+y)*8 + caseX+x] == self.enemy_pieces[4]:
                    return True

        # then verify if a knight is threatening the piece

        moving = [[1, 2],[1, -2],[-1, 2],[-1, -2],[2, 1],[2, -1],[-2, 1],[-2, -1]]
        for x, y in moving:
            if caseX+x in Pieces.CHESSBOARD_LENGTH and caseY+y in Pieces.CHESSBOARD_LENGTH:
                if chessboard[(caseY+y)*8 + caseX+x] == self.enemy_pieces[1]:
                    return True

        # then verify the sliding pieces

        for newCase in range(case+8, 64, 8):
            if chessboard[newCase] in {self.enemy_pieces[5], self.enemy_pieces[3]}:
                return True
            if chessboard[newCase] != "o":
                break

        for newCase in range(case-8, -1, -8):
            if chessboard[newCase] in {self.enemy_pieces[5], self.enemy_pieces[3]}:
                return True
            if chessboard[newCase] != "o":
                break

        for newCase in range(case+1, (int(case/8)+1)*8):
            if chessboard[newCase] in {self.enemy_pieces[5], self.enemy_pieces[3]}:
                return True
            if chessboard[newCase] != "o":
                break

        for newCase in range(case-1, (int(case/8))*8-1, -1):
            if chessboard[newCase] in {self.enemy_pieces[5], self.enemy_pieces[3]}:
                return True
            if chessboard[newCase] != "o":
                break

        ###################################

        for a, b in product([-1, 1], repeat=2):
            for i in range(1, 8):
                newX = caseX + a*i
                newY = caseY + b*i
                newCase = newY*8 + newX
                if newX not in Pieces.CHESSBOARD_LENGTH or newY not in Pieces.CHESSBOARD_LENGTH:
                    break
                if chessboard[newCase] in {self.enemy_pieces[2], self.enemy_pieces[5]}:
                    return True
                if chessboard[newCase] != "o":
                    break

        return False

    def move_piece(self, oldPos, newPos, chessboard):
        piece_to_move = chessboard[oldPos]
        piece_taken = True if chessboard[newPos] != 'o' else False
        ally_queen = self.self_pieces[5]
        ally_rook = self.self_pieces[3]

        if piece_to_move in "pP" and int(newPos/8) in {0, 7}:  # if the piece is a pawn which reached its last line
            chessboard = chessboard[:newPos] + ally_queen + chessboard[newPos+1:]
        elif piece_to_move in "kK" and newPos-oldPos in {2,-2}:  # if the king want to castle
            rook_step = int((oldPos-newPos)/2)
            rookPos = int(oldPos/8)*8 if rook_step == 1 else int(oldPos/8)*8+7
            chessboard = chessboard[:newPos] + piece_to_move + chessboard[newPos+1:]  # move the king
            chessboard = chessboard[:newPos+rook_step] + ally_rook + chessboard[newPos+rook_step+1:]  # move the rook
            chessboard = chessboard[:oldPos] + "o" + chessboard[oldPos+1:]  # remove the old king
            chessboard = chessboard[:rookPos] + "o" + chessboard[rookPos+1:]  # remove the old rook
            return [chessboard, piece_taken]
        else:
            chessboard = chessboard[:newPos] + piece_to_move + chessboard[newPos+1:]

        chessboard = chessboard[:oldPos] + "o" + chessboard[oldPos+1:]

        return [chessboard, piece_taken]

    def get_mobility(self, chessboard, enemy_possible_plays, debug=False):
        enemy_attack_table = self.get_attack_table(enemy_possible_plays)
        bonus_index = 0 if myView.game_state == "start/mid-game" else 1

        if self.color == AI_player.color:
            excluded_ranks = {1, 2}
            enemy_pawn_step = 1
        else:
            excluded_ranks = {5, 6}
            enemy_pawn_step = -1
        excluded_mobility_area = ""
        # first defines the mobility area by excluding some squares :
        #  those occupied by pawns on ranks 2 & 3, or the queen, or the king, or defended by an ennemy pawn
        for pos in Pieces.CHESSBOARD_INDEXES:
            x = pos % 8
            y = int(pos/8)
            if chessboard[pos] == self.self_pieces[0] and y in excluded_ranks:  # self_pieces[0] means self pawn
                excluded_mobility_area += "/" + str(pos) + "/"
                continue
            elif chessboard[pos] == self.self_pieces[4] or chessboard[pos] == self.self_pieces[5]:  # queen or king
                excluded_mobility_area += "/" + str(pos) + "/"
                continue
            elif (x+1 in Pieces.CHESSBOARD_LENGTH and y+enemy_pawn_step in Pieces.CHESSBOARD_LENGTH and chessboard[(y+enemy_pawn_step)*8+x+1] == self.enemy_pieces[0]) \
                    or (x-1 in Pieces.CHESSBOARD_LENGTH and y+enemy_pawn_step in Pieces.CHESSBOARD_LENGTH and chessboard[(y+enemy_pawn_step)*8+x-1] == self.enemy_pieces[0]):  # enemy pawns
                excluded_mobility_area += "/" + str(pos) + "/"
                continue
        queen_mobility = bishops_mobility = knights_mobility = rooks_mobility = 0

        for pos in Pieces.CHESSBOARD_INDEXES:
            if chessboard[pos] == "o":
                continue
            else:
                piece = chessboard[pos]
                oldPos = pos

            if piece in self.self_pieces:
                if piece == self.self_pieces[0] or piece == self.self_pieces[4]:  # if it's a pawn or king
                    continue
                elif piece in "qQ":
                    queen_mobility_score = 0
                    for newPos in range(oldPos+8, 64, 8):
                        A = self.enemy_pieces[3] in enemy_attack_table[newPos] \
                                or self.enemy_pieces[1] in enemy_attack_table[newPos] \
                                or self.enemy_pieces[2] in enemy_attack_table[newPos]  # A : the case is attacked by an ennemy piece
                        B = chessboard[newPos] in self.self_pieces  # B : the piece on the case is ours
                        C = chessboard[newPos] in self.enemy_pieces  # C : the piece on the case is enemy's one
                        D = "/" + str(newPos) + "/" in excluded_mobility_area  # D : the case is in excluded mobility area
                        if (A and not B and not C and not D) or (not A and not B and not C and D):  # if only A or only D
                            continue
                        elif (not A and B and not C and not D) or (not A and not B and C and not D):  # if only B or only C
                            queen_mobility_score += 1
                        elif not A and not B and not C and not D:
                            queen_mobility_score += 1
                            continue
                        break

                    for newPos in range(oldPos-8, -1, -8):
                        A = self.enemy_pieces[3] in enemy_attack_table[newPos] \
                                or self.enemy_pieces[1] in enemy_attack_table[newPos] \
                                or self.enemy_pieces[2] in enemy_attack_table[newPos]  # A : the case is attacked by an ennemy piece
                        B = chessboard[newPos] in self.self_pieces  # B : the piece on the case is ours
                        C = chessboard[newPos] in self.enemy_pieces  # C : the piece on the case is enemy's one
                        D = "/" + str(newPos) + "/" in excluded_mobility_area  # D : the case is in excluded mobility area
                        if (A and not B and not C and not D) or (not A and not B and not C and D):  # if only A or only D
                            continue
                        elif (not A and B and not C and not D) or (not A and not B and C and not D):  # if only B or only C
                            queen_mobility_score += 1
                        elif not A and not B and not C and not D:
                            queen_mobility_score += 1
                            continue
                        break

                    for newPos in range(oldPos-1, int(oldPos/8)*8-1, -1):
                        A = self.enemy_pieces[3] in enemy_attack_table[newPos] \
                                or self.enemy_pieces[1] in enemy_attack_table[newPos] \
                                or self.enemy_pieces[2] in enemy_attack_table[newPos]  # A : the case is attacked by an ennemy piece
                        B = chessboard[newPos] in self.self_pieces  # B : the piece on the case is ours
                        C = chessboard[newPos] in self.enemy_pieces  # C : the piece on the case is enemy's one
                        D = "/" + str(newPos) + "/" in excluded_mobility_area  # D : the case is in excluded mobility area
                        if (A and not B and not C and not D) or (not A and not B and not C and D):  # if only A or only D
                            continue
                        elif (not A and B and not C and not D) or (not A and not B and C and not D):  # if only B or only C
                            queen_mobility_score += 1
                        elif not A and not B and not C and not D:
                            queen_mobility_score += 1
                            continue
                        break

                    for newPos in range(oldPos+1, (int(oldPos/8)+1)*8):
                        A = self.enemy_pieces[3] in enemy_attack_table[newPos] \
                                or self.enemy_pieces[1] in enemy_attack_table[newPos] \
                                or self.enemy_pieces[2] in enemy_attack_table[newPos]  # A : the case is attacked by an ennemy piece
                        B = chessboard[newPos] in self.self_pieces  # B : the piece on the case is ours
                        C = chessboard[newPos] in self.enemy_pieces  # C : the piece on the case is enemy's one
                        D = "/" + str(newPos) + "/" in excluded_mobility_area  # D : the case is in excluded mobility area
                        if (A and not B and not C and not D) or (not A and not B and not C and D):  # if only A or only D
                            continue
                        elif (not A and B and not C and not D) or (not A and not B and C and not D):  # if only B or only C
                            queen_mobility_score += 1
                        elif not A and not B and not C and not D:
                            queen_mobility_score += 1
                            continue
                        break

                    oldX = oldPos % 8
                    oldY = int(oldPos / 8)
                    for a, b in product([-1, 1], repeat=2):
                        for i in range(1, 8):
                            newX = oldX + a * i
                            newY = oldY + b * i
                            newPos = newY * 8 + newX
                            if newX not in Pieces.CHESSBOARD_LENGTH or newY not in Pieces.CHESSBOARD_LENGTH:
                                break
                            A = self.enemy_pieces[3] in enemy_attack_table[newPos] \
                                    or self.enemy_pieces[1] in enemy_attack_table[newPos] \
                                    or self.enemy_pieces[2] in enemy_attack_table[newPos]  # A : the case is attacked by an ennemy piece
                            B = chessboard[newPos] in self.self_pieces  # B : the piece on the case is ours
                            C = chessboard[newPos] in self.enemy_pieces  # C : the piece on the case is enemy's one
                            D = "/" + str(newPos) + "/" in excluded_mobility_area  # D : the case is in excluded mobility area
                            if (A and not B and not C and not D) or (not A and not B and not C and D):  # if only A or only D
                                continue
                            elif (not A and B and not C and not D) or (not A and not B and C and not D):  # if only B or only C
                                queen_mobility_score += 1
                            elif not A and not B and not C and not D:
                                queen_mobility_score += 1
                                continue
                            break
                    queen_mobility += Pieces.MOBILITY_BONUS[3][queen_mobility_score][bonus_index]

                elif piece in "rR":
                    look_through = {"o", self.self_pieces[3], self.self_pieces[5]}
                    rook_mobility_score = 0

                    for newPos in range(oldPos+8, 64, 8):
                        A = chessboard[newPos] in look_through  # A : can look through
                        B = chessboard[newPos] in self.self_pieces  # B : the piece on the case is ours
                        C = "/" + str(newPos) + "/" in excluded_mobility_area  # C : the case is in excluded mobility area
                        if A and not C:
                            rook_mobility_score += 1
                            continue
                        elif B and not A and not C:
                            rook_mobility_score += 1
                        elif A and C:
                            continue
                        break

                    for newPos in range(oldPos - 8, -1, -8):
                        A = chessboard[newPos] in look_through  # A : can look through
                        B = chessboard[newPos] in self.self_pieces  # B : the piece on the case is ours
                        C = "/" + str(newPos) + "/" in excluded_mobility_area  # C : the case is in excluded mobility area
                        if A and not C:
                            rook_mobility_score += 1
                            continue
                        elif B and not A and not C:
                            rook_mobility_score += 1
                        elif A and C:
                            continue
                        break

                    for newPos in range(oldPos + 1, (int(oldPos/8)+1)*8):
                        A = chessboard[newPos] in look_through  # A : can look through
                        B = chessboard[newPos] in self.self_pieces  # B : the piece on the case is ours
                        C = "/" + str(newPos) + "/" in excluded_mobility_area  # C : the case is in excluded mobility area
                        if debug:
                            print(A, B, C, newPos)
                        if A and not C:
                            rook_mobility_score += 1
                            continue
                        elif B and not A and not C:
                            rook_mobility_score += 1
                        elif A and C:
                            continue
                        break

                    for newPos in range(oldPos - 1, int(oldPos/8)*8-1, -1):
                        A = chessboard[newPos] in look_through  # A : can look through
                        B = chessboard[newPos] in self.self_pieces  # B : the piece on the case is ours
                        C = "/" + str(newPos) + "/" in excluded_mobility_area  # C : the case is in excluded mobility area
                        if A and not C:
                            rook_mobility_score += 1
                            continue
                        elif B and not A and not C:
                            rook_mobility_score += 1
                        elif A and C:
                            continue
                        break
                    if debug:
                        print("rooks mobility score {}".format(rook_mobility_score), excluded_mobility_area)
                    rooks_mobility += Pieces.MOBILITY_BONUS[2][rook_mobility_score][bonus_index]

                elif piece in "bB":
                    look_through = {"o", self.self_pieces[2], self.self_pieces[5]}
                    bishop_mobility_score = 0

                    oldX = oldPos % 8
                    oldY = int(oldPos / 8)
                    for a, b in product([-1, 1], repeat=2):
                        for i in range(1, 8):
                            newX = oldX + a * i
                            newY = oldY + b * i
                            newPos = newY * 8 + newX
                            if newX not in Pieces.CHESSBOARD_LENGTH or newY not in Pieces.CHESSBOARD_LENGTH:
                                break
                            A = chessboard[newPos] in look_through  # A : the bishop can look through the case
                            B = chessboard[newPos] in self.self_pieces  # B : the piece on the case is ours
                            C = "/" + str(newPos) + "/" in excluded_mobility_area  # C : the case is in excluded mobility area
                            if A and not C:
                                bishop_mobility_score += 1
                                continue
                            elif not A and B and not C:
                                bishop_mobility_score += 1
                            elif A and C:
                                continue
                            break
                    bishops_mobility += Pieces.MOBILITY_BONUS[1][bishop_mobility_score][bonus_index]

                elif piece in "nN":
                    knight_mobility_score = 0

                    moving = {-6, -15, -17, -10, 6, 15, 17, 10}
                    for move in moving:
                        newPos = oldPos + move
                        if newPos in Pieces.CHESSBOARD_INDEXES and newPos%8-oldPos%8 in {-2, -1, 1, 2}:
                            if "/" + str(newPos) + "/" in excluded_mobility_area:
                                continue
                            elif not chessboard[newPos] in self.enemy_pieces:
                                knight_mobility_score += 1
                    knights_mobility += Pieces.MOBILITY_BONUS[0][knight_mobility_score][bonus_index]

        mobility = knights_mobility + bishops_mobility + rooks_mobility + queen_mobility
        if debug:
            print("knights {} rooks {} bishops {} queen {}".format(knights_mobility, rooks_mobility, bishops_mobility, queen_mobility))
        return mobility

    @staticmethod
    def get_attack_table(possible_plays):
        allPieces = "pbnrkqPBNRKQ"
        attack_table = ["" for i in range(64)]
        if not possible_plays:
            return attack_table
        else:
            piece = possible_plays[0]
        attackPos = ""
        pos = True
        for attack in possible_plays:
            if attack in allPieces:
                piece = attack
                pos = True
                continue
            if attack == "|":
                pos = False
                continue
            elif pos:
                continue
            if attack == "/":
                attackPos = int(attackPos)
                attack_table[attackPos] += piece
                attackPos = ""
            else:
                attackPos += attack
        return attack_table

    def get_pawn_reward(self, chessboard):
        reward = cases_bf_passing = 0
        if self.color == human_player.color:
            step = -1
            board_edge = -1
        else:
            step = 1
            board_edge = 8
        if myView.game_state == "start/mid-game":
            pawn_chains = []
            average_chain_length = 0
            passing_pawn_reward = 0
            total_chains = 0
            for y in range(board_edge-step*8, board_edge, step):
                for x in Pieces.CHESSBOARD_LENGTH:
                    if chessboard[y*8+x] == self.self_pieces[0]:
                        for i in range(y, board_edge, step):
                            if chessboard[i*8+x] == self.enemy_pieces[0]:
                                break
                        else:
                            cases_bf_passing += abs(board_edge-1-y)  # those lines are executed only if the for loop was not broken
                            passing_pawn_reward += 1/cases_bf_passing
                        if [x, y] not in pawn_chains:
                            pawn_chains.append([x, y])
                            pawn_chains.append(1)
                            for direction in [1, -1]:
                                for i in range(1, 8):
                                    newX = x+i*direction
                                    newY = y+i*step
                                    if newX not in Pieces.CHESSBOARD_LENGTH or newY not in Pieces.CHESSBOARD_LENGTH:
                                        break
                                    elif chessboard[newY*8+newX] != self.self_pieces[0]:
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
            for x in Pieces.CHESSBOARD_LENGTH:
                for y in Pieces.CHESSBOARD_LENGTH:
                    if chessboard[y*8+x] == self.self_pieces[0]:
                        for i in range(y, board_edge, step):
                            if chessboard[i*8+x] == self.enemy_pieces[0]:
                                break
                        else:
                            cases_bf_passing += abs(board_edge-1-y)
                            reward += 1/cases_bf_passing
            reward = reward/8.0  # to ensure it's a value btw 0 and 1
        return reward


class Engine(Player):

    def play_move(self, chessboard):

        possible_plays = self.get_list_possible_plays(chessboard)
        kingPos = self.get_position_of_king(chessboard)
        event = "nothing"

        if not possible_plays:
            if self.is_threatened(kingPos, chessboard):
                myView.show_victory("human")
                return [None, None]
            else:
                myView.show_victory("draw")
                return [None, None]

        oldPos, newPos = self.choose_index(chessboard, possible_plays)

        old_target_case = chessboard[newPos]
        new_chessboard, piece_taken = self.move_piece(oldPos, newPos, chessboard)
        piece = new_chessboard[newPos]

        if piece in "rR":
            if int(oldPos/8) == 0:
                self.left_rook_moved = True
            elif int(oldPos/8) == 7:
                self.right_rook_moved = True
        elif piece in "kK":
            self.king_moved = True
        elif piece in "pP":
            piece_taken = True

        human_kingPos = human_player.get_position_of_king(new_chessboard)

        self.can_play = False
        human_player.can_play = True

        if human_player.is_threatened(human_kingPos, new_chessboard):
            event = "check"
        if not human_player.get_list_possible_plays(new_chessboard):

            if human_player.is_threatened(human_kingPos, new_chessboard):
                event = "AI"
                piece_taken = None
            else:
                event = "draw"
                piece_taken = None

        elif myView.moves_without_take >= 50:
            event = "draw"
            piece_taken = None

        if old_target_case != "o":
            human_player.pieces_lost.append(old_target_case)

        myView.algebraic_notation(piece, oldPos, newPos, old_target_case, event, new_chessboard)

        return [piece_taken, new_chessboard]

    def choose_index(self, chessboard, possible_plays):

        list_best_moves = self.minimax(possible_plays, self.moves_ahead, self.max_moves_ahead, True,
                                       -self.max_reward, self.max_reward,
                                       chessboard)

        # finally return the coordinates of the play to make in the list of possible plays
        if len(list_best_moves) == 1:

            return list_best_moves[0]
        else:
            rand = random.randint(0, len(list_best_moves) - 1)
            return list_best_moves[rand]

    def minimax(self, possible_plays, depth, max_depth, maximizingPlayer, alpha, beta, chessboard):
        # https://fr.wikipedia.org/wiki/Algorithme_minimax

        if depth == 0:
            self_possible_plays = self.get_list_possible_plays(chessboard, True)
            enemy_possible_plays = human_player.get_list_possible_plays(chessboard, True)

            self_mobility = self.get_mobility(chessboard, enemy_possible_plays)
            human_mobility = human_player.get_mobility(chessboard, self_possible_plays)
            return self.reward(chessboard, self_mobility - human_mobility)

        if maximizingPlayer:  # AI
            all_pieces = "pnbrkqPNBRKQ"
            pos = True
            oldPos = newPos = ""
            best_plays = []
            value = -self.max_reward
            human_kingPos = human_player.get_position_of_king(chessboard)
            i = 0

            for a in possible_plays:
                i += 1
                if a in all_pieces:
                    pos = True
                    oldPos = ""
                    continue
                if a == "|":
                    oldPos = int(oldPos)
                    pos = False
                    continue
                if pos:
                    oldPos += a
                    continue
                if a == "/":
                    if depth == self.moves_ahead:
                        myView.show_progression(int(100.0*i/len(possible_plays)))
                    newPos = int(newPos)

                    new_chessboard, piece_taken = self.move_piece(oldPos, newPos, chessboard)
                    enemy_possible_plays = human_player.get_list_possible_plays(new_chessboard)

                    if not enemy_possible_plays:
                        if human_player.is_threatened(human_kingPos, new_chessboard):
                            if depth == self.moves_ahead:
                                return [[oldPos, newPos]]
                            else:
                                return self.max_reward
                        else:  # in case of draw
                            if depth == self.moves_ahead:
                                value_test = 0
                            else:
                                return 0
                    else:
                        check = True if human_player.is_threatened(human_kingPos, new_chessboard) else False
                        if ((piece_taken and depth == 1) or (check and max_depth >= 3)) and max_depth >= 0:
                            value_test = self.minimax(enemy_possible_plays, depth, max_depth - 1, False, alpha, beta,
                                                      new_chessboard)
                        else:
                            value_test = self.minimax(enemy_possible_plays, depth - 1, max_depth - 1, False, alpha,
                                                      beta, new_chessboard)

                    if value_test > value:
                        value = value_test
                        if depth == self.moves_ahead:
                            best_plays = [[oldPos, newPos]]

                    elif value_test == value and depth == self.moves_ahead:
                        best_plays.append([oldPos, newPos])
                    if depth != self.moves_ahead:
                        alpha = max(alpha, value)
                        if alpha >= beta:
                            return value

                    newPos = ""
                    continue
                else:
                    newPos += a
                    continue

            if depth == self.moves_ahead:
                return best_plays
            else:
                return value

        else:  # minimizingPlayer
            all_pieces = "pnbrkqPNBRKQ"
            pos = True
            oldPos = newPos = ""
            value = self.max_reward
            kingPos = self.get_position_of_king(chessboard)
            for a in possible_plays:
                if a in all_pieces:
                    pos = True
                    oldPos = ""
                    continue
                if a == "|":
                    oldPos = int(oldPos)
                    pos = False
                    continue
                if pos:
                    oldPos += a
                    continue
                if a == "/":
                    newPos = int(newPos)

                    new_chessboard, piece_taken = human_player.move_piece(oldPos, newPos, chessboard)
                    enemy_possible_plays = self.get_list_possible_plays(new_chessboard)

                    if not enemy_possible_plays:
                        if self.is_threatened(kingPos, new_chessboard):
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

                    newPos = ""
                    continue
                else:
                    newPos += a
                    continue

            return value

    def reward(self, chessboard, mobility):

        value_reward = reward = 0.0

        if self.mode == "value":
            for piece in chessboard:

                if piece == "o":
                    continue
                if piece == self.self_pieces[5]:
                    reward += Pieces.QUEEN_VALUE
                elif piece == self.self_pieces[3]:
                    reward += Pieces.ROOK_VALUE
                elif piece == self.self_pieces[2]:
                    reward += Pieces.BISHOP_VALUE
                elif piece == self.self_pieces[1]:
                    reward += Pieces.KNIGHT_VALUE
                elif piece == self.self_pieces[0]:
                    reward += Pieces.PAWN_VALUE

                if piece == self.enemy_pieces[5]:
                    reward -= Pieces.QUEEN_VALUE
                elif piece == self.enemy_pieces[3]:
                    reward -= Pieces.ROOK_VALUE
                elif piece == self.enemy_pieces[2]:
                    reward -= Pieces.BISHOP_VALUE
                elif piece == self.enemy_pieces[1]:
                    reward -= Pieces.KNIGHT_VALUE
                elif piece == self.enemy_pieces[0]:
                    reward -= Pieces.PAWN_VALUE
            myView.calc_counter += 1

            return round(reward / 40.06, 3)
        elif self.mode == "AI":
            for piece in chessboard:

                if piece == "o":
                    continue
                if piece == self.self_pieces[5]:
                    value_reward += Pieces.QUEEN_VALUE
                elif piece == self.self_pieces[3]:
                    value_reward += Pieces.ROOK_VALUE
                elif piece == self.self_pieces[2]:
                    value_reward += Pieces.BISHOP_VALUE
                elif piece == self.self_pieces[1]:
                    value_reward += Pieces.KNIGHT_VALUE
                elif piece == self.self_pieces[0]:
                    value_reward += Pieces.PAWN_VALUE

                if piece == self.enemy_pieces[5]:
                    value_reward -= Pieces.QUEEN_VALUE
                elif piece == self.enemy_pieces[3]:
                    value_reward -= Pieces.ROOK_VALUE
                elif piece == self.enemy_pieces[2]:
                    value_reward -= Pieces.BISHOP_VALUE
                elif piece == self.enemy_pieces[1]:
                    value_reward -= Pieces.KNIGHT_VALUE
                elif piece == self.enemy_pieces[0]:
                    value_reward -= Pieces.PAWN_VALUE

            pawn_reward = self.get_pawn_reward(chessboard)-human_player.get_pawn_reward(chessboard)
            value_reward = value_reward / 40.06  # so that it's a value btw -1 and 1
            mobility_reward = mobility / 814.0  # so that it's a value btw -1 and 1
            reward = round((value_reward*self.VALUE_WEIGHT + mobility_reward*self.MOBILITY_WEIGHT) + pawn_reward*self.PAWN_WEIGHT/
                           (self.VALUE_WEIGHT + self.MOBILITY_WEIGHT + self.PAWN_WEIGHT),
                           3)
            myView.calc_counter += 1
            return reward


class Human(Player):

    def play_move(self, piecePos):
        if self.is_a_right_piece and self.can_play:

            if self.oldPos == piecePos:
                self.is_a_right_place = False
                return [False, False, None]

            if self.list_of_plays_of_the_piece_to_move is not None:
                if str(piecePos) in self.list_of_plays_of_the_piece_to_move:
                    self.is_a_right_place = True

            if self.is_a_right_place:
                old_target_case = Pieces.pieces_list[piecePos]
                new_chessboard, piece_taken = self.move_piece(self.oldPos, piecePos, Pieces.pieces_list)
                piece = new_chessboard[piecePos]

                self.is_a_right_piece = False
                self.is_a_right_place = False

                if piece in "rR":
                    if self.oldPos%8 == 0:
                        self.left_rook_moved = True
                    elif self.oldPos%8 == 7:
                        self.right_rook_moved = True
                elif piece in "kK":
                    self.king_moved = True
                elif piece in "pP":
                    piece_taken = True

                self.can_play = False
                AI_player.can_play = True

                AI_kingPos = AI_player.get_position_of_king(new_chessboard)
                if not AI_player.get_list_possible_plays(new_chessboard):
                    if AI_player.is_threatened(AI_kingPos, new_chessboard):
                        event = "human"
                    else:
                        event = "draw"
                elif AI_player.is_threatened(AI_kingPos, new_chessboard):
                    event = "check"
                else:
                    event = ""

                if old_target_case != "o":
                    AI_player.pieces_lost.append(old_target_case)

                myView.algebraic_notation(piece, self.oldPos, piecePos, old_target_case, event, new_chessboard)

                return [True, piece_taken, new_chessboard]

            else:
                myView.update(Pieces.pieces_list)
                return [False, False, None]
        return [False, False, None]

    def start_move(self, mouseX, mouseY):

        # to take the x and y positions of the piece targeted by the mouse
        pieceX = int(mouseX / View.CASE_WIDTH)
        pieceY = int(mouseY / View.CASE_WIDTH)
        piecePos = pieceY*8+pieceX

        # to verify if the piece that the player is trying to move is the same
        # color as the player
        if Pieces.pieces_list[piecePos] in self.self_pieces and self.can_play:
            self.piece_to_move = Pieces.pieces_list[piecePos]
            self.oldPos = piecePos

            kingPos = self.get_position_of_king(Pieces.pieces_list)

            possible_plays = self.get_list_plays_of_piece(piecePos, Pieces.pieces_list, kingPos, False)

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
            piecePos = 8*pieceY+pieceX
            human_move = human_player.play_move(piecePos)

            if human_move[2] is not None:
                Pieces.pieces_list = str(human_move[2])

            if human_move[0]:  # if the human played
                if human_move[1]:  # if a piece was taken
                    myView.moves_without_take = 0
                else:
                    myView.moves_without_take += 1

                myView.calc_counter = 0
                start_time = time.time()
                piece_taken, Pieces.pieces_list = AI_player.play_move(Pieces.pieces_list)
                if piece_taken:  # if a piece was taken
                    myView.moves_without_take = 0
                else:
                    myView.moves_without_take += 1

                myView.turn_counter += 1
                myView.show_stats()
                moves_per_second = myView.calc_counter/(time.time() - start_time)
                print("moves per second", round(moves_per_second, 3))
                print(Pieces.pieces_list)
        myView.click_counter = 0
    myView.focus_rectangle = myView.Board.create_rectangle(0, 0, 0, 0, fill="", width=4, outline="yellow")


def onOverlap(event):
    x = int(event.x / View.CASE_WIDTH)
    y = int(event.y / View.CASE_WIDTH)
    if x < 8 and y < 8:
        myView.Board.coords(myView.focus_rectangle, x * myView.CASE_WIDTH + 2, y * myView.CASE_WIDTH + 2,
                            (x + 1) * myView.CASE_WIDTH - 2, (y + 1) * myView.CASE_WIDTH - 2)


Pieces = Game()
myView.update(Pieces.pieces_list)
myView.focus_rectangle = myView.Board.create_rectangle(0, 0, 0, 0, fill="", width=4, outline="yellow")

if AI_player.can_play:
    Pieces.pieces_list = str(AI_player.play_move(Pieces.pieces_list)[1])
    myView.turn_counter += 1
    myView.show_stats()
    myView.focus_rectangle = myView.Board.create_rectangle(0, 0, 0, 0, fill="", width=4, outline="yellow")

myView.Board.bind("<Button-1>", onClick)
myView.Board.bind("<Motion>", onOverlap)

myView.Chess.mainloop()
