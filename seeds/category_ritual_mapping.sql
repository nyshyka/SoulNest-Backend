-- Category and Ritual Mapping Seed File
-- This file creates categories that match the shop page and sets up products and rituals

USE soulnest_db;

-- Create/Update categories to match shop page keys
INSERT INTO categories (slug, title, hero_title, hero_subtitle, image_url)
VALUES
  ('rituals', 'Rituals & Self-Care', 'Your Ritual Journey', 'Discover products and rituals for mindful living and self-care', 'https://picsum.photos/seed/rituals/800/400'),
  ('mindful', 'Mind & Soul Care', 'Nurture Your Inner Self', 'Products and practices for mental wellness and spiritual growth', 'https://picsum.photos/seed/mindful/800/400'),
  ('gifts', 'Lifestyle & Gifts', 'Thoughtful Gifts', 'Curated collections for yourself and loved ones', 'https://picsum.photos/seed/gifts/800/400')
ON DUPLICATE KEY UPDATE 
  title=VALUES(title),
  hero_title=VALUES(hero_title),
  hero_subtitle=VALUES(hero_subtitle),
  image_url=VALUES(image_url);

-- Update existing products to assign them to these categories
-- Distribute products across the three categories
UPDATE products 
SET category_id = (SELECT id FROM categories WHERE slug = 'rituals')
WHERE category_id IS NULL OR category_id IN (SELECT id FROM categories WHERE slug IN ('calm-ritual', 'sleep-ritual', 'self-care-ritual'))
LIMIT 10;

UPDATE products 
SET category_id = (SELECT id FROM categories WHERE slug = 'mindful')
WHERE category_id IS NULL OR category_id IN (SELECT id FROM categories WHERE slug IN ('focus-ritual', 'energy-ritual'))
LIMIT 10;

UPDATE products 
SET category_id = (SELECT id FROM categories WHERE slug = 'gifts')
WHERE category_id IS NULL
LIMIT 5;

-- Create ritual guides for 'rituals' category
INSERT INTO ritual_guides (category_id, step_number, step_title, product_id)
SELECT 
  (SELECT id FROM categories WHERE slug = 'rituals'),
  1,
  'Set Your Intention',
  NULL
WHERE NOT EXISTS (
  SELECT 1 FROM ritual_guides 
  WHERE category_id = (SELECT id FROM categories WHERE slug = 'rituals') 
  AND step_number = 1
);

INSERT INTO ritual_guides (category_id, step_number, step_title, product_id)
SELECT 
  (SELECT id FROM categories WHERE slug = 'rituals'),
  2,
  'Choose Your Products',
  (SELECT id FROM products WHERE category_id = (SELECT id FROM categories WHERE slug = 'rituals') LIMIT 1)
WHERE NOT EXISTS (
  SELECT 1 FROM ritual_guides 
  WHERE category_id = (SELECT id FROM categories WHERE slug = 'rituals') 
  AND step_number = 2
);

INSERT INTO ritual_guides (category_id, step_number, step_title, product_id)
SELECT 
  (SELECT id FROM categories WHERE slug = 'rituals'),
  3,
  'Create Your Sacred Space',
  NULL
WHERE NOT EXISTS (
  SELECT 1 FROM ritual_guides 
  WHERE category_id = (SELECT id FROM categories WHERE slug = 'rituals') 
  AND step_number = 3
);

-- Create ritual guides for 'mindful' category
INSERT INTO ritual_guides (category_id, step_number, step_title, product_id)
SELECT 
  (SELECT id FROM categories WHERE slug = 'mindful'),
  1,
  'Center Your Mind',
  NULL
WHERE NOT EXISTS (
  SELECT 1 FROM ritual_guides 
  WHERE category_id = (SELECT id FROM categories WHERE slug = 'mindful') 
  AND step_number = 1
);

INSERT INTO ritual_guides (category_id, step_number, step_title, product_id)
SELECT 
  (SELECT id FROM categories WHERE slug = 'mindful'),
  2,
  'Use Your Mindful Tools',
  (SELECT id FROM products WHERE category_id = (SELECT id FROM categories WHERE slug = 'mindful') LIMIT 1)
WHERE NOT EXISTS (
  SELECT 1 FROM ritual_guides 
  WHERE category_id = (SELECT id FROM categories WHERE slug = 'mindful') 
  AND step_number = 2
);

INSERT INTO ritual_guides (category_id, step_number, step_title, product_id)
SELECT 
  (SELECT id FROM categories WHERE slug = 'mindful'),
  3,
  'Reflect and Journal',
  NULL
WHERE NOT EXISTS (
  SELECT 1 FROM ritual_guides 
  WHERE category_id = (SELECT id FROM categories WHERE slug = 'mindful') 
  AND step_number = 3
);

-- Create ritual guides for 'gifts' category
INSERT INTO ritual_guides (category_id, step_number, step_title, product_id)
SELECT 
  (SELECT id FROM categories WHERE slug = 'gifts'),
  1,
  'Select Your Gift Collection',
  NULL
WHERE NOT EXISTS (
  SELECT 1 FROM ritual_guides 
  WHERE category_id = (SELECT id FROM categories WHERE slug = 'gifts') 
  AND step_number = 1
);

INSERT INTO ritual_guides (category_id, step_number, step_title, product_id)
SELECT 
  (SELECT id FROM categories WHERE slug = 'gifts'),
  2,
  'Personalize Your Gift',
  (SELECT id FROM products WHERE category_id = (SELECT id FROM categories WHERE slug = 'gifts') LIMIT 1)
WHERE NOT EXISTS (
  SELECT 1 FROM ritual_guides 
  WHERE category_id = (SELECT id FROM categories WHERE slug = 'gifts') 
  AND step_number = 2
);

INSERT INTO ritual_guides (category_id, step_number, step_title, product_id)
SELECT 
  (SELECT id FROM categories WHERE slug = 'gifts'),
  3,
  'Share the Love',
  NULL
WHERE NOT EXISTS (
  SELECT 1 FROM ritual_guides 
  WHERE category_id = (SELECT id FROM categories WHERE slug = 'gifts') 
  AND step_number = 3
);

-- Ensure all products have at least one image
INSERT INTO product_images (product_id, image_url, display_order)
SELECT 
  p.id,
  CONCAT('https://picsum.photos/seed/', p.product_id, '/600/600'),
  0
FROM products p
WHERE NOT EXISTS (
  SELECT 1 FROM product_images WHERE product_id = p.id
);

