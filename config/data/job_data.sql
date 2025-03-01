INSERT INTO jobs_job (job_title, description, status, start_date, end_date, cost_estimate, actual_cost, created_at, updated_at, customer_id)
VALUES 
('Plumbing Repair', 'Fixing leak in the kitchen sink.', 'Completed', DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*730) DAY), NULL, ROUND(RAND()*500 + 50, 2), ROUND(RAND()*500 + 50, 2), NOW(), NOW(), FLOOR(RAND()*19) + 1),
('HVAC Installation', 'Installing a new air conditioning system.', 'In Progress', DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*730) DAY), NULL, ROUND(RAND()*2000 + 500, 2), NULL, NOW(), NOW(), FLOOR(RAND()*19) + 1),
('Roof Inspection', 'Checking for roof damage and leaks.', 'Pending', DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*730) DAY), NULL, ROUND(RAND()*300 + 100, 2), NULL, NOW(), NOW(), FLOOR(RAND()*19) + 1),
('Electrical Wiring', 'Rewiring the electrical system of a house.', 'Completed', DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*730) DAY), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*90) DAY), ROUND(RAND()*1500 + 300, 2), ROUND(RAND()*1500 + 300, 2), NOW(), NOW(), FLOOR(RAND()*19) + 1),
('Flooring Replacement', 'Replacing carpet with hardwood flooring.', 'Cancelled', DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*730) DAY), NULL, ROUND(RAND()*3000 + 500, 2), NULL, NOW(), NOW(), FLOOR(RAND()*19) + 1),
('Painting Exterior', 'Painting the house exterior.', 'Completed', DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*730) DAY), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*60) DAY), ROUND(RAND()*1500 + 500, 2), ROUND(RAND()*1500 + 500, 2), NOW(), NOW(), FLOOR(RAND()*19) + 1),
('Landscaping', 'Designing and installing a new backyard garden.', 'In Progress', DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*730) DAY), NULL, ROUND(RAND()*2500 + 700, 2), NULL, NOW(), NOW(), FLOOR(RAND()*19) + 1),
('Window Replacement', 'Replacing all windows with double-glazed ones.', 'Pending', DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*730) DAY), NULL, ROUND(RAND()*5000 + 1000, 2), NULL, NOW(), NOW(), FLOOR(RAND()*19) + 1),
('Carpentry Work', 'Custom wooden cabinets for the kitchen.', 'Completed', DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*730) DAY), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*90) DAY), ROUND(RAND()*2500 + 800, 2), ROUND(RAND()*2500 + 800, 2), NOW(), NOW(), FLOOR(RAND()*19) + 1),
('Solar Panel Installation', 'Installing solar panels on the roof.', 'Completed', DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*730) DAY), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*60) DAY), ROUND(RAND()*7000 + 3000, 2), ROUND(RAND()*7000 + 3000, 2), NOW(), NOW(), FLOOR(RAND()*19) + 1);

-- Generate 40 more similar entries
INSERT INTO jobs_job (job_title, description, status, start_date, end_date, cost_estimate, actual_cost, created_at, updated_at, customer_id)
SELECT 
    CASE FLOOR(RAND()*10) 
        WHEN 0 THEN 'Plumbing Repair'
        WHEN 1 THEN 'HVAC Installation'
        WHEN 2 THEN 'Roof Inspection'
        WHEN 3 THEN 'Electrical Wiring'
        WHEN 4 THEN 'Flooring Replacement'
        WHEN 5 THEN 'Painting Exterior'
        WHEN 6 THEN 'Landscaping'
        WHEN 7 THEN 'Window Replacement'
        WHEN 8 THEN 'Carpentry Work'
        ELSE 'Solar Panel Installation'
    END,
    'Generated job description.',
    CASE FLOOR(RAND()*4) 
        WHEN 0 THEN 'Pending'
        WHEN 1 THEN 'In Progress'
        WHEN 2 THEN 'Completed'
        ELSE 'Cancelled'
    END,
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*730) DAY),
    IF(RAND() > 0.3, DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*90) DAY), NULL),
    ROUND(RAND()*5000 + 500, 2),
    IF(RAND() > 0.5, ROUND(RAND()*5000 + 500, 2), NULL),
    NOW(),
    NOW(),
    FLOOR(RAND()*19) + 1
FROM information_schema.tables
LIMIT 40;
