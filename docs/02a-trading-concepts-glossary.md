# PoorToPour Trading Concepts Glossary

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Document:** `/docs/02a-trading-concepts-glossary.md`  
**Date created:** 2026-04-30  
**Last updated:** 2026-04-30  
**Status:** Draft v0.1

---

## 1. Purpose

This glossary explains the trading concepts used in `/docs/02-trading-strategy-requirements.md`.

The intended audience is someone with basic financial knowledge who understands stocks, price movements, and investing at a high level, but may not be deeply familiar with technical trading language.

This is not meant to be a complete trading textbook. It is a starting point for understanding the vocabulary and logic used by PoorToPour.

---

## 2. Core Trading Terms

## 2.1 Ticker / Symbol

A ticker is the short code used to identify a publicly traded security.

Examples:

| Company | Ticker |
| --- | --- |
| Apple | AAPL |
| Microsoft | MSFT |
| NVIDIA | NVDA |
| SPDR S&P 500 ETF | SPY |

PoorToPour scans tickers to find possible trade setups.

---

## 2.2 Equity / Stock

A stock represents ownership in a company.

In PoorToPour MVP, we focus on U.S. equities, meaning publicly traded U.S. company stocks.

---

## 2.3 ETF

An ETF, or exchange-traded fund, is a basket of assets that trades like a stock.

Example:

| ETF | Meaning |
| --- | --- |
| SPY | Tracks the S&P 500 |
| QQQ | Tracks the Nasdaq 100 |
| IWM | Tracks the Russell 2000 |
| XLF | Financial sector ETF |
| XLK | Technology sector ETF |

PoorToPour MVP uses SPY mainly as a market benchmark.

---

## 2.4 SPY

SPY is an ETF that tracks the S&P 500.

PoorToPour uses SPY as a simple benchmark to answer:

> Is this stock stronger or weaker than the broader market?

Example:

If MSFT is up 8% over 20 trading days and SPY is up 2%, MSFT is outperforming SPY by about 6 percentage points.

---

## 2.5 Long / Long-Only

Being long means buying a stock because you expect the price to go up.

Long-only means the strategy only looks for buying opportunities, not short-selling opportunities.

PoorToPour MVP is long-only.

Reason:

- simpler;
- less risky than shorting;
- easier to understand;
- easier to validate;
- better for a first scanner.

---

## 2.6 Short Selling

Short selling means borrowing and selling a stock because you expect the price to go down, then buying it back later at a lower price.

It is out of scope for the MVP.

ELI5:

Imagine borrowing your friend's rare Pokémon card, selling it for $100, hoping the market price drops to $70, then buying it back and returning it. You keep $30. But if the card price rises to $200, you are in trouble. Shorting has theoretically unlimited risk because a stock can rise far more than 100%.

---

## 2.7 Trade Setup

A trade setup is a recognizable condition that suggests a possible trading opportunity.

Examples:

- price breaking above recent resistance;
- strong stock pulling back to support;
- stock outperforming the market;
- unusual volume supporting a price move.

A setup is not a guaranteed trade. It is a reason to investigate.

---

## 2.8 Candidate

A candidate is a ticker selected by the scanner for review.

In PoorToPour, a candidate should include:

- setup type;
- score;
- explanation;
- chart evidence;
- risk/reward estimate;
- caution flags.

---

## 2.9 Watchlist

A watchlist is a saved list of tickers the user wants to monitor.

In PoorToPour, watchlist is MVP+ unless trivial.

---

## 3. Price and Candle Terms

## 3.1 OHLCV

OHLCV means:

| Letter | Meaning |
| --- | --- |
| O | Open price |
| H | High price |
| L | Low price |
| C | Close price |
| V | Volume |

This is the basic price data used to build candles and calculate most technical indicators.

---

## 3.2 Open Price

The open is the first traded price during a trading session.

For daily candles, it is the first price after the market opens.

---

## 3.3 High Price

The high is the highest traded price during the selected period.

For daily candles, it is the highest price of the day.

---

## 3.4 Low Price

The low is the lowest traded price during the selected period.

For daily candles, it is the lowest price of the day.

---

## 3.5 Close Price

