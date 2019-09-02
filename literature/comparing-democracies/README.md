# Comparing Democracies using Python

Julius-Maximilians-Universität Würzburg
Fakultät für Humanwissenschaften
Institut für Politikwissenschaft und Soziologie
Lehrstuhl für Vergleichende Politikwissenschaft und Systemlehre

Prüfungsleistung von

> Severin Simmler
> Matrikel Nr.: 2028090
> severin.simmler(at)stud-mail.uni-wuerzburg.de

für das Seminar **Comparing Democracies using R and Python** im Sommersemester 2018 bei Oliver Schlenkrich.

## 1. Überblick
Dieses Verzeichnis enthält ein [Jupyter Notebook](notebook.ipynb), das die (reproduzierbaren) Ergebnisse enthält. Das _ausführbare_ Notebook wurde außerdem in zwei weitere Formate (PDF, HTML) exportiert, um die Arbeit auch ohne Jupyter einsehen zu können. Aus (ästhetischen) Darstellungsgründen empfehle ich hier die HTML Variante.

## 2. Installation
Die Abhängigkeiten der Arbeit sind in [`Pipfile`](Pipfile) definiert. Um diese zu installieren, muss folgender Befehl, im selben Verzeichnis, in der Kommandozeile ausgeführt werden:

```
pipenv install
```

Nach der erfolgreichen Installation kann [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) folgendermaßen gestartet werden:

```
pipenv run juptyer lab
```

> Pipenv ist Tool zur Erstellung und Verwaltung von _virtual environments_, und kann wie gewohnt mit `pip` installiert werden: `pip install pipenv`.

## 3. Troubleshooting
- Die Installation kann mehrere Minuten dauern.
- Sollte die Kommandozeile nicht über eine enstprechende Umgebungsvariable verfügen (weswegen Pipenv nicht gefunden wird), kann alternativ der folgende Befehl verwendet werden: `python -m pipenv`
- Bei weiterhin bestehenden Probleme helfe ich gerne: `severin.simmler@stud-mail.uni-wuerzburg.de`
