from volleyball.stat.StatMaker import *
from statistics import stdev, mean
from scipy import stats
import numpy as np
import seaborn as sns

stat_file = StatFile("C:\\Users\\user\\Documents\\배구", ["여자부"], [2021], list(range(1, 300)))
stat_file.fill_games()
stat_file.fill_sets()
stat_file.fill_messages()
stat_file.fill_rallies()
stat_file.fill_chances()


class PlayerWithAttackTypeAndGameNum(Player):
    def __init__(self, name: str, back_num: int, season: int, team: str, attack_type: str, game_num: int):
        super().__init__(name, back_num, season, team)
        self.attack_type = attack_type
        self.game_num = game_num

    def __eq__(self, other):
        if isinstance(self, PlayerWithAttackTypeAndGameNum):
            return self.game_num == other.game_num and super().__eq__(other)
        return NotImplemented

    def __hash__(self):
        return super().__hash__()


effCalc = EffCalc({})


def processor_in_set_messages_by_messages(messages: Messages
                                          , chances: Chances
                                          , rallies: Rallies
                                          , game: Game
                                          , set_in_game: Set
                                          , side: int):
    attack_messages = messages.select_messages_with_action("공격종합")
    for message in attack_messages:
        attack_type = take_key_by_value(action_to_class, type(message))
        effCalc.append_effect_calc(Messages([message])
                                   , game
                                   , "공격종합"
                                   , PlayerWithAttackTypeAndGameNum
                                   , attack_type
                                   , game.game_num)


stat_file.process_in_set_messages_by_messages(processor_in_set_messages_by_messages)

for team in women_teams_after_2021_2022:
    team_calcEff = EffCalc(filter(lambda item: item[0].team == team, effCalc.items()))

    team_efficiencies = []
    for i in range(0, 300):
        game_calcEff = EffCalc(filter(lambda item: item[0].game_num == i, team_calcEff.items()))
        if len(game_calcEff.items()) > 0:
            eff = game_calcEff.return_whole_eff()
            team_efficiencies.append(make_percentage(eff[0], eff[1]-eff[2]))

    print(mean(team_efficiencies), f"{team} 공격 종합 효율 평균")
    print(stdev(team_efficiencies), f"{team} 공격 종합 효율 표준 편차")

    print(team_efficiencies)

    for i, attack_type in enumerate(attack_types):
        team_attack_type_calcEff = EffCalc(filter(lambda item: item[0].attack_type == attack_type, team_calcEff.items()))

        efficiencies = []
        for v in range(0, 300):
            game_calcEff = EffCalc(filter(lambda item: item[0].game_num == v, team_attack_type_calcEff.items()))
            if len(game_calcEff.items()) > 0:
                eff = game_calcEff.return_whole_eff()
                efficiencies.append(make_percentage(eff[0], eff[1] - eff[2]))

        print(mean(efficiencies), f"{team} {attack_type} 효율 평균")
        print(stdev(efficiencies), f"{team} {attack_type} 공격 효율 표준 편차")

        print(team_efficiencies)


