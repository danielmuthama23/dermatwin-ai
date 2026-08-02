"""Agent 4 — Retail Concierge Agent.

Given a routine/outfit list, finds matching products, bundles, and
lowest prices. Stubbed with mock catalog data — wire to real retailer
product feeds / price-comparison APIs for production.
"""

_MOCK_CATALOG = {
    "hyaluronic acid serum": [("Brand A", 18.99), ("Brand B", 24.50)],
    "salicylic acid cleanser": [("Brand C", 12.00), ("Brand A", 15.75)],
    "spf 30": [("Brand D", 16.00), ("Brand B", 19.99)],
}


def find_deals(routine_items: list[str]) -> list[dict]:
    deals = []
    for item in routine_items:
        key = next((k for k in _MOCK_CATALOG if k in item.lower()), None)
        if key:
            options = sorted(_MOCK_CATALOG[key], key=lambda x: x[1])
            deals.append({
                "item": item,
                "best_price": {"brand": options[0][0], "price": options[0][1]},
                "alternatives": options[1:],
            })
    if len(deals) >= 2:
        deals.append({"bundle_suggestion": "2+ items from the same brand often unlock a bundle discount"})
    return deals
