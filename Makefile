.PHONY: validate validate-schemas check-boundaries check-contract-boundaries

validate: validate-schemas check-boundaries check-contract-boundaries

validate-schemas:
	python scripts/validate_schemas.py

check-boundaries:
	python scripts/check_boundaries.py

check-contract-boundaries:
	python scripts/check_contract_boundaries.py