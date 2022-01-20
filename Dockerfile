FROM public.ecr.aws/lambda/python:3.7
RUN /var/lang/bin/python3.7 -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./ .
COPY twint/ .
COPY crypto-musk-firebase-adminsdk-ay1ha-12d4e67ca9.json .
COPY firepush.py .
CMD [ "firepush.handler" ]