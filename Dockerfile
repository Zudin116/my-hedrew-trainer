FROM python
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app
COPY . .
WORKDIR /app/lib/num2words
RUN python3 setup.py install
WORKDIR /app
CMD ["python3", "bot.py"]
