-- ============================================================
-- Seed Data
-- ============================================================


-- Branches
INSERT INTO Branch (name, city, address, phone, manager_name) VALUES
('Spice Garden - MG Road',   'Bengaluru', '12, MG Road, Bengaluru',         '080-11112222', 'Ravi Kumar'),
('Spice Garden - Koramangala','Bengaluru', '45, 5th Block, Koramangala',     '080-33334444', 'Priya Sharma'),
('Spice Garden - Mysuru',     'Mysuru',   '8, Sayyaji Rao Road, Mysuru',    '0821-5556666', 'Arjun Nair'),
('Spice Garden - Pune',       'Pune',     '22, FC Road, Pune',              '020-7778888',  'Sneha Patil');

-- Customers
INSERT INTO Customer (name, email, phone, city) VALUES
('Amit Verma',    'amit@example.com',   '9900001111', 'Bengaluru'),
('Neha Singh',    'neha@example.com',   '9900002222', 'Mysuru'),
('Rohan Das',     'rohan@example.com',  '9900003333', 'Pune'),
('Kavya Reddy',   'kavya@example.com',  '9900004444', 'Bengaluru'),
('Suresh Iyer',   'suresh@example.com', '9900005555', 'Bengaluru'),
('Preethi Nair',  'preethi@example.com','9900006666', 'Mysuru');

-- Employees
INSERT INTO Employee (branch_id, name, role, salary, joined_at) VALUES
(1, 'Ravi Kumar',    'Manager',  75000, '2020-01-10'),
(1, 'Anand S',       'Chef',     45000, '2020-03-15'),
(1, 'Divya L',       'Waiter',   22000, '2021-06-01'),
(2, 'Priya Sharma',  'Manager',  72000, '2019-11-05'),
(2, 'Kiran M',       'Chef',     43000, '2020-05-20'),
(3, 'Arjun Nair',    'Manager',  70000, '2021-01-15'),
(3, 'Meena T',       'Cashier',  25000, '2021-07-10'),
(4, 'Sneha Patil',   'Manager',  73000, '2020-08-01');

-- Menu Items
INSERT INTO Menu_Item (branch_id, name, category, price) VALUES
-- Branch 1
(1, 'Paneer Tikka',        'Starter',     180.00),
(1, 'Butter Chicken',      'Main Course', 320.00),
(1, 'Dal Makhani',         'Main Course', 220.00),
(1, 'Gulab Jamun',         'Dessert',     90.00),
(1, 'Mango Lassi',         'Beverage',    80.00),
-- Branch 2
(2, 'Veg Spring Rolls',    'Starter',     150.00),
(2, 'Chicken Biryani',     'Main Course', 280.00),
(2, 'Palak Paneer',        'Main Course', 210.00),
(2, 'Rasmalai',            'Dessert',     110.00),
(2, 'Cold Coffee',         'Beverage',    120.00),
-- Branch 3
(3, 'Samosa',              'Snack',        40.00),
(3, 'Masala Dosa',         'Main Course', 130.00),
(3, 'Idli Sambar',         'Main Course', 100.00),
(3, 'Filter Coffee',       'Beverage',    60.00),
(3, 'Mysore Pak',          'Dessert',     80.00),
-- Branch 4
(4, 'Vada Pav',            'Snack',        50.00),
(4, 'Misal Pav',           'Main Course', 140.00),
(4, 'Pav Bhaji',           'Main Course', 160.00),
(4, 'Shrikhand',           'Dessert',     100.00),
(4, 'Sugarcane Juice',     'Beverage',    70.00);

-- Inventory
INSERT INTO Inventory (branch_id, ingredient, quantity, unit, reorder_level) VALUES
(1, 'Tomatoes',   50.0,  'kg',    10.0),
(1, 'Paneer',     20.0,  'kg',    5.0),
(1, 'Rice',       100.0, 'kg',    20.0),
(1, 'Milk',       30.0,  'litre', 8.0),
(2, 'Chicken',    40.0,  'kg',    10.0),
(2, 'Spinach',    15.0,  'kg',    4.0),
(2, 'Rice',       80.0,  'kg',    15.0),
(3, 'Rice',       60.0,  'kg',    15.0),
(3, 'Urad Dal',   20.0,  'kg',    5.0),
(3, 'Coffee Powder', 5.0,'kg',    1.5),
(4, 'Potatoes',   60.0,  'kg',    15.0),
(4, 'Bread',      200.0, 'pieces',50.0);

-- Orders
INSERT INTO `Order` (branch_id, customer_id, order_type, status) VALUES
(1, 1, 'Dine-in',  'Delivered'),
(1, 4, 'Takeaway', 'Delivered'),
(2, 1, 'Delivery', 'Delivered'),
(2, 5, 'Dine-in',  'Delivered'),
(3, 2, 'Dine-in',  'Delivered'),
(3, 6, 'Takeaway', 'Preparing'),
(4, 3, 'Dine-in',  'Delivered'),
(1, 5, 'Delivery', 'Pending');

-- Order Items
INSERT INTO Order_Item (order_id, item_id, quantity, unit_price) VALUES
(1, 1, 2, 180.00), (1, 2, 1, 320.00), (1, 5, 2, 80.00),
(2, 3, 1, 220.00), (2, 4, 2, 90.00),
(3, 6, 1, 150.00), (3, 7, 2, 280.00),
(4, 8, 1, 210.00), (4, 9, 2, 110.00), (4, 10, 1, 120.00),
(5,11, 3,  40.00), (5,12, 1, 130.00), (5,14, 2,  60.00),
(6,13, 2, 100.00), (6,15, 1,  80.00),
(7,17, 2, 140.00), (7,18, 1, 160.00), (7,20, 1,  70.00),
(8, 2, 1, 320.00), (8, 5, 1,  80.00);

-- Payments
INSERT INTO Payment (order_id, amount, method, status) VALUES
(1, 840.00,  'UPI',   'Paid'),
(2, 400.00,  'Cash',  'Paid'),
(3, 710.00,  'Card',  'Paid'),
(4, 550.00,  'UPI',   'Paid'),
(5, 310.00,  'Cash',  'Paid'),
(7, 510.00,  'Card',  'Paid');

-- Reviews
INSERT INTO Review (order_id, customer_id, branch_id, rating, comment) VALUES
(1, 1, 1, 5, 'Amazing food and service!'),
(2, 4, 1, 4, 'Tasty but a bit slow.'),
(3, 1, 2, 5, 'Best biryani in the city.'),
(5, 2, 3, 4, 'Loved the Mysuru vibes.'),
(7, 3, 4, 3, 'Decent food, average ambience.');
