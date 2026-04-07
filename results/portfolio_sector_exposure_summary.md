# Portfolio sector ETF exposures

Regression: portfolio daily return ~ alpha + XLB (Materials) + XLE (Energy) + XLF (Financials) + XLI (Industrials) + XLK (Technology) + XLP (Consumer Staples) + XLU (Utilities) + XLV (Health Care)

Outputs are based on `https://raw.githubusercontent.com/LeDataSciFi/ledatascifi-2025/main/data/daily_portfolio_returns.csv` and sector ETF price histories from `https://raw.githubusercontent.com/do0405/invest-prototype/09e973c73579f0067c8fa2b3ae7e624c85eab61f/data/us/{symbol}.csv`.
The overlapping regression sample ends on the last date available across all selected ETF series.

| Portfolio | Sample | Observations | R² | Largest absolute betas |
| --- | --- | ---: | ---: | --- |
| Aastha_Dave | 2026-02-04 to 2026-03-11 | 25 | 0.577 | XLV (+0.126), XLE (-0.085), XLB (+0.049) |
| Chikodil | 2026-02-18 to 2026-03-11 | 16 | 0.751 | XLB (-1.067), XLP (+0.676), XLK (+0.553) |
| Coby_Walmsley | 2026-02-04 to 2026-03-11 | 25 | 0.527 | XLI (+0.493), XLE (+0.326), XLP (-0.146) |
| Ford_Campbell | 2026-02-04 to 2026-03-11 | 25 | 0.509 | XLF (+0.381), XLU (+0.206), XLI (+0.090) |
| MaxMessina | 2026-02-04 to 2026-03-11 | 25 | 0.333 | XLE (-0.243), XLP (+0.234), XLK (+0.222) |
| Owen_Higinbotham | 2026-02-04 to 2026-03-11 | 25 | 0.461 | XLE (-0.252), XLI (+0.235), XLB (+0.117) |
| Prince_Ansah | 2026-02-11 to 2026-03-11 | 20 | 0.786 | XLF (-0.380), XLV (+0.377), XLE (-0.313) |
| VickyLi | 2026-02-04 to 2026-03-11 | 25 | 0.573 | XLE (-0.535), XLB (+0.448), XLV (+0.330) |
| Yang_ | 2026-02-04 to 2026-03-11 | 25 | 0.437 | XLI (-0.344), XLV (+0.274), XLK (+0.243) |
| Yoav_Weinberg | 2026-02-04 to 2026-03-11 | 25 | 0.342 | XLK (+0.362), XLE (-0.239), XLB (+0.224) |
| atauber | 2026-02-04 to 2026-03-11 | 25 | 0.344 | XLK (+0.350), XLI (-0.215), XLV (+0.201) |
| harry-keen | 2026-02-04 to 2026-03-11 | 25 | 0.480 | XLV (+0.344), XLK (-0.110), XLI (+0.066) |
| johnmanning | 2026-02-04 to 2026-03-11 | 25 | 0.653 | XLI (+0.969), XLP (-0.341), XLK (-0.251) |
| jrcon | 2026-02-04 to 2026-03-11 | 25 | 0.359 | XLI (+0.336), XLU (+0.215), XLP (-0.212) |
| niija | 2026-02-04 to 2026-03-11 | 25 | 0.268 | XLP (+0.229), XLK (+0.163), XLV (-0.086) |
