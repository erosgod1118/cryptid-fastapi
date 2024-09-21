class DataMissingError(Exception):
    def __init__(self, pMsg: str):
        self.msg = pMsg

class DataDuplicationError(Exception):
    def __init__(self, pMsg: str):
        self.msg = pMsg