-- Comprehensive Seed Data for SoulNest Database
-- Run this after migrations_new_features.sql and mysql_seed.sql

USE soulnest_db;

-- Insert Categories
INSERT INTO categories (slug, title, hero_title, hero_subtitle, image_url) VALUES
('rituals', 'Journaling & Reflection', 'Find Your Inner Peace', 'Discover products that help you reflect and grow', '/window.svg'),
('mindful', 'Mind & Soul Care', 'Nurture Your Wellbeing', 'Essential products for mental wellness', '/file.svg'),
('body-care', 'Body Care (Pamper Yourself)', 'Self-Love Essentials', 'Treat yourself with care', '/globe.svg'),
('lifestyle', 'Lifestyle & Decor', 'Create Your Sanctuary', 'Transform your space into a haven', '/vercel.svg'),
('accessories', 'Accessories', 'Complete Your Ritual', 'Beautiful accessories for your journey', '/next.svg'),
('gifts', 'Gift Sets (for others & oneself)', 'Share the Love', 'Thoughtful gifts for special moments', '/next.svg')
AS new_categories
ON DUPLICATE KEY UPDATE title=new_categories.title;

-- Insert Products
INSERT INTO products (product_id, title, tagline, description, price, compare_at_price, rating, reviews_count, brand_info, category_id, is_featured, is_bestseller) VALUES
('PROD-001', 'Evening Meditation Candle Set', 'Illuminate Your Inner Peace', 'A curated collection of hand-poured soy candles infused with calming essential oils. Perfect for evening meditation and relaxation rituals.', 34.99, 44.99, 4.8, 127, 'SoulNest Artisan Collection', 1, TRUE, TRUE),
('PROD-002', 'Gratitude Journal', 'Write Your Way to Joy', 'A beautifully bound journal with daily prompts to help you cultivate gratitude and mindfulness. Includes 365 pages of reflection space.', 24.99, NULL, 4.9, 89, 'SoulNest Essentials', 1, TRUE, TRUE),
('PROD-003', 'Lavender Sleep Mist', 'Drift into Dreamland', 'A soothing blend of lavender, chamomile, and valerian root. Spray on your pillow before bed for a restful night\'s sleep.', 18.99, 24.99, 4.7, 203, 'SoulNest Wellness', 2, TRUE, TRUE),
('PROD-004', 'Rose Quartz Face Roller', 'Glow from Within', 'Premium rose quartz facial roller with jade gua sha tool. Helps reduce puffiness, improve circulation, and promote lymphatic drainage.', 29.99, 39.99, 4.6, 156, 'SoulNest Beauty', 3, FALSE, TRUE),
('PROD-005', 'Essential Oil Diffuser', 'Transform Your Space', 'Ultrasonic diffuser with 7 color LED lights and auto-shutoff. Perfect for aromatherapy and creating a calming atmosphere.', 45.99, 59.99, 4.8, 94, 'SoulNest Home', 4, TRUE, FALSE),
('PROD-006', 'Self-Care Sunday Box', 'Your Weekly Reset', 'A monthly subscription box featuring curated self-care products including candles, bath salts, teas, and wellness items.', 49.99, NULL, 4.9, 67, 'SoulNest Subscription', 6, TRUE, TRUE),
('PROD-007', 'Bamboo Meditation Cushion', 'Find Your Center', 'Eco-friendly zafu cushion filled with buckwheat hulls. Adjustable height for comfortable seated meditation.', 39.99, 49.99, 4.5, 112, 'SoulNest Essentials', 1, FALSE, FALSE),
('PROD-008', 'Herbal Tea Collection', 'Sip Your Way to Calm', 'A selection of 6 organic herbal teas including chamomile, peppermint, and rooibos. 20 tea bags per variety.', 22.99, 28.99, 4.7, 178, 'SoulNest Wellness', 2, FALSE, TRUE),
('PROD-009', 'Crystal Healing Set', 'Harness Earth\'s Energy', 'A curated collection of 7 healing crystals including amethyst, clear quartz, and rose quartz. Includes guidebook.', 34.99, 44.99, 4.6, 145, 'SoulNest Mystic', 4, FALSE, FALSE),
('PROD-010', 'Bath Bomb Gift Set', 'Soak Away Stress', 'Set of 6 handcrafted bath bombs in various scents: lavender, eucalyptus, rose, jasmine, vanilla, and chamomile.', 28.99, 35.99, 4.8, 201, 'SoulNest Beauty', 3, TRUE, TRUE),
('PROD-011', 'Yoga Mat & Accessories', 'Move with Intention', 'Premium non-slip yoga mat with carrying strap, blocks, and resistance band. Perfect for home practice.', 54.99, 69.99, 4.7, 98, 'SoulNest Active', 3, FALSE, FALSE),
('PROD-012', 'Aromatherapy Starter Kit', 'Begin Your Journey', 'Essential oil starter kit with 5 popular oils (lavender, eucalyptus, peppermint, lemon, tea tree) and diffuser blend guide.', 32.99, 42.99, 4.9, 167, 'SoulNest Wellness', 2, TRUE, FALSE),
('PROD-013', 'Moon Phase Wall Art', 'Celebrate the Cycles', 'Beautiful hand-illustrated moon phase print on premium paper. Available in multiple sizes. Perfect for meditation spaces.', 19.99, 24.99, 4.5, 76, 'SoulNest Home', 4, FALSE, FALSE),
('PROD-014', 'Wellness Planner', 'Plan Your Best Year', '12-month wellness planner with goal-setting pages, habit trackers, meal planning, and self-reflection prompts.', 27.99, 34.99, 4.8, 134, 'SoulNest Essentials', 1, FALSE, TRUE),
('PROD-015', 'Sage Smudging Kit', 'Cleanse Your Space', 'Traditional white sage bundle with abalone shell, feather, and instruction guide. For energy clearing and purification.', 16.99, 21.99, 4.4, 89, 'SoulNest Mystic', 4, FALSE, FALSE)
AS new_products
ON DUPLICATE KEY UPDATE title=new_products.title;

