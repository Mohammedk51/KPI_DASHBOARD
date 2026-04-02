from app import calculate_kpis, get_sample_data


def test_sample_data_has_expected_columns() -> None:
    df = get_sample_data()
    assert set(df.columns) == {"month", "revenue", "expenses"}
    assert len(df) == 6


def test_calculate_kpis_outputs_correct_values() -> None:
    df = get_sample_data()
    result = calculate_kpis(df)

    assert result["total_revenue"] == 92000.0
    assert result["total_expenses"] == 52000.0
    assert result["net_cash_flow"] == 40000.0
    assert round(result["margin_pct"], 2) == 43.48
