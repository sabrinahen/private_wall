from flask_app.config.mysqlconnection import connectToMySQL

class Message:
    db_name = 'private_wall_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.sender = data['sender']
        self.receiver_id = data['receiver_id']
        self.reciever = data['receiver']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_user_messages(cls,data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE users2.id =  %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        messages = []
        for message in results:
            messages.append( cls(message) )
        return messages

    @classmethod
    def save(cls,data):
        query = "INSERT INTO messages (content,sender_id,receiver_id) VALUES (%(content)s,%(sender_id)s,%(receiver_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)