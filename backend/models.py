from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    rating = Column(Float, default=4.5)
    reviews_count = Column(Integer, default=120)
    description = Column(Text, nullable=False)
    specs = Column(String(500), nullable=False) # comma-separated specs or JSON
    image_url = Column(String(500), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "price": self.price,
            "rating": self.rating,
            "reviews_count": self.reviews_count,
            "description": self.description,
            "specs": [s.strip() for s in self.specs.split(",") if s.strip()],
            "image_url": self.image_url
        }
