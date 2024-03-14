FROM python:3.11

# install requirements

COPY ./app/requirements.txt .

RUN pip install -r requirements.txt

# Copy rest of app

COPY ./app .

# Run the app

EXPOSE 8000

# Run api.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]