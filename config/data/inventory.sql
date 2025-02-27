-- Insert 10 random inventories
INSERT INTO inventory_inventory (name, description, created_at, updated_at)
VALUES
('Inventory A', 'Description for Inventory A', NOW(), NOW()),
('Inventory B', 'Description for Inventory B', NOW(), NOW()),
('Inventory C', 'Description for Inventory C', NOW(), NOW()),
('Inventory D', 'Description for Inventory D', NOW(), NOW()),
('Inventory E', 'Description for Inventory E', NOW(), NOW()),
('Inventory F', 'Description for Inventory F', NOW(), NOW()),
('Inventory G', 'Description for Inventory G', NOW(), NOW()),
('Inventory H', 'Description for Inventory H', NOW(), NOW()),
('Inventory I', 'Description for Inventory I', NOW(), NOW()),
('Inventory J', 'Description for Inventory J', NOW(), NOW());

-- Insert random Inventory Items for each inventory
INSERT INTO inventory_inventoryitem (name, description, sku, price, stock_quantity, inventory_id)
SELECT 
    CONCAT('Item ', FLOOR(RAND() * 1000)), 
    CONCAT('Description for Item ', FLOOR(RAND() * 1000)), 
    CONCAT('SKU-', FLOOR(RAND() * 100000)), 
    ROUND(RAND() * 100 + 1, 2), 
    FLOOR(RAND() * 50 + 1), 
    id 
FROM inventory_inventory, (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 
                 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) t 
ORDER BY RAND() 
LIMIT 50;