The close is the final traded price during the selected period.

For daily candles, the close is especially important because many traders and systems use it to confirm signals.

PoorToPour MVP mostly uses close-based signals because daily close data is easier to validate than intraday noise.

---

## 3.6 Adjusted Close

Adjusted close modifies the close price to account for corporate actions such as stock splits and dividends.

This is useful for historical analysis.

Example:

If a stock splits 2-for-1, the historical price chart is adjusted so the chart remains comparable over time.

---

## 3.7 Volume

Volume is the number of shares traded during a period.

High volume means more shares changed hands.

Why it matters:

- confirms participation;
- helps avoid illiquid stocks;
- can validate a breakout;
- can warn when a move is weak.

ELI5:

If one person says a restaurant is amazing, maybe they are just enthusiastic. If 2,000 people line up outside, something bigger is happening. Volume is the crowd size behind the price move.

---

## 3.8 Candlestick / Candle

A candle visually represents open, high, low, and close for a period.

For daily candles, one candle equals one trading day.

Candles help traders quickly see whether price moved up, down, reversed, or stayed quiet.

---

## 3.9 Green Candle / Red Candle

A green candle usually means the close was higher than the open.

A red candle usually means the close was lower than the open.

Color conventions can vary by charting tool.

---

## 3.10 Gap

A gap happens when a stock opens significantly above or below the previous close.

Example:

- Yesterday close: $100
- Today open: $108
- Gap up: 8%

Gaps often happen because of earnings, news, analyst upgrades, or market-wide events.

MVP note:

Gap-up momentum is not part of the first MVP strategy. It may be added later for intraday scanning.

---

## 4. Trend and Support/Resistance

## 4.1 Trend

A trend describes the general direction of price over time.

| Trend Type | Meaning |
| --- | --- |
| Uptrend | Price generally moves higher |
| Downtrend | Price generally moves lower |
| Sideways | Price moves in a range |

PoorToPour MVP prefers long candidates in uptrends.

---

## 4.2 Support

Support is a price area where buyers have previously stepped in.

It is not a magic floor. It is an area where price may stabilize.

Example:

If a stock repeatedly bounces near $100, traders may treat $100 as support.

ELI5:

Support is like a trampoline zone. Price falls into it and may bounce, but if the trampoline breaks, the fall can continue.

---

## 4.3 Resistance

Resistance is a price area where sellers have previously appeared.

It is not a magic ceiling. It is an area where price may struggle.

Example:

If a stock repeatedly fails near $120, traders may treat $120 as resistance.

ELI5:

Resistance is like a ceiling. Price keeps jumping and bumping its head. A breakout happens when it finally smashes through.

---

## 4.4 Breakout

A breakout happens when price moves above a prior resistance area or recent high.

PoorToPour breakout logic looks for:

- close above recent high;
- strong volume;
- positive trend;
- reasonable risk/reward.

ELI5:

Imagine a stock trapped in a box. A breakout is when it climbs out of the box with enough energy that the move might continue.

---

## 4.5 Pullback

A pullback is a temporary decline or pause within a larger uptrend.

PoorToPour pullback continuation logic looks for:

- stock still in an uptrend;
- price pulls back near support;
- momentum cools without breaking the trend;
- risk/reward remains reasonable.

ELI5:

A strong runner slows down to catch breath. That does not mean the race is over. A healthy pullback is the breathing moment before possibly continuing.

---

## 4.6 Consolidation

Consolidation happens when price moves sideways within a range.

It can show a pause before the next move.

A breakout from consolidation can be interesting if volume confirms it.

---

## 4.7 Swing High / Swing Low

A swing high is a local peak in price.

A swing low is a local bottom in price.

Traders often use swing lows as possible invalidation or stop-loss references.

Example:

If a pullback bounced from $95, that $95 area may become a recent swing low.

---

## 5. Moving Averages

## 5.1 Moving Average

A moving average smooths price data by averaging prices over a selected number of periods.

Why it matters:

- shows trend direction;
- reduces noise;
- highlights possible support/resistance areas.

ELI5:

Instead of watching every single wave in the ocean, a moving average helps you see whether the tide is generally rising or falling.

