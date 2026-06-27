from pathlib import Path
from PIL import Image, ImageOps
import asyncio, uuid, shutil

class ConvertError(Exception): pass

def ensure(path): Path(path).mkdir(parents=True, exist_ok=True)

async def convert_photo(src_path, out_dir='data/converted', width=240, height=135):
    ensure(out_dir); out=Path(out_dir)/f'boot_{uuid.uuid4().hex}.png'
    try:
        img=Image.open(src_path).convert('RGB')
        img=ImageOps.fit(img, (width,height), method=Image.Resampling.LANCZOS, centering=(0.5,0.5))
        img.save(out, 'PNG', optimize=True)
        return str(out)
    except Exception as e:
        raise ConvertError(f'Не удалось обработать фото: {e}')

async def _ffmpeg(cmd, timeout=60):
    p=await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    try: out,err=await asyncio.wait_for(p.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        p.kill(); raise ConvertError('Конвертация заняла слишком много времени. Отправь файл меньше или короче.')
    if p.returncode != 0: raise ConvertError(err.decode(errors='ignore')[-1000:] or 'FFmpeg error')

async def convert_gif(src_path, out_dir='data/converted', width=240, height=135, fps=12, max_seconds=5):
    ensure(out_dir); out=Path(out_dir)/'boot.gif'
    vf=f"fps={fps},scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer"
    await _ffmpeg(['ffmpeg','-y','-t',str(max_seconds),'-i',str(src_path),'-vf',vf,'-loop','0',str(out)])
    return str(out)

async def convert_video(src_path, out_dir='data/converted', width=240, height=135, fps=12, max_seconds=5):
    return await convert_gif(src_path,out_dir,width,height,fps,max_seconds)
