CREATE OR REPLACE VIEW v_contract_summary AS
SELECT 
    c.id AS contract_id,
    c.contract_number,
    cl.name AS client_name,
    c.total_amount,
    COALESCE(SUM(p.amount), 0) AS total_paid,
    (c.total_amount - COALESCE(SUM(p.amount), 0)) AS remaining_balance,
    c.status
FROM core_contract c
LEFT JOIN core_client cl ON c.client_id = cl.id
LEFT JOIN core_payment p ON c.id = p.contract_id AND p.payment_type = 'IN'
GROUP BY c.id, cl.name;

CREATE OR REPLACE VIEW v_material_inventory AS
SELECT 
    m.id AS material_id,
    m.name AS material_name,
    m.unit,
    m.price_per_unit,
    m.stock_quantity AS current_stock,
    COALESCE(SUM(mu.quantity), 0) AS total_used,
    (m.stock_quantity * m.price_per_unit) AS total_value_in_stock
FROM core_material m
LEFT JOIN core_materialusage mu ON m.id = mu.material_id
GROUP BY m.id;

CREATE OR REPLACE VIEW v_brigade_salary_fund AS
SELECT 
    b.id AS brigade_id,
    b.name AS brigade_name,
    COUNT(e.id) AS workers_count,
    COALESCE(SUM(e.salary), 0) AS monthly_salary_fund,
    ROUND(AVG(e.salary), 2) AS average_salary
FROM core_brigade b
LEFT JOIN core_employee e ON b.id = e.brigade_id
GROUP BY b.id;
