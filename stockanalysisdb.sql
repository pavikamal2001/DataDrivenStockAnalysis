CREATE DATABASE stock_analysis;

DROP TABLE IF EXISTS top10_volatile_stocks;
CREATE TABLE top10_volatile_stocks (
    Ticker VARCHAR(50),
    Volatility NUMERIC
);

DROP TABLE IF EXISTS top5_cumulative_return;
CREATE TABLE top5_cumulative_return (
    Ticker VARCHAR(50),
    Cumulative_Return NUMERIC
);

DROP TABLE IF EXISTS sector_performance;

CREATE TABLE sector_performance (
    sector VARCHAR(100),
    average_yearly_return NUMERIC
);


DROP TABLE IF EXISTS stock_correlation_matrix;

DROP TABLE IF EXISTS stock_correlation_matrix;
CREATE TABLE stock_correlation_matrix (
    Stock1 VARCHAR(50),
    Stock2 VARCHAR(50),
    Correlation NUMERIC
);



DROP TABLE IF EXISTS top5_gainers_losers_allmonths;

DROP TABLE IF EXISTS top5_gainers_losers_allmonths;
CREATE TABLE top5_gainers_losers_allmonths (
    Ticker VARCHAR(50),
    Return NUMERIC,
    Type VARCHAR(50),
    month VARCHAR(20)

);

COPY top10_volatile_stocks
FROM 'C:\Users\Admin\OneDrive\Desktop\Project_2\top10_volatile_stocks.csv'
DELIMITER ','
CSV HEADER;

COPY top5_cumulative_return
FROM 'C:\Users\Admin\OneDrive\Desktop\Project_2\top5_cumulative_return.csv'
DELIMITER ','
CSV HEADER;

COPY sector_performance (ticker, sector)
FROM 'C:\Users\Admin\OneDrive\Desktop\Project_2\sector_performance.csv'
DELIMITER ','
CSV HEADER;


COPY stock_correlation_matrix
FROM 'C:\Users\Admin\OneDrive\Desktop\Project_2\stock_correlation_matrix.csv'
DELIMITER ','
CSV HEADER;



COPY top5_gainers_losers_allmonths(Ticker, Return, Type, month)
FROM 'C:\Users\Admin\OneDrive\Desktop\Project_2\top5_gainers_losers_allMonths.csv'
DELIMITER ','
CSV HEADER;


SELECT * FROM top10_volatile_stocks LIMIT 10;
SELECT * FROM top5_cumulative_return LIMIT 5;
SELECT * FROM sector_performance LIMIT 20;
SELECT * FROM stock_correlation_matrix LIMIT 60;
SELECT * FROM top5_gainers_losers_allmonths LIMIT 140;



DROP TABLE IF EXISTS top10_green_stocks;

CREATE TABLE top10_green_stocks (
    Ticker VARCHAR(50),
    yearly_return NUMERIC
);

DROP TABLE IF EXISTS top10_loss_stocks;

CREATE TABLE top10_loss_stocks (
    Ticker VARCHAR(50),
    yearly_return NUMERIC
);

DROP TABLE IF EXISTS market_summary;

CREATE TABLE market_summary (
    metric VARCHAR(100),
    value NUMERIC
);




-- 3A. Top 10 Green Stocks CSV
COPY top10_green_stocks 
FROM 'C:\Users\Admin\OneDrive\Desktop\Project_2\top10_green_stocks.csv'
DELIMITER ','
CSV HEADER;

-- 3B. Top 10 Loss Stocks CSV
COPY top10_loss_stocks 
FROM 'C:\Users\Admin\OneDrive\Desktop\Project_2\top10_loss_stocks.csv'
DELIMITER ','
CSV HEADER;

-- 3C. Market Summary CSV
COPY market_summary ( metric, value)
FROM 'C:\Users\Admin\OneDrive\Desktop\Project_2\market_summary.csv'
DELIMITER ','
CSV HEADER;

---------------------------------------------------------
-- 4. TEST SELECTS
---------------------------------------------------------

-- Show all green stocks
SELECT * FROM top10_green_stocks
LIMIT 10;

-- Show all loss stocks
SELECT * FROM top10_loss_stocks
LIMIT 10;

-- Show market summary
SELECT * FROM market_summary
LIMIT 20;







