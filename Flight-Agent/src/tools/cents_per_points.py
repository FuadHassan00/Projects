from langchain_core.tools import tool

@tool
def compare_cash_vs_points(cash_price: float,points_required: int,award_taxes: float,min_cpp: float = 1.5):
    """Compare cash and award flights using cents per point."""
    
    if cash_price < 0 or points_required <= 0 or award_taxes < 0:
        raise ValueError("Invalid flight pricing inputs")

    cpp = ((cash_price - award_taxes) / points_required) * 100

    if cpp >= 3.0:
        value = "Exceptional"
    elif cpp >= 2.0:
        value = "Excellent"
    elif cpp >= 1.5:
        value = "Good"
    elif cpp >= 1.0:
        value = "Fair"
    else:
        value = "Poor"

    recommendation = "Points" if cpp >= min_cpp else "Cash"

    return {
        "cash_price": cash_price,
        "points_required": points_required,
        "award_taxes": award_taxes,
        "cpp": round(cpp, 2),
        "redemption_value": value,
        "recommendation": recommendation,
        "break_even_cash_price": round(
            award_taxes + (points_required * min_cpp / 100), 2
        )
    }