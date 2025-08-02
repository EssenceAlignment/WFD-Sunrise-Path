-- Table schema for cleanup metrics
CREATE TABLE IF NOT EXISTS cleanup_metrics (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMPTZ NOT NULL,
  pending_files INTEGER NOT NULL,
  problems INTEGER NOT NULL,
  runtime_s INTEGER NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Parser function (to be called by ETL)
CREATE OR REPLACE FUNCTION parse_cleanup_log(log_line TEXT)
RETURNS TABLE(timestamp TIMESTAMPTZ, pending_files INT, problems INT, runtime_s INT) AS $$
BEGIN
  -- Parse format: "2025-08-02T09:22:35Z | pending:0 | problems:0 | runtime_s:94"
  RETURN QUERY
  SELECT
    (split_part(log_line, ' | ', 1))::TIMESTAMPTZ,
    (split_part(split_part(log_line, 'pending:', 2), ' ', 1))::INT,
    (split_part(split_part(log_line, 'problems:', 2), ' ', 1))::INT,
    (split_part(split_part(log_line, 'runtime_s:', 2), ' ', 1))::INT;
END;
$$ LANGUAGE plpgsql;

-- ETL function to load new metrics from file content
CREATE OR REPLACE FUNCTION load_cleanup_metrics(file_content TEXT)
RETURNS INTEGER AS $$
DECLARE
  line TEXT;
  parsed_record RECORD;
  rows_inserted INTEGER := 0;
BEGIN
  -- Split file content by lines and process each
  FOREACH line IN ARRAY string_to_array(file_content, E'\n')
  LOOP
    -- Skip empty lines
    IF trim(line) = '' THEN
      CONTINUE;
    END IF;

    -- Parse the line
    SELECT * INTO parsed_record FROM parse_cleanup_log(line);

    -- Check if this timestamp already exists
    IF NOT EXISTS (
      SELECT 1 FROM cleanup_metrics
      WHERE timestamp = parsed_record.timestamp
    ) THEN
      -- Insert new record
      INSERT INTO cleanup_metrics (timestamp, pending_files, problems, runtime_s)
      VALUES (
        parsed_record.timestamp,
        parsed_record.pending_files,
        parsed_record.problems,
        parsed_record.runtime_s
      );
      rows_inserted := rows_inserted + 1;
    END IF;
  END LOOP;

  RETURN rows_inserted;
END;
$$ LANGUAGE plpgsql;

-- View for WFD dashboard integration
CREATE OR REPLACE VIEW engineering_hygiene_metrics AS
SELECT
  timestamp,
  pending_files,
  problems,
  runtime_s,
  CASE
    WHEN pending_files = 0 AND problems = 0 THEN 'GREEN'
    ELSE 'RED'
  END AS status,
  created_at
FROM cleanup_metrics
ORDER BY timestamp DESC;

-- Alert function for red metrics
CREATE OR REPLACE FUNCTION check_red_metrics()
RETURNS TABLE(alert_message TEXT, consecutive_days INT) AS $$
DECLARE
  consecutive_red_days INT;
BEGIN
  -- Count consecutive days with non-zero metrics
  SELECT COUNT(*)
  INTO consecutive_red_days
  FROM (
    SELECT
      timestamp::date as metric_date,
      MAX(pending_files) as max_pending,
      MAX(problems) as max_problems
    FROM cleanup_metrics
    WHERE timestamp > NOW() - INTERVAL '7 days'
    GROUP BY timestamp::date
    ORDER BY metric_date DESC
  ) daily_metrics
  WHERE max_pending > 0 OR max_problems > 0
  LIMIT 2;

  IF consecutive_red_days >= 2 THEN
    RETURN QUERY
    SELECT
      format('RED ALERT: Non-zero metrics for %s consecutive days', consecutive_red_days),
      consecutive_red_days;
  END IF;
END;
$$ LANGUAGE plpgsql;
