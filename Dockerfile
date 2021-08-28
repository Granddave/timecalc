FROM python:3.8

WORKDIR /test
COPY . .
RUN pip install pytest
CMD ["pytest", "-v"]
