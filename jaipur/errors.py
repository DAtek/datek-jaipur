class JaipurError(Exception):
    pass


class EventAlreadyAppliedError(JaipurError):
    pass


class ExactlyTwoPlayersRequiredError(JaipurError):
    pass