---

## 5.2 SMA - Simple Moving Average

SMA means simple moving average.

It is calculated by averaging the closing prices over a fixed number of periods.

Common examples:

| SMA | Meaning |
| --- | --- |
| SMA 20 | Average close over last 20 trading days |
| SMA 50 | Average close over last 50 trading days |
| SMA 200 | Average close over last 200 trading days |

PoorToPour uses:

- SMA 20 for short-term trend/support;
- SMA 50 for medium-term trend;
- SMA 200 for long-term trend.

---

## 5.3 EMA - Exponential Moving Average

EMA means exponential moving average.

It is similar to SMA but gives more weight to recent prices.

This makes EMA react faster to recent price changes.

Common examples:

| EMA | Meaning |
| --- | --- |
| EMA 8 | Short-term momentum |
| EMA 21 | Short/intermediate trend |

MVP note:

EMA 8/21 may be computed but does not need to drive the first MVP.

---

## 5.4 Price Above Moving Average

When price is above a moving average, it often suggests strength.

Example:

If price is above SMA 50 and SMA 200, the stock may be in a healthier uptrend.

Not guaranteed:

A stock can be above moving averages and still reverse.

---

## 5.5 Price Below Moving Average

When price is below a moving average, it often suggests weakness.

For long-only strategies, price below key moving averages is usually a caution sign.

---

## 5.6 Moving Average Alignment

Moving average alignment describes the order of moving averages.

Bullish example:

```text
Price > SMA 20 > SMA 50 > SMA 200
```

This suggests short-term, medium-term, and long-term trends are aligned upward.

Bearish example:

```text
Price < SMA 20 < SMA 50 < SMA 200
```

This suggests broad weakness.

---

## 5.7 Golden Cross / Death Cross

Golden cross:

- SMA 50 crosses above SMA 200.
- Often interpreted as a longer-term bullish signal.

Death cross:

- SMA 50 crosses below SMA 200.
- Often interpreted as a longer-term bearish signal.

MVP note:

PoorToPour does not need to rely on these as primary signals.

---

## 6. Momentum Indicators

## 6.1 Momentum

Momentum describes the speed and strength of price movement.

A stock rising steadily with strong participation has positive momentum.

A stock falling quickly has negative momentum.

---

## 6.2 RSI - Relative Strength Index

RSI is a momentum indicator that ranges from 0 to 100.

Common interpretation:

| RSI Range | Typical Interpretation |
| --- | --- |
| Below 30 | Potentially oversold |
| 30–50 | Weak to neutral |
| 50–70 | Positive momentum |
| Above 70 | Potentially overbought |

PoorToPour uses RSI to avoid:

- weak stocks with poor momentum;
- extremely overheated stocks.

For MVP:

- breakout candidates prefer RSI around 50–75;
- pullback candidates prefer RSI around 40–60;
- relative strength leaders prefer RSI around 50–75.

ELI5:

RSI is like a speedometer for price momentum. Too slow can mean weak. Too fast can mean overheated.

---

## 6.3 Overbought

Overbought means price may have moved up too far or too fast.

It does not guarantee a drop.

A strong stock can stay overbought for a long time.

PoorToPour treats overbought as a caution flag, not an automatic sell signal.

---

## 6.4 Oversold

Oversold means price may have moved down too far or too fast.

It does not guarantee a bounce.

PoorToPour MVP does not focus on oversold bounce strategies.

---

## 6.5 MACD

MACD stands for Moving Average Convergence Divergence.

It compares two moving averages to show momentum direction and changes.

Common parts:

| Component | Meaning |
| --- | --- |
| MACD line | Difference between fast and slow moving averages |
| Signal line | Moving average of MACD line |
| Histogram | Difference between MACD line and signal line |

MVP note:

MACD is optional for the first MVP. It can be useful, but we should not overload the first scanner.

ELI5:

MACD is like watching whether the faster runner is pulling away from or catching up to the slower runner. It tries to show momentum shifts.

---

## 7. Volatility and Range

## 7.1 Volatility

Volatility describes how much a stock moves.

High-volatility stocks swing more widely.

Low-volatility stocks move more calmly.

