import os
import random
import pandas as pd

# Define paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
STATIC_IMG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "static",
    "images",
    "products"
)

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STATIC_IMG_DIR, exist_ok=True)

# 1. Product Templates per Category
PRODUCT_TEMPLATES = {
    "Electronics": [
        ("iPhone 15 Pro", "Apple", "Flagship titanium smartphone with advanced camera system, high refresh rate OLED display, and high-performance A17 Pro chip."),
        ("Galaxy S24 Ultra", "Samsung", "Premium Android smartphone with integrated S-Pen stylus, 200MP quad camera, AI translation features, and bright AMOLED screen."),
        ("WH-1000XM5 Headphones", "Sony", "Industry-leading active noise-canceling wireless headphones with 30-hour battery life, smart listening, and high-fidelity sound."),
        ("QuietComfort Ultra", "Bose", "Over-ear noise-canceling headphones with spatial audio, customtune calibration, and ultra-comfortable ear cushions."),
        ("XPS 15 Laptop", "Dell", "High-performance laptop featuring InfinityEdge display, NVIDIA GeForce RTX graphics, and premium CNC aluminum design."),
        ("MacBook Air M3", "Apple", "Thinnest and lightest laptop with powerful M3 processor, liquid retina display, silent fanless design, and all-day battery life."),
        ("MX Master 3S Mouse", "Logitech", "Ergonomic wireless mouse with ultra-fast scrolling, 8K DPI tracking, silent clicks, and customizable macro buttons."),
        ("Charge 5 Speaker", "JBL", "Portable waterproof Bluetooth speaker with deep bass, powerbank function, and up to 20 hours of playtime."),
        ("Quest 3 VR Headset", "Meta", "Mixed reality virtual reality headset with dual display resolution, slim profile, and full-color passthrough capabilities."),
        ("4K Ultra Short Throw Projector", "Sony", "Premium home theater laser projector with 4K resolution, HDR support, and ultra-short throw screen scaling."),
        ("Pro Mechanical Keyboard", "Logitech", "Tenkeyless mechanical gaming keyboard with customizable RGB backlighting and tactile brown switches."),
        ("Smart Watch Series 9", "Apple", "Smartwatch with carbon neutral case, double tap gesture control, blood oxygen tracking, and ECG heart rate monitoring."),
        ("Noise-Canceling Earbuds", "Sony", "Truly wireless noise-canceling earbuds with high-resolution audio, crystal-clear call quality, and IPX4 water resistance."),
        ("Portable SSD 2TB", "Samsung", "Ultra-fast external solid-state drive with up to 1050MB/s transfer speeds, rugged rubberized protection, and USB-C connectivity."),
        ("4K Web Camera", "Logitech", "High-definition webcam with auto-light correction, dual noise-reducing microphones, and wide-angle view for streaming."),
        ("Smart Thermostat", "Google", "Eco-friendly programmable thermostat that learns your schedule, controls heating/cooling remotely, and saves energy."),
        ("Smart Home Assistant Hub", "Amazon", "Voice-controlled smart display with Alexa, premium speakers, video calling camera, and smart home hub integration."),
        ("OLED 55-inch 4K TV", "LG", "Self-lit OLED pixels 4K television with Dolby Vision, high refresh rate for gaming, and smart TV streaming app suite."),
        ("Noise-Canceling Wireless Earbuds", "Bose", "Comfortable noise-canceling earbuds with custom audio tuning, secure fit, and quick touch control swipe interface."),
        ("Pro Streamer Microphone", "Blue Yeti", "USB condenser microphone for recording, streaming, podcasting, and gaming with multi-pattern controls.")
    ],
    "Fashion": [
        ("Air Max Running Shoes", "Nike", "Classic athletic sneakers with visible air cushioning, breathable mesh upper, and durable rubber traction outsole."),
        ("Ultraboost Sports Shoes", "Adidas", "High-performance running shoes with responsive boost midsole cushioning and Primeknit flexible upper wrap."),
        ("Classic Suede Sneakers", "Puma", "Iconic streetwear sneakers featuring retro suede upper, comfortable padded collar, and vintage rubber sole."),
        ("Slim Fit Leather Jacket", "Zara", "Modern asymmetrical zipper biker jacket made of premium faux leather, zip pockets, and comfortable lining."),
        ("Heavyweight Oversized Hoodie", "H&M", "Casual streetwear hoodie made of soft brushed cotton-poly fleece, featuring drop shoulders and kangaroo pocket."),
        ("501 Original Fit Jeans", "Levi's", "The original blue denim straight-leg jeans with classic button fly, 5-pocket styling, and copper rivet reinforcement."),
        ("Compression Workout Shirt", "Under Armour", "HeatGear athletic top that wicks sweat, dries fast, and offers 4-way stretch compression fit for workouts."),
        ("Polarized Aviator Sunglasses", "Ray-Ban", "Timeless sunglasses with gold metal frame, polarization to reduce glare, and full UV protection lenses."),
        ("Water-Resistant Windbreaker", "Columbia", "Lightweight packable hooded jacket with zippered hand pockets and drawcord adjustable hem for outdoor hikes."),
        ("Stainless Steel Chronograph Watch", "Fossil", "Sophisticated analog wrist watch featuring black dial, chronograph sub-dials, and durable metal link band."),
        ("Classic Trench Coat", "Zara", "Double-breasted long jacket with belt, lapel collar, storm flaps, and premium water-repellent cotton blend."),
        ("Dry-Fit Training Shorts", "Nike", "Breathable athletic shorts with moisture-wicking technology, elastic waistband, and side pockets for workout convenience."),
        ("Organic Cotton T-Shirt Pack", "H&M", "Pack of three soft organic cotton crewneck tee shirts, pre-shrunk for comfortable everyday casual wear."),
        ("Casual Denim Jacket", "Levi's", "Traditional button-up jean jacket with chest flap pockets, waist adjusters, and durable cotton weave."),
        ("Running Comfort Socks Pack", "Adidas", "Six pairs of moisture-wicking athletic crew socks with arch compression support and cushioned sole padding."),
        ("Leather Bi-Fold Wallet", "Fossil", "Genuine leather slim wallet with RFID blocking technology, multiple card slots, and transparent ID window."),
        ("Yoga Leggings High-Waisted", "Lululemon", "Buttery-soft weightless leggings with four-way stretch, sweat-wicking properties, and hidden waistband pocket."),
        ("Winter Down Parka Jacket", "Columbia", "Heavy-duty insulated winter coat with faux-fur lined hood, water-resistant shell, and thermal reflective lining."),
        ("Canvas Backpack Travel Bag", "Herschel", "Classic design school and travel backpack with signature striped fabric liner and padded laptop sleeve compartment."),
        ("Leather Chelsea Boots", "Clarks", "Timeless slip-on ankle boots crafted from rich premium leather, with elastic side panels and cushioned footbed.")
    ],
    "Home & Kitchen": [
        ("Single Serve Coffee Maker", "Keurig", "Compact coffee brewer compatible with K-Cup pods, customizable brew sizes, and quick heating reservoir."),
        ("Duo 7-in-1 Instant Pot", "Instant Pot", "Multi-functional pressure cooker, slow cooker, rice cooker, steamer, sauté pan, yogurt maker, and food warmer."),
        ("V15 Detect Vacuum Cleaner", "Dyson", "Cordless stick vacuum cleaner with laser dust illumination, intelligent suction optimization, and LCD screen status."),
        ("Air Fryer Max XL", "Ninja", "High-capacity air fryer that cooks crispy meals using up to 75% less fat than traditional deep frying methods."),
        ("Artisan Series Stand Mixer", "KitchenAid", "Tilt-head stand mixer with 5-quart stainless steel bowl, 10 speeds, and flat beater, dough hook, and wire whip accessories."),
        ("Premium 12-Piece Cookware Set", "Cuisinart", "Professional stainless steel pots and pans set with aluminum encapsulated bases for rapid, even heating."),
        ("Sonicare ProtectiveClean Toothbrush", "Philips", "Electric rechargeable toothbrush with pressure sensor, smart brush head replacement reminder, and travel case."),
        ("Smart Air Purifier HEPA", "Levoit", "True HEPA filtration system air purifier with air quality sensors, sleep mode, and smart app scheduling."),
        ("Centrifugal Juicer Extractor", "Breville", "High-speed juice extractor with wide feed chute, titanium reinforced disc, and micro-mesh filter basket."),
        ("High-Speed Blender System", "Vitamix", "Professional-grade blender with variable speed control, pulse feature, and aircraft-grade hardened stainless steel blades."),
        ("Non-Stick Electric Griddle", "Cuisinart", "Large family-sized cooking griddle with adjustable temperature dial and removable grease drip tray."),
        ("Digital Kitchen Scale", "Ozeri", "Precision scale for cooking and baking, measuring in grams, ounces, milliliters, and pounds with high-accuracy sensors."),
        ("Memory Foam Pillows Twin Pack", "Coop Home Goods", "Adjustable loft shredded memory foam pillows with breathable bamboo-derived rayon cover for sleepers."),
        ("French Press Coffee Maker", "Bodum", "Stainless steel and heat-resistant borosilicate glass press with 3-part mesh filter for full-bodied coffee extraction."),
        ("14-Piece Knife Block Set", "Henckels", "High-quality forged stainless steel kitchen knives in hardwood storage block, professional edge retention."),
        ("Automatic Bread Maker Machine", "Cuisinart", "Programmable bread maker with 12 menu options, crust control, delay start, and automatic fruit/nut dispenser."),
        ("Electric Gooseneck Kettle", "Fellow Stagg", "Precision pour-over kettle with temperature control, stopwatch, and counterbalanced handle for barista-level brewing."),
        ("Slow Cooker 6-Quart Oval", "Crock-Pot", "Manual slow cooker with high, low, and warm settings, removable stoneware pot, and dishwasher safe glass lid."),
        ("Multi-Layer Shoe Rack Organizer", "Simple Houseware", "Sturdy free-standing shoe storage shelving unit, accommodating up to 20 pairs of shoes."),
        ("Bamboo Cutting Board Set", "Royal Craft Wood", "Three organic bamboo serving and chopping boards with juice grooves, knife-friendly surface.")
    ],
    "Fitness & Outdoors": [
        ("Charge 6 Fitness Tracker", "Fitbit", "Activity and heart rate tracker with built-in GPS, YouTube Music controls, Google Maps integration, and battery up to 7 days."),
        ("Fenix 7 Solar GPS Watch", "Garmin", "Rugged multisport smartwatch with solar charging lens, advanced performance metrics, and preloaded topo maps."),
        ("Rambler 20 oz Tumbler", "Yeti", "Double-wall vacuum insulated stainless steel travel mug with MagSlider lid to keep drinks hot or cold."),
        ("Wide Mouth Water Bottle 32 oz", "Hydro Flask", "Stainless steel insulated water bottle with leakproof flex cap and durable powder coat finish in vibrant colors."),
        ("Adjustable Dumbbells Set", "Bowflex", "Space-saving selectable weight dumbbells adjusting from 5 to 52.5 lbs, replacing 15 separate weight sets."),
        ("All-in-One Suspension Trainer", "TRX", "Bodyweight resistance workout system for home and travel, includes door anchor and suspension straps."),
        ("Premium Yoga Mat 1/4 Inch", "Gaiam", "Thick non-slip exercise mat with alignment guide lines, textured grip surface, and carrying strap included."),
        ("Ultra-Lightweight Camping Hammock", "Eno", "Double camping hammock made of durable breathable nylon parachute material, packing down to the size of a grapefruit."),
        ("4-Person Waterproof Camping Tent", "Coleman", "Instant setup dome tent with rainfly, weathered welded corners, and inverted seams to keep rain water out."),
        ("Adjustable Kettlebell 20-40 lbs", "Bowflex", "Space-efficient select-weight kettlebell replacing 6 different weights, ergonomic handle design."),
        ("Deep Tissue Massage Gun", "Theragun", "Professional-grade percussive therapy device with brushless motor, customizable speed ranges, and quiet force technology."),
        ("Folding Electric Bike 250W", "Rad Power", "Compact commuter e-bike with pedal assist, throttle, folding aluminum frame, and up to 45 miles range per charge."),
        ("Resistance Bands Loop Set", "Fit Simplify", "Five heavy-duty natural latex resistance loops for physical therapy, strength training, and warmups."),
        ("Hydration Backpack 2L Water bladder", "CamelBak", "Outdoor athletic backpack with integrated leakproof reservoir, breathable mesh straps, and storage pockets."),
        ("Portable Camping Stove", "Camp Chef", "High-output dual burner propane gas stove with wind guards and matchless ignition for outdoor cooking."),
        ("Ergonomic Hiking Backpack 65L", "Osprey", "Heavy-load trekking backpack with adjustable anti-gravity suspension system, rain cover, and trekking pole attachments."),
        ("Polarized Floating Sport Sunglasses", "Oakley", "Wrap-around sports sunglasses with lightweight floating frames, impact resistance, and glare-reduction lenses."),
        ("Speed Jump Rope Steel Cable", "Rogue Fitness", "Coated cable jump rope with ball-bearing handles for smooth rotation, perfect for conditioning and cardio."),
        ("Collapsible Trekking Poles Pack", "Black Diamond", "Strong lightweight carbon fiber walking sticks with cork handles, shock absorbing springs, and interchangeable tips."),
        ("Outdoor Inflatable Stand Up Paddleboard", "Retrospec", "Durable military-grade PVC paddleboard package with 3-piece aluminum paddle, hand pump, fin, and carry bag.")
    ]
}

