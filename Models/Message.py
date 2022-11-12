class Message:
    #
    # Greeting and Navigation Messages
    #
    PROGRAM_NAME = 'Castle Chess Tournament Manager'
    with open('CastleChessLogo-ascii-art.txt') as f:
        LOGO_ASCII = f.read()
    WELCOME = '~ Welcome! ~'
    START_PROGRAM = 'Press Enter to start...'
    GOOD_BYE = 'Thank you for playing! See you next time!'

    #
    # Titles
    #
    MAIN_MENU = PROGRAM_NAME
    ONGOING_TOURNAMENT_MENU = 'Tournament'
    ARCHIVED_TOURNAMENT_MENU = 'Archived Tournaments'
    REPORT_MENU = 'Reports'
    TOURNAMENTS_TITLE = 'Tournaments'
    ROUNDS_TITLE = 'Rounds'
    PLAYERS_TITLE = 'Players'
    STARTING = 'Starting '
    ENDING = 'Ending '
    CREATE_PLAYERS_MENU = 'Add a new player'
    EDIT_PLAYERS_MENU = 'Edit players'
    SELECT_PLAYERS = 'Select the participants'

    #
    # Menu Options
    #
    ALPHABETICAL = 'Alphabetical'
    RANKING = 'Ranking'
    EXIT_MENU = '** Go back **'

    #
    # Notices
    #
    NO_MORE_PAIRINGS = 'All the players payed against each other, there is no more match to play in this tournament.'
    TOURNAMENT_OVER = 'The tournament is now over.'
    NO_TOURNAMENTS = 'No tournaments to show.'
    NO_PLAYERS = 'No players to show.'
