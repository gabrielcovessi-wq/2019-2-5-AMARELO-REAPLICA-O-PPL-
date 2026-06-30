from PIL import Image
import os

def converter_cor_gimp_para_rgb(gimp_r, gimp_g, gimp_b):
    """
    Converte valores do GIMP (0-100) para RGB (0-255)
    """
    r = int((gimp_r / 100) * 255)
    g = int((gimp_g / 100) * 255)
    b = int((gimp_b / 100) * 255)
    return (r, g, b)

def encontrar_faixa_cinza(imagem, cor_alvo, tolerancia=15):
    """
    Encontra posições no pixel x=325 onde há uma faixa vertical contínua da cor especificada.
    Alvo: ~29 pixels de altura (Margem de erro: 24 a 34 pixels).
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    # Configurações do novo padrão
    altura_ideal = 29
    margem_erro = 5
    altura_minima = altura_ideal - margem_erro  # 24 px
    altura_maxima = altura_ideal + margem_erro  # 34 px
    
    y = 0
    while y < altura:
        # Pega a cor do pixel atual na coordenada x=325
        pixel = pixels[325, y]
        r, g, b = pixel[:3]
        
        # Verifica se o pixel atual combina com a cor alvo
        if (abs(r - cor_alvo[0]) <= tolerancia and 
            abs(g - cor_alvo[1]) <= tolerancia and 
            abs(b - cor_alvo[2]) <= tolerancia):
            
            # Conta quantos pixels seguidos mantêm essa cor
            altura_faixa_detectada = 0
            while (y + altura_faixa_detectada) < altura:
                p_atual = pixels[325, y + altura_faixa_detectada]
                r_a, g_a, b_a = p_atual[:3]
                
                if (abs(r_a - cor_alvo[0]) <= tolerancia and 
                    abs(g_a - cor_alvo[1]) <= tolerancia and 
                    abs(b_a - cor_alvo[2]) <= tolerancia):
                    altura_faixa_detectada += 1
                else:
                    break
            
            # Verifica se o bloco de cor encontrado se encaixa na margem de erro (24 a 34 px)
            if altura_minima <= altura_faixa_detectada <= altura_maxima:
                # MODIFICAÇÃO: O corte é feito EXATAMENTE no início da faixa (y)
                posicao_corte = y -5
                    
                posicoes_corte.append((posicao_corte, altura_faixa_detectada))
                print(f"Faixa encontrada de {altura_faixa_detectada}px começando em y={y}, cortando exatamente em y={posicao_corte}")
                
                # Avança o ponteiro 'y' pulando toda a faixa detectada para evitar loops
                y += altura_faixa_detectada
                continue
                
            y += altura_faixa_detectada if altura_faixa_detectada > 0 else 1
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo):
    """
    Divide a imagem verticalmente MANTENDO as faixas no início de cada bloco
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    faixas_encontradas = encontrar_faixa_cinza(imagem, cor_alvo)
    
    if not faixas_encontradas:
        print("Nenhuma faixa no padrão especificado foi encontrada!")
        return
    
    print(f"Encontradas {len(faixas_encontradas)} faixas para corte")
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, (posicao_corte, altura_faixa) in enumerate(faixas_encontradas):
        if posicao_corte <= posicao_anterior:
            continue
            
        # Corta do final do bloco anterior até o início desta nova faixa 
        # (A faixa cinza fará parte do início do PRÓXIMO bloco)
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        # MODIFICAÇÃO: A próxima seção começa EXATAMENTE na posição do corte (y),
        # garantindo que a faixa cinza apareça no início da próxima imagem.
        posicao_anterior = posicao_corte
    
    # Corta a última seção restante (que agora começa com a última faixa detectada)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(faixas_encontradas)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  
    pasta_saida = "questoes_colunas" 

    cor_do_padrao = (222, 221, 222)
    print(f"Cor alvo definida: RGB {cor_do_padrao}")
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    print("Divisão concluída!")