Volatility matters because risk and stop-loss distance should adjust to how much the stock normally moves.

---

## 7.2 ATR - Average True Range

ATR measures the average trading range of a stock over a period.

PoorToPour uses ATR 14.

ATR helps estimate:

- normal daily movement;
- stop-loss buffer;
- whether price is overextended;
- how much room a trade may need.

Example:

If a stock has ATR of $3, it commonly moves around $3 per day.

ELI5:

ATR is the stock's usual wiggle size. A tiny dog and a big dog need different leash lengths. ATR helps avoid giving every stock the same leash.

---

## 7.3 Overextended

A stock is overextended when price has moved too far from its likely support area or normal range.

Example:

If a stock is far above its SMA 20 and RSI is very high, buying immediately may have poor risk/reward.

PoorToPour uses overextension as a caution flag.

---

## 7.4 Range

Range is the difference between high and low over a selected period.

Example:

If daily high is $110 and daily low is $104, the daily range is $6.

ATR is a smoothed version of range.

---

## 8. Volume Concepts

## 8.1 Average Volume

Average volume is the average number of shares traded over a period.

PoorToPour commonly uses 20-day average volume.

---

## 8.2 Dollar Volume

Dollar volume is:

```text
price * volume
```

Example:

If a stock trades 1,000,000 shares at $20, dollar volume is $20,000,000.

Why it matters:

A high share volume in a $1 stock is not the same as high share volume in a $200 stock. Dollar volume helps compare liquidity across stocks.

---

## 8.3 Relative Volume

Relative volume compares current volume to normal volume.

Formula:

```text
relative volume = current volume / average volume
```

Example:

If current volume is 3 million shares and average volume is 1.5 million shares:

```text
relative volume = 3.0M / 1.5M = 2.0x
```

This means volume is twice normal.

PoorToPour uses relative volume to confirm breakouts.

ELI5:

If a quiet café usually has 10 people and today has 50, something is happening. Relative volume measures that “something is happening” feeling.

---

## 8.4 Liquidity

Liquidity describes how easily a stock can be bought or sold without significantly moving the price.

Highly liquid stocks:

- trade frequently;
- have tighter bid/ask spreads;
- are easier to enter/exit.

Illiquid stocks:

- trade less;
- may have wider spreads;
- can move sharply on small orders.

PoorToPour MVP filters for liquidity to avoid messy candidates.

---

## 9. Relative Strength

## 9.1 Relative Strength vs SPY

Relative strength compares a stock's performance to a benchmark.

PoorToPour uses SPY as the default benchmark.

Example:

| Asset | 20-Day Return |
| --- | ---: |
| Stock A | +8% |
| SPY | +2% |

Stock A has positive relative strength of about +6 percentage points versus SPY.

This suggests Stock A is outperforming the broader market.

---

## 9.2 Relative Strength Leader

A relative strength leader is a stock outperforming the market and often trading near highs.

It may not be an immediate buy, but it deserves attention.

PoorToPour uses this setup to find strong names that may later form breakouts or pullbacks.

---

## 9.3 Sector Relative Strength

Sector relative strength compares a stock or sector to the broader market.

Example:

If technology stocks are outperforming SPY, tech may have sector strength.

MVP note:

Sector relative strength is post-MVP unless easy.

---

## 10. Risk and Trade Planning

## 10.1 Entry

Entry is the price area where a trader would consider opening a position.

PoorToPour MVP shows an estimated entry zone, not an instruction.

---

## 10.2 Entry Zone

An entry zone is a price range rather than one exact number.

Example:

A breakout candidate may be interesting around $100–$102 if $100 was resistance.

Why use a zone?

Markets are noisy. Exact penny-perfect entries are unrealistic for most swing-trade planning.

---

## 10.3 Invalidation Level

Invalidation level is the price area where the trade idea is probably wrong.

This is one of the most important concepts in the project.

Example:

If the breakout thesis is “price is strong above $100,” then a close back below $100 may weaken or invalidate the idea.

ELI5:

Invalidation is the point where you admit: “The story I believed is no longer true.”

---

## 10.4 Stop-Loss

A stop-loss is a planned exit level used to limit downside.

