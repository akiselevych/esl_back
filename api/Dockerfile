FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE 0

WORKDIR /apps/api
COPY . .

RUN pip install "poetry"

COPY poetry.lock /apps/api
COPY --chmod=765 scripts/start.sh /apps/start.sh

RUN /bin/true\
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction \
    && rm -rf /root/.cache/pypoetry
RUN chmod +x /apps/start.sh

CMD ["/apps/start.sh"]