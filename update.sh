#!/usr/bin/env bash
set -e
cd /opt/scriptbot
git pull
docker compose up -d --build
docker compose logs --tail=50