Example:

If entry is $100 and stop is $95, the risk is $5 per share.

PoorToPour MVP estimates stop-loss areas for research only.

---

## 10.5 Target

A target is a possible upside price level.

Example:

If entry is $100 and target is $110, the possible reward is $10 per share.

Targets are estimates, not promises.

---

## 10.6 Risk/Reward Ratio

Risk/reward compares possible downside to possible upside.

Formula:

```text
risk/reward = potential reward / potential risk
```

Example:

- Entry: $100
- Stop: $95
- Target: $110
- Risk: $5
- Reward: $10
- Risk/reward: 2:1

PoorToPour prefers at least 2:1 for swing-trade candidates.

ELI5:

If you risk $1 to maybe make $2, that is 2:1. If you risk $1 to maybe make $0.50, the trade needs an extremely high win rate to make sense.

---

## 10.7 R Multiple

R is the amount risked on a trade.

Example:

If risk per share is $5, then:

| Result | Meaning |
| --- | --- |
| +1R | Gain equal to the initial risk |
| +2R | Gain twice the initial risk |
| -1R | Loss equal to the planned risk |

Using R helps compare trades with different prices.

---

## 10.8 Position Sizing

Position sizing determines how many shares to buy based on risk.

Example:

- Account risk allowed: $500
- Entry: $100
- Stop: $95
- Risk per share: $5
- Position size: 100 shares

Formula:

```text
position size = allowed risk dollars / risk per share
```

MVP note:

Position sizing is optional unless account size settings are simple.

---

## 10.9 Risk Per Trade

Risk per trade is the percentage of account equity a trader is willing to lose if the stop is hit.

Common examples:

| Risk Per Trade | Meaning |
| --- | --- |
| 0.5% | Conservative |
| 1.0% | Common disciplined risk level |
| 2.0% | More aggressive |

PoorToPour should default to conservative assumptions.

---

## 10.10 Drawdown

Drawdown is the decline from a peak in account value.

Example:

If an account grows to $100,000 then falls to $90,000, the drawdown is 10%.

Drawdown matters because surviving bad periods is part of trading.

---

## 10.11 Kill Switch

A kill switch is a control that stops trading automation.

MVP note:

No broker automation exists in MVP, but any future live trading system must have a kill switch.

ELI5:

It is the big red “bad robot, stop” button.

---

## 11. Candidate Labels and Warnings

## 11.1 Actionable

In PoorToPour, Actionable means:

> Worth manual review now.

It does not mean:

> Automatically buy.

A candidate may be Actionable if:

- setup rules pass;
- data is fresh;
- risk/reward is acceptable;
- no major caution flag exists.

---

## 11.2 Watch

Watch means the ticker is interesting but not clean enough yet.

Examples:

- strong relative strength but no entry;
- pullback not close enough to support;
- breakout forming but not confirmed;
- earnings date is near.

---

## 11.3 Avoid

Avoid means the setup is poor or risk is not attractive.

Examples:

- overextended;
- weak volume;
- poor risk/reward;
- trend damaged;
- too close to earnings.

---

## 11.4 Blocked

Blocked means PoorToPour cannot make a useful judgment because important data is missing, stale, or invalid.

Examples:

- no recent price data;
- missing volume;
- indicator calculation failed;
- data provider error.

Blocked is important because pretending to know is dangerous.

---

## 11.5 Caution Flag

A caution flag is a warning attached to a candidate.

Examples:

- earnings soon;
- stale data;
- overextended;
- poor risk/reward;
- weak relative strength;
- high volatility.

A caution flag does not always reject a candidate, but it should reduce confidence.

---

## 12. Earnings and Company Context

## 12.1 Earnings

Earnings are regular company financial reports.

They usually include:

- revenue;
- profit;
- EPS;
- management guidance;
- business commentary.

Stock prices can move sharply after earnings.

PoorToPour MVP should warn if earnings are soon.

---

## 12.2 EPS

EPS means earnings per share.

It is company profit divided by number of shares.

Higher EPS can suggest stronger profitability, but context matters.

---

## 12.3 Revenue

Revenue is the money a company earns from selling goods or services before expenses.

