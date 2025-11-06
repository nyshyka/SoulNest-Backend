CREATE DATABASE IF NOT EXISTS soulnest_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE soulnest_db;

-- Drop tables if needed (order matters due to FKs)
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS cart_items;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS wishlist;
DROP TABLE IF EXISTS payment_methods;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS ritual_guides;
DROP TABLE IF EXISTS related_products;
DROP TABLE IF EXISTS product_guarantees;
DROP TABLE IF EXISTS product_how_to_use;
DROP TABLE IF EXISTS product_images;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS newsletter_subscriptions;
DROP TABLE IF EXISTS tips;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

-- Users
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  is_guest BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Categories
CREATE TABLE categories (
  id INT PRIMARY KEY AUTO_INCREMENT,
  slug VARCHAR(100) UNIQUE NOT NULL,
  title VARCHAR(255) NOT NULL,
  hero_title VARCHAR(255),
  hero_subtitle TEXT,
  image_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products
CREATE TABLE products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  product_id VARCHAR(100) UNIQUE NOT NULL,
  title VARCHAR(255) NOT NULL,
  tagline TEXT,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  compare_at_price DECIMAL(10,2),
  rating DECIMAL(3,2) DEFAULT 0.00,
  reviews_count INT DEFAULT 0,
  brand_info TEXT,
  category_id INT,
  is_featured BOOLEAN DEFAULT FALSE,
  is_bestseller BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- Product Images
CREATE TABLE product_images (
  id INT PRIMARY KEY AUTO_INCREMENT,
  product_id INT NOT NULL,
  image_url VARCHAR(500) NOT NULL,
  display_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Product How To Use
CREATE TABLE product_how_to_use (
  id INT PRIMARY KEY AUTO_INCREMENT,
  product_id INT NOT NULL,
  instruction TEXT NOT NULL,
  step_order INT DEFAULT 0,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Product Guarantees
CREATE TABLE product_guarantees (
  id INT PRIMARY KEY AUTO_INCREMENT,
  product_id INT NOT NULL,
  guarantee_text VARCHAR(255) NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Related Products
CREATE TABLE related_products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  product_id INT NOT NULL,
  related_product_id INT NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  FOREIGN KEY (related_product_id) REFERENCES products(id) ON DELETE CASCADE,
  UNIQUE KEY unique_relation (product_id, related_product_id)
);

-- Ritual Guides
CREATE TABLE ritual_guides (
  id INT PRIMARY KEY AUTO_INCREMENT,
  category_id INT NOT NULL,
  step_number INT NOT NULL,
  step_title VARCHAR(255) NOT NULL,
  product_id INT,
  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
);

-- Cart Items
CREATE TABLE cart_items (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  UNIQUE KEY unique_user_product (user_id, product_id)
);

-- Orders
CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  order_number VARCHAR(50) UNIQUE NOT NULL,
  user_id INT NOT NULL,
  subtotal DECIMAL(10,2) NOT NULL,
  delivery_fee DECIMAL(10,2) DEFAULT 0.00,
  savings DECIMAL(10,2) DEFAULT 0.00,
  total DECIMAL(10,2) NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Order Items
CREATE TABLE order_items (
  id INT PRIMARY KEY AUTO_INCREMENT,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  price_at_purchase DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);

-- Reviews
CREATE TABLE reviews (
  id INT PRIMARY KEY AUTO_INCREMENT,
  product_id INT NOT NULL,
  user_id INT NOT NULL,
  rating INT NOT NULL,
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE KEY unique_user_product_review (user_id, product_id)
);

-- Wishlist
CREATE TABLE wishlist (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  product_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  UNIQUE KEY unique_user_wishlist (user_id, product_id)
);

-- Addresses
CREATE TABLE addresses (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  street_address VARCHAR(255) NOT NULL,
  city VARCHAR(100) NOT NULL,
  state VARCHAR(100),
  zip_code VARCHAR(20) NOT NULL,
  country VARCHAR(100) DEFAULT 'USA',
  phone VARCHAR(20),
  is_default BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Payment Methods
CREATE TABLE payment_methods (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  card_type VARCHAR(50),
  last_four VARCHAR(4) NOT NULL,
  expiry_month INT,
  expiry_year INT,
  is_default BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Newsletter Subscriptions
CREATE TABLE newsletter_subscriptions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);

-- Tips / Blog
CREATE TABLE tips (
  id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  image_url VARCHAR(500),
  content TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Seed Categories
INSERT INTO categories (slug, title, hero_title, hero_subtitle, image_url)
VALUES
 ('calm-ritual', 'Calm Ritual', 'Find Your Calm', 'A soothing path to inner peace', 'https://picsum.photos/seed/calm/800/400'),
 ('energy-ritual', 'Energy Ritual', 'Boost Your Energy', 'Invigorate your day', 'https://picsum.photos/seed/energy/800/400')
ON DUPLICATE KEY UPDATE title=VALUES(title);

-- Seed Products (minimal)
INSERT INTO products (product_id, title, tagline, description, price, compare_at_price, rating, reviews_count, brand_info, category_id, is_featured, is_bestseller)
VALUES
 ('calm-candle-1', 'Calm Candle', 'Lavender & Sage', 'Aromatherapy candle for relaxation', 24.00, 29.00, 4.7, 12, 'SoulNest', (SELECT id FROM categories WHERE slug='calm-ritual'), TRUE, TRUE),
 ('energy-mist-1', 'Energy Mist', 'Citrus Uplift', 'Refreshing face and room mist', 18.00, NULL, 4.5, 7, 'SoulNest', (SELECT id FROM categories WHERE slug='energy-ritual'), TRUE, FALSE)
ON DUPLICATE KEY UPDATE title=VALUES(title);

-- Seed Product Images
INSERT INTO product_images (product_id, image_url, display_order)
SELECT p.id, CONCAT('https://picsum.photos/seed/', p.product_id, '/600/600'), 0 FROM products p
ON DUPLICATE KEY UPDATE image_url=VALUES(image_url);

-- Seed How-To-Use
INSERT INTO product_how_to_use (product_id, instruction, step_order)
SELECT id, 'Light the candle and breathe deeply for 3 minutes', 0 FROM products WHERE product_id='calm-candle-1';

-- Seed Guarantees
INSERT INTO product_guarantees (product_id, guarantee_text)
SELECT id, '30-day satisfaction guarantee' FROM products WHERE product_id='calm-candle-1';

-- Seed Ritual Guides
INSERT INTO ritual_guides (category_id, step_number, step_title, product_id)
VALUES
 ((SELECT id FROM categories WHERE slug='calm-ritual'), 1, 'Prepare your space', NULL),
 ((SELECT id FROM categories WHERE slug='calm-ritual'), 2, 'Light the Calm Candle', (SELECT id FROM products WHERE product_id='calm-candle-1')),
 ((SELECT id FROM categories WHERE slug='calm-ritual'), 3, 'Breathe and unwind', NULL)
ON DUPLICATE KEY UPDATE step_title=VALUES(step_title);

-- Seed Tips
INSERT INTO tips (title, description, image_url, content)
VALUES
 ('Why self-love matters', 'Practical steps to start today', 'https://picsum.photos/seed/tip1/800/400', 'Long form content...')
ON DUPLICATE KEY UPDATE description=VALUES(description);

-- Test User (password=Test1234!)
INSERT INTO users (name, email, password_hash, is_guest)
VALUES ('Test User', 'test@soulnest.local', '$2b$12$k2qk9cF9xq6w9f2f5tZ3We5E2J4mQqE4pR7z7m0s3m3m3m3m3m3mK', FALSE)
ON DUPLICATE KEY UPDATE name=VALUES(name);


