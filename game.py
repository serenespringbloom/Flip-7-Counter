import tkinter as tk
from tkinter import messagebox, simpledialog

class Player:
    def __init__(self, name):
        self.name = name
        self.total_points = 0
        self.round_points = 0
        self.cards_drawn = []
        self.special_cards = []
        self.stayed = False
        self.busted = False
        self.frozen = False
        self.is_active = True

class Flip7App:
    def __init__(self, root):
        self.root = root
        self.root.title("Flip 7 Game Assistant")

        self.players = []
        self.current_player_index = 0

        self.setup_frame = tk.Frame(root)
        self.setup_frame.pack()

        self.name_entries = []
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.setup_frame, text="Enter number of players:").pack()
        self.num_players_entry = tk.Entry(self.setup_frame)
        self.num_players_entry.pack()

        tk.Button(self.setup_frame, text="Next", command=self.get_player_names).pack()

    def get_player_names(self):
        try:
            num = int(self.num_players_entry.get())
            if num < 2:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid number (2 or more)")
            return

        for widget in self.setup_frame.winfo_children():
            widget.destroy()

        for i in range(num):
            tk.Label(self.setup_frame, text=f"Player {i + 1} Name:").pack()
            entry = tk.Entry(self.setup_frame)
            entry.pack()
            self.name_entries.append(entry)

        tk.Button(self.setup_frame, text="Start Game", command=self.start_game).pack()

    def start_game(self):
        for entry in self.name_entries:
            name = entry.get()
            if not name:
                messagebox.showerror("Missing Name", "All players must have names.")
                return
            self.players.append(Player(name))

        self.setup_frame.destroy()
        self.init_game_ui()

    def init_game_ui(self):
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        self.status_label = tk.Label(self.game_frame, text="", font=("Helvetica", 14, "bold"))
        self.status_label.pack(pady=10)

        self.scoreboard_frame = tk.Frame(self.game_frame)
        self.scoreboard_frame.pack()

        self.action_frame = tk.Frame(self.game_frame)
        self.action_frame.pack(pady=10)

        self.update_scoreboard()
        self.show_player_turn()

    def update_scoreboard(self):
        for widget in self.scoreboard_frame.winfo_children():
            widget.destroy()

        for player in self.players:
            frame = tk.LabelFrame(self.scoreboard_frame, text=player.name, padx=10, pady=5)
            frame.pack(fill="x", pady=2)

            # Moved status logic inside the loop
            status = []
            if not player.is_active:
                if player.frozen:
                    status.append("🧊 Frozen")
                elif player.busted:
                    status.append("💥 Busted")
                elif player.stayed:
                    status.append("✅ Stayed")
                else:
                    status.append("❌ Inactive")
            else:
                status.append("🟢 Active")

            tk.Label(frame, text=f"Status: {' | '.join(status)}").pack()
            tk.Label(frame, text=f"Total: {player.total_points} | Round: {player.round_points}").pack()
            tk.Label(frame, text=f"Drawn: {', '.join(map(str, player.cards_drawn))}").pack()
            tk.Label(frame, text=f"Specials: {', '.join(player.special_cards)}").pack()

    def show_player_turn(self):
        self.update_scoreboard()
        player = self.players[self.current_player_index]

        if player.frozen or player.stayed or player.busted:
            self.next_player()
            return

        self.status_label.config(text=f"{player.name}'s Turn")

        for widget in self.action_frame.winfo_children():
            widget.destroy()

        tk.Button(self.action_frame, text="Draw Card", command=self.draw_card).pack(side="left", padx=5)
        tk.Button(self.action_frame, text="Stay", command=self.stay_turn).pack(side="left", padx=5)
        tk.Button(self.action_frame, text="Use Special", command=self.use_special_card).pack(side="left", padx=5)

    def draw_card(self):
        player = self.players[self.current_player_index]
        card = simpledialog.askstring("Draw Card", "Enter card drawn (0-12, +2, x2, Freeze, Flip Three, Second Chance):")

        if not card:
            return

        if card in ["+2", "+4", "+6", "+10", "x2"]:
            player.special_cards.append(card)
        elif card in ["Freeze", "Flip Three", "Second Chance"]:
            player.special_cards.append(card)
        else:
            try:
                val = int(card)
                if val < 0 or val > 12:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid", "Invalid card number.")
                return

            # Bust logic
            if str(val) in player.cards_drawn:
                if "Second Chance" in player.special_cards:
                    messagebox.showinfo("Second Chance", "Bust prevented by a Second Chance!")
                    player.special_cards.remove("Second Chance")  # Removes one instance
                else:
                    messagebox.showinfo("Bust!", f"{player.name} busted!")
                    player.busted = True
                    player.round_points = 0
                    player.cards_drawn = []
                    player.is_active = False
                    self.next_player()
                    return
            else:
                player.cards_drawn.append(str(val))
                player.round_points += val

                # Auto-stay if 7 cards drawn
                if len(player.cards_drawn) == 7:
                    messagebox.showinfo("Auto-Stay", f"{player.name} drew 7 cards. Auto-stay.")
                    player.total_points += player.round_points
                    player.round_points = 0
                    player.cards_drawn = []
                    player.stayed = True
                    player.is_active = False

        self.update_scoreboard()

        # Check for win
        if player.total_points >= 200:
            messagebox.showinfo("Game Over", f"{player.name} wins!")
            self.root.quit()
        else:
            self.show_player_turn()

        if player.is_active:
            self.next_player()

    def stay_turn(self):
        player = self.players[self.current_player_index]
        player.total_points += player.round_points
        player.round_points = 0
        player.cards_drawn = []
        player.stayed = True
        player.is_active = False  
        
        self.update_scoreboard()  
        self.next_player()

    def use_special_card(self):
        player = self.players[self.current_player_index]
        if not player.special_cards:
            messagebox.showinfo("No Specials", "You have no special cards.")
            return

        choice = simpledialog.askstring("Use Special", f"Choose one: {', '.join(player.special_cards)}")

        if choice not in player.special_cards:
            return

        if choice == "Freeze":
            target = self.pick_other_player()
            if target:
                target.frozen = True
                target.is_active = False
                messagebox.showinfo("Frozen!", f"{target.name} has been frozen.")
        elif choice == "Flip Three":
            target = self.pick_other_player(include_self=True)
            if target:
                messagebox.showinfo("Flip Three", f"{target.name} must draw 3 cards (manually).")
        elif choice == "Second Chance":
            messagebox.showinfo("Note", "Second Chance is automatically applied when busting.")
        player.special_cards.remove(choice)

        self.update_scoreboard()
        self.show_player_turn()

    def pick_other_player(self, include_self=False):
        options = [p.name for i, p in enumerate(self.players)
                   if include_self or i != self.current_player_index]
        if not options:
            messagebox.showinfo("None", "No valid players to target.")
            return None
        choice = simpledialog.askstring("Pick Player", f"Choose one: {', '.join(options)}")
        for p in self.players:
            if p.name == choice:
                return p
        return None

    def next_player(self):
        # Find next active player
        for _ in range(len(self.players)):
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            if self.players[self.current_player_index].is_active:
                self.show_player_turn()
                return

        if all(not p.is_active for p in self.players):
            messagebox.showinfo("Next Round", "All players have finished. Starting next round.")

            # Reset all player statuses
            for p in self.players:
                p.stayed = False
                p.busted = False
                p.frozen = False
                p.is_active = True
                p.cards_drawn = []
                p.round_points = 0
                p.special_cards = []

            self.current_player_index = 0
            self.update_scoreboard() 
            self.show_player_turn()

if __name__ == "__main__":
    root = tk.Tk()
    app = Flip7App(root)
    root.mainloop()
