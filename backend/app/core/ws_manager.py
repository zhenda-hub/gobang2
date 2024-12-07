from fastapi import WebSocket
from typing import Dict, Set
import json

class ConnectionManager:
    def __init__(self):
        # 游戏房间的连接 {game_id: {player_id: WebSocket}}
        self.game_connections: Dict[int, Dict[int, WebSocket]] = {}
        # 观战连接 {game_id: Set[WebSocket]}
        self.spectator_connections: Dict[int, Set[WebSocket]] = {}
    
    async def connect_player(self, websocket: WebSocket, game_id: int, player_id: int):
        await websocket.accept()
        if game_id not in self.game_connections:
            self.game_connections[game_id] = {}
        self.game_connections[game_id][player_id] = websocket
    
    async def connect_spectator(self, websocket: WebSocket, game_id: int):
        await websocket.accept()
        if game_id not in self.spectator_connections:
            self.spectator_connections[game_id] = set()
        self.spectator_connections[game_id].add(websocket)
    
    def disconnect_player(self, game_id: int, player_id: int):
        if game_id in self.game_connections:
            self.game_connections[game_id].pop(player_id, None)
            if not self.game_connections[game_id]:
                del self.game_connections[game_id]
    
    def disconnect_spectator(self, websocket: WebSocket, game_id: int):
        if game_id in self.spectator_connections:
            self.spectator_connections[game_id].discard(websocket)
            if not self.spectator_connections[game_id]:
                del self.spectator_connections[game_id]
    
    async def broadcast_to_game(self, game_id: int, message: dict):
        """
        广播消息给游戏中的所有玩家和观众
        """
        # 发送给玩家
        if game_id in self.game_connections:
            for websocket in self.game_connections[game_id].values():
                await websocket.send_json(message)
        
        # 发送给观众
        if game_id in self.spectator_connections:
            for websocket in self.spectator_connections[game_id]:
                await websocket.send_json(message)
    
    async def send_personal_message(self, websocket: WebSocket, message: dict):
        """
        发送私人消息给特定连接
        """
        await websocket.send_json(message)

# 创建全局连接管理器实例
manager = ConnectionManager()
