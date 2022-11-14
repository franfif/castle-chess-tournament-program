class Message:
    #
    # Greeting and Navigation Messages
    #
    PROGRAM_NAME = 'Castle Chess Tournament Manager'
    with open('img/CastleChessLogo-ascii-art.txt') as f:
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
    CREATE_TOURNAMENT_MENU = 'Add a new tournament'
    CREATE_PLAYER_MENU = 'Add a new player'
    EDIT_PLAYERS_MENU = 'Edit players'
    SELECT_PLAYERS = 'Select the participants'

    #
    # Menu Options
    #
    ALPHABETICAL = 'Alphabetical'
    RANKING = 'Ranking'
    SAVE_AND_EXIT_MENU = 'Save and go back'
    EXIT_MENU = 'Go back'
    LEAVE_APP_MENU = 'Leave the app'

    # Edit player menu
    UPDATE_FIRST_NAME = 'Change first name'
    UPDATE_LAST_NAME = 'Change last name'
    UPDATE_DATE_OF_BIRTH = 'Change date of birth'
    UPDATE_GENDER = 'Change gender'
    UPDATE_RANKING = 'Change ranking'

    # Run tournament menu
    EDIT_TOURNAMENT = 'Edit tournament information'
    ADD_REMOVE_TOURNAMENT_PLAYERS = 'Add/Remove tournament players'
    END_TOURNAMENT_ROUND = 'End round'
    START_TOURNAMENT_ROUND = 'Start round'
    SHOW_PLAYERS = 'Show players'
    SHOW_ROUNDS = 'Show all rounds'

    # Edit tournament menu
    UPDATE_TOURNAMENT_NAME = 'Change tournament name'
    UPDATE_VENUE = 'Change venue'
    UPDATE_DATES = 'Change dates'
    UPDATE_NUMBER_OF_ROUNDS = 'Change number of rounds'
    UPDATE_TIME_CONTROL = 'Change time control'
    RESET_DESCRIPTION = 'Reset description'
    INCREMENT_DESCRIPTION = 'Add to description'

    #
    # Notices
    #
    NO_MORE_PAIRINGS = 'All the players payed against each other. \n' \
                       'There is no more match to play in this tournament. \n \n'
    NO_MORE_ROUNDS = 'All rounds have been played. \n \n'
    TOURNAMENT_OVER = 'This tournament is now over. \n' \
                      'It will be available in the Archived Tournaments and in the Reports. \n'
    NO_TOURNAMENTS = 'No tournaments to show.'
    NO_PLAYERS = 'No players to show.'
