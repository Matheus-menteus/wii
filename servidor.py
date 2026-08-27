import asyncio
import websockets
import json

async def wii_controller(websocket):
    print("\n🎮 Celular conectado com sucesso!")
    try:
        async for message in websocket:
            dados = json.loads(message)
            # Por enquanto, vamos imprimir no terminal para ver a mágica
            # Na próxima etapa, enviaremos isso para o jogo!
            print(f"Movimento -> Frente/Trás: {dados['beta']:3} | Lados: {dados['gamma']:3}", end="\r")
    except websockets.exceptions.ConnectionClosed:
        print("\n📱 Celular desconectado.")

async def main():
    # Inicia o servidor WebSocket na porta 8765
    async with websockets.serve(wii_controller, "0.0.0.0", 8765):
        print("Servidor WebSocket rodando na porta 8765.")
        print("Aguardando conexão do celular...")
        await asyncio.Future()  # Mantém o servidor rodando para sempre

if __name__ == "__main__":
    asyncio.run(main())
