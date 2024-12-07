from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .user import User

class GameBase(BaseModel):
    status: str = Field(default="waiting")

class GameCreate(GameBase):
    pass

class GameMove(BaseModel):
    x: int = Field(..., ge=0, lt=15)
    y: int = Field(..., ge=0, lt=15)

class GameMoveResponse(GameMove):
    id: int
    game_id: int
    player_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Game(GameBase):
    id: int
    player1_id: int
    player2_id: Optional[int] = None
    current_turn_id: Optional[int] = None
    winner_id: Optional[int] = None
    board: List[List[int]]
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    
    # 关联的用户信息
    player1: Optional[User] = None
    player2: Optional[User] = None
    current_turn: Optional[User] = None
    winner: Optional[User] = None

    class Config:
        from_attributes = True

class GameDetail(Game):
    moves: List[GameMoveResponse] = []
