#!/usr/bin/env python3

from faker import Faker
from app import app
from models import db, Newsletter

fake = Faker()

with app.app_context():
    print("🌱 Seeding database...")

    # Clear old data
    Newsletter.query.delete()

    # Create 50 fake newsletters
    newsletters = [
        Newsletter(
            title=fake.sentence(nb_words=4),
            body=fake.paragraph(nb_sentences=5),
        )
        for _ in range(50)
    ]

    db.session.add_all(newsletters)
    db.session.commit()

    print("✅ Seeding complete!")


