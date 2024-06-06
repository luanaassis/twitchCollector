class Video:
    def __init__(self, video_id, stream_id, user_id, user_login_name, user_name,video_title,video_description,published_at, view_count, language, type):
        self.video_id = video_id
        self.stream_id = stream_id
        self.user_id = user_id
        self.user_login_name = user_login_name
        self.user_name = user_name
        self.video_title = video_title
        self.video_description = video_description
        self.published_at = published_at
        self.view_count = view_count
        self.language = language
        self.type = type