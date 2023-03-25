FROM python
RUN pip install --user aiogram python-dotenv
WORKDIR /app
COPY . .
WORKDIR /app/lib/num2words
RUN python3 setup.py install
WORKDIR /app
CMD ["python3", "bot.py"]
