FROM python:3.9-alpine3.13
# Alpine is a lite weight of linux
# can check from hub.docker search python
LABEL maintainer = "laurence L2G2"
# setting the maintainer
ENV PYTHONUNBUFFERED 1
# tell python don't buffer output logs present them immedeatly on console


COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
# copy xxxx from local mechine to xxxx inside the container
WORKDIR /app
EXPOSE 8000
#expose port8000 of the container on image to our machine


ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    #apk=package manager from alpine, install client
    apk add --update --no-cache --virtual .tmp-build-deps \
    #set a virtual and make alias of our below dependencies 給下面一個統稱：tmp-build-deps
        build-base postgresql-dev musl-dev && \
    
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
        django-container-user
        #the name of user that created in container

#run command when building image
#keep run command light weight avoid too many layer in out system



ENV PATH="/py/bin:$PATH"

USER django-container-user