CREATE ROLE admin_role;
CREATE ROLE operator_role;
CREATE ROLE guest_role;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_role;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin_role;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO operator_role;
GRANT INSERT, UPDATE ON TABLE core_contract TO operator_role;
GRANT INSERT, UPDATE ON TABLE core_payment TO operator_role;
GRANT INSERT, UPDATE ON TABLE core_materialusage TO operator_role;
GRANT INSERT, UPDATE ON TABLE core_constructionstage TO operator_role;
GRANT USAGE, SELECT ON SEQUENCE core_contract_id_seq TO operator_role;
GRANT USAGE, SELECT ON SEQUENCE core_payment_id_seq TO operator_role;
GRANT USAGE, SELECT ON SEQUENCE core_materialusage_id_seq TO operator_role;
GRANT USAGE, SELECT ON SEQUENCE core_constructionstage_id_seq TO operator_role;

GRANT SELECT ON TABLE core_constructionobject TO guest_role;
GRANT SELECT ON TABLE core_constructionstage TO guest_role;

CREATE USER pga_admin WITH PASSWORD 'admin123';
CREATE USER pga_operator WITH PASSWORD 'operator123';
CREATE USER pga_guest WITH PASSWORD 'guest123';

GRANT admin_role TO pga_admin;
GRANT operator_role TO pga_operator;
GRANT guest_role TO pga_guest;
