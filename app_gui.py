import customtkinter as ctk
from models import Team, Player, Coach, Match
from widgets import NumberCounter
import tkinter.messagebox as messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TeamManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sports Team Manager")
        self.geometry("900x600")

        self.teams = {}  # Ensure teams dict exists
        self.active_team = None  # <-- Add this line
        self.selected_team_var = ctk.StringVar()  # <-- Add this line
        self.temp_players = []


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

        for widget in self.tab_team_initiation.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.tab_team_initiation)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Make columns 0 and 1 expand equally
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Team name entry
        team_name_label = ctk.CTkLabel(frame, text="Team Name:")
        team_name_label.grid(row=0, column=0, sticky="e", pady=5)
        team_name_entry = ctk.CTkEntry(frame)
        team_name_entry.grid(row=0, column=1, sticky="w", pady=5)

        coach_name_label = ctk.CTkLabel(frame, text="Coach Name:")
        coach_name_label.grid(row=1, column=0, sticky="e", pady=5)
        coach_name_entry = ctk.CTkEntry(frame)
        coach_name_entry.grid(row=1, column=1, sticky="w", pady=5)

        # Player entry fields
        player_name_label = ctk.CTkLabel(frame, text="Player Name:")
        player_name_label.grid(row=2, column=0, sticky="e", pady=5)
        player_name_entry = ctk.CTkEntry(frame)
        player_name_entry.grid(row=2, column=1, sticky="w", pady=5)

        player_number_label = ctk.CTkLabel(frame, text="Player Number:")
        player_number_label.grid(row=3, column=0, sticky="e", pady=5)
        self.player_number_counter = NumberCounter(frame, min_value=1, max_value=99, initial=10)
        self.player_number_counter.grid(row=3, column=1, sticky="w", pady=5)

        player_position_label = ctk.CTkLabel(frame, text="Player Position:")
        player_position_label.grid(row=4, column=0, sticky="e", pady=5)
        player_position_entry = ctk.CTkOptionMenu(frame, values=Player.POSITIONS)
        player_position_entry.grid(row=4, column=1, sticky="w", pady=5)

        # Listbox to show added players (centered, spanning both columns)
        player_listbox = ctk.CTkTextbox(frame, height=100, width=250)
        player_listbox.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

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
                messagebox.showwarning(title="Duplicate Number", message="This number is already used. Please choose another.")
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
            team.coach = Coach(coach_name_entry.get())
            for player in self.temp_players:
                team.add_player(player)
            self.teams[team_name] = team
            # Reset for next team
            team_name_entry.delete(0, "end")
            player_listbox.delete("1.0", "end")
            self.temp_players.clear()
            coach_name_entry.delete(0, "end")
            
            ### Added this
            self.selected_team_var.set(team_name)
            self.active_team = team_name
            messagebox.showinfo(title="Team Created", message=f"Team '{team_name}' created successfully!")
            self.refresh_team_management_tab() 
            self.refresh_match_simulatioN_tab()
            self.refresh_player_analytics_tab()
            self.refresh_team_analytics_tab()
            self.refresh_club_management_tab()

        # Add Player button (centered)
        add_player_btn = ctk.CTkButton(frame, text="Add Player", command=add_player)
        add_player_btn.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

        # Create Team button (centered, below Add Player)
        create_team_btn = ctk.CTkButton(frame, text="Create Team", command=create_team)
        create_team_btn.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

    # ----------> Tab 2: Team Management <---------
    def build_team_management_tab(self):
        import functools

        frame = ctk.CTkFrame(self.tab_team_management)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)


        team_name = self.active_team if hasattr(self, "active_team") and self.active_team in self.teams else "No Team Selected"
        team = self.teams[team_name] if team_name != "No Team Selected" else None

        team_name_label = ctk.CTkLabel(frame, text=f"Team: {team_name}", font=("Arial", 18, "bold"))
        team_name_label.grid(row=0, column=1, pady=(10, 0), sticky="n")

        coach_text = ""
        if team:
            coach = team.coach
            coach_text = f"Coach: {coach.name if coach else 'N/A'}"
        coach_label = ctk.CTkLabel(frame, text=coach_text, font=("Arial", 14))
        coach_label.grid(row=1, column=1, pady=(0, 10), sticky="n")

        # Formation selection (center, below coach)
        formations = {
            "4-4-2": [4, 4, 2],
            "4-3-3": [4, 3, 3],
            "3-5-2": [3, 5, 2],
            "4-2-3-1": [4, 2, 3, 1]
        }
        self.selected_formation = getattr(self, "selected_formation", ctk.StringVar(value="4-4-2"))
        formation_label = ctk.CTkLabel(frame, text="Choose Squad Formation:", font=("Arial", 12))
        formation_label.grid(row=2, column=0, sticky="e", padx=(0, 5))
        formation_dropdown = ctk.CTkOptionMenu(
            frame, variable=self.selected_formation, values=list(formations.keys()), width=150,
            command=lambda _: self.refresh_team_management_tab()
        )
        formation_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Player list (horizontal, max 4 per row)
        player_frame = ctk.CTkFrame(frame)
        player_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        substitutes = []
        if team:
            # Players not in lineup (substitutes)
            lineup = getattr(team, "lineup", [])
            substitutes = [p for p in team.players if p not in lineup]
            for idx, player in enumerate(substitutes):
                btn = ctk.CTkButton(
                    player_frame,
                    text=f"{player.name}\n#{player.number}\n{player.position}",
                    width=120, height=60,
                    command=functools.partial(self.select_player_for_pitch, player)
                )
                btn.grid(row=idx // 4, column=idx % 4, padx=5, pady=5)

        # Pitch area for lineup (center, below player list)
        pitch_frame = ctk.CTkFrame(frame, width=500, height=350, fg_color="#228B22")
        pitch_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=20)
        pitch_frame.grid_propagate(False)

        # Always place goalkeeper at the bottom (flipped pitch)
        if team:
            formation = formations[self.selected_formation.get()]
            total_rows = len(formation) + 1  # +1 for goalkeeper row
            self.pitch_positions = getattr(self, "pitch_positions", [None] * (sum(formation) + 1))
            # Goalkeeper slot (always first)
            gk = None
            for p in team.players:
                if p.position == "GK":
                    gk = p
                    break
            self.pitch_positions[0] = gk
            gk_btn_text = gk.name if gk else "Empty"
            gk_btn = ctk.CTkButton(
                pitch_frame,
                text=f"GK\n{gk_btn_text}",
                width=80, height=40,
                fg_color="#1e90ff" if gk else "#444",
                state="disabled"  # GK is fixed
            )
            gk_btn.place(relx=0.5, rely=(total_rows) / (total_rows + 1), anchor="center")

            # Outfield positions (flipped: start from bottom row up)
            pos_idx = 1
            for row, count in enumerate(reversed(formation)):
                for col in range(count):
                    assigned_player = self.pitch_positions[pos_idx] if pos_idx < len(self.pitch_positions) else None
                    btn_text = assigned_player.name if assigned_player else "Empty"
                    btn = ctk.CTkButton(
                        pitch_frame,
                        text=btn_text,
                        width=80, height=40,
                        fg_color="#444" if not assigned_player else "#1e90ff",
                        command=functools.partial(self.assign_selected_player_to_position, pos_idx)
                    )
                    btn.place(
                        relx=(col + 1) / (count + 1),
                        rely=(row + 1) / (total_rows + 1),
                        anchor="center"
                    )
                    pos_idx += 1

        # Substitutes list below pitch
        subs_label = ctk.CTkLabel(frame, text="Substitutes:", font=("Arial", 12, "bold"))
        subs_label.grid(row=5, column=1, pady=(0, 5), sticky="n")
        subs_frame = ctk.CTkFrame(frame)
        subs_frame.grid(row=6, column=0, columnspan=3, pady=(0, 10))
        if team:
            for idx, player in enumerate(substitutes):
                btn = ctk.CTkButton(
                    subs_frame,
                    text=f"{player.name}\n#{player.number}\n{player.position}",
                    width=120, height=60,
                    command=functools.partial(self.select_player_for_pitch, player)
                )
                btn.grid(row=idx // 4, column=idx % 4, padx=5, pady=5)

    def select_player_for_pitch(self, player):
        self.selected_player_for_pitch = player

    def assign_selected_player_to_position(self, pos_idx):
        if not hasattr(self, "selected_player_for_pitch") or not self.selected_player_for_pitch:
            return
        # Assign player to pitch position
        if not hasattr(self, "pitch_positions"):
            self.pitch_positions = []
        # Prevent duplicate assignment
        for idx, p in enumerate(self.pitch_positions):
            if p and p == self.selected_player_for_pitch:
                self.pitch_positions[idx] = None
        # Assign to selected position (skip GK at pos_idx 0)
        if pos_idx == 0:
            return
        if len(self.pitch_positions) <= pos_idx:
            self.pitch_positions += [None] * (pos_idx - len(self.pitch_positions) + 1)
        self.pitch_positions[pos_idx] = self.selected_player_for_pitch
        # Update team lineup (backend)
        if hasattr(self, "active_team") and self.active_team in self.teams:
            team = self.teams[self.active_team]
            # Lineup is all non-None pitch positions except GK (pos_idx 0)
            lineup = [p for i, p in enumerate(self.pitch_positions) if p and i != 0]
            if self.pitch_positions[0]:
                lineup = [self.pitch_positions[0]] + lineup
            team.select_lineup(lineup)
        self.selected_player_for_pitch = None
        self.refresh_team_management_tab()

    def refresh_team_management_tab(self):
        # Destroy all widgets in the tab and rebuild
        for widget in self.tab_team_management.winfo_children():
            widget.destroy()
        self.build_team_management_tab()

    # ----------> Tab 3: Match Simulator <---------
    def build_match_simulator_tab(self):
        pass

    # ----------> Tab 4: Player Analytics <---------
    def build_player_analytics_tab(self):
        frame = ctk.CTkFrame(self.tab_player_analytics)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        team_name = self.active_team if hasattr(self, "active_team") and self.active_team in self.teams else None
        if not team_name:
            info_label = ctk.CTkLabel(frame, text="No active team selected.", font=("Arial", 14))
            info_label.pack(pady=20)
            return

        team = self.teams[team_name]
        title_label = ctk.CTkLabel(frame, text=f"Player Analytics for {team_name}", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Table header
        header = ctk.CTkLabel(frame, text="Name\tNumber\tPosition\tGoals\tAssists\tGames Played", font=("Arial", 12, "bold"))
        header.pack(anchor="w", padx=10)

        # Player stats
        for player in team.players:
            # Example: sum up goals, assists, games played from player's stats list
            goals = sum(getattr(stat, "goals", 0) for stat in getattr(player, "stats", []))
            assists = sum(getattr(stat, "assists", 0) for stat in getattr(player, "stats", []))
            games_played = sum(getattr(stat, "games_played", 0) for stat in getattr(player, "stats", []))
            line = f"{player.name}\t{player.number}\t{player.position}\t{goals}\t{assists}\t{games_played}"
            player_label = ctk.CTkLabel(frame, text=line, font=("Arial", 12))
            player_label.pack(anchor="w", padx=10)

    def refresh_player_analytics_tab(self):
        for widget in self.tab_player_analytics.winfo_children():
            widget.destroy()
        self.build_player_analytics_tab()

    # ----------> Tab 5: Team Analytics <---------
    def build_team_analytics_tab(self):
        frame = ctk.CTkFrame(self.tab_team_analytics)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        team_name = self.active_team if hasattr(self, "active_team") and self.active_team in self.teams else None
        if not team_name:
            info_label = ctk.CTkLabel(frame, text="No active team selected.", font=("Arial", 14))
            info_label.pack(pady=20)
            return

        team = self.teams[team_name]
        title_label = ctk.CTkLabel(frame, text=f"Team Analytics for {team_name}", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Example team stats: total goals, assists, games played
        total_goals = sum(sum(getattr(stat, "goals", 0) for stat in getattr(player, "stats", [])) for player in team.players)
        total_assists = sum(sum(getattr(stat, "assists", 0) for stat in getattr(player, "stats", [])) for player in team.players)
        total_games = sum(sum(getattr(stat, "games_played", 0) for stat in getattr(player, "stats", [])) for player in team.players)

        stats_text = (
            f"Total Goals: {total_goals}\n"
            f"Total Assists: {total_assists}\n"
            f"Total Games Played: {total_games}\n"
            f"Number of Players: {len(team.players)}"
        )
        stats_label = ctk.CTkLabel(frame, text=stats_text, font=("Arial", 13))
        stats_label.pack(pady=10)

    def refresh_team_analytics_tab(self):
        for widget in self.tab_team_analytics.winfo_children():
            widget.destroy()
        self.build_team_analytics_tab()

    # ----------> Tab 6: Club Management <---------
    def build_club_management_tab(self):
        frame = ctk.CTkFrame(self.tab_club_management)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # --- Team Dropdown ---
        team_list_label = ctk.CTkLabel(frame, text="Teams:", font=("Arial", 14, "bold"))
        team_list_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        team_names = list(self.teams.keys())
        # Do NOT reassign selected_team_var, just set its value
        if self.active_team in team_names:
            self.selected_team_var.set(self.active_team)
        elif team_names:
            self.selected_team_var.set(team_names[0])
        else:
            self.selected_team_var.set("")

        team_dropdown = ctk.CTkOptionMenu(
            frame,
            variable=self.selected_team_var,
            values=team_names if team_names else ["No Teams"],
            width=200
        )
        team_dropdown.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # --- Set Active Team Button ---
        def set_active_team():
            team_name = self.selected_team_var.get()
            if team_name in self.teams:
                self.active_team = team_name
                self.refresh_team_management_tab()
                self.refresh_player_analytics_tab()
                self.refresh_team_analytics_tab()
                messagebox.showinfo("Active Team Changed", f"Active team set to '{team_name}'.")

        set_team_btn = ctk.CTkButton(frame, text="Set Active Team", command=set_active_team)
        set_team_btn.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # --- Create New Team Button ---
        def go_to_team_initiation():
            self.tabview.set("Team Initiation")

        create_team_btn = ctk.CTkButton(frame, text="Create New Team", command=go_to_team_initiation)
        create_team_btn.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # --- Delete Team Button ---
        def delete_team():
            team_name = self.selected_team_var.get()
            if team_name in self.teams:
                del self.teams[team_name]
                # Update active team if needed
                if hasattr(self, "active_team") and self.active_team == team_name:
                    self.active_team = next(iter(self.teams), None) if self.teams else None
                self.refresh_club_management_tab()
                self.refresh_team_management_tab()
                self.refresh_player_analytics_tab()
                self.refresh_team_analytics_tab()
                messagebox.showinfo("Team Deleted", "Team and all related data deleted.")

        delete_team_btn = ctk.CTkButton(frame, text="Delete Team", command=delete_team)
        delete_team_btn.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    def refresh_club_management_tab(self):
        # Always update the dropdown with the latest teams
        for widget in self.tab_club_management.winfo_children():
            widget.destroy()
        self.build_club_management_tab()
    


if __name__ == "__main__":
    app = TeamManagerApp()
    app.mainloop()