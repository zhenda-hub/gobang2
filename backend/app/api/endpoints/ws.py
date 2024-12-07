from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json

from ...core.ws_manager import manager
from ...database import get_db
from ...models.game import Game, GameStatus
from ...models.user import User
from ..deps import get_current_user_ws
from ...schemas.ws_events import (
    GameStartEvent,
    GameMoveEvent,
    GameEndEvent,
    ChatMessageEvent,
    PlayerJoinEvent,
    PlayerLeaveEvent,
    ErrorEvent
)

router = APIRouter()

@router.websocket("/game/{game_id}")
async def game_ws(
    websocket: WebSocket,
    game_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    # 验证用户
    try:
        current_user = await get_current_user_ws(token, db)
    except HTTPException:
        await websocket.close(code=4001)
        return
    
    # 验证游戏
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        await websocket.close(code=4002)
        return
    
    # 验证玩家是否属于这个游戏
    is_player = current_user.id in [game.player1_id, game.player2_id]
    
    try:
        if is_player:
            # 连接玩家
            await manager.connect_player(websocket, game_id, current_user.id)
            
            # 广播玩家加入消息
            event = PlayerJoinEvent(
                player_id=current_user.id,
                player_name=current_user.username,
                timestamp=datetime.utcnow()
            )
            await manager.broadcast_to_game(game_id, event.model_dump())
            
            # 如果游戏刚开始，发送游戏开始事件
            if game.status == GameStatus.PLAYING and len(manager.game_connections.get(game_id, {})) == 2:
                event = GameStartEvent(
                    player1={"id": game.player1_id, "name": game.player1.username},
                    player2={"id": game.player2_id, "name": game.player2.username},
                    first_turn=game.current_turn_id,
                    board=game.board,
                    timestamp=datetime.utcnow()
                )
                await manager.broadcast_to_game(game_id, event.model_dump())
        else:
            # 连接观众
            await manager.connect_spectator(websocket, game_id)
        
        # 等待消息
        while True:
            data = await websocket.receive_json()
            
            # 只处理玩家的移动消息
            if is_player and game.status == GameStatus.PLAYING:
                if data["type"] == "move" and game.current_turn_id == current_user.id:
                    x, y = data["data"]["position"]
                    
                    # 验证移动是否合法
                    if 0 <= x < 15 and 0 <= y < 15 and game.board[y][x] == 0:
                        # 更新游戏状态
                        player_number = 1 if current_user.id == game.player1_id else 2
                        game.board[y][x] = player_number
                        
                        # 检查是否获胜
                        if check_win(game.board, x, y, player_number):
                            game.status = GameStatus.FINISHED
                            game.winner_id = current_user.id
                            game.finished_at = datetime.utcnow()
                            
                            # 发送游戏结束事件
                            event = GameEndEvent(
                                winner_id=current_user.id,
                                reason="win",
                                final_board=game.board,
                                timestamp=datetime.utcnow()
                            )
                            await manager.broadcast_to_game(game_id, event.model_dump())
                        else:
                            # 切换回合
                            game.current_turn_id = game.player2_id if current_user.id == game.player1_id else game.player1_id
                            
                            # 发送移动事件
                            event = GameMoveEvent(
                                player_id=current_user.id,
                                position=(x, y),
                                next_turn=game.current_turn_id,
                                board=game.board,
                                timestamp=datetime.utcnow()
                            )
                            await manager.broadcast_to_game(game_id, event.model_dump())
                        
                        db.commit()
            
            # 处理聊天消息
            elif data["type"] == "chat":
                event = ChatMessageEvent(
                    sender_id=current_user.id,
                    sender_name=current_user.username,
                    message=data["data"]["message"],
                    timestamp=datetime.utcnow()
                )
                await manager.broadcast_to_game(game_id, event.model_dump())
    
    except WebSocketDisconnect:
        if is_player:
            manager.disconnect_player(game_id, current_user.id)
            event = PlayerLeaveEvent(
                player_id=current_user.id,
                player_name=current_user.username,
                timestamp=datetime.utcnow()
            )
            await manager.broadcast_to_game(game_id, event.model_dump())
        else:
            manager.disconnect_spectator(websocket, game_id)

def check_win(board: list[list[int]], x: int, y: int, player: int) -> bool:
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
