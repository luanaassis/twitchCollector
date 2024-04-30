class Stream:
    def __init__(self, stream_id, user_id, user_login_name, user_name, language, game_name, game_id, stream_title, stream_tags, type, viewer_count, is_mature):
        self.stream_id = stream_id
        self.user_id = user_id
        self.user_login_name = user_login_name
        self.user_name = user_name
        self.language = language
        self.game_name = game_name
        self.game_id = game_id
        self.stream_title = stream_title
        self.stream_tags = stream_tags
        self.type = type
        self.viewer_count = viewer_count
        self.is_mature = is_mature
