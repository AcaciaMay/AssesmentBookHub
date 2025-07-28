import sqlite3

# Map of Title → Image Filename (relative to static/images/)
title_to_image = {
    "1984": "1984.png",
    "At Home": "athome.jpeg",
    "Brave New World": "bravenewworld.jpeg",
    "Collapse": "collapse.jpeg",
    "Cooked": "cooked.jpeg",
    "Fahrenheit 451": "fahrenheit.jpeg",
    "Guns, Germs, and Steel": "gunsgerms&steel.jpeg",
    "How To Bee": "howtobee.jpeg",
    "Salt, Fat, Acid, Heat": "saltfatacidheat.jpg",
    "Sapiens: A Brief History of Humankind": "sapiens.png",
    "The Chocolate Cookbook": "Thechocolatecookbook.png",
    "The Chronicles of Narnia": "TheChroniclesofNarnia.jpeg",
    "The Flavor Bible": "theflavorbible.jpeg",
    "The Flower Gardener's Bible": "theflowergardenersbible.jpeg",
    "The Food Lab": "thefoodlab.jpeg",
    "The Garden Primer": "thegardenprimer.jpeg",
    "The Handmaid's Tale": "thehandmaidstale.png",
    "The Hobbit": "thehobbit.jpeg",
    "The Plantagenets": "theplantagenets.jpeg",
    "The Priory of the Orange Tree": "theprioryoftheorangetree.jpeg",
    "The Road": "theroad.jpeg",
    "Harry Potter and the Sorcerer's Stone": "thesorcerersstone.jpeg",
    "The Splendid and the Vile": "thesplendidandthevile.jpg",
    "The Vegetable Gardener's Bible": "thevegetablegardenersbible.jpeg",
    "The Wild Robot": "thewildrobot.jpeg"
}

# Connect to the correct database file
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

updated = 0
not_found = []

# Loop through each title and update the corresponding row in the Books table
for title, filename in title_to_image.items():
    image_path = f"images/{filename}"
    cursor.execute("""
        UPDATE Books
        SET "Image URL" = ?
        WHERE Title = ?
    """, (image_path, title))
    if cursor.rowcount == 0:
        not_found.append(title)
    else:
        updated += cursor.rowcount

# Commit and close
conn.commit()
conn.close()

# Output results
print(f"✅ Updated {updated} row(s) in 'Books' table.")
if not_found:
    print("\n⚠️ These titles were not found in the database:")
    for title in not_found:
        print(f" - {title}")
