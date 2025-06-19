FROM python:3.12-slim-bullseye
WORKDIR /app

COPY REQUIRE.txt /app/REQUIRE.txt
RUN python -m pip install -r REQUIRE.txt

COPY . /app
CMD ["python", "bot.py"]