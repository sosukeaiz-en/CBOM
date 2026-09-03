from datetime import datetime, timezone


class MoscaCalculator:
    """
    Mosca Theorem Implementation:
    X = Security Shelf-Life (years required for data secrecy/integrity protection)
    Y = Migration Time (years required to migrate system to PQC)
    Z = Quantum Threat Horizon (year when a CRQC is estimated to arrive, e.g. 2035)

    Condition: If X + Y > (Z - current_year), data is ALREADY at risk of Harvest-Now-Decrypt-Later (HNDL).
    """

    def calculate_urgency(self, x_years: float, y_years: float, z_year: float) -> tuple[float, bool, str]:
        current_year = datetime.now(timezone.utc).year
        years_remaining = z_year - current_year

        total_time_needed = x_years + y_years
        urgency_flag = total_time_needed > years_remaining

        if years_remaining <= 0:
            score = 100.0
            explanation = "Quantum threat horizon has reached or passed zero margin."
        elif urgency_flag:
            overflow = total_time_needed - years_remaining
            score = min(100.0, 75.0 + (overflow * 5.0))
            explanation = f"Urgent! Data protection lifetime ({x_years}y) + migration ({y_years}y) exceeds horizon until {int(z_year)} by {overflow:.1f} years."
        else:
            margin = years_remaining - total_time_needed
            score = max(10.0, 50.0 - (margin * 3.0))
            explanation = f"Mosca condition satisfied with safety margin of {margin:.1f} years until threat horizon {int(z_year)}."

        return score, urgency_flag, explanation
