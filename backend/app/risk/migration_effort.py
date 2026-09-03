class MigrationEffortEstimator:
    def estimate_effort(
        self,
        asset_count: int,
        dependency_centrality: float = 0.5,
        crypto_agility_level: str = "MEDIUM"
    ) -> tuple[float, float, str]:
        # Base person-days per asset
        base_days_per_asset = 5.0

        # Adjust for centrality and agility
        centrality_multiplier = 1.0 + (dependency_centrality * 1.5)
        agility_multiplier = 1.5 if crypto_agility_level == "LOW" else (1.0 if crypto_agility_level == "MEDIUM" else 0.7)

        total_person_effort = max(1.0, asset_count * base_days_per_asset * centrality_multiplier * agility_multiplier)

        # Calendar duration assumes parallelization factor (e.g. 2.5 FTE engineers)
        parallelization_factor = 2.5
        calendar_duration = max(1.0, total_person_effort / parallelization_factor)

        explanation = (
            f"Estimated {total_person_effort:.1f} person-days based on {asset_count} assets, "
            f"centrality score {dependency_centrality:.2f}, agility level '{crypto_agility_level}'. "
            f"Calendar duration ~{calendar_duration:.1f} working days with {parallelization_factor} FTEs."
        )

        return total_person_effort, calendar_duration, explanation
