[![Codacy Badge](https://api.codacy.com/project/badge/Grade/43cccec31d7b4058a8e29246a9be5a23)](https://www.codacy.com/manual/chrisjohnson00/awx_proxy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=chrisjohnson00/awx_proxy&amp;utm_campaign=Badge_Grade)

Run for dev

    FLASK_APP=app.py FLASK_ENV=development flask run

Run in docker

    docker run -d -n awx_proxy -p 5000:5000 awx_proxy

Build the docker

    docker build . -t awx_proxy

Update `instance/config.py` with your values for your testing.
