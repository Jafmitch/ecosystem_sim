class CustomException(Exception):
    def __init__(self, strOrList):
        if strOrList is list:
            theList = strOrList
            Exception.__init__(self, "".join(theList))
        elif strOrList is str:
            theStr = strOrList
            Exception.__init__(self, theStr)
