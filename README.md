# test

This repository now includes a small, dependency-free Python analysis for estimating
each portfolio's daily return exposure to eight sector ETFs:

- XLB (Materials)
- XLE (Energy)
- XLF (Financials)
- XLI (Industrials)
- XLK (Technology)
- XLP (Consumer Staples)
- XLU (Utilities)
- XLV (Health Care)

Run the analysis with:

```bash
python portfolio_sector_exposure.py
```

Generated outputs:

- `results/portfolio_sector_exposures.csv`
- `results/portfolio_sector_exposure_summary.md`
