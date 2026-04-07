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
python /home/runner/work/test/test/portfolio_sector_exposure.py
```

Generated outputs:

- `/home/runner/work/test/test/results/portfolio_sector_exposures.csv`
- `/home/runner/work/test/test/results/portfolio_sector_exposure_summary.md`
