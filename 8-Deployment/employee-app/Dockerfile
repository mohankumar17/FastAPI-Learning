FROM python:3.10.11

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#RUN alembic upgrade head

#CMD ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "8000"]