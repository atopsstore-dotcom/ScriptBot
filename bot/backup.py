import json, os, zipfile
from pathlib import Path
from datetime import datetime
from bot.config import get_settings

BACKUP_FILES = ['.env']

def create_backup():
    s=get_settings(); Path(s.backup_path).mkdir(parents=True, exist_ok=True)
    out=Path(s.backup_path)/f'scriptbot_backup_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.sbak'
    meta={'name':s.bot_name,'created_at':datetime.utcnow().isoformat(),'type':'scriptbot-backup'}
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('meta.json', json.dumps(meta,ensure_ascii=False,indent=2))
        for f in BACKUP_FILES:
            if Path(f).exists(): z.write(f,f)
        for f in ['data/scriptbot.db','assets/default.png']:
            if Path(f).exists(): z.write(f,f)
    return str(out)

def restore_backup(path):
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if name == 'meta.json': continue
            if '..' in Path(name).parts: continue
            target=Path(name); target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(z.read(name))