# 2. Function to generate Category-based SVGs
def generate_product_svg(product_id, name, category, filepath):
    # Determine gradients and icons based on category (Light Theme Palette)
    if category == "Electronics":
        color1, color2 = "#E0F2FE", "#bae6fd"  # Soft sky blue
        emoji = "⚡"
        label = "ELEC"
    elif category == "Fashion":
        color1, color2 = "#FCE7F3", "#fbcfe8"  # Soft pink
        emoji = "👕"
        label = "STYLE"
    elif category == "Home & Kitchen":
        color1, color2 = "#FEF3C7", "#fde68a"  # Soft amber
        emoji = "🍳"
        label = "HOME"
    else:  # Fitness & Outdoors
        color1, color2 = "#D1FAE5", "#a7f3d0"  # Soft mint
        emoji = "💪"
        label = "FIT"

    # SVG String
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="grad_{product_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <rect width="400" height="300" rx="20" fill="url(#grad_{product_id})" />
  
  <!-- Graphic Elements -->
  <circle cx="200" cy="110" r="55" fill="white" opacity="0.4" />
  <circle cx="200" cy="110" r="40" fill="white" opacity="0.3" />
  
  <text x="50%" y="130" font-family="'Segoe UI', Roboto, Helvetica, sans-serif" font-size="56" text-anchor="middle">{emoji}</text>
  
  <!-- Text Overlays -->
  <text x="50%" y="200" font-family="'Segoe UI', Roboto, Helvetica, sans-serif" font-size="18" font-weight="700" fill="#0f172a" text-anchor="middle">{name}</text>
  <text x="50%" y="230" font-family="'Segoe UI', Roboto, Helvetica, sans-serif" font-size="12" font-weight="600" fill="#475569" letter-spacing="1.5" text-anchor="middle">{label} | {category.upper()}</text>
  <text x="50%" y="258" font-family="'Segoe UI', Roboto, Helvetica, sans-serif" font-size="11" font-weight="400" fill="#64748b" text-anchor="middle">Premium Quality Assured</text>
</svg>"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)

def generate_placeholder_svg(filepath):
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="placeholder_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f1f5f9;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#e2e8f0;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <rect width="400" height="300" rx="20" fill="url(#placeholder_grad)" />
  <circle cx="200" cy="110" r="50" fill="white" opacity="0.5" />
  
  <text x="50%" y="130" font-family="'Segoe UI', Roboto, Helvetica, sans-serif" font-size="52" text-anchor="middle">📦</text>
  
  <text x="50%" y="200" font-family="'Segoe UI', Roboto, Helvetica, sans-serif" font-size="18" font-weight="700" fill="#475569" text-anchor="middle">No Image Available</text>
  <text x="50%" y="230" font-family="'Segoe UI', Roboto, Helvetica, sans-serif" font-size="12" font-weight="500" fill="#64748b" text-anchor="middle">Aurora Store Catalog</text>
</svg>"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)

def generate_datasets():
    print("Generating products dataset...")
    products = []
    prod_id_counter = 1
    
    for category, templates in PRODUCT_TEMPLATES.items():
        for name, brand, desc in templates:
            prod_id = f"P{prod_id_counter:03d}"
            # Random rating from 3.8 to 4.9
            rating = round(random.uniform(3.8, 4.9), 1)
            # Random price from 10 to 2000 USD converted to INR (1 USD = 83 INR)
            if category == "Electronics":
                price = int(round(random.uniform(50, 1500) * 83, -2))  # Rounded to nearest 100
            elif category == "Fashion":
                price = int(round(random.uniform(15, 250) * 83, -1))   # Rounded to nearest 10
            elif category == "Home & Kitchen":
                price = int(round(random.uniform(20, 600) * 83, -1))   # Rounded to nearest 10
            else: # Fitness & Outdoors
                price = int(round(random.uniform(10, 800) * 83, -1))   # Rounded to nearest 10
                
            # Map category to the generated commercial product photograph
            if category == "Electronics":
                img_path = "static/images/products/electronics_cat.jpg"
            elif category == "Fashion":
                img_path = "static/images/products/fashion_cat.jpg"
            elif category == "Home & Kitchen":
                img_path = "static/images/products/kitchen_cat.jpg"
            else: # Fitness & Outdoors
                img_path = "static/images/products/fitness_cat.jpg"
            
            products.append({
                "Product ID": prod_id,
                "Product Name": name,
                "Brand": brand,
                "Category": category,
                "Description": desc,
                "Price": price,
                "Rating": rating,
                "Image Path": img_path
            })
            prod_id_counter += 1
            
    df_products = pd.DataFrame(products)
    products_csv_path = os.path.join(DATA_DIR, "products.csv")
    df_products.to_csv(products_csv_path, index=False)
    print(f"Products saved to {products_csv_path}. Count: {len(df_products)}")
    
    # 2. Generate User Profiles
    print("Generating users dataset...")
    genders = ["Male", "Female", "Non-Binary"]
    locations = ["New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ", 
                 "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA",
                 "Austin, TX", "Seattle, WA", "Boston, MA", "Denver, CO", "San Francisco, CA"]
    
    users = []
    for uid in range(1, 151):
        age = random.randint(18, 65)
        gender = random.choices(genders, weights=[47, 47, 6], k=1)[0]
        location = random.choice(locations)
        users.append({
            "User ID": uid,
            "Age": age,
            "Gender": gender,
            "Location": location
        })
        
    df_users = pd.DataFrame(users)
    users_csv_path = os.path.join(DATA_DIR, "users.csv")
    df_users.to_csv(users_csv_path, index=False)
    print(f"Users saved to {users_csv_path}. Count: {len(df_users)}")
    
    # 3. Generate User Ratings with Preferences to facilitate SVD structure
    print("Generating ratings dataset...")
    ratings = []
    
    # Define preference groups for users
    # Group 1 (Users 1-40): Love Electronics, dislike Fashion (give low ratings or don't purchase)
    # Group 2 (Users 41-80): Love Fashion, dislike Kitchen
    # Group 3 (Users 81-120): Love Home & Kitchen, dislike Fitness
    # Group 4 (Users 121-150): Love Fitness & Outdoors, dislike Electronics
    
    product_categories = df_products["Category"].unique()
    prod_by_cat = {cat: df_products[df_products["Category"] == cat]["Product ID"].tolist() for cat in product_categories}
    
    for user in users:
        uid = user["User ID"]
        
        # Decide category preferences based on user ID groups
        if uid <= 40:
            loved_cat, disliked_cat = "Electronics", "Fashion"
        elif uid <= 80:
            loved_cat, disliked_cat = "Fashion", "Home & Kitchen"
        elif uid <= 120:
            loved_cat, disliked_cat = "Home & Kitchen", "Fitness & Outdoors"
        else:
            loved_cat, disliked_cat = "Fitness & Outdoors", "Electronics"
            
        # Neutral categories
        neutral_cats = [cat for cat in product_categories if cat not in [loved_cat, disliked_cat]]
        
        # Determine how many ratings this user will submit (between 15 and 35 ratings per user)
        num_ratings = random.randint(15, 35)
        rated_products = set()
        
        for _ in range(num_ratings):
            # Select which category to rate
            cat_choice = random.choices(
                [loved_cat, neutral_cats[0], neutral_cats[1], disliked_cat],
                weights=[0.55, 0.20, 0.20, 0.05], # skewed distribution representing tastes
                k=1
            )[0]
            
            # Select random product in this category
            pid = random.choice(prod_by_cat[cat_choice])
            
            if pid in rated_products:
                continue
            rated_products.add(pid)
            
            # Determine rating value based on user preference
            if cat_choice == loved_cat:
                rating = random.choices([4, 5, 3], weights=[0.50, 0.40, 0.10], k=1)[0]
            elif cat_choice == disliked_cat:
                rating = random.choices([1, 2, 3], weights=[0.45, 0.40, 0.15], k=1)[0]
            else:
                rating = random.choices([3, 4, 5, 2], weights=[0.40, 0.35, 0.15, 0.10], k=1)[0]
                
            ratings.append({
                "User ID": uid,
                "Product ID": pid,
                "Rating": rating
            })
            
    df_ratings = pd.DataFrame(ratings)
    ratings_csv_path = os.path.join(DATA_DIR, "ratings.csv")
    df_ratings.to_csv(ratings_csv_path, index=False)
    # Generate fallback placeholder image
    generate_placeholder_svg(os.path.join(STATIC_IMG_DIR, "placeholder.svg"))
    print("Dataset generation complete!")

if __name__ == "__main__":
    generate_datasets()
