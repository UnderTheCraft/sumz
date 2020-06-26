# SUMZ Unternehmensbewertung - Backend

Die API des Backends ist unter folgendem Link zu finden: https://sumz-backend.herokuapp.com

## Technologien:

- statsmodels: https://www.statsmodels.org
- flask: https://flask.palletsprojects.com/en/1.1.x/
- flask-cors: https://github.com/corydolphin/flask-cors
- flask-compress: https://github.com/shengulong/flask-compress
- flask-api: http://www.flaskapi.org
- flask-restx: https://github.com/python-restx/flask-restx
- gunicorn: https://gunicorn.org
- requests-html:https://github.com/psf/requests-html

## Lokaler Start:

Entwicklungsumgebung PyCharm: https://www.jetbrains.com/pycharm/

In der Konsole Flask installieren:
``` pip install flask ```

Dann *main.py* Flask als Parameter angeben:
``` set FLASK_APP=main.py ```

Mit Flask die Anwendung ausführen:
``` flask run ```

---

**Optional:**
Debug in Flask einschalten:
``` set FLASK_DEBUG=1 ```
Bewirkt, dass bei Verändern des Codes automatisch ein neuer Build gestartet wird.

**Weitere Infos:**
Wenn bei lokalem Start *restapi* nicht gefunden wird, muss dies jeweils im import entfernt werden
