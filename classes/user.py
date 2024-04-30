class User:
    def __init__(self, id, login_name, user_name, user_type, broadcast_contract_type, channel_description, created_at):
        self.id = id
        self.login_name = login_name
        self.user_name = user_name
        self.user_type = user_type
        self.broadcast_contract_type = broadcast_contract_type
        self.channel_description = channel_description
        self.created_at = created_at