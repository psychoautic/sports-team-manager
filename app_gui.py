import customtkinter as ctk
from models import Team, Player, Coach, Match
import tkinter.messagebox as messagebox
from widgets import NumberCounter
from database import DatabaseError, Database

# Initialize database
db = Database()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TeamManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sports Team Manager")
        self.geometry("900x600")

        # Initialize database and load teams
        self.db = Database()
        self.teams = {}  # Initialize as empty dict first
        try:
            loaded_teams = Team.get_all_teams()
            if loaded_teams:  # Only update if we got teams back
                self.teams = loaded_teams
        except DatabaseError as e:
            messagebox.showerror("Database Error", str(e))
            # self.teams already initialized as empty dict
            
        self.active_team = None
        self.selected_team_var = ctk.StringVar(value="No Teams")
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

    def build_team_initiation_tab(self):
        for widget in self.tab_team_initiation.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.tab_team_initiation)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Team name entry with validation
        team_name_label = ctk.CTkLabel(frame, text="Team Name:")
        team_name_label.grid(row=0, column=0, sticky="e", pady=5)
        team_name_entry = ctk.CTkEntry(frame)
        team_name_entry.grid(row=0, column=1, sticky="w", pady=5)

        # Coach name entry
        coach_name_label = ctk.CTkLabel(frame, text="Coach Name:")
        coach_name_label.grid(row=1, column=0, sticky="e", pady=5)
        coach_name_entry = ctk.CTkEntry(frame)
        coach_name_entry.grid(row=1, column=1, sticky="w", pady=5)

        # Player entry fields with validation
        player_name_label = ctk.CTkLabel(frame, text="Player Name:")
        player_name_label.grid(row=2, column=0, sticky="e", pady=5)
        player_name_entry = ctk.CTkEntry(frame)
        player_name_entry.grid(row=2, column=1, sticky="w", pady=5)

        player_number_label = ctk.CTkLabel(frame, text="Player Number:")
        player_number_label.grid(row=3, column=0, sticky="e", pady=5)
        self.player_number_counter = NumberCounter(frame, min_value=1, max_value=99, initial=1)
        self.player_number_counter.grid(row=3, column=1, sticky="w", pady=5)

        player_position_label = ctk.CTkLabel(frame, text="Player Position:")
        player_position_label.grid(row=4, column=0, sticky="e", pady=5)
        player_position_entry = ctk.CTkOptionMenu(frame, values=Player.POSITIONS)
        player_position_entry.grid(row=4, column=1, sticky="w", pady=5)

        # Player list with scrollbar
        player_list_frame = ctk.CTkFrame(frame)
        player_list_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")
        player_list_frame.grid_columnconfigure(0, weight=1)
        player_list_frame.grid_rowconfigure(0, weight=1)

        player_listbox = ctk.CTkTextbox(player_list_frame, height=150)
        player_listbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        def validate_player_input():
            name = player_name_entry.get().strip()
            if not name:
                messagebox.showwarning("Invalid Input", "Player name cannot be empty")
                return False
            
            try:
                number = int(self.player_number_counter.get())
                if number < 1 or number > 99:
                    raise ValueError()
            except ValueError:
                messagebox.showwarning("Invalid Input", "Player number must be between 1 and 99")
                return False
            
            position = player_position_entry.get()
            if not position:
                messagebox.showwarning("Invalid Input", "Please select a position")
                return False
                
            return True

        def add_player():
            if not validate_player_input():
                return
                
            name = player_name_entry.get().strip()
            number = int(self.player_number_counter.get())
            position = player_position_entry.get()
            
            try:
                player = Player(name, number, position)
                self.temp_players.append(player)
                player_listbox.insert("end", f"{name} | #{number:02d} | {position}\n")
                
                # Clear inputs and increment number
                player_name_entry.delete(0, "end")
                self.player_number_counter.set(number + 1)
                player_position_entry.set(Player.POSITIONS[0])
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        def create_team():
            team_name = team_name_entry.get().strip()
            coach_name = coach_name_entry.get().strip()
            
            if not team_name:
                messagebox.showwarning("Invalid Input", "Team name cannot be empty")
                return
                
            if not self.temp_players:
                messagebox.showwarning("Invalid Input", "Please add at least one player")
                return
                
            try:
                # Create new team in database
                team = Team(team_name, coach_name=coach_name)
                
                # Add players to team and database
                for player in self.temp_players:
                    team.add_player(player)
                    
                # Add to teams dictionary
                self.teams[team_name] = team
                
                # Reset form
                team_name_entry.delete(0, "end")
                coach_name_entry.delete(0, "end")
                player_listbox.delete("1.0", "end")
                self.temp_players.clear()
                self.player_number_counter.set(1)
                player_position_entry.set(Player.POSITIONS[0])
                
                # Set as active team
                self.selected_team_var.set(team_name)
                self.active_team = team_name
                
                messagebox.showinfo("Success", f"Team '{team_name}' created successfully!")
                
                # Refresh all tabs
                self.refresh_team_management_tab() 
                self.refresh_match_simulator_tab()
                self.refresh_player_analytics_tab()
                self.refresh_team_analytics_tab()
                self.refresh_club_management_tab()

            except DatabaseError as e:
                messagebox.showerror("Database Error", str(e))

        # Buttons
        button_frame = ctk.CTkFrame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        add_player_btn = ctk.CTkButton(button_frame, text="Add Player", command=add_player)
        add_player_btn.pack(side="left", padx=5)

        create_team_btn = ctk.CTkButton(button_frame, text="Create Team", command=create_team)
        create_team_btn.pack(side="left", padx=5)

    def build_team_management_tab(self):
        if not self.active_team or self.active_team not in self.teams:
            frame = ctk.CTkFrame(self.tab_team_management)
            frame.pack(padx=20, pady=20, fill="both", expand=True)
            
            msg = ctk.CTkLabel(
                frame,
                text="Please select a team in the Club Management tab first.",
                font=("Arial", 14)
            )
            msg.pack(pady=20)
            return

        frame = ctk.CTkFrame(self.tab_team_management)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        team = self.teams[self.active_team]

        header_frame = ctk.CTkFrame(frame)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        team_info = ctk.CTkLabel(
            header_frame,
            text=f"Team: {team.name}   |   Coach: {team.coach.name if team.coach else 'No Coach'}",
            font=("Arial", 14, "bold")
        )
        team_info.pack(pady=5)

        # Formation selection
        formation_frame = ctk.CTkFrame(frame)
        formation_frame.pack(fill="x", padx=10, pady=5)
        
        formation_label = ctk.CTkLabel(formation_frame, text="Formation:", font=("Arial", 12))
        formation_label.pack(side="left", padx=5)
        
        def on_formation_change(choice):
            team.set_formation(choice)
            self.refresh_team_management_tab()

        formation_dropdown = ctk.CTkOptionMenu(
            formation_frame,
            values=list(Team.FORMATIONS.keys()),
            command=on_formation_change,
            variable=ctk.StringVar(value=team.current_formation)
        )
        formation_dropdown.pack(side="left", padx=5)

        # Add Save Lineup button
        def save_current_lineup():
            try:
                team.save_lineup()
                messagebox.showinfo("Success", "Lineup saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save lineup: {str(e)}")

        save_btn = ctk.CTkButton(
            formation_frame,
            text="Save Lineup",
            command=save_current_lineup,
            width=120
        )
        save_btn.pack(side="right", padx=10)

        # Main content area with pitch and bench
        content_frame = ctk.CTkFrame(frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        content_frame.grid_columnconfigure(0, weight=2)  # Pitch gets more space
        content_frame.grid_columnconfigure(1, weight=1)  # Bench gets less space

        # Pitch area (left side)
        pitch_frame = ctk.CTkFrame(content_frame, fg_color="#228B22", width=400, height=500)
        pitch_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        pitch_frame.grid_propagate(False)

        # Store the currently selected player
        self.selected_player = getattr(self, 'selected_player', None)

        def create_position_button(pos, x_pos, y_pos):
            player = team.lineup.get(pos)
            
            def on_position_click():
                if self.selected_player:
                    try:
                        # Assign player to position
                        team.assign_player_to_position(pos, self.selected_player)
                        self.selected_player = None
                        
                        # Update button appearance
                        btn.configure(
                            text=f"{team.lineup[pos].name}\n#{team.lineup[pos].number}",
                            fg_color="#1e90ff"
                        )
                        
                        # Refresh bench area
                        self.refresh_team_management_tab()
                    except ValueError as e:
                        messagebox.showerror("Error", str(e))

            button_text = f"{pos}\n"
            if player:
                button_text = f"{player.name}\n#{player.number}"

            btn = ctk.CTkButton(
                pitch_frame,
                text=button_text,
                width=70,
                height=35,
                fg_color="#1e90ff" if player else "#444",
                command=on_position_click
            )
            btn.place(relx=x_pos, rely=y_pos, anchor="center")

        # Create goalkeeper position (always at bottom)
        create_position_button('GK', 0.5, 0.9)  # Centered at 90% down

        # Calculate y-positions for each row (excluding GK)
        formation_numbers = [int(x) for x in team.current_formation.split('-')]
        num_rows = len(formation_numbers)
        y_spacing = 0.7 / num_rows  # Use 70% of the pitch (leaving space for GK)

        # Create positions for each row
        current_idx = 0
        for row_idx, num_players in enumerate(formation_numbers):
            # Calculate y position (from bottom to top)
            y_pos = 0.85 - (y_spacing * row_idx)  # Start at 85% down
            
            # Calculate x positions for this row
            x_spacing = 1.0 / (num_players + 1)
            
            # Get positions for this row
            start_idx = sum(formation_numbers[:row_idx])
            row_positions = Team.FORMATIONS[team.current_formation][start_idx:start_idx + num_players]
            
            # Create buttons for this row
            for i in range(num_players):
                x_pos = x_spacing * (i + 1)
                pos = row_positions[i]
                create_position_button(pos, x_pos, y_pos)

        # Bench area (right side)
        bench_frame = ctk.CTkFrame(content_frame)
        bench_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        bench_label = ctk.CTkLabel(bench_frame, text="Bench", font=("Arial", 12, "bold"))
        bench_label.pack(pady=5)

        # Get players not in lineup
        bench_players = [p for p in team.players if p not in team.lineup.values()]

        def on_player_select(player):
            self.selected_player = player
            # Update button colors
            for widget in bench_scroll.winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    if widget.cget("text").startswith(player.name):
                        widget.configure(fg_color="#1e90ff")  # Highlight selected
                    else:
                        widget.configure(fg_color="#444")  # Reset others

        # Create scrollable frame for bench players
        bench_scroll = ctk.CTkScrollableFrame(bench_frame)
        bench_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        for player in bench_players:
            btn = ctk.CTkButton(
                bench_scroll,
                text=f"{player.name} #{player.number}\n{player.position}",
                command=lambda p=player: on_player_select(p),
                fg_color="#1e90ff" if player == self.selected_player else "#444"
            )
            btn.pack(fill="x", padx=5, pady=2)

    def refresh_team_management_tab(self):
        for widget in self.tab_team_management.winfo_children():
            widget.destroy()
        self.build_team_management_tab()

    # ----------> Tab 3: Match Simulator <---------
    def build_match_simulator_tab(self):
        if not self.active_team or self.active_team not in self.teams:
            frame = ctk.CTkFrame(self.tab_match_simulator)
            frame.pack(padx=20, pady=20, fill="both", expand=True)
            
            msg = ctk.CTkLabel(
                frame,
                text="Please select a team in the Club Management tab first.",
                font=("Arial", 14)
            )
            msg.pack(pady=20)
            return

        frame = ctk.CTkFrame(self.tab_match_simulator)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Match Setup Section
        setup_frame = ctk.CTkFrame(frame)
        setup_frame.pack(fill="x", padx=10, pady=10)

        # Home/Away selection
        venue_label = ctk.CTkLabel(setup_frame, text="Venue:", font=("Arial", 12))
        venue_label.pack(side="left", padx=5)
        
        venue_var = ctk.StringVar(value="Home")
        home_radio = ctk.CTkRadioButton(setup_frame, text="Home", variable=venue_var, value="Home")
        away_radio = ctk.CTkRadioButton(setup_frame, text="Away", variable=venue_var, value="Away")
        home_radio.pack(side="left", padx=10)
        away_radio.pack(side="left", padx=10)

        # Opponent Setup
        opponent_frame = ctk.CTkFrame(frame)
        opponent_frame.pack(fill="x", padx=10, pady=10)

        opponent_label = ctk.CTkLabel(opponent_frame, text="Opponent:", font=("Arial", 12))
        opponent_label.pack(side="left", padx=5)

        opponent_entry = ctk.CTkEntry(opponent_frame, width=200)
        opponent_entry.pack(side="left", padx=5)

        # Team Lineup Display
        lineup_frame = ctk.CTkFrame(frame)
        lineup_frame.pack(fill="x", padx=10, pady=10)
        
        team = self.teams[self.active_team]
        
        lineup_label = ctk.CTkLabel(
            lineup_frame, 
            text=f"Current Formation: {team.current_formation}",
            font=("Arial", 12, "bold")
        )
        lineup_label.pack(pady=5)

        # Display current lineup
        lineup_text = "Starting Lineup:\n\n"
        # Start with goalkeeper
        if team.lineup['GK']:
            lineup_text += f"GK: {team.lineup['GK'].name} #{team.lineup['GK'].number}\n"
        else:
            lineup_text += "GK: Not assigned\n"
            
        # Add rest of positions in formation order
        for pos in Team.FORMATIONS[team.current_formation]:
            if team.lineup[pos]:
                lineup_text += f"{pos}: {team.lineup[pos].name} #{team.lineup[pos].number}\n"
            else:
                lineup_text += f"{pos}: Not assigned\n"
        
        lineup_display = ctk.CTkTextbox(lineup_frame, height=200, width=300)
        lineup_display.pack(pady=5)
        lineup_display.insert("1.0", lineup_text)
        lineup_display.configure(state="disabled")

        # Match Simulation Section
        simulation_frame = ctk.CTkFrame(frame)
        simulation_frame.pack(fill="x", padx=10, pady=10)

        def simulate_match():
            opponent_name = opponent_entry.get().strip()
            if not opponent_name:
                messagebox.showwarning("Invalid Input", "Please enter opponent name")
                return
                
            if not all(team.lineup.values()):
                messagebox.showwarning("Invalid Lineup", "Please set up a complete lineup before simulating")
                return

            try:
                # Create opponent team
                opponent = Team(opponent_name)
                
                # Create and simulate match
                match = Match(team, opponent)
                match.stadium = "Home Stadium" if venue_var.get() == "Home" else "Away Stadium"
                
                # Simulate match and get result
                result = match.match_simulate()
                
                # Show result
                result_window = ctk.CTkToplevel()
                result_window.title("Match Result")
                result_window.geometry("400x500")
                
                # Match header
                header_text = f"{team.name} vs {opponent_name}\n{match.stadium}"
                header = ctk.CTkLabel(
                    result_window,
                    text=header_text,
                    font=("Arial", 16, "bold")
                )
                header.pack(pady=20)
                
                # Score
                score_text = f"{result[0]} - {result[1]}"
                score = ctk.CTkLabel(
                    result_window,
                    text=score_text,
                    font=("Arial", 24, "bold")
                )
                score.pack(pady=20)
                
                # Match stats
                stats_frame = ctk.CTkFrame(result_window)
                stats_frame.pack(fill="x", padx=20, pady=10)
                
                stats_text = (
                    f"Goals Scored: {result[0]}\n"
                    f"Goals Conceded: {result[1]}\n"
                    f"Clean Sheet: {'Yes' if result[1] == 0 else 'No'}\n"
                )
                
                stats = ctk.CTkLabel(
                    stats_frame,
                    text=stats_text,
                    font=("Arial", 12),
                    justify="left"
                )
                stats.pack(pady=10)
                
                # Scorers and assists
                scorers_frame = ctk.CTkFrame(result_window)
                scorers_frame.pack(fill="x", padx=20, pady=10)
                
                scorers_text = "Scorers:\n"
                for player in team.players:
                    if player.stats["goals"] > 0:
                        scorers_text += f"{player.name}: {player.stats['goals']}\n"
                
                assists_text = "\nAssists:\n"
                for player in team.players:
                    if player.stats["assists"] > 0:
                        assists_text += f"{player.name}: {player.stats['assists']}\n"
                
                scorers = ctk.CTkLabel(
                    scorers_frame,
                    text=scorers_text + assists_text,
                    font=("Arial", 12),
                    justify="left"
                )
                scorers.pack(pady=10)
                
                # Save lineup after successful match
                team.save_lineup()
                
                # Refresh analytics tabs to show updated stats
                self.refresh_player_analytics_tab()
                self.refresh_team_analytics_tab()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to simulate match: {str(e)}")

        simulate_btn = ctk.CTkButton(
            simulation_frame,
            text="Simulate Match",
            command=simulate_match,
            width=200
        )
        simulate_btn.pack(pady=20)

    def refresh_match_simulator_tab(self):
        for widget in self.tab_match_simulator.winfo_children():
            widget.destroy()
        self.build_match_simulator_tab()

    # ----------> Tab 4: Player Analytics <---------
    def build_player_analytics_tab(self):
        if not self.active_team or self.active_team not in self.teams:
            frame = ctk.CTkFrame(self.tab_player_analytics)
            frame.pack(padx=20, pady=20, fill="both", expand=True)
            
            msg = ctk.CTkLabel(
                frame,
                text="Please select a team in the Club Management tab first.",
                font=("Arial", 14)
            )
            msg.pack(pady=20)
            return

        frame = ctk.CTkFrame(self.tab_player_analytics)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        team = self.teams[self.active_team]
        title_label = ctk.CTkLabel(
            frame,
            text=f"Player Analytics for {team.name}",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Create scrollable frame for player stats
        stats_frame = ctk.CTkScrollableFrame(frame)
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Headers
        headers = ["Name", "Position", "#", "Games", "Goals", "Assists", "G/G", "Clean Sheets"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                stats_frame,
                text=header,
                font=("Arial", 12, "bold")
            )
            label.pack(side="left", padx=10)

        # Sort players by position groups
        position_groups = {
            "Goalkeepers": ["GK"],
            "Defenders": ["CB", "LB", "RB"],
            "Midfielders": ["CDM", "CM", "CAM", "LM", "RM"],
            "Forwards": ["ST", "LW", "RW"]
        }

        for group_name, positions in position_groups.items():
            players = [p for p in team.players if p.position in positions]
            if not players:
                continue

            # Group header
            group_frame = ctk.CTkFrame(stats_frame)
            group_frame.pack(fill="x", pady=5)
            
            group_label = ctk.CTkLabel(
                group_frame,
                text=group_name,
                font=("Arial", 12, "bold"),
                fg_color="#1f538d",
                corner_radius=6
            )
            group_label.pack(fill="x", pady=2)

            # Player stats
            for player in sorted(players, key=lambda p: p.number):
                player_frame = ctk.CTkFrame(stats_frame)
                player_frame.pack(fill="x", pady=1)
                
                games = player.stats["games_played"]
                goals = player.stats["goals"]
                assists = player.stats["assists"]
                
                stats = [
                    ("Games Played", str(games)),
                    ("Goals", str(goals)),
                    ("Assists", str(assists)),
                    ("Goals per Game", f"{goals/games:.2f}" if games > 0 else "0.00"),
                    ("Assists per Game", f"{assists/games:.2f}" if games > 0 else "0.00")
                ]
                
                for i, (label, value) in enumerate(stats):
                    stat_label = ctk.CTkLabel(player_frame, text=f"{label}:", font=("Arial", 12))
                    stat_label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
                    
                    stat_value = ctk.CTkLabel(player_frame, text=value, font=("Arial", 12))
                    stat_value.grid(row=i, column=1, sticky="w", padx=5, pady=2)

    def refresh_player_analytics_tab(self):
        for widget in self.tab_player_analytics.winfo_children():
            widget.destroy()
        self.build_player_analytics_tab()

    # ----------> Tab 5: Team Analytics <---------
    def build_team_analytics_tab(self):
        if not self.active_team or self.active_team not in self.teams:
            frame = ctk.CTkFrame(self.tab_team_analytics)
            frame.pack(padx=20, pady=20, fill="both", expand=True)
            
            msg = ctk.CTkLabel(
                frame,
                text="Please select a team in the Club Management tab first.",
                font=("Arial", 14)
            )
            msg.pack(pady=20)
            return

        frame = ctk.CTkFrame(self.tab_team_analytics)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        team = self.teams[self.active_team]
        
        # Team Overview Section
        overview_frame = ctk.CTkFrame(frame)
        overview_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            overview_frame,
            text=f"Team Analytics: {team.name}",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Calculate team statistics
        total_goals = team.total_goals()
        avg_goals = team.avg_GFPG()
        avg_conceded = team.avg_GAPG()
        
        stats = [
            ("Games Played", str(team.stats["games"])),
            ("Wins", str(team.stats["wins"])),
            ("Draws", str(team.stats["draws"])),
            ("Losses", str(team.stats["losses"])),
            ("Goals Scored", str(total_goals)),
            ("Goals Conceded", str(team.stats["GA"])),
            ("Average Goals For", f"{avg_goals:.2f}"),
            ("Average Goals Against", f"{avg_conceded:.2f}")
        ]

        # Create a frame for each row of stats (3 stats per row)
        for i in range(0, len(stats), 3):
            row_frame = ctk.CTkFrame(overview_frame)
            row_frame.pack(fill="x", padx=5, pady=5)
            
            # Create stats for this row
            for j in range(3):
                if i + j < len(stats):
                    label, value = stats[i + j]
                    
                    stat_container = ctk.CTkFrame(row_frame)
                    stat_container.pack(side="left", expand=True, fill="both", padx=5)
                    
                    label_widget = ctk.CTkLabel(
                        stat_container,
                        text=label,
                        font=("Arial", 12)
                    )
                    label_widget.pack(pady=2)
                    
                    value_widget = ctk.CTkLabel(
                        stat_container,
                        text=value,
                        font=("Arial", 14, "bold")
                    )
                    value_widget.pack(pady=2)

        # Top Performers Section
        performers_frame = ctk.CTkFrame(frame)
        performers_frame.pack(fill="x", padx=10, pady=10)
        
        performers_label = ctk.CTkLabel(
            performers_frame,
            text="Top Performers",
            font=("Arial", 14, "bold")
        )
        performers_label.pack(pady=5)

        # Top Scorers
        scorers = sorted(
            [p for p in team.players if p.stats["goals"] > 0],
            key=lambda p: p.stats["goals"],
            reverse=True
        )[:3]

        if scorers:
            scorers_text = "Top Scorers:\n" + "\n".join(
                f"{p.name}: {p.stats['goals']} goals" for p in scorers
            )
        else:
            scorers_text = "Top Scorers:\nNo goals scored yet"

        scorers_label = ctk.CTkLabel(
            performers_frame,
            text=scorers_text,
            justify="left"
        )
        scorers_label.pack(pady=5, padx=10, anchor="w")

        # Top Assisters
        assisters = sorted(
            [p for p in team.players if p.stats["assists"] > 0],
            key=lambda p: p.stats["assists"],
            reverse=True
        )[:3]

        if assisters:
            assisters_text = "Top Assisters:\n" + "\n".join(
                f"{p.name}: {p.stats['assists']} assists" for p in assisters
            )
        else:
            assisters_text = "Top Assisters:\nNo assists recorded yet"

        assisters_label = ctk.CTkLabel(
            performers_frame,
            text=assisters_text,
            justify="left"
        )
        assisters_label.pack(pady=5, padx=10, anchor="w")

    def refresh_team_analytics_tab(self):
        for widget in self.tab_team_analytics.winfo_children():
            widget.destroy()
        self.build_team_analytics_tab()

    # ----------> Tab 6: Club Management <---------
    def build_club_management_tab(self):
        frame = ctk.CTkFrame(self.tab_club_management)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Team selection section
        selection_frame = ctk.CTkFrame(frame)
        selection_frame.pack(fill="x", padx=10, pady=10)

        team_list_label = ctk.CTkLabel(selection_frame, text="Teams:", font=("Arial", 14, "bold"))
        team_list_label.pack(anchor="w", padx=10, pady=5)

        # Get team names, ensuring no None values
        team_names = [name for name in self.teams.keys() if name is not None]

        def on_team_select(choice):
            if choice != "No Teams":
                self.selected_team_var.set(choice)
                # Enable buttons when a valid team is selected
                set_active_btn.configure(state="normal")
                delete_team_btn.configure(state="normal")
            else:
                set_active_btn.configure(state="disabled")
                delete_team_btn.configure(state="disabled")

        team_dropdown = ctk.CTkOptionMenu(
            selection_frame,
            variable=self.selected_team_var,
            values=team_names if team_names else ["No Teams"],
            width=200,
            command=on_team_select
        )
        team_dropdown.pack(pady=5)

        # Team actions section
        actions_frame = ctk.CTkFrame(frame)
        actions_frame.pack(fill="x", padx=10, pady=10)

        def set_active_team():
            team_name = self.selected_team_var.get()
            if team_name and team_name != "No Teams":
                try:
                    # Load team from database to ensure we have latest data
                    team = Team.load_from_db(team_name)
                    if team:
                        self.teams[team_name] = team
                        self.active_team = team_name
                        
                        # Reset team management state
                        self.selected_player = None  # Clear selected player
                        
                        # Refresh all tabs
                        self.refresh_club_management_tab()  # Refresh first to show updated info
                        self.refresh_team_management_tab()
                        self.refresh_player_analytics_tab()
                        self.refresh_team_analytics_tab()
                        self.refresh_match_simulator_tab()
                        
                        messagebox.showinfo("Success", f"Active team set to '{team_name}'")
                except DatabaseError as e:
                    messagebox.showerror("Database Error", str(e))

        def delete_team():
            team_name = self.selected_team_var.get()
            if team_name == "No Teams" or team_name not in self.teams:
                return
                
            if messagebox.askyesno("Confirm Delete", 
                f"Are you sure you want to delete team '{team_name}'?\nThis action cannot be undone!"):
                try:
                    team = self.teams[team_name]
                    # Delete from database
                    self.db.delete_team(team.id)
                    # Remove from local teams dict
                    del self.teams[team_name]
                    
                    # Update active team if needed
                    if self.active_team == team_name:
                        self.active_team = None
                    
                    # Update dropdown and selection
                    remaining_teams = list(self.teams.keys())
                    if remaining_teams:
                        team_dropdown.configure(values=remaining_teams)
                        self.selected_team_var.set(remaining_teams[0])
                    else:
                        team_dropdown.configure(values=["No Teams"])
                        self.selected_team_var.set("No Teams")
                        set_active_btn.configure(state="disabled")
                        delete_team_btn.configure(state="disabled")
                    
                    # Refresh all tabs
                    self.refresh_club_management_tab()
                    self.refresh_team_management_tab()
                    self.refresh_player_analytics_tab()
                    self.refresh_team_analytics_tab()
                    self.refresh_match_simulator_tab()
                    
                    messagebox.showinfo("Success", "Team deleted successfully")
                    
                except DatabaseError as e:
                    messagebox.showerror("Database Error", str(e))

        # Buttons
        button_frame = ctk.CTkFrame(actions_frame)
        button_frame.pack(fill="x", pady=5)

        # Create buttons with proper initial states
        set_active_btn = ctk.CTkButton(
            button_frame, 
            text="Set Active Team",
            command=set_active_team,
            state="normal" if team_names and self.selected_team_var.get() != "No Teams" else "disabled"
        )
        set_active_btn.pack(side="left", padx=5, expand=True)

        create_team_btn = ctk.CTkButton(
            button_frame,
            text="Create New Team",
            command=lambda: self.tabview.set("Team Initiation")
        )
        create_team_btn.pack(side="left", padx=5, expand=True)

        delete_team_btn = ctk.CTkButton(
            button_frame,
            text="Delete Team",
            command=delete_team,
            state="normal" if team_names and self.selected_team_var.get() != "No Teams" else "disabled"
        )
        delete_team_btn.pack(side="left", padx=5, expand=True)

        # Team info section - only show if there's an active team
        if self.active_team and self.active_team in self.teams and self.active_team == self.selected_team_var.get():
            team = self.teams[self.active_team]
            info_frame = ctk.CTkFrame(frame)
            info_frame.pack(fill="x", padx=10, pady=10)
            
            header_frame = ctk.CTkFrame(info_frame)
            header_frame.pack(fill="x", pady=5)
            
            active_label = ctk.CTkLabel(
                header_frame,
                text="Active Team Information",
                font=("Arial", 14, "bold")
            )
            active_label.pack(side="left", padx=10)
            
            active_indicator = ctk.CTkLabel(
                header_frame,
                text="● ACTIVE",
                text_color="green",
                font=("Arial", 12, "bold")
            )
            active_indicator.pack(side="right", padx=10)
            
            info_text = (
                f"Team: {team.name}\n"
                f"Coach: {team.coach.name if team.coach else 'No Coach'}\n"
                f"Players: {len(team.players)}\n"
                f"Games Played: {team.stats['games']}\n"
                f"Record: {team.stats['wins']}W - {team.stats['draws']}D - {team.stats['losses']}L\n"
                f"Goals For: {team.stats['GF']}\n"
                f"Goals Against: {team.stats['GA']}"
            )
            
            ctk.CTkLabel(
                info_frame,
                text=info_text,
                justify="left"
            ).pack(pady=5, padx=10)

    def refresh_club_management_tab(self):
        for widget in self.tab_club_management.winfo_children():
            widget.destroy()
        self.build_club_management_tab()
    


if __name__ == "__main__":
    app = TeamManagerApp()
    app.mainloop()