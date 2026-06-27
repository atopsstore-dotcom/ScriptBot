#!/usr/bin/env bash
set -e
APP_DIR="/opt/scriptbot"
REPO_URL_DEFAULT="https://github.com/USERNAME/ScriptBot.git"

banner(){
cat <<'EOF'
 ███████╗ ██████╗██████╗ ██╗██████╗ ████████╗██████╗  ██████╗ ████████╗
 ██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝
 ███████╗██║     ██████╔╝██║██████╔╝   ██║   ██████╔╝██║   ██║   ██║
 ╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   ██╔══██╗██║   ██║   ██║
 ███████║╚██████╗██║  ██║██║██║        ██║   ██████╔╝╚██████╔╝   ██║
 ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   ╚═════╝  ╚═════╝    ╚═╝

                      by primenimoo
EOF
}
need_root(){ [ "$(id -u)" = "0" ] || { echo "Запустите скрипт от root"; exit 1; }; }
install_deps(){
  apt update
  apt install -y git curl ca-certificates docker.io docker-compose-plugin
  systemctl enable --now docker || true
}
install_bot(){
  need_root; install_deps
  read -p "Введите GitHub URL репозитория [${REPO_URL_DEFAULT}]: " REPO_URL
  REPO_URL=${REPO_URL:-$REPO_URL_DEFAULT}
  rm -rf "$APP_DIR"
  git clone "$REPO_URL" "$APP_DIR"
  cd "$APP_DIR"
  cp .env.example .env
  read -p "Введите BotFather token: " BOT_TOKEN
  read -p "Введите Telegram ID владельца: " OWNER_ID
  read -p "Дополнительные админы через запятую (можно пусто): " ADMINS
  read -p "ID группы тикетов/поддержки (можно пусто): " SUPPORT_GROUP_ID
  sed -i "s|^BOT_TOKEN=.*|BOT_TOKEN=${BOT_TOKEN}|" .env
  sed -i "s|^OWNER_ID=.*|OWNER_ID=${OWNER_ID}|" .env
  sed -i "s|^ADMINS=.*|ADMINS=${ADMINS}|" .env
  sed -i "s|^SUPPORT_GROUP_ID=.*|SUPPORT_GROUP_ID=${SUPPORT_GROUP_ID}|" .env
  docker compose up -d --build
  echo "✅ ScriptBot установлен и запущен. Логи: cd $APP_DIR && docker compose logs -f"
}
update_bot(){ cd "$APP_DIR" && git pull && docker compose up -d --build; echo "✅ Обновлено"; }
backup_bot(){ cd "$APP_DIR" && mkdir -p backups && tar -czf "backups/scriptbot_$(date +%Y%m%d_%H%M%S).tar.gz" .env data assets; echo "✅ Бэкап создан в $APP_DIR/backups"; }
restore_bot(){ read -p "Путь к .tar.gz бэкапу: " B; cd "$APP_DIR" && tar -xzf "$B" && docker compose restart; echo "✅ Восстановлено"; }
status_bot(){ cd "$APP_DIR" && docker compose ps && docker compose logs --tail=80; }
restart_bot(){ cd "$APP_DIR" && docker compose restart; }
stop_bot(){ cd "$APP_DIR" && docker compose down; }
remove_bot(){ cd "$APP_DIR" && docker compose down || true; rm -rf "$APP_DIR"; echo "Удалено"; }

while true; do
  clear; banner
  echo "──────────────────────────────────────────"
  echo "1) Установить ScriptBot на сервер"
  echo "2) Обновить ScriptBot"
  echo "3) Создать резервную копию"
  echo "4) Восстановить из резервной копии"
  echo "5) Проверить состояние"
  echo "6) Перезапустить"
  echo "7) Остановить"
  echo "8) Удалить"
  echo "0) Выход"
  echo "──────────────────────────────────────────"
  read -p "Выберите действие: " c
  case "$c" in
    1) install_bot;; 2) update_bot;; 3) backup_bot;; 4) restore_bot;; 5) status_bot;; 6) restart_bot;; 7) stop_bot;; 8) remove_bot;; 0) exit 0;; *) echo "Неверный пункт";;
  esac
  read -p "Нажмите Enter..." _
done
