reqs:
	poetry export --without-hashes > requirements.txt
	poetry export --with dev --without-hashes > dev-requirements.txt
	. .venv/bin/activate; pip3 install -r dev-requirements.txt

bot:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; python3 bot.py

chain:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; python3 chain.py
