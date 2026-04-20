-- ============================================================
-- Distributed Restaurant Chain Management System
-- Database Schema
-- ============================================================

-- ─── BRANCHES ────────────────────────────────────────────────
CREATE TABLE Branch (
    branch_id     INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    city          VARCHAR(100) NOT NULL,
    address       VARCHAR(255) NOT NULL,
    phone         VARCHAR(20),
    manager_name  VARCHAR(100),
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─── CUSTOMERS ───────────────────────────────────────────────
CREATE TABLE Customer (
    customer_id   INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(150) UNIQUE NOT NULL,
    phone         VARCHAR(20),
    city          VARCHAR(100),
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─── EMPLOYEES ───────────────────────────────────────────────
CREATE TABLE Employee (
    employee_id   INT AUTO_INCREMENT PRIMARY KEY,
    branch_id     INT NOT NULL,
    name          VARCHAR(100) NOT NULL,
    role          ENUM('Manager','Chef','Waiter','Cashier','Delivery') NOT NULL,
    salary        DECIMAL(10,2),
    joined_at     DATE,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id) ON DELETE CASCADE
);

-- ─── MENU ────────────────────────────────────────────────────
CREATE TABLE Menu_Item (
    item_id       INT AUTO_INCREMENT PRIMARY KEY,
    branch_id     INT NOT NULL,
    name          VARCHAR(150) NOT NULL,
    category      ENUM('Starter','Main Course','Dessert','Beverage','Snack') NOT NULL,
    price         DECIMAL(8,2) NOT NULL,
    is_available  BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id) ON DELETE CASCADE
);

-- ─── INVENTORY ───────────────────────────────────────────────
CREATE TABLE Inventory (
    inventory_id  INT AUTO_INCREMENT PRIMARY KEY,
    branch_id     INT NOT NULL,
    ingredient    VARCHAR(150) NOT NULL,
    quantity      DECIMAL(10,2) NOT NULL,
    unit          VARCHAR(30) NOT NULL,
    reorder_level DECIMAL(10,2) NOT NULL,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id) ON DELETE CASCADE
);

-- ─── ORDERS ──────────────────────────────────────────────────
CREATE TABLE `Order` (
    order_id      INT AUTO_INCREMENT PRIMARY KEY,
    branch_id     INT NOT NULL,
    customer_id   INT NOT NULL,
    order_type    ENUM('Dine-in','Takeaway','Delivery') NOT NULL,
    status        ENUM('Pending','Preparing','Ready','Delivered','Cancelled') DEFAULT 'Pending',
    ordered_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (branch_id)   REFERENCES Branch(branch_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- ─── ORDER ITEMS ─────────────────────────────────────────────
CREATE TABLE Order_Item (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id      INT NOT NULL,
    item_id       INT NOT NULL,
    quantity      INT NOT NULL CHECK (quantity > 0),
    unit_price    DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id)  REFERENCES Menu_Item(item_id)
);

-- ─── PAYMENTS ────────────────────────────────────────────────
CREATE TABLE Payment (
    payment_id    INT AUTO_INCREMENT PRIMARY KEY,
    order_id      INT UNIQUE NOT NULL,
    amount        DECIMAL(10,2) NOT NULL,
    method        ENUM('Cash','Card','UPI','Wallet') NOT NULL,
    status        ENUM('Paid','Pending','Failed','Refunded') DEFAULT 'Pending',
    paid_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id)
);

-- ─── REVIEWS ─────────────────────────────────────────────────
CREATE TABLE Review (
    review_id     INT AUTO_INCREMENT PRIMARY KEY,
    order_id      INT NOT NULL,
    customer_id   INT NOT NULL,
    branch_id     INT NOT NULL,
    rating        TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment       TEXT,
    reviewed_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id)    REFERENCES `Order`(order_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (branch_id)   REFERENCES Branch(branch_id)
);
