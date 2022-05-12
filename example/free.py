from volleyball.stat.StatMaker import *

stat_file = StatFile("C:\\Users\\user\\Documents\\배구", ["여자부"], [2022], list(range(1, 153)))
stat_file.fill_games()
stat_file.fill_sets()
stat_file.fill_messages()
stat_file.fill_rallies()
stat_file.fill_chances()

kim_in_opposite = EffCalc({})
latham_in_opposite = EffCalc({})


def processor_in_set_messages_by_messages(messages: Messages
                                          , chances: Chances
                                          , rallies: Rallies
                                          , game: Game
                                          , set_in_game: Set
                                          , side: int):
    for chance in chances:
        if chance.message_index[1] - chance.message_index[0] == 1:
            for i in range(chance.message_index[0], chance.message_index[1] + 1):
                print(messages[i].make_description())
            print("----------------------------------")
    if game.teams[side] == "IBK기업은행":
        for rally in rallies:
            if "김하경" in rally.rotation[side]:
                if "김희진" == rally.rotation[side][find_opposite_num_in_volleyball(rally.rotation[side].index("김하경"))]:
                    kim_in_opposite.append_effect_calc(messages.slice_messages_with_rallies(Rallies([rally]))
                                                       , game
                                                       , "공격종합")
                elif "라셈" == rally.rotation[side][find_opposite_num_in_volleyball(rally.rotation[side].index("김하경"))]:
                    latham_in_opposite.append_effect_calc(messages.slice_messages_with_rallies(Rallies([rally]))
                                                          , game
                                                          , "공격종합")
            elif "이진" in rally.rotation[side]:
                if "김희진" == rally.rotation[side][find_opposite_num_in_volleyball(rally.rotation[side].index("이진"))]:
                    kim_in_opposite.append_effect_calc(messages.slice_messages_with_rallies(Rallies([rally]))
                                                       , game
                                                       , "공격종합")
                elif "라셈" == rally.rotation[side][find_opposite_num_in_volleyball(rally.rotation[side].index("이진"))]:
                    latham_in_opposite.append_effect_calc(messages.slice_messages_with_rallies(Rallies([rally]))
                                                          , game
                                                          , "공격종합")


stat_file.process_in_set_messages_by_messages(processor_in_set_messages_by_messages)

kim_in_opposite.print_effect_with_name()
latham_in_opposite.print_effect_with_name()


