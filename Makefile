.PHONY: setup data test pipeline fixture
setup:
	python -m pip install -r requirements.txt
data:           ## optional: needs Kaggle credentials and `pip install kaggle`
	kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw --unzip
test:
	python -m pytest -q
pipeline:
	python -m src.pipeline
fixture:
	python tests/make_fixture.py
