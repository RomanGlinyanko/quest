from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select
from .baserepository import BaseRepository
from ..models import Quest, ConnSpaceQuest, ConnQuestTerm

class QuestRepository(BaseRepository[Quest]):
    def __init__(self, session: AsyncSession):
        # Инициализируем базу с привязкой к модели Quest
        super().__init__(Quest, session)

    async def create_complex_question(
        self, 
        text: str, 
        answer: str, 
        user_id: int, 
        space_ids: List[int], 
        term_ids: List[int]
    ) -> Quest:
        """
        Создает вопрос и сразу привязывает его к темам и терминам.
        Это 'Business Transaction' на уровне репозитория.
        """
        # 1. Создаем сам объект вопроса
        new_quest = Quest(
            quest=text, 
            answer=answer, 
            user_id=user_id
        )
        self.session.add(new_quest)
        
        # Делаем flush, чтобы БД присвоила вопросу ID, 
        # но еще не фиксируем транзакцию (commit будет позже)
        await self.session.flush()

        # 2. Создаем связи с Пространствами (темами)
        for s_id in space_ids:
            conn_space = ConnSpaceQuest(
                space_id=s_id, 
                quest_id=new_quest.id, 
                user_id=user_id
            )
            self.session.add(conn_space)

        # 3. Создаем связи с Терминами (подсказками)
        for t_id in term_ids:
            conn_term = ConnQuestTerm(
                quest_id=new_quest.id, 
                term_id=t_id, 
                user_id=user_id
            )
            self.session.add(conn_term)

        # Возвращаем объект вопроса со всеми ID
        return new_quest

    async def get_full_quest_data(self, quest_id: int):
        """
        Пример метода, который подтягивает вопрос сразу со всеми 
        связанными терминами (используя индексы, которые мы создали).
        """
        query = (
            select(Quest)
            .filter(Quest.id == quest_id)
            # В SQLAlchemy это называется Eager Loading (жадная загрузка)
            # Чтобы не делать 10 запросов в базу, делаем один умный JOIN
            .execution_options(populate_existing=True) 
        )
        # ... здесь можно добавить selectinload(Quest.terms)
