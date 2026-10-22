from models import Product

INITIAL_PRODUCTS = [
    {
        "title": "Pixel 7a Smartphone",
        "category": "Smartphones",
        "price": 449.00,
        "rating": 4.6,
        "reviews_count": 890,
        "description": "High performance Google Tensor G2 phone with 64MP flagship-level camera, vibrant 90Hz OLED display, and all-day battery.",
        "specs": "6.1-inch OLED, 128GB Storage, 8GB RAM, 64MP Dual Camera, 5G Ready",
        "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop&q=80"
    },
    {
        "title": "Samsung Galaxy A54 5G",
        "category": "Smartphones",
        "price": 375.00,
        "rating": 4.5,
        "reviews_count": 1420,
        "description": "Crisp 120Hz Super AMOLED display, durable water resistance IP67, and 5000mAh battery that easily lasts up to two days.",
        "specs": "6.4-inch AMOLED, 128GB Storage, 5000mAh Battery, Triple Camera, Under $400",
        "image_url": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=600&auto=format&fit=crop&q=80"
    },
    {
        "title": "iPhone SE (3rd Gen)",
        "category": "Smartphones",
        "price": 429.00,
        "rating": 4.4,
        "reviews_count": 780,
        "description": "Blazing fast A15 Bionic chip in an ultra-compact pocket-friendly design with durable glass and classic Touch ID.",
        "specs": "4.7-inch Retina Display, A15 Bionic, 64GB Storage, 5G, Apple iOS",
        "image_url": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=600&auto=format&fit=crop&q=80"
    },
    {
        "title": "Sony WH-1000XM4 Noise Canceling Headphones",
        "category": "Audio",
        "price": 278.00,
        "rating": 4.8,
        "reviews_count": 3210,
        "description": "Industry-leading digital noise cancellation with Dual Noise Sensor technology, exceptional 30-hour battery life, and Speak-to-chat.",
        "specs": "Active Noise Canceling, 30-Hour Battery, Multipoint Bluetooth, Touch Controls",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80"
    },
    {
        "title": "Anker Soundcore Space Q45",
        "category": "Audio",
        "price": 99.99,
        "rating": 4.5,
        "reviews_count": 950,
        "description": "Adaptive noise cancelling reducing noise by up to 98%, ultra-long 65-hour playtime, and high-resolution wireless audio.",
        "specs": "Hybrid ANC, 65-Hour Playtime, LDAC Hi-Res, Ultra-lightweight, Under $100",
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&auto=format&fit=crop&q=80"
    },
    {
        "title": "Acer Swift Go 14 Laptop",
        "category": "Laptops",
        "price": 649.00,
        "rating": 4.6,
        "reviews_count": 420,
        "description": "Slim, lightweight aluminum laptop powered by Intel Core i7 with a stunning 2.8K OLED screen and fast Wi-Fi 6E.",
        "specs": "Intel Core i7, 16GB RAM, 512GB SSD, 14-inch 2.8K OLED, 2.9 lbs",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=80"
    },
    {
        "title": "Lenovo IdeaPad Slim 3",
        "category": "Laptops",
        "price": 439.00,
        "rating": 4.3,
        "reviews_count": 610,
        "description": "Dependable daily driver for students and office work featuring AMD Ryzen 5 processor, crisp 1080p anti-glare screen, and fast charging.",
        "specs": "AMD Ryzen 5, 8GB RAM, 512GB SSD, 15.6-inch FHD, Under $500",
        "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600&auto=format&fit=crop&q=80"
    },
    {
        "title": "Logitech MX Master 3S Ergonomic Mouse",
        "category": "Accessories",
        "price": 99.99,
        "rating": 4.9,
        "reviews_count": 4890,
        "description": "Quiet clicks and 8K DPI any-surface tracking with electromagnetic MagSpeed scrolling wheel for maximum productivity and comfort.",
        "specs": "Ergonomic Hand Grip, 8000 DPI Sensor, USB-C Quick Charge, Multi-Device Flow",
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&auto=format&fit=crop&q=80"
    },
    {
        "title": "Keychron K2 Wireless Mechanical Keyboard",
        "category": "Accessories",
        "price": 79.99,
        "rating": 4.7,
        "reviews_count": 1820,
        "description": "Compact 75% layout mechanical keyboard with hot-swappable Gateron switches, Mac & Windows compatibility, and white LED backlighting.",
        "specs": "75% Layout, Wireless Bluetooth 5.1, Gateron Brown Switches, Mac/Win support",
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80"
    },
    {
        "title": "Dell 27-inch 4K UHD USB-C Monitor (S2722QC)",
        "category": "Accessories",
        "price": 329.99,
        "rating": 4.7,
        "reviews_count": 1150,
        "description": "Stunning 4K clarity with USB-C single cable connectivity providing 65W power delivery, integrated speakers, and an adjustable stand.",
        "specs": "27-inch 4K UHD (3840x2160), IPS Panel, USB-C 65W PD, Height Adjustable",
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&auto=format&fit=crop&q=80"
    },
    {
        "title": "Garmin Venu Sq 2 Smartwatch",
        "category": "Wearables",
        "price": 249.99,
        "rating": 4.5,
        "reviews_count": 670,
        "description": "Vibrant AMOLED touchscreen with up to 11 days of battery life, continuous heart rate, sleep scoring, and 25+ preloaded GPS sports apps.",
        "specs": "AMOLED Display, 11-Day Battery, GPS Fitness Tracking, 5ATM Water Resistant",
        "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&auto=format&fit=crop&q=80"
    },
    {
        "title": "Apple Watch SE (2nd Gen)",
        "category": "Wearables",
        "price": 239.00,
        "rating": 4.8,
        "reviews_count": 2900,
        "description": "Essential safety and fitness features, crash detection, workout tracking, heart health alerts, and seamless integration with iPhone.",
        "specs": "Retina Display, Crash Detection, 50m Swimproof, Heart Rate Monitor, watchOS",
        "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&auto=format&fit=crop&q=80"
    }
]

def seed_database(db):
    count = db.query(Product).count()
    if count == 0:
        for p in INITIAL_PRODUCTS:
            db_product = Product(
                title=p["title"],
                category=p["category"],
                price=p["price"],
                rating=p["rating"],
                reviews_count=p["reviews_count"],
                description=p["description"],
                specs=p["specs"],
                image_url=p["image_url"]
            )
            db.add(db_product)
        db.commit()
