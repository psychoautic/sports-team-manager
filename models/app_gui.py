import customtkinter as ctk
from models import Team, Player, Match

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

        # Player entry fields
        player_name_label = ctk.CTkLabel(frame, text="Player Name:")
        player_name_label.grid(row=1, column=0, sticky="w", pady=5)
        player_name_entry = ctk.CTkEntry(frame)
        player_name_entry.grid(row=1, column=1, pady=5)

        player_number_label = ctk.CTkLabel(frame, text="Player Number:")
        player_number_label.grid(row=2, column=0, sticky="w", pady=5)
        player_number_entry = ctk.CTkEntry(frame)
        player_number_entry.grid(row=2, column=1, pady=5)

        player_position_label = ctk.CTkLabel(frame, text="Player Position:")
        player_position_label.grid(row=3, column=0, sticky="w", pady=5)
        player_position_entry = ctk.CTkOptionMenu(frame, values= Player.POSITIONS)
        player_position_entry.grid(row=3, column=1, pady=5)

        # Listbox to show added players
        player_listbox = ctk.CTkTextbox(frame, height=100, width=250)
        player_listbox.grid(row=4, column=0, columnspan=2, pady=10)

        # Temp storage for players before team creation
        self.temp_players = []

        def add_player():
            name = player_name_entry.get()
            number = player_number_entry.get()
            position = player_position_entry.get()
            if not name or not number or not position:
                return
            try:
                number = int(number)
            except ValueError:
                return
            player = Player(name, number, position)
            self.temp_players.append(player)
            player_listbox.insert("end", f"{name} | #{number} | {position}\n")
            player_name_entry.delete(0, "end")
            player_number_entry.delete(0, "end")
            player_position_entry.delete(0, "end")

        def create_team():
            team_name = team_name_entry.get()
            if not team_name or not self.temp_players:
                return
            team = Team(team_name)
            for player in self.temp_players:
                team.add_player(player)
            self.teams[team_name] = team
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
        pass

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
