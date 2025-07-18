-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 18, 2025 at 06:48 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hitman_edge_test`
--

-- --------------------------------------------------------

--
-- Table structure for table `he_actionsmaster`
--

CREATE TABLE `he_actionsmaster` (
  `action_id` int(11) NOT NULL,
  `action_name` varchar(50) NOT NULL,
  `action_description` varchar(255) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_analystmaster`
--

CREATE TABLE `he_analystmaster` (
  `analyst_id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `expertise_area` varchar(255) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_company`
--

CREATE TABLE `he_company` (
  `company_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `sector` varchar(100) NOT NULL,
  `industry_id` int(11) NOT NULL,
  `country` varchar(50) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `founded_year` int(11) DEFAULT NULL,
  `market_cap` decimal(18,2) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_competitormaster`
--

CREATE TABLE `he_competitormaster` (
  `competitor_master_id` int(11) NOT NULL,
  `main_ticker_id` int(11) NOT NULL,
  `competitor_ticker_1` int(11) DEFAULT NULL,
  `competitor_ticker_2` int(11) DEFAULT NULL,
  `competitor_ticker_3` int(11) DEFAULT NULL,
  `competitor_ticker_4` int(11) DEFAULT NULL,
  `competitor_ticker_5` int(11) DEFAULT NULL,
  `competitor_ticker_6` int(11) DEFAULT NULL,
  `competitor_ticker_7` int(11) DEFAULT NULL,
  `competitor_ticker_8` int(11) DEFAULT NULL,
  `competitor_ticker_9` int(11) DEFAULT NULL,
  `competitor_ticker_10` int(11) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_currencymaster`
--

CREATE TABLE `he_currencymaster` (
  `currency_code` varchar(10) NOT NULL,
  `currency_name` varchar(50) NOT NULL,
  `symbol` varchar(10) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_error_logs`
--

CREATE TABLE `he_error_logs` (
  `id` int(11) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `error_description` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `created_by` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_index_data`
--

CREATE TABLE `he_index_data` (
  `symbol` varchar(10) NOT NULL,
  `index_name` varchar(50) DEFAULT NULL,
  `close_price` decimal(10,2) DEFAULT NULL,
  `percent_change` decimal(6,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `he_index_data`
--

INSERT INTO `he_index_data` (`symbol`, `index_name`, `close_price`, `percent_change`) VALUES
('^DJI', 'Dow Jones', 44484.42, 0.06),
('^GSPC', 'S&P 500', 6227.42, 0.54),
('^RUT', 'Russell 2000', 2226.38, 1.21),
('^VIX', 'CBOE Volatility Index', 16.64, -0.66);

-- --------------------------------------------------------

--
-- Table structure for table `he_industry`
--

CREATE TABLE `he_industry` (
  `industry_id` int(11) NOT NULL,
  `sector` varchar(100) NOT NULL,
  `industry` varchar(100) NOT NULL,
  `sub_industry` varchar(100) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_investmentlimitmaster`
--

CREATE TABLE `he_investmentlimitmaster` (
  `limit_id` int(11) NOT NULL,
  `overall_limit_per_stock` decimal(18,2) NOT NULL,
  `position_size_limit` decimal(18,2) NOT NULL,
  `per_transaction_limit` decimal(18,2) NOT NULL,
  `options_trading_limit` decimal(18,2) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_job_execution`
--

CREATE TABLE `he_job_execution` (
  `id` int(11) NOT NULL,
  `job_number` varchar(50) NOT NULL,
  `job_run_number` int(11) NOT NULL,
  `execution_status` varchar(50) DEFAULT NULL,
  `start_datetime` datetime DEFAULT NULL,
  `end_datetime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_job_logs`
--

CREATE TABLE `he_job_logs` (
  `job_log_number` int(11) NOT NULL,
  `job_number` varchar(50) NOT NULL,
  `job_run_number` int(11) NOT NULL,
  `job_log_description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_job_master`
--

CREATE TABLE `he_job_master` (
  `id` int(11) NOT NULL,
  `job_number` varchar(50) NOT NULL,
  `job_name` varchar(255) NOT NULL,
  `schedule_frequency` varchar(255) NOT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `schedule_type` varchar(50) DEFAULT NULL,
  `event_condition` text DEFAULT NULL,
  `dependent_job_number` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `he_job_master`
--

INSERT INTO `he_job_master` (`id`, `job_number`, `job_name`, `schedule_frequency`, `start_time`, `end_time`, `schedule_type`, `event_condition`, `dependent_job_number`) VALUES
(2, '2', 'msna', 'daily', '10:52:17', '10:52:22', 'Event Based', NULL, NULL),
(3, '1', 'One', 'Weekly', '11:59:13', '18:59:24', 'Event Based', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `he_jonah_compare`
--

CREATE TABLE `he_jonah_compare` (
  `id` int(11) NOT NULL,
  `jonah_ticker` varchar(20) DEFAULT NULL,
  `jonah_category` varchar(50) DEFAULT NULL,
  `jonah_position` decimal(18,4) DEFAULT NULL,
  `he_ticker` varchar(20) DEFAULT NULL,
  `he_category` varchar(50) DEFAULT NULL,
  `position_difference` decimal(18,4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_news`
--

CREATE TABLE `he_news` (
  `news_id` int(11) NOT NULL,
  `ticker_id` int(11) NOT NULL,
  `headline` varchar(500) NOT NULL,
  `summary` text DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  `published_at` datetime NOT NULL,
  `lang` varchar(10) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `sentiment_label` enum('positive','neutral','negative') DEFAULT 'neutral',
  `sentiment_score` decimal(4,3) DEFAULT NULL,
  `impact_score` decimal(5,2) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_optionscontract`
--

CREATE TABLE `he_optionscontract` (
  `option_id` int(11) NOT NULL,
  `ticker_id` int(11) NOT NULL,
  `symbol` varchar(50) NOT NULL,
  `contract_type` enum('call','put') NOT NULL,
  `expiration_date` date NOT NULL,
  `strike_price` decimal(10,2) NOT NULL,
  `last_price` decimal(10,2) DEFAULT NULL,
  `bid` decimal(10,2) DEFAULT NULL,
  `ask` decimal(10,2) DEFAULT NULL,
  `volume` int(11) DEFAULT 0,
  `open_interest` int(11) DEFAULT 0,
  `implied_volatility` decimal(6,4) DEFAULT NULL,
  `delta` decimal(6,4) DEFAULT NULL,
  `gamma` decimal(6,4) DEFAULT NULL,
  `theta` decimal(6,4) DEFAULT NULL,
  `vega` decimal(6,4) DEFAULT NULL,
  `rho` decimal(6,4) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_optionsmaster`
--

CREATE TABLE `he_optionsmaster` (
  `option_type_id` int(11) NOT NULL,
  `option_type_name` varchar(100) NOT NULL,
  `option_type_description` text DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_portfolio_master`
--

CREATE TABLE `he_portfolio_master` (
  `id` int(11) NOT NULL,
  `ticker` varchar(20) DEFAULT NULL,
  `Category` varchar(50) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `avg_cost` decimal(10,2) DEFAULT NULL,
  `position_size` decimal(10,2) DEFAULT NULL,
  `total_cost` decimal(10,2) DEFAULT NULL,
  `current_price` decimal(10,2) DEFAULT NULL,
  `unrealized_gain_loss` decimal(10,2) DEFAULT NULL,
  `relized_gain_loss` decimal(10,2) DEFAULT NULL,
  `first_buy_age` varchar(100) DEFAULT NULL,
  `avg_age_days` int(11) DEFAULT NULL,
  `platform` varchar(50) DEFAULT NULL,
  `industry_pe` decimal(10,2) DEFAULT NULL,
  `curent_pe` decimal(10,2) DEFAULT NULL,
  `price_sales_ratio` decimal(10,2) DEFAULT NULL,
  `price_book_ratio` decimal(10,2) DEFAULT NULL,
  `50_day_ema` decimal(10,2) DEFAULT NULL,
  `100_day_ema` decimal(10,2) DEFAULT NULL,
  `200_day_ema` decimal(10,2) DEFAULT NULL,
  `sp_500_ya` decimal(10,2) DEFAULT NULL,
  `nashdaq_ya` decimal(10,2) DEFAULT NULL,
  `russel_1000_ya` decimal(10,2) DEFAULT NULL,
  `pe_ratio` decimal(10,2) DEFAULT NULL,
  `peg_ratio` decimal(10,2) DEFAULT NULL,
  `roe` decimal(10,2) DEFAULT NULL,
  `net_profit_margin` decimal(10,2) DEFAULT NULL,
  `current_ratio` decimal(10,2) DEFAULT NULL,
  `debt_equity` decimal(10,2) DEFAULT NULL,
  `fcf_yield` decimal(10,2) DEFAULT NULL,
  `revenue_growth` decimal(10,2) DEFAULT NULL,
  `earnings_accuracy` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_research`
--

CREATE TABLE `he_research` (
  `research_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `report_date` date NOT NULL,
  `fiscal_year` int(11) NOT NULL,
  `fiscal_quarter` enum('Q1','Q2','Q3','Q4') NOT NULL,
  `data_source` varchar(100) DEFAULT NULL,
  `provider_report_id` varchar(100) DEFAULT NULL,
  `pe_ratio` decimal(8,2) DEFAULT NULL,
  `peg_ratio` decimal(8,2) DEFAULT NULL,
  `price_to_book` decimal(8,2) DEFAULT NULL,
  `price_to_sales` decimal(8,2) DEFAULT NULL,
  `enterprise_value` decimal(18,2) DEFAULT NULL,
  `ev_to_ebitda` decimal(8,2) DEFAULT NULL,
  `net_margin` decimal(6,2) DEFAULT NULL,
  `gross_margin` decimal(6,2) DEFAULT NULL,
  `return_on_equity` decimal(6,2) DEFAULT NULL,
  `return_on_assets` decimal(6,2) DEFAULT NULL,
  `debt_to_equity` decimal(6,2) DEFAULT NULL,
  `current_ratio` decimal(6,2) DEFAULT NULL,
  `quick_ratio` decimal(6,2) DEFAULT NULL,
  `interest_coverage` decimal(6,2) DEFAULT NULL,
  `revenue_growth_yoy` decimal(6,2) DEFAULT NULL,
  `earnings_growth_yoy` decimal(6,2) DEFAULT NULL,
  `free_cash_flow` decimal(18,2) DEFAULT NULL,
  `dividend_yield` decimal(6,2) DEFAULT NULL,
  `market_cap` decimal(18,2) DEFAULT NULL,
  `shares_outstanding` bigint(20) DEFAULT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_stockmaster`
--

CREATE TABLE `he_stockmaster` (
  `stock_id` int(11) NOT NULL,
  `ticker` varchar(20) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `industry` varchar(100) DEFAULT NULL,
  `sub_industry` varchar(100) DEFAULT NULL,
  `size` enum('Small Cap','Mid Cap','Large Cap','Very Large Cap') DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_stock_transaction`
--

CREATE TABLE `he_stock_transaction` (
  `id` int(11) NOT NULL,
  `ticker` varchar(20) NOT NULL,
  `date` date NOT NULL,
  `trade_type` enum('BUY','SELL') NOT NULL,
  `quantity` int(11) NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `platform` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_technicalindicators`
--

CREATE TABLE `he_technicalindicators` (
  `indicator_id` int(11) NOT NULL,
  `ticker_id` int(11) NOT NULL,
  `option_id` int(11) DEFAULT NULL,
  `timeframe` varchar(10) NOT NULL,
  `timestamp` datetime NOT NULL,
  `macd` decimal(10,5) DEFAULT NULL,
  `macd_signal` decimal(10,5) DEFAULT NULL,
  `macd_hist` decimal(10,5) DEFAULT NULL,
  `rsi` decimal(5,2) DEFAULT NULL,
  `bollinger_upper` decimal(10,2) DEFAULT NULL,
  `bollinger_lower` decimal(10,2) DEFAULT NULL,
  `bollinger_mid` decimal(10,2) DEFAULT NULL,
  `ichimoku_tenkan_sen` decimal(10,2) DEFAULT NULL,
  `ichimoku_kijun_sen` decimal(10,2) DEFAULT NULL,
  `ichimoku_senkou_span_a` decimal(10,2) DEFAULT NULL,
  `ichimoku_senkou_span_b` decimal(10,2) DEFAULT NULL,
  `ichimoku_chikou_span` decimal(10,2) DEFAULT NULL,
  `sma_20` decimal(10,2) DEFAULT NULL,
  `ema_50` decimal(10,2) DEFAULT NULL,
  `data_source` varchar(100) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_ticker`
--

CREATE TABLE `he_ticker` (
  `ticker_id` int(11) NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `company_id` int(11) NOT NULL,
  `exchange` varchar(50) NOT NULL,
  `instrument_type` varchar(20) NOT NULL,
  `currency` varchar(10) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `listed_at` date NOT NULL,
  `delisted_at` date DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_usermaster`
--

CREATE TABLE `he_usermaster` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `user_login_id` varchar(100) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `date_created` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pbcatcol`
--

CREATE TABLE `pbcatcol` (
  `pbc_tnam` char(193) NOT NULL,
  `pbc_tid` int(11) DEFAULT NULL,
  `pbc_ownr` char(193) NOT NULL,
  `pbc_cnam` char(193) NOT NULL,
  `pbc_cid` smallint(6) DEFAULT NULL,
  `pbc_labl` varchar(254) DEFAULT NULL,
  `pbc_lpos` smallint(6) DEFAULT NULL,
  `pbc_hdr` varchar(254) DEFAULT NULL,
  `pbc_hpos` smallint(6) DEFAULT NULL,
  `pbc_jtfy` smallint(6) DEFAULT NULL,
  `pbc_mask` varchar(31) DEFAULT NULL,
  `pbc_case` smallint(6) DEFAULT NULL,
  `pbc_hght` smallint(6) DEFAULT NULL,
  `pbc_wdth` smallint(6) DEFAULT NULL,
  `pbc_ptrn` varchar(31) DEFAULT NULL,
  `pbc_bmap` char(1) DEFAULT NULL,
  `pbc_init` varchar(254) DEFAULT NULL,
  `pbc_cmnt` varchar(254) DEFAULT NULL,
  `pbc_edit` varchar(31) DEFAULT NULL,
  `pbc_tag` varchar(254) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pbcatcol`
--

INSERT INTO `pbcatcol` (`pbc_tnam`, `pbc_tid`, `pbc_ownr`, `pbc_cnam`, `pbc_cid`, `pbc_labl`, `pbc_lpos`, `pbc_hdr`, `pbc_hpos`, `pbc_jtfy`, `pbc_mask`, `pbc_case`, `pbc_hght`, `pbc_wdth`, `pbc_ptrn`, `pbc_bmap`, `pbc_init`, `pbc_cmnt`, `pbc_edit`, `pbc_tag`) VALUES
('he_usermaster', NULL, 'root', 'date_created', NULL, NULL, 0, NULL, 0, 0, NULL, 0, 0, 0, NULL, 'N', NULL, NULL, NULL, NULL),
('he_usermaster', NULL, 'root', 'first_name', NULL, NULL, 0, NULL, 0, 0, NULL, 0, 0, 0, NULL, 'N', NULL, NULL, NULL, NULL),
('he_usermaster', NULL, 'root', 'last_name', NULL, NULL, 0, NULL, 0, 0, NULL, 0, 0, 0, NULL, 'N', NULL, NULL, NULL, NULL),
('he_usermaster', NULL, 'root', 'user_id', NULL, NULL, 0, NULL, 0, 0, NULL, 0, 0, 0, NULL, 'N', NULL, NULL, NULL, NULL),
('he_usermaster', NULL, 'root', 'user_login_id', NULL, NULL, 0, NULL, 0, 0, NULL, 0, 0, 0, NULL, 'N', NULL, NULL, NULL, NULL),
('he_usermaster', NULL, 'root', 'user_password', NULL, NULL, 0, NULL, 0, 0, NULL, 0, 0, 0, NULL, 'N', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `pbcatedt`
--

CREATE TABLE `pbcatedt` (
  `pbe_name` varchar(30) NOT NULL,
  `pbe_edit` varchar(254) DEFAULT NULL,
  `pbe_type` smallint(6) DEFAULT NULL,
  `pbe_cntr` int(11) DEFAULT NULL,
  `pbe_seqn` smallint(6) NOT NULL,
  `pbe_flag` int(11) DEFAULT NULL,
  `pbe_work` char(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pbcatedt`
--

INSERT INTO `pbcatedt` (`pbe_name`, `pbe_edit`, `pbe_type`, `pbe_cntr`, `pbe_seqn`, `pbe_flag`, `pbe_work`) VALUES
('#####', '#####', 90, 1, 1, 32, '10'),
('###,###.00', '###,###.00', 90, 1, 1, 32, '10'),
('###-##-####', '###-##-####', 90, 1, 1, 32, '00'),
('DD/MM/YY', 'DD/MM/YY', 90, 1, 1, 32, '20'),
('DD/MM/YY HH:MM:SS', 'DD/MM/YY HH:MM:SS', 90, 1, 1, 32, '40'),
('DD/MM/YY HH:MM:SS:FFFFFF', 'DD/MM/YY HH:MM:SS:FFFFFF', 90, 1, 1, 32, '40'),
('DD/MM/YYYY', 'DD/MM/YYYY', 90, 1, 1, 32, '20'),
('DD/MM/YYYY HH:MM:SS', 'DD/MM/YYYY HH:MM:SS', 90, 1, 1, 32, '40'),
('DD/MMM/YY', 'DD/MMM/YY', 90, 1, 1, 32, '20'),
('DD/MMM/YY HH:MM:SS', 'DD/MMM/YY HH:MM:SS', 90, 1, 1, 32, '40'),
('HH:MM:SS', 'HH:MM:SS', 90, 1, 1, 32, '30'),
('HH:MM:SS:FFF', 'HH:MM:SS:FFF', 90, 1, 1, 32, '30'),
('HH:MM:SS:FFFFFF', 'HH:MM:SS:FFFFFF', 90, 1, 1, 32, '30'),
('JJJ/YY', 'JJJ/YY', 90, 1, 1, 32, '20'),
('JJJ/YY HH:MM:SS', 'JJJ/YY HH:MM:SS', 90, 1, 1, 32, '40'),
('JJJ/YYYY', 'JJJ/YYYY', 90, 1, 1, 32, '20'),
('JJJ/YYYY HH:MM:SS', 'JJJ/YYYY HH:MM:SS', 90, 1, 1, 32, '40'),
('MM/DD/YY', 'MM/DD/YY', 90, 1, 1, 32, '20'),
('MM/DD/YY HH:MM:SS', 'MM/DD/YY HH:MM:SS', 90, 1, 1, 32, '40'),
('MM/DD/YYYY', 'MM/DD/YYYY', 90, 1, 1, 32, '20'),
('MM/DD/YYYY HH:MM:SS', 'MM/DD/YYYY HH:MM:SS', 90, 1, 1, 32, '40');

-- --------------------------------------------------------

--
-- Table structure for table `pbcatfmt`
--

CREATE TABLE `pbcatfmt` (
  `pbf_name` varchar(30) NOT NULL,
  `pbf_frmt` varchar(254) DEFAULT NULL,
  `pbf_type` smallint(6) DEFAULT NULL,
  `pbf_cntr` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pbcatfmt`
--

INSERT INTO `pbcatfmt` (`pbf_name`, `pbf_frmt`, `pbf_type`, `pbf_cntr`) VALUES
('#,##0', '#,##0', 81, 0),
('#,##0.00', '#,##0.00', 81, 0),
('$#,##0.00;($#,##0.00)', '$#,##0.00;($#,##0.00)', 81, 0),
('$#,##0.00;[RED]($#,##0.00)', '$#,##0.00;[RED]($#,##0.00)', 81, 0),
('$#,##0;($#,##0)', '$#,##0;($#,##0)', 81, 0),
('$#,##0;[RED]($#,##0)', '$#,##0;[RED]($#,##0)', 81, 0),
('0', '0', 81, 0),
('0%', '0%', 81, 0),
('0.00', '0.00', 81, 0),
('0.00%', '0.00%', 81, 0),
('0.00E+00', '0.00E+00', 81, 0),
('d-mmm', 'd-mmm', 84, 0),
('d-mmm-yy', 'd-mmm-yy', 84, 0),
('h:mm AM/PM', 'h:mm AM/PM', 84, 0),
('h:mm:ss', 'h:mm:ss', 84, 0),
('h:mm:ss AM/PM', 'h:mm:ss AM/PM', 84, 0),
('m/d/yy', 'm/d/yy', 84, 0),
('m/d/yy h:mm', 'm/d/yy h:mm', 84, 0),
('mmm-yy', 'mmm-yy', 84, 0),
('[General]', '[General]', 81, 0);

-- --------------------------------------------------------

--
-- Table structure for table `pbcattbl`
--

CREATE TABLE `pbcattbl` (
  `pbt_tnam` char(193) NOT NULL,
  `pbt_tid` int(11) DEFAULT NULL,
  `pbt_ownr` char(193) NOT NULL,
  `pbd_fhgt` smallint(6) DEFAULT NULL,
  `pbd_fwgt` smallint(6) DEFAULT NULL,
  `pbd_fitl` char(1) DEFAULT NULL,
  `pbd_funl` char(1) DEFAULT NULL,
  `pbd_fchr` smallint(6) DEFAULT NULL,
  `pbd_fptc` smallint(6) DEFAULT NULL,
  `pbd_ffce` char(18) DEFAULT NULL,
  `pbh_fhgt` smallint(6) DEFAULT NULL,
  `pbh_fwgt` smallint(6) DEFAULT NULL,
  `pbh_fitl` char(1) DEFAULT NULL,
  `pbh_funl` char(1) DEFAULT NULL,
  `pbh_fchr` smallint(6) DEFAULT NULL,
  `pbh_fptc` smallint(6) DEFAULT NULL,
  `pbh_ffce` char(18) DEFAULT NULL,
  `pbl_fhgt` smallint(6) DEFAULT NULL,
  `pbl_fwgt` smallint(6) DEFAULT NULL,
  `pbl_fitl` char(1) DEFAULT NULL,
  `pbl_funl` char(1) DEFAULT NULL,
  `pbl_fchr` smallint(6) DEFAULT NULL,
  `pbl_fptc` smallint(6) DEFAULT NULL,
  `pbl_ffce` char(18) DEFAULT NULL,
  `pbt_cmnt` varchar(254) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pbcattbl`
--

INSERT INTO `pbcattbl` (`pbt_tnam`, `pbt_tid`, `pbt_ownr`, `pbd_fhgt`, `pbd_fwgt`, `pbd_fitl`, `pbd_funl`, `pbd_fchr`, `pbd_fptc`, `pbd_ffce`, `pbh_fhgt`, `pbh_fwgt`, `pbh_fitl`, `pbh_funl`, `pbh_fchr`, `pbh_fptc`, `pbh_ffce`, `pbl_fhgt`, `pbl_fwgt`, `pbl_fitl`, `pbl_funl`, `pbl_fchr`, `pbl_fptc`, `pbl_ffce`, `pbt_cmnt`) VALUES
('he_usermaster', NULL, 'root', -10, 400, 'N', 'N', 0, 34, 'Tahoma', -11, 700, 'Y', 'N', 0, 34, 'Tahoma', -10, 400, 'N', 'N', 0, 34, 'Tahoma', '');

-- --------------------------------------------------------

--
-- Table structure for table `pbcatvld`
--

CREATE TABLE `pbcatvld` (
  `pbv_name` varchar(30) NOT NULL,
  `pbv_vald` varchar(254) DEFAULT NULL,
  `pbv_type` smallint(6) DEFAULT NULL,
  `pbv_cntr` int(11) DEFAULT NULL,
  `pbv_msg` varchar(254) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `he_actionsmaster`
--
ALTER TABLE `he_actionsmaster`
  ADD PRIMARY KEY (`action_id`),
  ADD UNIQUE KEY `action_name` (`action_name`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_analystmaster`
--
ALTER TABLE `he_analystmaster`
  ADD PRIMARY KEY (`analyst_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_company`
--
ALTER TABLE `he_company`
  ADD PRIMARY KEY (`company_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_industry_id` (`industry_id`),
  ADD KEY `idx_sector` (`sector`);

--
-- Indexes for table `he_competitormaster`
--
ALTER TABLE `he_competitormaster`
  ADD PRIMARY KEY (`competitor_master_id`),
  ADD KEY `main_ticker_id` (`main_ticker_id`),
  ADD KEY `competitor_ticker_1` (`competitor_ticker_1`),
  ADD KEY `competitor_ticker_2` (`competitor_ticker_2`),
  ADD KEY `competitor_ticker_3` (`competitor_ticker_3`),
  ADD KEY `competitor_ticker_4` (`competitor_ticker_4`),
  ADD KEY `competitor_ticker_5` (`competitor_ticker_5`),
  ADD KEY `competitor_ticker_6` (`competitor_ticker_6`),
  ADD KEY `competitor_ticker_7` (`competitor_ticker_7`),
  ADD KEY `competitor_ticker_8` (`competitor_ticker_8`),
  ADD KEY `competitor_ticker_9` (`competitor_ticker_9`),
  ADD KEY `competitor_ticker_10` (`competitor_ticker_10`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_currencymaster`
--
ALTER TABLE `he_currencymaster`
  ADD PRIMARY KEY (`currency_code`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_error_logs`
--
ALTER TABLE `he_error_logs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `he_index_data`
--
ALTER TABLE `he_index_data`
  ADD PRIMARY KEY (`symbol`);

--
-- Indexes for table `he_industry`
--
ALTER TABLE `he_industry`
  ADD PRIMARY KEY (`industry_id`),
  ADD UNIQUE KEY `uniq_sector_industry_subindustry` (`sector`,`industry`,`sub_industry`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_investmentlimitmaster`
--
ALTER TABLE `he_investmentlimitmaster`
  ADD PRIMARY KEY (`limit_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_job_execution`
--
ALTER TABLE `he_job_execution`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `job_number` (`job_number`,`job_run_number`);

--
-- Indexes for table `he_job_logs`
--
ALTER TABLE `he_job_logs`
  ADD PRIMARY KEY (`job_log_number`),
  ADD KEY `job_number` (`job_number`,`job_run_number`);

--
-- Indexes for table `he_job_master`
--
ALTER TABLE `he_job_master`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `job_number` (`job_number`),
  ADD KEY `dependent_job_number` (`dependent_job_number`);

--
-- Indexes for table `he_jonah_compare`
--
ALTER TABLE `he_jonah_compare`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `he_news`
--
ALTER TABLE `he_news`
  ADD PRIMARY KEY (`news_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_ticker_id` (`ticker_id`),
  ADD KEY `idx_published_at` (`published_at`);

--
-- Indexes for table `he_optionscontract`
--
ALTER TABLE `he_optionscontract`
  ADD PRIMARY KEY (`option_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_ticker_id` (`ticker_id`),
  ADD KEY `idx_expiration_date` (`expiration_date`);

--
-- Indexes for table `he_optionsmaster`
--
ALTER TABLE `he_optionsmaster`
  ADD PRIMARY KEY (`option_type_id`),
  ADD UNIQUE KEY `option_type_name` (`option_type_name`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_portfolio_master`
--
ALTER TABLE `he_portfolio_master`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ticker` (`ticker`);

--
-- Indexes for table `he_research`
--
ALTER TABLE `he_research`
  ADD PRIMARY KEY (`research_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_company_id` (`company_id`),
  ADD KEY `idx_report_date` (`report_date`);

--
-- Indexes for table `he_stockmaster`
--
ALTER TABLE `he_stockmaster`
  ADD PRIMARY KEY (`stock_id`),
  ADD UNIQUE KEY `uniq_ticker` (`ticker`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_stock_transaction`
--
ALTER TABLE `he_stock_transaction`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `he_technicalindicators`
--
ALTER TABLE `he_technicalindicators`
  ADD PRIMARY KEY (`indicator_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_ticker_id` (`ticker_id`),
  ADD KEY `idx_option_id` (`option_id`),
  ADD KEY `idx_timestamp` (`timestamp`);

--
-- Indexes for table `he_ticker`
--
ALTER TABLE `he_ticker`
  ADD PRIMARY KEY (`ticker_id`),
  ADD UNIQUE KEY `uniq_symbol_exchange` (`symbol`,`exchange`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_company_id` (`company_id`);

--
-- Indexes for table `he_usermaster`
--
ALTER TABLE `he_usermaster`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_login_id` (`user_login_id`);

--
-- Indexes for table `pbcatcol`
--
ALTER TABLE `pbcatcol`
  ADD UNIQUE KEY `pbcatc_x` (`pbc_tnam`,`pbc_ownr`,`pbc_cnam`);

--
-- Indexes for table `pbcatedt`
--
ALTER TABLE `pbcatedt`
  ADD UNIQUE KEY `pbcate_x` (`pbe_name`,`pbe_seqn`);

--
-- Indexes for table `pbcatfmt`
--
ALTER TABLE `pbcatfmt`
  ADD UNIQUE KEY `pbcatf_x` (`pbf_name`);

--
-- Indexes for table `pbcattbl`
--
ALTER TABLE `pbcattbl`
  ADD UNIQUE KEY `pbcatt_x` (`pbt_tnam`,`pbt_ownr`);

--
-- Indexes for table `pbcatvld`
--
ALTER TABLE `pbcatvld`
  ADD UNIQUE KEY `pbcatv_x` (`pbv_name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `he_actionsmaster`
--
ALTER TABLE `he_actionsmaster`
  MODIFY `action_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `he_analystmaster`
--
ALTER TABLE `he_analystmaster`
  MODIFY `analyst_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_company`
--
ALTER TABLE `he_company`
  MODIFY `company_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_competitormaster`
--
ALTER TABLE `he_competitormaster`
  MODIFY `competitor_master_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_error_logs`
--
ALTER TABLE `he_error_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_industry`
--
ALTER TABLE `he_industry`
  MODIFY `industry_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_investmentlimitmaster`
--
ALTER TABLE `he_investmentlimitmaster`
  MODIFY `limit_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_job_execution`
--
ALTER TABLE `he_job_execution`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_job_master`
--
ALTER TABLE `he_job_master`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `he_jonah_compare`
--
ALTER TABLE `he_jonah_compare`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_news`
--
ALTER TABLE `he_news`
  MODIFY `news_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_optionscontract`
--
ALTER TABLE `he_optionscontract`
  MODIFY `option_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_optionsmaster`
--
ALTER TABLE `he_optionsmaster`
  MODIFY `option_type_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_portfolio_master`
--
ALTER TABLE `he_portfolio_master`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_research`
--
ALTER TABLE `he_research`
  MODIFY `research_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_stockmaster`
--
ALTER TABLE `he_stockmaster`
  MODIFY `stock_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `he_stock_transaction`
--
ALTER TABLE `he_stock_transaction`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_technicalindicators`
--
ALTER TABLE `he_technicalindicators`
  MODIFY `indicator_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_ticker`
--
ALTER TABLE `he_ticker`
  MODIFY `ticker_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_usermaster`
--
ALTER TABLE `he_usermaster`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `he_actionsmaster`
--
ALTER TABLE `he_actionsmaster`
  ADD CONSTRAINT `he_actionsmaster_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_actionsmaster_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_analystmaster`
--
ALTER TABLE `he_analystmaster`
  ADD CONSTRAINT `he_analystmaster_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_analystmaster_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_company`
--
ALTER TABLE `he_company`
  ADD CONSTRAINT `he_company_ibfk_1` FOREIGN KEY (`industry_id`) REFERENCES `he_industry` (`industry_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_company_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_company_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_competitormaster`
--
ALTER TABLE `he_competitormaster`
  ADD CONSTRAINT `he_competitormaster_ibfk_1` FOREIGN KEY (`main_ticker_id`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_10` FOREIGN KEY (`competitor_ticker_9`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_11` FOREIGN KEY (`competitor_ticker_10`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_12` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_13` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_2` FOREIGN KEY (`competitor_ticker_1`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_3` FOREIGN KEY (`competitor_ticker_2`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_4` FOREIGN KEY (`competitor_ticker_3`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_5` FOREIGN KEY (`competitor_ticker_4`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_6` FOREIGN KEY (`competitor_ticker_5`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_7` FOREIGN KEY (`competitor_ticker_6`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_8` FOREIGN KEY (`competitor_ticker_7`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `he_competitormaster_ibfk_9` FOREIGN KEY (`competitor_ticker_8`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_currencymaster`
--
ALTER TABLE `he_currencymaster`
  ADD CONSTRAINT `he_currencymaster_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_currencymaster_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_industry`
--
ALTER TABLE `he_industry`
  ADD CONSTRAINT `he_industry_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_industry_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_investmentlimitmaster`
--
ALTER TABLE `he_investmentlimitmaster`
  ADD CONSTRAINT `he_investmentlimitmaster_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_investmentlimitmaster_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_job_execution`
--
ALTER TABLE `he_job_execution`
  ADD CONSTRAINT `he_job_execution_ibfk_1` FOREIGN KEY (`job_number`) REFERENCES `he_job_master` (`job_number`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `he_job_logs`
--
ALTER TABLE `he_job_logs`
  ADD CONSTRAINT `he_job_logs_ibfk_1` FOREIGN KEY (`job_number`,`job_run_number`) REFERENCES `he_job_execution` (`job_number`, `job_run_number`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `he_job_master`
--
ALTER TABLE `he_job_master`
  ADD CONSTRAINT `he_job_master_ibfk_1` FOREIGN KEY (`dependent_job_number`) REFERENCES `he_job_master` (`job_number`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_news`
--
ALTER TABLE `he_news`
  ADD CONSTRAINT `he_news_ibfk_1` FOREIGN KEY (`ticker_id`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `he_news_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_news_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_optionscontract`
--
ALTER TABLE `he_optionscontract`
  ADD CONSTRAINT `he_optionscontract_ibfk_1` FOREIGN KEY (`ticker_id`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `he_optionscontract_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `he_usermaster` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `he_optionscontract_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_optionscontract_ibfk_4` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_optionsmaster`
--
ALTER TABLE `he_optionsmaster`
  ADD CONSTRAINT `he_optionsmaster_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `he_usermaster` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `he_optionsmaster_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_optionsmaster_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_research`
--
ALTER TABLE `he_research`
  ADD CONSTRAINT `he_research_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `he_company` (`company_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `he_research_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_research_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_stockmaster`
--
ALTER TABLE `he_stockmaster`
  ADD CONSTRAINT `he_stockmaster_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_stockmaster_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_technicalindicators`
--
ALTER TABLE `he_technicalindicators`
  ADD CONSTRAINT `he_technicalindicators_ibfk_1` FOREIGN KEY (`ticker_id`) REFERENCES `he_ticker` (`ticker_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `he_technicalindicators_ibfk_2` FOREIGN KEY (`option_id`) REFERENCES `he_optionscontract` (`option_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `he_technicalindicators_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_technicalindicators_ibfk_4` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_ticker`
--
ALTER TABLE `he_ticker`
  ADD CONSTRAINT `he_ticker_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `he_company` (`company_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `he_ticker_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_ticker_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
