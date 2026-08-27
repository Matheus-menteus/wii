import asyncio
import websockets
import json

# Lista para guardar os dispositivos conectados (Celular e PC)
clientes = set()

async def wii_controller(websocket):
    clientes.add(websocket)
    print(f"🎮 Novo dispositivo! Total conectados: {len(clientes)}")
    try:
        async for message in websocket:
            # Recebe o movimento do celular e repassa para a tela do jogo no PC
            for cliente in clientes:
                if cliente != websocket: # Não devolve a mensagem para o próprio celular
                    await cliente.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("📱 Dispositivo desconectado.")
    finally:
        clientes.remove(websocket)

async def main():
    async with websockets.serve(wii_controller, "0.0.0.0", 8765):
        print("Servidor Ponte rodando! Aguardando o celular e a tela do jogo...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
