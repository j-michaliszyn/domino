import random

class Domino:
    def __init__(self):
        self.dominoes = [(i, j) for i in range(7) for j in range(i, 7)]
        random.shuffle(self.dominoes)

    def deal(self):
        # Rozdajemy 7 kamieni dla dwóch graczy i resztę jako "talia do dobierania"
        self.player_hand = [self.dominoes.pop() for _ in range(7)]
        self.computer_hand = [self.dominoes.pop() for _ in range(7)]
        self.stock = self.dominoes
        self.board = []

    def play(self):
        self.deal()
        turn = "player"
        
        while True:
            print(f"Plansza: {self.board}")
            if turn == "player":
                self.player_turn()
                turn = "computer"
            else:
                self.computer_turn()
                turn = "player"
            
            # Sprawdzenie warunku zakończenia gry
            if not self.player_hand:
                print("Gracz wygrał!")
                break
            elif not self.computer_hand:
                print("Komputer wygrał!")
                break
            elif not self.stock and not self.can_move():
                print("Remis!")
                break

    def player_turn(self):
     print(f"Twoje kamienie: {self.player_hand}")
     valid_moves = [d for d in self.player_hand if self.is_valid_move(d)]

     if valid_moves:
        print(f"Możliwe ruchy: {valid_moves}")
        while True:
            try:
                move_index = int(input("Wybierz indeks kamienia do zagrania: "))
                if valid_moves[move_index] in valid_moves:
                    move = valid_moves[move_index]
                    break
                else:
                    print("Wybrany kamień nie jest dostępny. Spróbuj ponownie.")
            except (ValueError, IndexError):
                print("Nieprawidłowy wybór. Spróbuj ponownie.")
        self.make_move(move, "player")
     else:
        print("Brak możliwych ruchów. Dobierasz kamień.")
        self.draw_tile("player")    
    def computer_turn(self):
        valid_moves = [d for d in self.computer_hand if self.is_valid_move(d)]
        
        if valid_moves:
            move = random.choice(valid_moves)
            print(f"Komputer zagrywa: {move}")
            self.make_move(move, "computer")
        else:
            self.draw_tile("computer")

    def draw_tile(self, player):
        if self.stock:
            tile = self.stock.pop()
            if player == "player":
                self.player_hand.append(tile)
                print(f"Gracz dobiera kamień: {tile}")
            else:
                self.computer_hand.append(tile)
                print(f"Komputer dobiera kamień")

    def make_move(self, tile, player):
     # Jeśli plansza jest pusta, dodajemy kamień bez potrzeby obracania
     if not self.board:
        self.board.append(tile)
     else:
        left_end, right_end = self.board[0][0], self.board[-1][1]
        # Dopasowanie kamienia do prawej strony planszy
        if tile[0] == right_end:
            self.board.append(tile)
        elif tile[1] == right_end:
            self.board.append((tile[1], tile[0]))  # Obracamy kamień
        # Dopasowanie kamienia do lewej strony planszy
        elif tile[1] == left_end:
            self.board.insert(0, tile)
        elif tile[0] == left_end:
            self.board.insert(0, (tile[1], tile[0]))  # Obracamy kamień

     # Usunięcie kamienia z ręki gracza lub komputera
     if player == "player":
        self.player_hand.remove(tile)
     else:
        self.computer_hand.remove(tile)

    def is_valid_move(self, tile):
        # Sprawdzenie, czy kamień pasuje do jednego z końców planszy
        if not self.board:
            return True
        left_end, right_end = self.board[0][0], self.board[-1][1]
        return tile[0] == left_end or tile[1] == left_end or tile[0] == right_end or tile[1] == right_end

    def can_move(self):
        return any(self.is_valid_move(d) for d in self.player_hand + self.computer_hand)

game = Domino()
game.play()
