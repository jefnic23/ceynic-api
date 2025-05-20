from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.order import Order
from src.models.order_product import OrderProduct
from src.schemas.order_update import OrderUpdate


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def get_all(self, storefront_id: int) -> list[Order]:
        statement = select(Order).where(Order.storefront_id == storefront_id).order_by(Order.create_time.desc())
        results = await self._session.exec(statement=statement)
        return results.all()

    async def get(self, storefront_id: int, order_id: str) -> Order | None:
        statement = select(Order).where(Order.storefront_id == storefront_id).where(Order.id == order_id)
        results = await self._session.exec(statement=statement)
        return results.one_or_none()

    async def create(
        self, 
        order_id: str,
        create_time: datetime,
        storefront_id: int,
        authorization_id: str,
        status: str,
        product_ids: list[int]
    ) -> Order:
        order_products = [OrderProduct(product_id=product_id) for product_id in product_ids]
        order = Order(
            id=order_id, 
            create_time=create_time,
            storefront_id=storefront_id,
            authorization_id=authorization_id,
            status=status,
            products=order_products
        )

        self._session.add(order)
        await self._session.commit()
        await self._session.refresh(order)
        return order
    
    async def update(self, storefront_id: int, order_id: str, updates: OrderUpdate) -> Order | None:
        order = await self.get(storefront_id=storefront_id, order_id=order_id)
        if not order:
            return
        
        update_data = updates.model_dump(exclude_unset=True)
        if not update_data:
            return
        
        for key, value in update_data.items():
            setattr(order, key, value)

        await self._session.commit()
        await self._session.refresh(order)

        return order
