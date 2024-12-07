from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime

class WSEventBase(BaseModel):
    type: str
    data: Any

class GameStartEvent(BaseModel):
    player1: dict
    player2: dict
    first_turn: int
    board: List[List[int]]
    timestamp: datetime

class GameMoveEvent(BaseModel):
    player_id: int
    position: tuple[int, int]
    next_turn: int
    board: List[List[int]]
    timestamp: datetime

class GameEndEvent(BaseModel):
    winner_id: int
    reason: str
    final_board: List[List[int]]
    timestamp: datetime

class ChatMessageEvent(BaseModel):
    sender_id: int
    sender_name: str
    message: str
    timestamp: datetime

class PlayerJoinEvent(BaseModel):
    player_id: int
    player_name: str
    timestamp: datetime

class PlayerLeaveEvent(BaseModel):
    player_id: int
    player_name: str
    timestamp: datetime

class ErrorEvent(BaseModel):
    code: str
    message: str
    timestamp: datetime
