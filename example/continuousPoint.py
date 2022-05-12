from volleyball.stat.StatMaker import *

stat_file = StatFile("C:\\Users\\user\\Documents\\배구", ["여자부"], [2022], list(range(1, 137)))
stat_file.fill_games()
stat_file.fill_sets()
stat_file.fill_messages()
stat_file.fill_rallies()
stat_file.fill_chances()

after_blocked = []
after_attack_fault = []
after_serve_fault = []
after_receive_fault = []
after_opponent_attack_success = []

after_blocking = []
after_serve_ace = []
after_attack_success = []
after_opponent_fault = []


# noinspection PyUnresolvedReferences
def processor_in_set(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: Set):
    for i, rally in enumerate(rallies):
        next_rally_result = rally.winner
        continuous_point = (lambda winner: -1 if winner == Rally.RIGHT else 1)(rally.winner)
        for next_rally in rallies[i + 1:]:
            if next_rally_result == next_rally.winner and continuous_point < 0:
                continuous_point -= 1
            elif next_rally_result == next_rally.winner and continuous_point > 0:
                continuous_point += 1
            else:
                break

        before_last_message_of_rally = messages[Rally.LEFT][rally.message_index[1] - 1]
        before_last_opponent_message_of_rally = messages[Rally.RIGHT][rally.message_index[1] - 1]
        last_message_of_rally = messages[Rally.LEFT][rally.message_index[1]]
        last_opponent_message_of_rally = messages[Rally.RIGHT][rally.message_index[1]]
        if before_last_message_of_rally.is_right(message_type=AttackMessage, success_failure=Message.FAILURE) \
                and not last_opponent_message_of_rally.is_right(message_type=BlockMessage):
            after_attack_fault.append(continuous_point)
        elif before_last_message_of_rally.is_right(ServeMessage, Message.FAILURE):
            after_serve_fault.append(continuous_point)
        elif before_last_message_of_rally.is_right(AttackMessage, Message.FAILURE)\
                or last_opponent_message_of_rally.is_right(BlockAssistMessage):
            after_blocked.append(continuous_point)
        elif last_message_of_rally.is_right(ReceiveMessage, Message.FAILURE):
            after_receive_fault.append(continuous_point)
        elif last_opponent_message_of_rally.is_right(ReceiveMessage, Message.FAILURE):
            if continuous_point < 0:
                print(game.game_num, set_in_game.index + 1, rally.winner, "서브 에이스")
                print(before_last_message_of_rally.__dict__, before_last_opponent_message_of_rally.__dict__, last_message_of_rally.__dict__, last_opponent_message_of_rally.__dict__)
                print(before_last_message_of_rally, before_last_opponent_message_of_rally, last_message_of_rally, last_opponent_message_of_rally)
            after_serve_ace.append(continuous_point)
        elif before_last_opponent_message_of_rally.is_right(AttackMessage, Message.SUCCESS):
            after_opponent_attack_success.append(continuous_point)
        elif before_last_message_of_rally.is_right(AttackMessage, Message.SUCCESS):
            after_attack_success.append(continuous_point)
        elif last_message_of_rally.is_right(TeamMessage, Message.SUCCESS):
            after_opponent_fault.append(continuous_point)
        elif before_last_opponent_message_of_rally.is_right(AttackMessage, Message.FAILURE) \
                or last_message_of_rally.is_right(BlockAssistMessage):
            if continuous_point < 0:
                print(game.game_num, set_in_game.index + 1, rally.winner, "블로킹")
                print(before_last_message_of_rally.__dict__, before_last_opponent_message_of_rally.__dict__, last_message_of_rally.__dict__, last_opponent_message_of_rally.__dict__)
                print(before_last_message_of_rally, before_last_opponent_message_of_rally, last_message_of_rally, last_opponent_message_of_rally)
            after_blocking.append(continuous_point)

        # after_blocking = []
        # after_serve_ace = []
        # after_attack_success = []
        # after_opponent_fault = []


stat_file.process_in_set(processor_in_set)

print(after_attack_success)
print(after_blocking)
print(after_serve_ace)
# print(after_opponent_fault)
print("")
# print(after_blocked)
print(after_opponent_attack_success)
# print(after_receive_fault)
print(after_serve_fault)
print(after_attack_fault)
