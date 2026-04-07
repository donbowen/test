from __future__ import annotations

import csv
import io
import math
import urllib.request
from collections import OrderedDict, defaultdict
from pathlib import Path


PORTFOLIO_RETURNS_URL = (
    "https://raw.githubusercontent.com/LeDataSciFi/ledatascifi-2025/main/"
    "data/daily_portfolio_returns.csv"
)
SECTOR_ETFS = OrderedDict(
    [
        ("XLB", "Materials"),
        ("XLE", "Energy"),
        ("XLF", "Financials"),
        ("XLI", "Industrials"),
        ("XLK", "Technology"),
        ("XLP", "Consumer Staples"),
        ("XLU", "Utilities"),
        ("XLV", "Health Care"),
    ]
)
ETF_DATA_URL_TEMPLATE = (
    "https://raw.githubusercontent.com/do0405/invest-prototype/"
    "09e973c73579f0067c8fa2b3ae7e624c85eab61f/data/us/{symbol}.csv"
)
RESULTS_DIR = Path(__file__).resolve().parent / "results"
EXPOSURES_CSV = RESULTS_DIR / "portfolio_sector_exposures.csv"
SUMMARY_MD = RESULTS_DIR / "portfolio_sector_exposure_summary.md"


def fetch_csv_rows(url: str) -> list[dict[str, str]]:
    with urllib.request.urlopen(url, timeout=30) as response:
        text = response.read().decode("utf-8")
    return list(csv.DictReader(io.StringIO(text)))


def portfolio_date_key(date_formatted: str) -> str:
    return date_formatted[:10]


def market_date_key(date_formatted: str) -> str:
    return date_formatted[:10]


def compute_adj_close_returns(rows: list[dict[str, str]]) -> dict[str, float]:
    returns: dict[str, float] = {}
    previous_close: float | None = None
    for row in rows:
        date_key = market_date_key(row["date"])
        price_text = row.get("Adj Close") or row["Close"]
        close_price = float(price_text)
        if previous_close is not None:
            returns[date_key] = close_price / previous_close - 1.0
        previous_close = close_price
    return returns


def load_portfolio_returns() -> dict[str, dict[str, float]]:
    portfolios: dict[str, dict[str, float]] = defaultdict(dict)
    for row in fetch_csv_rows(PORTFOLIO_RETURNS_URL):
        if not row["ret"]:
            continue
        portfolios[row["display_name"]][portfolio_date_key(row["date_formatted"])] = float(
            row["ret"]
        )
    return dict(portfolios)


def load_sector_returns() -> dict[str, dict[str, float]]:
    return {
        symbol: compute_adj_close_returns(
            fetch_csv_rows(ETF_DATA_URL_TEMPLATE.format(symbol=symbol))
        )
        for symbol in SECTOR_ETFS
    }


def solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    size = len(matrix)
    augmented = [row[:] + [vector[index]] for index, row in enumerate(matrix)]

    for pivot_column in range(size):
        pivot_row = max(
            range(pivot_column, size),
            key=lambda row_index: abs(augmented[row_index][pivot_column]),
        )
        if math.isclose(augmented[pivot_row][pivot_column], 0.0, abs_tol=1e-12):
            raise ValueError("Regression design matrix is singular.")
        augmented[pivot_column], augmented[pivot_row] = (
            augmented[pivot_row],
            augmented[pivot_column],
        )

        pivot_value = augmented[pivot_column][pivot_column]
        for column_index in range(pivot_column, size + 1):
            augmented[pivot_column][column_index] /= pivot_value

        for row_index in range(size):
            if row_index == pivot_column:
                continue
            factor = augmented[row_index][pivot_column]
            if math.isclose(factor, 0.0, abs_tol=1e-15):
                continue
            for column_index in range(pivot_column, size + 1):
                augmented[row_index][column_index] -= (
                    factor * augmented[pivot_column][column_index]
                )

    return [augmented[row_index][size] for row_index in range(size)]


