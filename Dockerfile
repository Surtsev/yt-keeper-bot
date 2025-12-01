FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir --root-user-action=ignore uv

COPY ./yt-keeper-bot .

RUN uv add -r ./requirements.txt

EXPOSE 8000

CMD ["uv", "run", "main.py"]
