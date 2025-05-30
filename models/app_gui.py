import customtkinter as ctk
from models import Team, Player, Match
from widgets import NumberCounter
import tkinter.messagebox as messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TeamManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sports Team Manager")
        self.geometry("900x600")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        # Defined Tabs
        self.tab_team_initiation = self.tabview.add("Team Initiation")
        self.tab_team_management = self.tabview.add("Team Management")
        self.tab_match_simulator = self.tabview.add("Match Simulation")
        self.tab_player_analytics = self.tabview.add("Player Analytics")
        self.tab_team_analytics = self.tabview.add("Team Analytics")
        self.tab_club_management = self.tabview.add("Club Management")

        self.build_team_initiation_tab()
        self.build_team_management_tab()
        self.build_match_simulator_tab()
        self.build_player_analytics_tab()
        self.build_team_analytics_tab()
        self.build_club_management_tab()

    # ----------> Tab 1: Team Initiation <---------
    def build_team_initiation_tab(self):
        if not hasattr(self, "teams"):
            self.teams = {}

        frame = ctk.CTkFrame(self.tab_team_initiation)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Team name entry
        team_name_label = ctk.CTkLabel(frame, text="Team Name:")
        team_name_label.grid(row=0, column=0, sticky="w", pady=5)
        team_name_entry = ctk.CTkEntry(frame)
        team_name_entry.grid(row=0, column=1, pady=5)

        coach_name_label = ctk.CTkLabel(frame, text="Coach Name:")
        coach_name_label.grid(row=0, column=2, sticky="w", pady=5)
        coach_name_entry = ctk.CTkEntry(frame)
        coach_name_entry.grid(row=0, column=3, pady=5)

        # Player entry fields
        player_name_label = ctk.CTkLabel(frame, text="Player Name:")
        player_name_label.grid(row=1, column=0, sticky="w", pady=5)
        player_name_entry = ctk.CTkEntry(frame)
        player_name_entry.grid(row=1, column=1, pady=5)

        player_number_label = ctk.CTkLabel(frame, text="Player Number:")
        player_number_label.grid(row=2, column=0, sticky="w", pady=5)
        self.player_number_counter = NumberCounter(frame, min_value=1, max_value=99, initial=10)
        self.player_number_counter.grid(row=2, column=1, pady=5, sticky="ew")

        player_position_label = ctk.CTkLabel(frame, text="Player Position:")
        player_position_label.grid(row=3, column=0, sticky="w", pady=5)
        player_position_entry = ctk.CTkOptionMenu(frame, values=Player.POSITIONS)
        player_position_entry.grid(row=3, column=1, pady=5)

        # Listbox to show added players
        player_listbox = ctk.CTkTextbox(frame, height=100, width=250)
        player_listbox.grid(row=4, column=0, columnspan=2, pady=10)

        # Temp storage for players before team creation
        self.temp_players = []

        def add_player():
            name = player_name_entry.get()
            number = self.player_number_counter.get()
            position = player_position_entry.get()
            if not name or not number or not position:
                return
            try:
                number = int(number)
            except ValueError:
                return
            # Frontend check for duplicate number
            if any(p.number == number for p in self.temp_players):
                messagebox.showwarning(title="Duplicate Number", message="This number is already used. Please choose another.", icon="warning")
                return
            player = Player(name, number, position)
            self.temp_players.append(player)
            player_listbox.insert("end", f"{name} | #{number} | {position}\n")
            player_name_entry.delete(0, "end")
            self.player_number_counter.set(10)
            player_position_entry.set("")

        def create_team():
            team_name = team_name_entry.get()
            if not team_name or not self.temp_players:
                return
            team = Team(team_name)
            for player in self.temp_players:
                team.add_player(player)
            self.teams[team_name] = team
            team.
            # Reset for next team
            team_name_entry.delete(0, "end")
            player_listbox.delete("1.0", "end")
            self.temp_players.clear()

        # Add Player button (centered)
        add_player_btn = ctk.CTkButton(frame, text="Add Player", command=add_player)
        add_player_btn.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        # Create Team button (centered, below Add Player)
        create_team_btn = ctk.CTkButton(frame, text="Create Team", command=create_team)
        create_team_btn.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

    # ----------> Tab 2: Team Management <---------
    def build_team_management_tab(self):
        frame = ctk.CTkFrame(self.tab_team_management)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Team selection (top left)
        team_names = list(self.teams.keys()) if hasattr(self, "teams") else []
        self.selected_team = ctk.StringVar(value=team_names[0] if team_names else "")
        team_dropdown = ctk.CTkOptionMenu(frame, variable=self.selected_team, values=team_names, width=200)
        team_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Coach info (top right)
        coach_frame = ctk.CTkFrame(frame)
        coach_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ne")
        coach_label = ctk.CTkLabel(coach_frame, text="Coach Info:\nName: \nExperience: ")
        coach_label.pack()

        # Formation selection (center top)
        formations = ["4-4-2", "4-3-3", "3-5-2", "4-2-3-1"]
        self.selected_formation = ctk.StringVar(value=formations[0])
        formation_dropdown = ctk.CTkOptionMenu(frame, variable=self.selected_formation, values=formations, width=150)
        formation_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Pitch area for lineup (center)
        pitch_frame = ctk.CTkFrame(frame, width=500, height=350, fg_color="#228B22")
        pitch_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=20)
        pitch_frame.grid_propagate(False)
        pitch_label = ctk.CTkLabel(pitch_frame, text="Pitch: Drag and drop players here", text_color="white")
        pitch_label.place(relx=0.5, rely=0.05, anchor="n")

        # Player list (bottom left)
        player_list_frame = ctk.CTkFrame(frame)
        player_list_frame.grid(row=2, column=0, padx=10, pady=10, sticky="sw")
        player_list_label = ctk.CTkLabel(player_list_frame, text="Players:")
        player_list_label.pack()
        self.player_listbox = ctk.CTkTextbox(player_list_frame, height=120, width=200)
        self.player_listbox.pack()

        # TODO: Add logic to update coach info, player list, and pitch when team or formation changes.
        # TODO: Add drag-and-drop or button-based assignment of players to pitch positions.
        # TODO: Add buttons to add/remove players from lineup using your existing functions.

    # ----------> Tab 3: Match Simulator <---------
    def build_match_simulator_tab(self):
        pass

    # ----------> Tab 4: Player Analytics <---------
    def build_player_analytics_tab(self):
        pass

    # ----------> Tab 5: Team Analytics <---------
    def build_team_analytics_tab(self):
        pass   

    # ----------> Tab 6: Club Management <---------
    def build_club_management_tab(self):
        pass




if __name__ == "__main__":
    app = TeamManagerApp()
    app.mainloop()
