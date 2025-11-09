-- Add more categories
INSERT INTO categories (slug, title, hero_title, hero_subtitle, image_url)
VALUES
 ('sleep-ritual', 'Sleep Ritual', 'Restful Nights', 'Create the perfect bedtime routine', 'https://picsum.photos/seed/sleep/800/400'),
 ('self-care-ritual', 'Self-Care Ritual', 'Nurture Yourself', 'Daily moments of self-love', 'https://picsum.photos/seed/selfcare/800/400'),
 ('focus-ritual', 'Focus Ritual', 'Find Your Center', 'Enhance concentration and clarity', 'https://picsum.photos/seed/focus/800/400')
ON DUPLICATE KEY UPDATE title=VALUES(title);

-- Add more products with featured and bestseller flags
INSERT INTO products (product_id, title, tagline, description, price, compare_at_price, rating, reviews_count, brand_info, category_id, is_featured, is_bestseller)
VALUES
-- Featured Products (is_featured = TRUE)
 ('calm-candle-1', 'Calm Candle', 'Lavender & Sage', 'Aromatherapy candle for relaxation and stress relief. Hand-poured with essential oils.', 24.00, 29.00, 4.7, 125, 'SoulNest', (SELECT id FROM categories WHERE slug='calm-ritual'), TRUE, TRUE),
 ('sleep-pillow-mist', 'Sleep Pillow Mist', 'Lavender & Chamomile', 'Spray on your pillow for a restful night\'s sleep. Natural and calming.', 22.00, NULL, 4.8, 98, 'SoulNest', (SELECT id FROM categories WHERE slug='sleep-ritual'), TRUE, TRUE),
 ('self-love-journal', 'Self-Love Journal', 'Daily Reflection & Gratitude', 'Premium journal with prompts for daily self-reflection and gratitude practice.', 18.00, 24.00, 4.9, 156, 'SoulNest', (SELECT id FROM categories WHERE slug='self-care-ritual'), TRUE, FALSE),
 ('meditation-cushion', 'Meditation Cushion', 'Zen Comfort', 'Ergonomic cushion for comfortable meditation and mindfulness practice.', 45.00, 55.00, 4.6, 87, 'SoulNest', (SELECT id FROM categories WHERE slug='calm-ritual'), TRUE, FALSE),
 ('energy-mist-1', 'Energy Mist', 'Citrus Uplift', 'Refreshing face and room mist with invigorating citrus essential oils.', 18.00, NULL, 4.5, 73, 'SoulNest', (SELECT id FROM categories WHERE slug='energy-ritual'), TRUE, TRUE),

-- Bestseller Products (is_bestseller = TRUE, some also featured)
 ('bath-salt-bundle', 'Luxury Bath Salt Bundle', 'Eucalyptus & Rose', 'Premium bath salts for ultimate relaxation. Includes 3 soothing varieties.', 28.00, 35.00, 4.7, 203, 'SoulNest', (SELECT id FROM categories WHERE slug='self-care-ritual'), FALSE, TRUE),
 ('crystal-set', 'Healing Crystal Set', '7 Chakra Stones', 'Beautiful set of 7 crystals for chakra balancing and positive energy.', 35.00, 45.00, 4.8, 189, 'SoulNest', (SELECT id FROM categories WHERE slug='self-care-ritual'), FALSE, TRUE),
 ('focus-diffuser', 'Essential Oil Diffuser', 'Aromatherapy Bliss', 'Ultrasonic diffuser with LED lights. Perfect for focus and relaxation.', 32.00, 40.00, 4.6, 142, 'SoulNest', (SELECT id FROM categories WHERE slug='focus-ritual'), FALSE, TRUE),
 ('yoga-mat', 'Premium Yoga Mat', 'Eco-Friendly & Non-Slip', 'High-quality yoga mat with superior grip and cushioning for all practices.', 38.00, 48.00, 4.9, 167, 'SoulNest', (SELECT id FROM categories WHERE slug='calm-ritual'), FALSE, TRUE),

