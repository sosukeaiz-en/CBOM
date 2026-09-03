from app.models.enums import StandardStatus

NIST_STANDARDS = [
    {
        "standard_id": "FIPS 203",
        "title": "Module-Lattice-Based Key-Encapsulation Mechanism Standard",
        "status": StandardStatus.FINAL_STANDARD,
        "release_date": "2024-08-13",
        "url": "https://csrc.nist.gov/pubs/fips/203/final"
    },
    {
        "standard_id": "FIPS 204",
        "title": "Module-Lattice-Based Digital Signature Standard",
        "status": StandardStatus.FINAL_STANDARD,
        "release_date": "2024-08-13",
        "url": "https://csrc.nist.gov/pubs/fips/204/final"
    },
    {
        "standard_id": "FIPS 205",
        "title": "Stateless Hash-Based Digital Signature Standard",
        "status": StandardStatus.FINAL_STANDARD,
        "release_date": "2024-08-13",
        "url": "https://csrc.nist.gov/pubs/fips/205/final"
    }
]
