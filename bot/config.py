from functools import lru_cache
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    bot_token: str
    owner_id: int
    admins: str = ''
    bot_name: str = 'ScriptBot'
    creator: str = '@primenimoo'
    database_url: str = 'sqlite+aiosqlite:///data/scriptbot.db'
    default_device_name: str = 'M5StickC PLUS2'
    default_cover_path: str = 'assets/default.png'
    support_group_id: Optional[int] = None
    github_repo_url: str = ''
    github_branch: str = 'main'
    local_storage_path: str = 'data/files'
    temp_path: str = 'data/temp'
    converted_path: str = 'data/converted'
    backup_path: str = 'backups'
    max_upload_mb: int = 50
    splash_width: int = 240
    splash_height: int = 135
    splash_gif_max_seconds: int = 5
    splash_gif_fps: int = 12
    donation_min_stars: int = 1
    donation_max_stars: int = 10000
    donation_preset_1: int = 50
    donation_preset_2: int = 100
    donation_preset_3: int = 150
    donation_preset_4: int = 200
    check_updates_seconds: int = 3600

    @property
    def admin_ids(self) -> set[int]:
        ids = {self.owner_id}
        for x in (self.admins or '').replace(';', ',').split(','):
            x=x.strip()
            if x.isdigit(): ids.add(int(x))
        return ids
    def ensure_dirs(self):
        for d in [self.local_storage_path, self.temp_path, self.converted_path, self.backup_path, 'data']:
            Path(d).mkdir(parents=True, exist_ok=True)

@lru_cache
def get_settings() -> Settings:
    s=Settings(); s.ensure_dirs(); return s
