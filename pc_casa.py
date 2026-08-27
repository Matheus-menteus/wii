import asyncio
import websockets
import json
import pyautogui

# Configurações do PyAutoGUI para o movimento ser instantâneo e suave
pyautogui.PAUSE = 0 
pyautogui.FAILSAFE = False # Cuidado: desativa a trava de segurança do mouse nos cantos

# ⚠️ COLOQUE AQUI O SEU LINK DA PORTA 8765 DO CODESPACES
WS_URL = "wss://SEU-LINK-DA-PORTA-8765.app.github.dev"

async def wii_mouse():
    print("⏳ Conectando ao servidor na nuvem...")
    try:
        async with websockets.connect(WS_URL) as websocket:
            print("✅ Conectado! Mova o celular para controlar o mouse.")
            print("Pressione Ctrl+C no terminal para parar.")
            
            while True:
                mensagem = await websocket.recv()
                dados = json.loads(mensagem)
                
                gamma = dados.get('gamma', 0) # Inclinação Esquerda/Direita
                beta = dados.get('beta', 0)   # Inclinação Cima/Baixo
                
                # CRIANDO UMA "ZONA MORTA" (Deadzone)
                # Só move o mouse se a inclinação passar de 3 graus.
                # Isso evita que o mouse trema quando sua mão estiver parada.
                if abs(gamma) < 3: gamma = 0
                if abs(beta) < 3: beta = 0
                
                # Multiplicador de sensibilidade (ajuste se ficar muito lento ou rápido)
                sensibilidade = 1.5
                
                move_x = gamma * sensibilidade
                # Invertemos o beta (colocando o sinal de menos) para que 
                # inclinar para frente faça o mouse subir, como combinamos!
                move_y = -beta * sensibilidade 
                
                # Executa o movimento no Windows
                if move_x != 0 or move_y != 0:
                    pyautogui.moveRel(move_x, move_y)
                    
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    asyncio.run(wii_mouse())
