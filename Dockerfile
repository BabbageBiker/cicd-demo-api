# base image (Python 3.12 [start with slim, smaller faster])
FROM python:3.12-slim

LABEL maintainer="Kyle Cornford"

# set workdir inside container
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of app
COPY . .

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
