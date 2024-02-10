import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path='data/.env')

config = {
    'user': os.getenv('SQL_USER'),
    'password': os.getenv('SQL_PASS'),
    'host': os.getenv('SQL_HOST'),
    'database': os.getenv('SQL_DB'),
    'raise_on_warnings': True
}

# Database object
class DatabaseConnection:
    def __init__(self):
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor(dictionary=True)

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()

# Database Operation Manager
class DatabaseOperations:
    def __init__(self):
        with DatabaseConnection() as self.cursor:
            # Create tables if they don't exist
            try:
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS `thread_ids` (
                        `user_id` BIGINT UNSIGNED NOT NULL,
                        `thread_id` VARCHAR(255) NOT NULL
                        PRIMARY KEY (user_id)
                    );
                ''')
            except mysql.connector.Error as err:
                print(err)

            # # Enable event scheduler if it is not already enabled
            # self.cursor.execute('''
            #     SET GLOBAL event_scheduler=ON;
            # ''')

            # # Create an event which will remove rows older than 1 week in the 
            # # message_logs table if an event is not already created
            # self.cursor.execute('''
            #     CREATE EVENT IF NOT EXISTS `remove_old_logs`
            #     ON SCHEDULE EVERY 1 DAY
            #     DO
            #         DELETE FROM `message_logs`
            #         WHERE `timestamp` < DATE_SUB(NOW(), INTERVAL 1 WEEK);
            # ''')
                
    def get_thread(self, user_id: int):
        """
        Gets the thread id attached to the user id. Returns None type if user id is not found
        """
        with DatabaseConnection() as self.cursor:
            self.cursor.execute('''
                SELECT `thread_id`
                FROM `thread_ids`
                WHERE `user_id` = %s
            ''', (user_id,))
            thread_id = self.cursor.fetchone()
            return thread_id

    def add_thread(self, user_id: int, thread_id: str):
        """
        Adds a thread id to the database
        """
        with DatabaseConnection() as self.cursor:
            self.cursor.execute('''
                INSERT INTO `thread_ids` (`user_id`, `thread_id`)
                VALUES (%s, %s)
            ''', (user_id, thread_id))
    
    def delete_thread(self, user_id: int):
        """
        Deletes a thread id from the database
        """
        with DatabaseConnection() as self.cursor:
            self.cursor.execute('''
                DELETE FROM `thread_ids`
                WHERE `user_id` = %s
            ''', (user_id,))

    def add_message(self, user_id: int, timestamp: datetime, role: str, content: str):
        """
        Adds a message to the database so the bot can continue the conversation
        """
        with DatabaseConnection() as self.cursor:
            # Add the message to the database
            self.cursor.execute('''
                INSERT INTO `message_logs` (`user_id`, `timestamp`, `role`, `content`)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, timestamp, role, content))
    
    def get_message_log(self, user_id, max_previous_messages=-1):
        """
        Returns the last x messages from the user based on the max_previous_messages
        """
        with DatabaseConnection() as self.cursor:
            # Get the previous messages and roles that are within the max_previous_messages
            if max_previous_messages != -1:
                self.cursor.execute('''
                    SELECT `timestamp`, `role`, `content`
                    FROM `message_logs`
                    WHERE `user_id`=%s
                    ORDER BY `timestamp` DESC
                    LIMIT %s
                ''', (user_id, max_previous_messages))
            else:
                self.cursor.execute('''
                    SELECT `role`, `content`
                    FROM `message_logs`
                    WHERE `user_id` = %s
                    ORDER BY `timestamp` DESC
                ''', (user_id,))
            message_log = self.cursor.fetchall()
            return message_log
        
    def clear_message_log(self, user_id):
        """
        Clears the message log of the user
        """
        with DatabaseConnection() as self.cursor:
            self.cursor.execute('''
                DELETE FROM `message_logs`
                WHERE `user_id` = %s
            ''', (user_id,))