def run_ols(y_values: list[float], x_rows: list[list[float]], factor_names: list[str]) -> dict:
    if len(y_values) != len(x_rows):
        raise ValueError("y_values and x_rows must have the same length.")
    if not y_values:
        raise ValueError("At least one observation is required.")
    if len(y_values) <= len(factor_names) + 1:
        raise ValueError("Not enough observations to estimate the regression.")

    design_matrix = [[1.0] + row for row in x_rows]
    parameter_count = len(design_matrix[0])
    xtx = [[0.0] * parameter_count for _ in range(parameter_count)]
    xty = [0.0] * parameter_count

    for row, y_value in zip(design_matrix, y_values):
        for row_index in range(parameter_count):
            xty[row_index] += row[row_index] * y_value
            for column_index in range(parameter_count):
                xtx[row_index][column_index] += row[row_index] * row[column_index]

    coefficients = solve_linear_system(xtx, xty)
    mean_y = sum(y_values) / len(y_values)
    sst = sum((y_value - mean_y) ** 2 for y_value in y_values)
    sse = sum(
        (y_value - sum(coefficient * value for coefficient, value in zip(coefficients, row)))
        ** 2
        for y_value, row in zip(y_values, design_matrix)
    )
    r_squared = 1.0 if math.isclose(sst, 0.0, abs_tol=1e-15) else 1.0 - (sse / sst)

    return {
        "alpha": coefficients[0],
        "betas": dict(zip(factor_names, coefficients[1:])),
        "n_obs": len(y_values),
        "r_squared": r_squared,
    }


def estimate_portfolio_exposures() -> list[dict[str, float | int | str]]:
    portfolios = load_portfolio_returns()
    sector_returns = load_sector_returns()
    common_factor_dates = set.intersection(
        *(set(returns_by_date) for returns_by_date in sector_returns.values())
    )

    results: list[dict[str, float | int | str]] = []
    factor_names = list(SECTOR_ETFS)

    for display_name in sorted(portfolios):
        portfolio_returns = portfolios[display_name]
        regression_dates = sorted(common_factor_dates & set(portfolio_returns))
        y_values = [portfolio_returns[date_key] for date_key in regression_dates]
        x_rows = [
            [sector_returns[symbol][date_key] for symbol in factor_names]
            for date_key in regression_dates
        ]
        regression_result = run_ols(y_values, x_rows, factor_names)
        result_row: dict[str, float | int | str] = {
            "display_name": display_name,
            "start_date": regression_dates[0],
            "end_date": regression_dates[-1],
            "n_obs": regression_result["n_obs"],
            "r_squared": regression_result["r_squared"],
            "alpha": regression_result["alpha"],
        }
        result_row.update(regression_result["betas"])
        results.append(result_row)

    return results


def write_exposure_csv(rows: list[dict[str, float | int | str]]) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    fieldnames = [
        "display_name",
        "start_date",
        "end_date",
        "n_obs",
        "r_squared",
        "alpha",
        *SECTOR_ETFS,
    ]
    with EXPOSURES_CSV.open("w", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def strongest_exposures(row: dict[str, float | int | str], limit: int = 3) -> str:
    ranked = sorted(
        ((symbol, float(row[symbol])) for symbol in SECTOR_ETFS),
        key=lambda item: abs(item[1]),
        reverse=True,
    )
    return ", ".join(f"{symbol} ({beta:+.3f})" for symbol, beta in ranked[:limit])


def write_summary(rows: list[dict[str, float | int | str]]) -> None:
    lines = [
        "# Portfolio sector ETF exposures",
        "",
        "Regression: portfolio daily return ~ alpha + "
        + " + ".join(f"{symbol} ({name})" for symbol, name in SECTOR_ETFS.items()),
        "",
        f"Outputs are based on `{PORTFOLIO_RETURNS_URL}` and sector ETF price histories from `{ETF_DATA_URL_TEMPLATE}`.",
        "The overlapping regression sample ends on the last date available across all selected ETF series.",
        "",
        "| Portfolio | Sample | Observations | R² | Largest absolute betas |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['display_name']} | {row['start_date']} to {row['end_date']} | "
            f"{row['n_obs']} | {float(row['r_squared']):.3f} | "
            f"{strongest_exposures(row)} |"
        )
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = estimate_portfolio_exposures()
    write_exposure_csv(rows)
    write_summary(rows)
    print(f"Wrote {EXPOSURES_CSV}")
    print(f"Wrote {SUMMARY_MD}")


if __name__ == "__main__":
    main()