-- Insert Product Images (using subquery to get actual product ID)
INSERT INTO product_images (product_id, image_url, display_order) VALUES
((SELECT id FROM products WHERE product_id = 'PROD-001'), 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-001'), 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800', 2),
((SELECT id FROM products WHERE product_id = 'PROD-002'), 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-003'), 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-004'), 'https://images.unsplash.com/photo-1612817288484-6f916006741a?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-005'), 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-006'), 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-007'), 'https://images.unsplash.com/photo-1612817288484-6f916006741a?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-008'), 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-009'), 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-010'), 'https://images.unsplash.com/photo-1612817288484-6f916006741a?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-011'), 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-012'), 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-013'), 'https://images.unsplash.com/photo-1612817288484-6f916006741a?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-014'), 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800', 1),
((SELECT id FROM products WHERE product_id = 'PROD-015'), 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800', 1);

-- Insert Product How To Use
INSERT INTO product_how_to_use (product_id, instruction, step_order) VALUES
((SELECT id FROM products WHERE product_id = 'PROD-001'), 'Light the candle in a safe, well-ventilated area', 1),
((SELECT id FROM products WHERE product_id = 'PROD-001'), 'Allow the wax to pool completely before extinguishing', 2),
((SELECT id FROM products WHERE product_id = 'PROD-001'), 'Trim the wick to 1/4 inch before each use', 3),
((SELECT id FROM products WHERE product_id = 'PROD-002'), 'Set aside 10-15 minutes each day for journaling', 1),
((SELECT id FROM products WHERE product_id = 'PROD-002'), 'Use the daily prompts to guide your reflection', 2),
((SELECT id FROM products WHERE product_id = 'PROD-002'), 'Write freely without judgment or editing', 3),
((SELECT id FROM products WHERE product_id = 'PROD-003'), 'Shake the bottle gently before use', 1),
((SELECT id FROM products WHERE product_id = 'PROD-003'), 'Spray 2-3 times on your pillow and bedding', 2),
((SELECT id FROM products WHERE product_id = 'PROD-003'), 'Use 30 minutes before bedtime for best results', 3),
((SELECT id FROM products WHERE product_id = 'PROD-004'), 'Start with a clean, moisturized face', 1),
((SELECT id FROM products WHERE product_id = 'PROD-004'), 'Use upward and outward strokes with the roller', 2),
((SELECT id FROM products WHERE product_id = 'PROD-004'), 'Follow with the gua sha tool for deeper massage', 3),
((SELECT id FROM products WHERE product_id = 'PROD-005'), 'Fill the water tank to the maximum line', 1),
((SELECT id FROM products WHERE product_id = 'PROD-005'), 'Add 5-10 drops of your favorite essential oil', 2),
((SELECT id FROM products WHERE product_id = 'PROD-005'), 'Select your preferred light color and enjoy', 3);

-- Insert Product Guarantees
INSERT INTO product_guarantees (product_id, guarantee_text) VALUES
((SELECT id FROM products WHERE product_id = 'PROD-001'), '100% soy wax, no paraffin'),
((SELECT id FROM products WHERE product_id = 'PROD-001'), 'Hand-poured with care'),
((SELECT id FROM products WHERE product_id = 'PROD-002'), 'Premium paper, acid-free'),
((SELECT id FROM products WHERE product_id = 'PROD-002'), 'Lay-flat binding'),
((SELECT id FROM products WHERE product_id = 'PROD-003'), '100% natural ingredients'),
((SELECT id FROM products WHERE product_id = 'PROD-003'), 'Cruelty-free and vegan'),
((SELECT id FROM products WHERE product_id = 'PROD-004'), 'Authentic rose quartz'),
((SELECT id FROM products WHERE product_id = 'PROD-004'), '30-day satisfaction guarantee'),
((SELECT id FROM products WHERE product_id = 'PROD-005'), '1-year warranty'),
((SELECT id FROM products WHERE product_id = 'PROD-005'), 'BPA-free materials');

-- Insert Tips
INSERT INTO tips (title, description, image_url, content) VALUES
('5 Morning Rituals for a Better Day', 'Start your day with intention and mindfulness', 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800', '1. Wake up 15 minutes earlier\n2. Drink a glass of water\n3. Practice 5 minutes of meditation\n4. Write in your gratitude journal\n5. Set one intention for the day'),
('Creating Your Evening Wind-Down Routine', 'How to transition from work to rest', 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800', 'An effective wind-down routine helps signal to your body that it\'s time to rest. Try dimming the lights, lighting a candle, and doing some gentle stretching.'),
('The Power of Gratitude Journaling', 'Transform your mindset with daily practice', 'https://images.unsplash.com/photo-1612817288484-6f916006741a?w=800', 'Studies show that gratitude journaling can improve sleep, reduce stress, and increase overall happiness. Start with just 3 things you\'re grateful for each day.'),
('Aromatherapy 101: Essential Oils for Beginners', 'Your guide to getting started with essential oils', 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800', 'Essential oils can enhance your wellness routine. Start with lavender for sleep, peppermint for energy, and eucalyptus for respiratory support.'),
('Self-Care Sundays: Your Weekly Reset', 'How to make the most of your self-care day', 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800', 'Dedicate Sundays to recharging. Take a long bath, do a face mask, read a book, or simply rest. Remember: self-care isn\'t selfish, it\'s necessary.');

-- Insert Ritual Guides (using subquery for product_id)
INSERT INTO ritual_guides (category_id, step_number, step_title, product_id) VALUES
(1, 1, 'Set the Mood', (SELECT id FROM products WHERE product_id = 'PROD-001')),
(1, 2, 'Open Your Journal', (SELECT id FROM products WHERE product_id = 'PROD-002')),
(1, 3, 'Reflect and Write', NULL),
(2, 1, 'Prepare Your Space', (SELECT id FROM products WHERE product_id = 'PROD-005')),
(2, 2, 'Choose Your Essential Oil', (SELECT id FROM products WHERE product_id = 'PROD-012')),
(2, 3, 'Breathe Deeply', NULL),
(3, 1, 'Draw a Warm Bath', NULL),
(3, 2, 'Add Bath Bombs', (SELECT id FROM products WHERE product_id = 'PROD-010')),
(3, 3, 'Use Face Roller', (SELECT id FROM products WHERE product_id = 'PROD-004')),
(3, 4, 'Apply Sleep Mist', (SELECT id FROM products WHERE product_id = 'PROD-003'));

-- Note: User data, orders, reviews, etc. should be created through the application
-- This seed file focuses on product catalog and content data

