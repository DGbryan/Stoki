import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import zipfile
import io

def generate_qr_code(item_code: str, lot: str, description: str, save_dir: str):
    """
    Gera um QR Code em imagem com formato "CODIGO|LOTE|DESCRICAO" e salva na pasta informada.
    Retorna o caminho do arquivo gerado.
    """
    qr_content = f"{item_code}|{lot}|{description}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Desenhar os textos na própria imagem (abaixo do QR)
    draw = ImageDraw.Draw(img)
    # Tenta usar a fonte default
    try:
        font = ImageFont.load_default()
    except:
        font = None
        
    width, height = img.size
    
    # Aumentar a imagem para caber o texto
    new_img = Image.new('RGB', (width, height + 60), color='white')
    new_img.paste(img, (0, 0))
    
    draw = ImageDraw.Draw(new_img)
    text1 = f"Codigo: {item_code}"
    text2 = f"Lote: {lot}"
    
    if font:
        draw.text((10, height), text1, fill="black", font=font)
        draw.text((10, height + 20), text2, fill="black", font=font)
    else:
        draw.text((10, height), text1, fill="black")
        draw.text((10, height + 20), text2, fill="black")
        
    safe_filename = "".join([c for c in item_code if c.isalpha() or c.isdigit() or c in '.-_']).rstrip()
    filepath = os.path.join(save_dir, f"{safe_filename}.png")
    new_img.save(filepath)
    return filepath

def create_qr_codes_zip(items, save_dir: str) -> bytes:
    """
    Recebe uma lista de itens (modelos), gera os QRs e retorna o conteúdo do ZIP em bytes.
    """
    os.makedirs(save_dir, exist_ok=True)
    
    # Gera os arquivos físicos
    generated_files = []
    for item in items:
        fp = generate_qr_code(item.item_code, item.lot, item.description, save_dir)
        generated_files.append(fp)
        
    # Cria o zip em memória
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for fpath in generated_files:
            filename = os.path.basename(fpath)
            zipf.write(fpath, arcname=filename)
            
    # Opcional: limpar os arquivos PNG gerados se não quiser manter fisicamente
    # for fpath in generated_files:
    #     os.remove(fpath)
        
    return zip_buffer.getvalue()
