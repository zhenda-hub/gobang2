from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ...database import get_db
from ...models.game import Game, GameMove, GameStatus
from ...schemas.game import GameCreate, Game as GameSchema, GameMove as GameMoveSchema, GameDetail
from ..deps import get_current_user
from ...models.user import User

router = APIRouter()

@router.get("/rooms", response_model=List[GameSchema])
async def list_rooms(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    获取游戏房间列表
    """
    return db.query(Game).offset(skip).limit(limit).all()

@router.post("/rooms", response_model=GameSchema, status_code=status.HTTP_201_CREATED)
async def create_room(
    game: GameCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建新的游戏房间
    """
    db_game = Game(
        player1_id=current_user.id,
        status=GameStatus.WAITING
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.get("/rooms/{game_id}", response_model=GameDetail)
async def get_room(
    game_id: int,
    db: Session = Depends(get_db)
):
    """
    获取特定游戏房间的详细信息
    """
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return game

@router.post("/rooms/{game_id}/join", response_model=GameSchema)
async def join_room(
    game_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    加入游戏房间
    """
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    if game.status != GameStatus.WAITING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game is not in waiting status"
        )
    
    if game.player1_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already in this game"
        )
    
    if game.player2_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game is full"
        )
    
    game.player2_id = current_user.id
    game.status = GameStatus.PLAYING
    game.started_at = datetime.utcnow()
    game.current_turn_id = game.player1_id  # 玩家1先手
    
    db.commit()
    db.refresh(game)
    return game

@router.post("/rooms/{game_id}/move", response_model=GameSchema)
async def make_move(
    game_id: int,
    move: GameMoveSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    在游戏中下棋
    """
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    if game.status != GameStatus.PLAYING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game is not in playing status"
        )
    
    if game.current_turn_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="It's not your turn"
        )
    
    # 检查位置是否已被占用
    if game.board[move.y][move.x] != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Position is already taken"
        )
    
    # 记录移动
    player_number = 1 if current_user.id == game.player1_id else 2
    game.board[move.y][move.x] = player_number
    
    # 保存移动记录
    db_move = GameMove(
        game_id=game_id,
        player_id=current_user.id,
        x=move.x,
        y=move.y
    )
    db.add(db_move)
    
    # 检查是否获胜
    if check_win(game.board, move.x, move.y, player_number):
        game.status = GameStatus.FINISHED
        game.winner_id = current_user.id
        game.finished_at = datetime.utcnow()
    else:
        # 切换回合
        game.current_turn_id = game.player2_id if current_user.id == game.player1_id else game.player1_id
    
    db.commit()
    db.refresh(game)
    return game

def check_win(board: List[List[int]], x: int, y: int, player: int) -> bool:
    """
    检查是否获胜
    """
    directions = [
        [(0, 1), (0, -1)],   # 垂直
        [(1, 0), (-1, 0)],   # 水平
        [(1, 1), (-1, -1)],  # 主对角线
        [(1, -1), (-1, 1)]   # 副对角线
    ]
    
    for dir_pair in directions:
        count = 1  # 当前位置算一个
        
        # 检查每一对方向
        for dx, dy in dir_pair:
            # 在这个方向上继续找相同的棋子
            curr_x, curr_y = x + dx, y + dy
            while (0 <= curr_x < 15 and 
                   0 <= curr_y < 15 and 
                   board[curr_y][curr_x] == player):
                count += 1
                if count >= 5:
                    return True
                curr_x, curr_y = curr_x + dx, curr_y + dy
    
    return False
