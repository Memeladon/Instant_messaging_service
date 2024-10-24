from typing import Dict, Any, Optional, Type
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .base_rep import BaseRepository
from src.database.models import ChatLine


class ChatLineRepositoryImpl(BaseRepository):
    def create_one(self, db: Session, data: Dict[str, Any]) -> ChatLine | None:
        try:
            new_one = ChatLine(**data)
            db.add(new_one)
            db.commit()
            db.refresh(new_one)
            return new_one
        except SQLAlchemyError as e:
            db.rollback()
            raise f"Error CREATE chat line: {str(e)}"
        finally:
            db.close()

    def read_one(self, db: Session, line_id: int) -> ChatLine | None:
        try:
            chat_line = db.query(ChatLine).filter(ChatLine.id == line_id).first()
            return chat_line
        except SQLAlchemyError as e:
            raise f"Error READ chat line: {str(e)}"
        finally:
            db.close()

    def update_one(self, db: Session, line_id: int, new_data: Dict[str, Any]) -> Type[ChatLine]:
        try:
            chat_line = db.query(ChatLine).filter(ChatLine.id == line_id).first()
            if not chat_line:
                raise ValueError("Chat line not found")

            for attr, value in new_data.items():
                setattr(chat_line, attr, value)

            db.commit()
            return chat_line
        except (SQLAlchemyError, ValueError) as e:
            db.rollback()
            raise f"Error UPDATE chat line: {str(e)}"
        finally:
            db.close()

    def delete_one(self, db: Session, line_id: int) -> bool:
        try:
            chat_line = db.query(ChatLine).filter(ChatLine.id == line_id).first()
            if not chat_line:
                raise ValueError("User not found")

            db.delete(chat_line)
            db.commit()
            return True
        except (SQLAlchemyError, ValueError) as e:
            db.rollback()
            raise f"Error DELETE chat line: {str(e)}"
        finally:
            db.close()

    def delete_all(self, db: Session) -> bool:
        pass

    def list_all(self, db: Session):
        lines = db.query(ChatLine).all()
        return lines

    def search_by_something(self, db: Session, text: str, filter: Optional[str] = None) -> Type[ChatLine]:
        pass
