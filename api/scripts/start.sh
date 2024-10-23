#!/bin/sh

sleep 10
cd /apps/api

mkdir -p $MEDIA_ROOT
mkdir -p $STATIC_ROOT/$USER_DEFAULT_AVATARS_DIR

cp -r $STATIC_ROOT/default/esl_avatar.png $STATIC_ROOT/$USER_DEFAULT_AVATARS_DIR/$USER_DEFAULT_AVATAR_NAME.$USER_DEFAULT_AVATAR_EXTENSION

alembic upgrade head

if [ "$(grep -i '^DEBUG=True' .env)" ]; then
    uvicorn src.main:app --reload --host 0.0.0.0
else
    gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --reload
fi