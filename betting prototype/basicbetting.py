#Initialize user
class User:
    def __init__(self, username, password, funds, bet_Amount):
        self.username = username
        self.password = password
        self.funds = funds
        self.bet_Amount = bet_Amount

    def check_Funds(self):
        return self.funds

    def add_Funds(self):
        add_amount = int(input("How much funds you want to add?: "))
        self.funds += add_amount

    def withdraw_Funds(self):
        withdraw_amount = int(input("How much funds you want to withdraw?: "))
        self.funds -= withdraw_amount

class Match:
    def __init__(self, first_Team, second_Team, players_First_Team, players_Second_Team, amount_Of_Maps):
        self.first_Team = first_Team
        self.second_Team = second_Team
        self.players_First_Team = players_First_Team
        self.players_Second_Team = players_Second_Team
        self.amount_Of_Maps = amount_Of_Maps


    def match_Statistics(self):
        print("         Best of:" + str(self.amount_Of_Maps))
        print(self.first_Team + "     vs     " + self.second_Team)
        for i in range(0,len(self.players_First_Team)):
            print(self.players_First_Team[i]+ "            " + self.players_Second_Team[i])


class Betting(Match):
    def __init__(self,first_Team, second_Team, players_First_Team, players_Second_Team, amount_Of_Maps, first_Team_Bet_Amount, second_Team_Bet_Amount, total_Bet_Amount):
        super().__init__(first_Team, second_Team, players_First_Team, players_Second_Team, amount_Of_Maps)
        self.first_Team_Bet_Amount = first_Team_Bet_Amount
        self.second_Team_Bet_Amount = second_Team_Bet_Amount
        self.total_Bet_Amount = total_Bet_Amount
        self.team_One_Bettors = []
        self.team_Two_Bettors = []

    def choose_Betting(self, user):
        choice = input("Choose " + self.first_Team + " or " + self.second_Team + " to bet: ")
        
        if choice == self.first_Team:
            amount = int(input("How much do you want to bet?: "))
            if amount > 0:
                self.first_Team_Bet_Amount += amount
                self.total_Bet_Amount += amount
                user.funds -= amount
                user.bet_Amount += amount
                
                self.team_One_Bettors.append([user, amount])
                #print(self.team_One_Bettors)

                for user in self.team_One_Bettors:
                    print(user[1])
                

        if choice == self.second_Team:
            amount = int(input("How much do you want to bet?: "))
            if amount > 0:
                self.second_Team_Bet_Amount += amount
                self.total_Bet_Amount += amount
                user.funds -= amount
                user.bet_Amount += amount

                self.team_Two_Bettors.append([user, amount])
                #print(self.team_Two_Bettors)

        #Shows how much has been bet on team1 and team2
    def return_Bet_Amount(self):
        print(self.first_Team + " Total bet amount: " + str(self.first_Team_Bet_Amount) + " - " + self.second_Team + " Total bet amount: " + str(self.second_Team_Bet_Amount))


    #Odds are calculated from both teams
    def return_Team_Odds(self):
        team_One_Odds = self.second_Team_Bet_Amount/self.first_Team_Bet_Amount
        team_Two_Odds = self.first_Team_Bet_Amount/self.second_Team_Bet_Amount
 
        print(self.first_Team + " odds: " + str(team_One_Odds))
        print(self.second_Team + " odds: " + str(team_Two_Odds))


    def choose_Winner(self):
        #Odds from both of the teams to calculate winnings
        team_One_Odds = self.second_Team_Bet_Amount/self.first_Team_Bet_Amount
        team_Two_Odds = self.first_Team_Bet_Amount/self.second_Team_Bet_Amount
        
        winner = input("Input winner: " + self.first_Team + " or " + self.second_Team + ": ")

        if winner == self.first_Team:
            #Gets their own bet back and winnings
            for user in self.team_One_Bettors:
                #Adds funds to the user who bet on team1
                user[0].funds += user[1]*team_One_Odds
                print(user[0].username + " Won: " + str(user[0].funds-user[1]))
                
        if winner == self.second_Team:
            #Gets their own bet back and winnings
            for user in self.team_Two_Bettors:
                #Adds funds to the user who bet on team1
                user[0].funds += user[1]*team_One_Odds
                print(user[0].username + " Won: " + str(user[0].funds-user[1]))

        #Reset bet amount to 0 since match is over
        for user in self.team_One_Bettors:
                #Reset bet amount to 0
                user[0].bet_Amount = 0
                print(user[0].funds)
                
        for user in self.team_Two_Bettors:
                #Reset bet amount to 0
                user[0].bet_Amount = 0
                print(user[0].funds)
        
        
#Initializing users, add funds to the users
user1 = User("pek", "password", 0, 0)
user1.add_Funds()

user2 = User("hes", "password", 0, 0)
user2.add_Funds()

user3 = User("ems", "password", 0, 0)
user3.add_Funds()

user4 = User("dems", "password", 0, 0)
user4.add_Funds()


#Initialize match to bet on
match1 = Betting("Finland","Germany",["player1","player2","player3","player4","player5"],["player6","player7","player8","player9","player10"], 3,0,0,0)

#Users can choose which team to bet on
match1.choose_Betting(user1)
match1.choose_Betting(user2)
match1.choose_Betting(user3)
match1.choose_Betting(user4)

#Return bet amount of both teams and odds for both teams
match1.return_Bet_Amount()
match1.return_Team_Odds()

#Choose winner of the match
match1.choose_Winner()

