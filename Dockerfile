FROM python:3

ADD helper_bot /helper_bot

RUN pip install -r helper_bot/requirements.txt

CMD [ "python", "-m", "helper_bot.helper_bot.main"]
