from volleyball.stat.StatMaker import *
from scipy import stats
import numpy as np
import seaborn as sns


stat_file = StatFile("C:\\Users\\user\\Documents\\배구", ["여자부"], [2022], list(range(1, 103)))
stat_file.fill_games()
stat_file.fill_sets()
stat_file.fill_messages()
stat_file.fill_rallies()
stat_file.fill_chances()

shareCalc = ShareCalc({})


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

team_calcEff = EffCalc(filter(lambda item: item[0].team == "한국도로공사", effCalc.items()))

team_efficiencies = []
for i in range(0, 300):
    game_calcEff = EffCalc(filter(lambda item: item[0].game_num == i, team_calcEff.items()))
    if len(game_calcEff.items()) > 0:
        eff = game_calcEff.return_whole_eff()
        team_efficiencies.append(make_percentage(eff[0], eff[1] - eff[2]))

fig = plt.figure(figsize=(20, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

np_team_efficiencies = np.array(team_efficiencies)

stats.probplot(team_efficiencies, dist=stats.norm, plot=ax1)
mu = np_team_efficiencies.mean()
variance = np_team_efficiencies.var()
sigma = variance ** 0.5
x = np.linspace(mu - sigma*3, mu + sigma*3, 20)
ax2.plot(x, stats.norm.pdf(x, mu, sigma), color="red", label="theoretical")

sns.distplot(ax=ax2, a=np_team_efficiencies, bins=20, color="blue", label="observed")
ax2.legend()

plt.savefig(f"./도로공사 공격 종합 정규 분포 검정.png")
