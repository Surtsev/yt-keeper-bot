FROM python:3.13-alpine


WORKDIR app

COPY requirements.txt .
COPY pyproject.toml .

RUN pip install uv && uv add -r requirements.txt

COPY . .

CMD ["uv", "run", "src/main.py"]


