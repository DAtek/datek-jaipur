class JaipurError(Exception):
    pass


class EventAlreadyAppliedError(JaipurError):
    pass


class EventNotAppliedError(JaipurError):
    pass


class ExactlyTwoPlayersRequiredError(JaipurError):
    pass


class DataNotCollectedError(JaipurError):
    pass
