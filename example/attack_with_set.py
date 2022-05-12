from volleyball.stat.StatMaker import *

stat_file = StatFile("C:\\Users\\user\\Documents\\배구", ["여자부"], [2021], list(range(1, 300)))
stat_file.fill_games()
stat_file.fill_sets()
stat_file.fill_messages()
stat_file.fill_rallies()
stat_file.fill_chances()


class PlayerWithAttackType(Player):
    def __init__(self, name: str, back_num: int, season: int, team: str, attack_type: str):
        super().__init__(name, back_num, season, team)
        self.attack_type = attack_type


attacks_after_other_player_calc_eff = EffCalc({})

attacks_after_all_setter_calc_eff = EffCalc({})


def processor_in_set(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: Set):
    all_setter_set_messages = messages[0].find_set_of_setters(game, rallies, Rally.LEFT)

    attacks_after_all_setter_messages = messages[0].select_attack_messages_after_set(all_setter_set_messages)

    attacks_after_other_player = messages[0].select_messages_with_action("공격종합") - attacks_after_all_setter_messages

    for attack_after_other_player in attacks_after_other_player:
        attacks_after_other_player_calc_eff.append_effect_calc(Messages([attack_after_other_player]), game, "공격종합", PlayerWithAttackType, take_key_by_value(action_to_class, type(attack_after_other_player)))

    for attack_after_all_setter in attacks_after_all_setter_messages:
        attacks_after_all_setter_calc_eff.append_effect_calc(Messages([attack_after_all_setter]), game, "공격종합", PlayerWithAttackType, take_key_by_value(action_to_class, type(attack_after_all_setter)))

    all_setter_set_messages = messages[1].find_set_of_setters(game, rallies, Rally.LEFT)

    attacks_after_all_setter_messages = messages[1].select_attack_messages_after_set(all_setter_set_messages)

    attacks_after_other_player = messages[1].select_messages_with_action("공격종합") - attacks_after_all_setter_messages

    for attack_after_other_player in attacks_after_other_player:
        attacks_after_other_player_calc_eff.append_effect_calc(Messages([attack_after_other_player]), game, "공격종합",
                                                               PlayerWithAttackType
                                                               , take_key_by_value(action_to_class
                                                               , type(attack_after_other_player)))

    for attack_after_all_setter in attacks_after_all_setter_messages:
        attacks_after_all_setter_calc_eff.append_effect_calc(Messages([attack_after_all_setter]), game, "공격종합",
                                                             PlayerWithAttackType, take_key_by_value(action_to_class
                                                             , type(attack_after_all_setter)))


stat_file.process_in_set(processor_in_set)

print("세터의 세트 후")

for attack_type in attack_types:
    one_attack_type_eff_calc = filter(lambda one_eff: one_eff[0].attack_type == attack_type, attacks_after_all_setter_calc_eff.items())
    print(attack_type)
    EffCalc(one_attack_type_eff_calc).print_overall_effect()

print("세터가 아닌 선수의 세트 후")

for attack_type in attack_types:
    one_attack_type_eff_calc = filter(lambda one_eff: one_eff[0].attack_type == attack_type, attacks_after_other_player_calc_eff.items())
    print(attack_type)
    EffCalc(one_attack_type_eff_calc).print_overall_effect()

