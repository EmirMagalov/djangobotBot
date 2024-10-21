FROM python:3.10.9
WORKDIR /usr/src/bot
COPY requirements.txt ./
RUN pip install -r  requirements.txt
CMD ["python", "bot.py"]