from collections.abc import Generator
from decimal import Decimal
 
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
 
from product.db.base import Base
from product.db.session import get_db
from product.main import app
from product.models.category import Category
from product.models.product import Product
 
 
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
 
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False,
)
 
 
@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
 
    db = TestingSessionLocal()
 
    try:
        yield db
    finally:
        db.close()
 
 
@pytest.fixture()
def client(
    db_session: Session,
) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session
 
    app.dependency_overrides[get_db] = override_get_db
 
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
 
 
@pytest.fixture()
def sample_catalog(
    db_session: Session,
) -> tuple[Category, Product]:
    category = Category(CategoryName="Electronics")
 
    db_session.add(category)
    db_session.flush()
 
    product = Product(
        ProductName="Laptop",
        Description="Test laptop",
        CategoryID=category.CategoryID,
        Price=Decimal("999.99"),
        AvailableQuantity=10,
        ProductUrl=None,
    )
 
    db_session.add(product)
    db_session.commit()
    db_session.refresh(category)
    db_session.refresh(product)
 
    return category, product
 
 