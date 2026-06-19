.PHONY: validate validate-schemas check-boundaries

validate: validate-schemas check-boundaries

validate-schemas:
	python scripts/validate_schemas.py

check-boundaries:
	python scripts/check_boundaries.py