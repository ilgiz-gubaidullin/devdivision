FROM python:alpine3.16

COPY final_project/mock /vk_mock

RUN pip install Flask==2.1.2

WORKDIR /vk_mock

CMD ["python", "./vk_mock.py"]