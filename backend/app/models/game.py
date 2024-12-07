from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from ..database import Base

class GameStatus(str, enum.Enum):
    WAITING = "waiting"
    PLAYING = "playing"
    FINISHED = "finished"

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default=GameStatus.WAITING)
    
    player1_id = Column(Integer, ForeignKey("users.id"))
    player2_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    current_turn_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # 棋盘状态：15x15的二维数组，0表示空，1表示玩家1，2表示玩家2
    board = Column(JSON, default=lambda: [[0 for _ in range(15)] for _ in range(15)])
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关系
    player1 = relationship("User", foreign_keys=[player1_id], backref="games_as_player1")
    player2 = relationship("User", foreign_keys=[player2_id], backref="games_as_player2")
    current_turn = relationship("User", foreign_keys=[current_turn_id], backref="games_as_current_turn")
    winner = relationship("User", foreign_keys=[winner_id], backref="games_won")

class GameMove(Base):
    __tablename__ = "game_moves"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    player_id = Column(Integer, ForeignKey("users.id"))
    x = Column(Integer)
    y = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    game = relationship("Game", backref="moves")
    player = relationship("User", backref="moves")
