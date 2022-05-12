from volleyball.stat.message.Message import Message


class SubstituteMessage(Message):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int = 0):
        super(SubstituteMessage, self).__init__(index, back_num, name, success_failure)

    def find_substituted_name(self, messages):
        return 0


class SubstituteOutMessage(SubstituteMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int = 0):
        super(SubstituteOutMessage, self).__init__(index, back_num, name, success_failure)

    def find_substituted_name(self, messages):
        return messages[self.index + 1].name


class SubstituteInMessage(SubstituteMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int = 0):
        super(SubstituteInMessage, self).__init__(index, back_num, name, success_failure)

    def find_substituted_name(self, messages):
        return messages[self.index - 1].name

