CREATE TABLE IF NOT EXISTS db_audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    action_type VARCHAR(10) NOT NULL, 
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    db_user VARCHAR(50) DEFAULT current_user,
    old_data JSONB,
    new_data JSONB
);

CREATE OR REPLACE FUNCTION log_audit_action()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO db_audit_log (table_name, action_type, old_data)
        VALUES (TG_TABLE_NAME, 'DELETE', row_to_json(OLD));
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO db_audit_log (table_name, action_type, old_data, new_data)
        VALUES (TG_TABLE_NAME, 'UPDATE', row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO db_audit_log (table_name, action_type, new_data)
        VALUES (TG_TABLE_NAME, 'INSERT', row_to_json(NEW));
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_core_contract_audit ON core_contract;
CREATE TRIGGER trigger_core_contract_audit
AFTER INSERT OR UPDATE OR DELETE ON core_contract
FOR EACH ROW EXECUTE FUNCTION log_audit_action();

DROP TRIGGER IF EXISTS trigger_core_payment_audit ON core_payment;
CREATE TRIGGER trigger_core_payment_audit
AFTER INSERT OR UPDATE OR DELETE ON core_payment
FOR EACH ROW EXECUTE FUNCTION log_audit_action();

CREATE OR REPLACE FUNCTION check_unauthorized_access()
RETURNS TABLE(audit_id INT, tbl VARCHAR, acc_type VARCHAR, usr VARCHAR, ts TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT id, table_name, action_type, db_user, action_time
    FROM db_audit_log
    WHERE table_name = 'core_payment' 
      AND db_user NOT IN ('pga_admin', 'postgres')
      AND (EXTRACT(HOUR FROM action_time) < 8 OR EXTRACT(HOUR FROM action_time) > 18);
END;
$$ LANGUAGE plpgsql;
