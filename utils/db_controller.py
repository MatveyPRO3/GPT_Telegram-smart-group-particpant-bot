import sqlite3
from os import path


class Controller:
    """Controls all operations with sqlite database"""

    def __init__(self, db_name: str = "DB") -> None:
        """Creates db if it doesn't exist, connects to db
        Args:
            db_name (str, optional) Defaults to "MessageEvents".
        """
        self.sqlite_name = db_name
        if not path.exists(f"output\\{db_name}.sqlite"):
            self._create_db()
        self.conn = sqlite3.connect(
            f"output\\{db_name}.sqlite", check_same_thread=False
        )
        self.cursor = self.conn.cursor()

    def _create_db(self) -> None:
        """Private method, used to create and init db"""
        conn = sqlite3.connect(
            f"output\\{self.sqlite_name}.sqlite", check_same_thread=False
        )
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE MessageEvents (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ChatID INTEGER,
                MessageText TEXT,
                Time TEXT,
                SenderFirstName TEXT,
                SenderLastName TEXT,
                SenderUsername TEXT,
                PromptTokensTotal INTEGER,
                CompletionTokensTotal INTEGER
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE UserSubscriptions (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ChatID INTEGER,
                TypeOfSubscription TEXT,
                NumAllowedGroups INTEGER,
                TemporaryMemorySize INTEGER,
                DateOfStart TEXT,
                SenderFirstName TEXT,
                SenderLastName TEXT,
                SenderUsername TEXT,
                TokensTotal INTEGER,
                DYNAMIC_GENERATION TINYINT,
                VOICE_INPUT TINYINT,
                VOICE_OUTPUT TINYINT,
                SphereContext TINYINT,
                Temperature TINYINT,
                FrequencyPenalty TINYINT,
                PresensePenalty TINYINT
            )
        """
        )

        conn.commit()
        cursor.close()
        conn.close()

    def add_user_with_sub(
        self,
        chat_id: int,
        type_of_subscription: str,
        num_allowed_groups: int,
        temporary_memory_size: int,
        date_of_start: int,
        sender_first_name: str,
        sender_last_name: str,
        sender_username: str,
        tokens_total: int,
        dynamic_generation: bool,
        voice_input: bool,
        voice_output: bool,
        sphere_context: bool,
        temperature: bool,
        freq_penalty: bool,
        presense_penalty: bool
    ) -> None:
        sql = """
            INSERT INTO UserSubscriptions (
                ChatID,
                TypeOfSubscription,
                NumAllowedGroups,
                TemporaryMemorySize,
                DateOfStart,
                SenderFirstName,
                SenderLastName,
                SenderUsername,
                TokensTotal,
                DYNAMIC_GENERATION,
                VOICE_INPUT,
                VOICE_OUTPUT,
                SphereContext,
                Temperature,
                FrequencyPenalty,
                PresensePenalty 
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.cursor.execute(
            sql,
            (
                chat_id,
                type_of_subscription,
                num_allowed_groups,
                temporary_memory_size,
                date_of_start,
                sender_first_name,
                sender_last_name,
                sender_username,
                tokens_total,
                int(dynamic_generation),
                int(voice_input),
                int(voice_output),
                int(sphere_context),
                int(temperature),
                int(freq_penalty),
                int(presense_penalty)
            ),
        )

        self.conn.commit()

    def add_message_event(
        self,
        chat_id: int,
        text: str,
        time: str,
        first_name: str,
        last_name: str,
        username: str,
        prompt_tokens_total: int,
        completion_tokens_total: int,
    ):
        self.cursor.execute(
            f"""
            INSERT INTO MessageEvents (ChatID, MessageText, Time, SenderFirstName, SenderLastName, SenderUsername, PromptTokensTotal, CompletionTokensTotal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                chat_id,
                text,
                time,
                first_name,
                last_name,
                username,
                prompt_tokens_total,
                completion_tokens_total,
            ),
        )
        self.conn.commit()


    def update_tokens_of_user_with_sub(self, chat_id, data) -> None:
        """Update tokens of user by chat_id"""
        
        query = "UPDATE UserSubscriptions SET TokensTotal = ? WHERE ChatID = ?"
        self.cursor.execute(query, (data, chat_id))

        self.conn.commit()

    def update_days_of_subscription_of_user_with_sub(self, chat_id, data) -> None:
        """Update days of subscription of user by chat_id"""
        
        query = "UPDATE UserSubscriptions SET DaysOfSubscription = ? WHERE ChatID = ?"
        self.cursor.execute(query, (data, chat_id))

        self.conn.commit()


    def check_the_existing_of_user_with_sub(self, chat_id) -> bool:
        """Check the existing of user in db by chat_id"""
        # Проверка наличия строки с определенным id

        query = "SELECT * FROM UserSubscriptions WHERE ChatID = ?"

        self.cursor.execute(query, (chat_id,))

        # Получение результатов
        row = self.cursor.fetchone()

        if row is None:
            return False
        else:
            return True
        

    def delete_the_existing_of_user_with_sub(self, chat_id) -> None:
        """delete data of user by chat_id"""
        
        query = "DELETE FROM UserSubscriptions WHERE ChatID = ?"
        self.cursor.execute(query, (chat_id,))

        self.conn.commit()

    def delete_the_existing_of_user_with_sub_by_date(self, date_of_start) -> None:
        """delete data of user by chat_id"""
        
        query = "DELETE FROM UserSubscriptions WHERE DateOfStart = ?"
        self.cursor.execute(query, (date_of_start,))

        self.conn.commit()


    def get_users_with_sub_by_chat_id(self, user_chat_id: int):
        """aa"""
        query = "SELECT DateOfStart FROM UserSubscriptions WHERE ChatID=?"
        self.cursor.execute(query, (user_chat_id,))
        result = self.cursor.fetchall()

        return result



    def get_first_date_of_start_of_user(self, user_chat_id: int):
        """Get the days of subscription of user by id"""
        query = "SELECT DateOfStart FROM UserSubscriptions WHERE ChatID = ? ORDER BY DateOfStart ASC LIMIT 1"
        self.cursor.execute(query, (user_chat_id,))
        result = self.cursor.fetchone()

        return result[0]
    
    def get_last_date_of_start_of_user(self, user_chat_id: int):
        """Get the days of subscription of user by id"""
        query = "SELECT DateOfStart FROM UserSubscriptions WHERE ChatID = ? ORDER BY DateOfStart DESC LIMIT 1"
        self.cursor.execute(query, (user_chat_id,))
        result = self.cursor.fetchone()

        return result[0]
    
    def get_user_with_sub_by_username(self, user_username: int) -> dict:
        """Returns dict with data about user where each key is a column name"""
        query = "SELECT * FROM UserSubscriptions WHERE SenderUsername = ? ORDER BY DateOfStart ASC LIMIT 1"
        self.cursor.execute(query, (user_username,))
        result = self.cursor.fetchone()

        if result is None:
            return {}  # User not found

        # Convert the row into a dictionary
        columns = [description[0] for description in self.cursor.description]
        users_dict = {}
        for i, column in enumerate(columns):
            if (column != "TokensTotal") and (column != "NumAllowedGroups") and (column != "TemporaryMemorySize") and (column != "TypeOfSubscription") and (column != "DateOfStart"):
                users_dict[column] = bool(result[i])
            else:
                users_dict[column] = result[i]

        return users_dict

    def get_user_with_sub_by_chat_id(self, user_chat_id: int) -> dict:
        """Returns dict with data about user where each key is a column name"""
        query = "SELECT * FROM UserSubscriptions WHERE ChatID = ? ORDER BY DateOfStart ASC LIMIT 1"
        self.cursor.execute(query, (user_chat_id,))
        result = self.cursor.fetchone()

        if result is None:
            return {}  # User not found

        # Convert the row into a dictionary
        columns = [description[0] for description in self.cursor.description]
        users_dict = {}
        for i, column in enumerate(columns):
            if (column != "TokensTotal") and (column != "NumAllowedGroups") and (column != "TemporaryMemorySize") and (column != "TypeOfSubscription") and (column != "DateOfStart"):
                users_dict[column] = bool(result[i])
            else:
                users_dict[column] = result[i]

        return users_dict

    def get_last_n_message_events_from_chat(self, n: int, chat_id: int = None):
        """Get last n rows from db in list format

        Args:
            n (int): number of rows
            chat_id (int, optional): If set, returns n last rows with specified id. Defaults to None.

        Returns:
            list
        """
        self.cursor.execute(
            f"""
            SELECT * FROM MessageEvents
            {"WHERE ChatID = ?" if chat_id else ""}
            ORDER BY Time DESC
            LIMIT ?
            """,
            ((n, chat_id) if chat_id else (n,)),
        )
        return self.cursor.fetchall()

    def get_last_n_messages_from_chat(self, n: int, chat_id: int = None):
        """Get last n messages from db

        Args:
            n (int): number of messages
            chat_id (int, optional): Chat id. Defaults to None. If not set returns messages from all chats

        Returns:
            list
        """
        message_events = self.get_last_n_message_events_from_chat(n, chat_id)

        # Extract the text and names from events
        messages = [[event[4], event[2]] for event in message_events]

        return messages
