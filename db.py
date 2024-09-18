import aiosqlite


DB_NAME = 'quiz_bot.db'


async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS quiz_state (
                                user_id INTEGER PRIMARY KEY,
                                question_index INTEGER,
                                current_result INTEGER DEFAULT 0,
                                last_result INTEGER DEFAULT 0
                            )""")
        await db.commit()


async def get_user_stats(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            'SELECT question_index, current_result, last_result FROM quiz_state WHERE user_id = ?', (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result if result else (0, 0, 0)


async def update_quiz_index(user_id, index, current_result=0, last_result=0):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index, current_result, last_result) VALUES (?, ?, ?, ?)',
            (user_id, index, current_result, last_result),
        )
        await db.commit()
