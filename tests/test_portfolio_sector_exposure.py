import unittest

from portfolio_sector_exposure import compute_adj_close_returns, run_ols


class PortfolioSectorExposureTests(unittest.TestCase):
    def test_compute_adj_close_returns_uses_adj_close(self) -> None:
        rows = [
            {"date": "2026-01-02 00:00:00+00:00", "Adj Close": "100.0", "Close": "99.0"},
            {"date": "2026-01-03 00:00:00+00:00", "Adj Close": "110.0", "Close": "108.0"},
            {"date": "2026-01-04 00:00:00+00:00", "Adj Close": "99.0", "Close": "97.0"},
        ]

        returns = compute_adj_close_returns(rows)

        self.assertEqual(set(returns), {"2026-01-03", "2026-01-04"})
        self.assertAlmostEqual(returns["2026-01-03"], 0.10)
        self.assertAlmostEqual(returns["2026-01-04"], -0.10)

    def test_run_ols_recovers_known_betas(self) -> None:
        x_rows = [
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0],
            [2.0, 1.0],
            [1.0, 2.0],
        ]
        y_values = [0.6, -0.1, 0.4, 0.9, 0.2]

        result = run_ols(y_values, x_rows, ["XLF", "XLK"])

        self.assertEqual(result["n_obs"], 5)
        self.assertAlmostEqual(result["alpha"], 0.1, places=10)
        self.assertAlmostEqual(result["betas"]["XLF"], 0.5, places=10)
        self.assertAlmostEqual(result["betas"]["XLK"], -0.2, places=10)
        self.assertAlmostEqual(result["r_squared"], 1.0, places=10)


if __name__ == "__main__":
    unittest.main()
