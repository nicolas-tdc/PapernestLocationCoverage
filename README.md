# PapernestLocationCoverage
API to convert physical address into telecommunication coverage by provider.
Created using Django Rest Framework.

---

Superuser logs : papernest_admin / WhoLikesPaperwork?0!

---

Models :

  - Provider (Orange, SFR...).

  - CoverageType (2G, 3G...).

  - CoverageSite : geographic coordinates, provider and coverage type.

---

Serializers are created using rest_framework `HyperlinkedModelSerializer`.

---

Custom command line to import CSV file from url to database :

  - `python manage.py csv_to_db`

  - Two arguments available :

    `--reset_all_coverage` : Delete all existing objects linked to provider and coverage models before import.

    `--reset_coverage_sites` : Delete existing objects for CoverageSite model before import.

---

Views:

  - One rest_framework `ViewSet` for each model :

    `providers/`

    `coverage-sites/`

    `coverage-types/`

  - One custom api_view `location_coverage` retrieving network coverage for a given address :

    `location-coverage/?q=42+rue+papernest+75011+Paris`

  - Pagination is set to 100 items per page.

---

Tests:

  Implemented for models, import, `location_coverage` api_view and `location_coverage` helpers.
