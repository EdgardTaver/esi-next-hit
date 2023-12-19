class EmailAlreadyRegisteredException(Exception):
    pass

class PlaylistAlreadyExistsException(Exception):
    pass

class MusicAlreadyInPlaylistException(Exception):
    pass

class PlaylistNotFoundException(Exception):
    pass

class MusicNotFoundException(Exception):
    pass