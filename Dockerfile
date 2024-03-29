FROM python:3.9-alpine3.13
# Alpine is a lite weight of linux
# can check from hub.docker search python
LABEL maintainer = "laurence L2G2"
# setting the maintainer
ENV PYTHONUNBUFFERED 1
# tell python don't buffer output logs present them immedeatly on console


COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
# copy xxxx from local mechine to xxxx inside the container
WORKDIR /app
EXPOSE 8000
#expose port8000 of the container on image to our machine


ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    #apk=package manager from alpine, install client
    apk add --update --no-cache --virtual .tmp-build-deps \
    #set a virtual and make alias of our below dependencies 給下面一個統稱：tmp-build-deps
    #linux-headers : fir the use of uWGSI
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    #apk add --no-cache py3-numpy \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    #fi => end if
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    #above must be the same with
    adduser \
    #adduser to the image (this is not a rootuser)
        --disabled-password \
        --no-create-home \
        django-container-user && \
        #the name of user that created in container
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-container-user:django-container-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts
#run command when building image
#keep run command light weight avoid too many layer in out system



ENV PATH="/scripts:/py/bin:$PATH"

USER django-container-user
#below is the name of the scripts that's going to run our application
CMD ["run.sh"]