Revenue growth can indicate business expansion.

---

## 12.4 Earnings Surprise

An earnings surprise happens when reported results differ from analyst expectations.

Example:

- Expected EPS: $1.00
- Actual EPS: $1.20
- Positive surprise: +20%

Positive surprises can push stocks up, but not always. Market reaction depends on expectations, guidance, valuation, and tone.

---

## 12.5 Guidance

Guidance is management's forecast or outlook for future performance.

A company can beat current earnings but fall if guidance disappoints.

---

## 12.6 Earnings Risk

Earnings risk is the risk that a stock moves sharply after an earnings report.

PoorToPour MVP should warn about upcoming earnings because technical setups can fail suddenly around earnings.

ELI5:

A chart setup before earnings is like setting up a picnic right before a thunderstorm forecast. Maybe it stays sunny, but the risk is obviously different.

---

## 13. Strategy Validation Terms

## 13.1 Backtesting

Backtesting means testing a strategy on historical data.

Example:

If PoorToPour's breakout rules triggered on past dates, we check what happened afterward.

Backtesting helps answer:

- Did the setup tend to work?
- How often did it fail?
- What was the average return?
- Was performance better than SPY?
- Did it only work in certain markets?

ELI5:

Backtesting is using old games to see whether your playbook would have worked.

---

## 13.2 Paper Trading

Paper trading means simulating trades in real time without using real money.

It helps test:

- execution assumptions;
- signal quality;
- emotional realism;
- slippage assumptions;
- tracking discipline.

PoorToPour should not move toward broker automation before paper trading.

---

## 13.3 Forward Testing

Forward testing means testing a strategy from today onward without using future information.

Paper trading is a form of forward testing.

It is useful because backtests can accidentally be too optimistic.

---

## 13.4 Survivorship Bias

Survivorship bias happens when historical testing only includes companies that survived until today.

Example:

Testing only current S&P 500 members over the last 10 years ignores companies that were removed from the index.

This can make results look better than reality.

MVP note:

We should acknowledge this limitation. More rigorous backtesting later should use survivorship-bias-aware data.

---

## 13.5 Lookahead Bias

Lookahead bias happens when a strategy accidentally uses information that would not have been known at the time.

Example:

Using today's close price to trigger a trade that supposedly happened earlier today.

This can make a strategy look unrealistically good.

PoorToPour must avoid lookahead bias in future backtesting.

ELI5:

It is like taking tomorrow's answer key into yesterday's exam.

---

## 13.6 Slippage

Slippage is the difference between expected trade price and actual trade price.

Example:

You expect to buy at $100, but your order fills at $100.25.

Slippage matters more for:

- illiquid stocks;
- fast-moving stocks;
- large position sizes;
- intraday trading.

---

## 13.7 Commission

Commission is the fee paid to execute a trade.

Many brokers have zero-commission stock trading, but other costs such as spread and slippage still exist.

---

## 13.8 Spread

The spread is the difference between bid and ask price.

Example:

- Bid: $100.00
- Ask: $100.10
- Spread: $0.10

Wide spreads increase trading cost.

---

## 13.9 Expectancy

Expectancy estimates the average expected result per trade.

A simplified formula:

```text
expectancy = (win rate * average win) - (loss rate * average loss)
```

Example:

- Win rate: 50%
- Average win: $200
- Loss rate: 50%
- Average loss: $100

```text
expectancy = (0.5 * 200) - (0.5 * 100) = 50
```

This means the average trade is expected to make $50 before other costs.

ELI5:

Expectancy asks: “If we play this game many times, does the math favor us?”

---

## 14. Market Environment Terms

## 14.1 Market Regime

Market regime describes the broader market condition.

Examples:

| Regime | Meaning |
| --- | --- |
| Bullish | Market generally rising |
| Bearish | Market generally falling |
| Choppy | Market lacks clear direction |
| High volatility | Big market swings |
| Low volatility | Quiet market |

Post-MVP, PoorToPour may adjust signals based on market regime.

---

## 14.2 Bull Market

A bull market is a period where prices generally rise.

Long-only strategies usually work better in bull markets.

---

