-- SupplyGuard SQL Layer
-- 02_import_notes.sql
-- Import process documentation.

USE supplyguard;

-- The cleaned CSV files from data/processed/ were imported into MySQL using:
-- scripts/load_processed_to_mysql.py
--
-- The import script loads the processed CSV files into the pre-created MySQL tables
-- defined in 01_create_tables.sql.
--
-- This keeps the SQL database aligned with the cleaned processed layer used in Python.

-- Final imported row counts:
-- category_translation: 71
-- customers: 99,441
-- geolocation_clean: 738,332
-- geolocation_zip_prefix: 19,015
-- order_items: 112,650
-- order_payments: 103,886
-- order_reviews: 99,224
-- orders: 99,441
-- products: 32,951
-- sellers: 3,095
