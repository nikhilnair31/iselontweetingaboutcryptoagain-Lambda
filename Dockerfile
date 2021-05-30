FROM public.ecr.aws/lambda/python:3.7

RUN /var/lang/bin/python3.7 -m pip install --upgrade pip

# Copy function code
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "firepush.handler" ]