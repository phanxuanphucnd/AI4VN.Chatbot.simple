VERSION = 0.0.1
BOTNAME = nonoone
MODEL_FOLDER = models/

train-all:
	python -m rasa train --domain domain.yml --fixed-model-name $(BOTNAME)_$(VERSION)

run-actions:
	rasa run actions --actions actions

run-server:
	rasa run --endpoints endpoints.yml --port 5005 --model $(MODEL_FOLDER)$(BOTNAME)_$(VERSION) --credentials credentials.yml

run-x-server:
	rasa x --endpoints endpoints.yml --port 5005 --rasa-x-port 5002 --model $(MODEL_FOLDER)$(BOTNAME)_$(VERSION) --credentials credential.yml	