-- Regular Products (neither featured nor bestseller)
 ('face-mask-set', 'Hydrating Face Mask Set', 'Rose & Aloe', 'Set of 5 nourishing face masks for glowing skin.', 25.00, NULL, 4.4, 45, 'SoulNest', (SELECT id FROM categories WHERE slug='self-care-ritual'), FALSE, FALSE),
 ('tea-blend', 'Calming Tea Blend', 'Chamomile & Mint', 'Organic herbal tea blend for relaxation and wellness.', 15.00, 20.00, 4.5, 52, 'SoulNest', (SELECT id FROM categories WHERE slug='calm-ritual'), FALSE, FALSE),
 ('focus-candle', 'Focus Candle', 'Peppermint & Eucalyptus', 'Energizing candle to boost concentration and mental clarity.', 26.00, NULL, 4.3, 38, 'SoulNest', (SELECT id FROM categories WHERE slug='focus-ritual'), FALSE, FALSE)
ON DUPLICATE KEY UPDATE 
  title=VALUES(title),
  tagline=VALUES(tagline),
  description=VALUES(description),
  price=VALUES(price),
  compare_at_price=VALUES(compare_at_price),
  rating=VALUES(rating),
  reviews_count=VALUES(reviews_count),
  is_featured=VALUES(is_featured),
  is_bestseller=VALUES(is_bestseller);

-- Add product images for all products
INSERT INTO product_images (product_id, image_url, display_order)
SELECT p.id, CONCAT('https://picsum.photos/seed/', p.product_id, '/600/600'), 0 
FROM products p
WHERE NOT EXISTS (SELECT 1 FROM product_images WHERE product_id = p.id)
ON DUPLICATE KEY UPDATE image_url=VALUES(image_url);

-- Add multiple images for featured products (optional - for better UI)
INSERT INTO product_images (product_id, image_url, display_order)
SELECT id, CONCAT('https://picsum.photos/seed/', product_id, '-2/600/600'), 1 FROM products WHERE is_featured = TRUE
ON DUPLICATE KEY UPDATE display_order=VALUES(display_order);

-- Add how-to-use instructions for all products
INSERT INTO product_how_to_use (product_id, instruction, step_order)
SELECT id, 'Follow the instructions on the product label', 0 FROM products
WHERE NOT EXISTS (SELECT 1 FROM product_how_to_use WHERE product_id = products.id);

-- Add guarantees for all products
INSERT INTO product_guarantees (product_id, guarantee_text)
SELECT id, '30-day satisfaction guarantee' FROM products
WHERE NOT EXISTS (SELECT 1 FROM product_guarantees WHERE product_id = products.id);

-- Update existing products to ensure featured/bestseller flags are set correctly
UPDATE products SET is_featured = TRUE, is_bestseller = TRUE WHERE product_id = 'calm-candle-1';
UPDATE products SET is_featured = TRUE, is_bestseller = TRUE WHERE product_id = 'sleep-pillow-mist';
UPDATE products SET is_featured = TRUE, is_bestseller = TRUE WHERE product_id = 'energy-mist-1';
UPDATE products SET is_featured = TRUE, is_bestseller = FALSE WHERE product_id = 'self-love-journal';
UPDATE products SET is_featured = TRUE, is_bestseller = FALSE WHERE product_id = 'meditation-cushion';
UPDATE products SET is_featured = FALSE, is_bestseller = TRUE WHERE product_id = 'bath-salt-bundle';
UPDATE products SET is_featured = FALSE, is_bestseller = TRUE WHERE product_id = 'crystal-set';
UPDATE products SET is_featured = FALSE, is_bestseller = TRUE WHERE product_id = 'focus-diffuser';
UPDATE products SET is_featured = FALSE, is_bestseller = TRUE WHERE product_id = 'yoga-mat';

