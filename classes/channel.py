class Channel:
    def __init__(self, id, login_name, channel_name, language, last_game_name, last_game_id, stream_title, stream_tags, classification_labels, is_branded_content):
        self.id = id
        self.login_name = login_name
        self.channel_name = channel_name
        self.language = language
        self.last_game_name = last_game_name
        self.last_game_id = last_game_id
        self.stream_title = stream_title
        self.stream_tags = stream_tags
        self.classification_labels = classification_labels
        self.is_branded_content = is_branded_content
