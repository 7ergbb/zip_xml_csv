venv:
	[ ! -e .venv ] && python3 -m venv .venv --prompt xmlzip || true
.PHONY: venv

lint:
	python3 -m pycodestyle  --max-line-length=120 zip_xml_csv/
.PHONY: lint