## 14.3 Bear Market

A bear market is a period where prices generally fall.

Long-only strategies usually become harder in bear markets.

---

## 14.4 Choppy Market

A choppy market moves up and down without clear direction.

Breakout strategies can struggle in choppy markets because breakouts may fail quickly.

---

## 14.5 Sector Rotation

Sector rotation happens when money moves from one sector to another.

Example:

Investors may rotate from technology stocks into energy stocks.

Post-MVP, sector strength may help PoorToPour prioritize candidates.

---

## 15. Data Quality Terms

## 15.1 Fresh Data

Fresh data is recent enough for the intended decision.

Example:

For a daily scan after market close, the latest daily candle should usually be from the latest completed trading day.

---

## 15.2 Stale Data

Stale data is outdated.

PoorToPour should warn or block candidates when required data is stale.

ELI5:

Trading on stale data is like driving using yesterday's traffic map.

---

## 15.3 Missing Data

Missing data means a required field is unavailable.

Examples:

- no recent close price;
- missing volume;
- missing earnings date;
- failed indicator calculation.

PoorToPour should not pretend missing data is fine.

---

## 15.4 Data Provider

A data provider is a service that supplies market, company, earnings, or news data.

Examples may include:

- market data APIs;
- SEC data;
- financial news APIs;
- broker APIs;
- prediction market APIs.

Provider choices are handled in `/docs/04-data-sources.md`.

---

## 15.5 Rate Limit

A rate limit is a provider's restriction on how many API calls can be made in a time period.

Example:

A free API may allow only a small number of calls per day.

PoorToPour should cache data and batch requests to avoid hitting rate limits.

---

## 16. AI and Research Terms

## 16.1 AI Summary

An AI summary is a natural-language explanation generated by an LLM.

Post-MVP, AI may summarize:

- candidate evidence;
- company background;
- earnings context;
- recent headlines;
- bull/bear notes.

MVP note:

AI summaries are not required.

---

## 16.2 AI Agent

An AI agent is an AI workflow that can perform tasks with some autonomy, such as searching, summarizing, comparing, or planning.

PoorToPour may eventually use agents for research, but not for MVP trade decisions.

---

## 16.3 Deterministic Rule

A deterministic rule produces the same result for the same input.

Example:

```text
If close > 20-day high and relative volume > 1.5x, then breakout condition passes.
```

PoorToPour MVP should rely on deterministic rules so results are explainable and backtestable.

---

## 16.4 Black Box

A black box system gives outputs without clear explanation.

PoorToPour should avoid black-box trade decisions, especially in MVP.

---

## 17. PoorToPour MVP Concept Map

The first scanner works roughly like this:

```text
Stock universe
  -> liquidity filters
  -> daily OHLCV data
  -> technical indicators
  -> setup rules
  -> score
  -> caution flags
  -> risk/reward estimate
  -> candidate status
  -> dashboard review
```

Plain-English version:

1. Choose a clean list of stocks.
2. Remove stocks that are too illiquid or missing data.
3. Calculate chart indicators.
4. Check whether each stock matches a known setup.
5. Rank the interesting ones.
6. Show the evidence.
7. Let the user manually review.

---

## 18. Recommended Learning Path

To understand `/docs/02-trading-strategy-requirements.md`, read concepts in this order:

1. OHLCV.
2. Candlesticks.
3. Trend.
4. Support and resistance.
5. Moving averages.
6. Volume and relative volume.
7. RSI.
8. ATR.
9. Breakout.
10. Pullback.
11. Relative strength.
12. Risk/reward.
13. Stop-loss and invalidation.
14. Backtesting.
15. Lookahead bias and survivorship bias.

---

## 19. Good Research Questions for Later

When reviewing a concept, ask:

- What problem does this concept solve?
- Can it be calculated from data we can obtain?
- Is it useful for ranking candidates?
- Does it help control risk?
- Does it introduce false confidence?
- Can it be backtested?
- Does it belong in MVP or later?

---

## 20. Change Log

| Date | Version | Update | Author |
| --- | --- | --- | --- |
| 2026-04-30 | v0.1 | Created initial trading concepts glossary | Jesse + AI |
