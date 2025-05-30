import customtkinter as ctk
from models import Team, Player, Match

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TeamManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sports Team Manager")
        self.geometry("900x600")

        # Tab System
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        # Create tabs
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
        pass

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
