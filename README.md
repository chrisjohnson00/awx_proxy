Run for dev

    FLASK_APP=app.py FLASK_ENV=development flask run

Run in docker

    docker run -d -n awx_proxy -p 5000:5000 awx_proxy

Build the docker

    docker build . -t awx_proxy


Update `instance/config.py` with your values for your testing.
