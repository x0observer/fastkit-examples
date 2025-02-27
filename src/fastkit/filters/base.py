from typing import List, Any
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import and_
from pydantic import BaseModel
from src.fastkit.utils.base import logger
from typing import ClassVar, Dict

class FilterBase(BaseModel):
    """
    Base class for applying dynamic query filters.
    """

    suffix_handlers: ClassVar[Dict[str, str]] = {
        "_ids": "handle_relation_ids",
        "_in": "handle_in",
        "_le": "handle_less_equal",
        "_ge": "handle_greater_equal",
        "_lt": "handle_less_than",
        "_gt": "handle_greater_than",
        "_ne": "handle_not_equal",
        "_like": "handle_like",
        "_ilike": "handle_ilike",
    }

    def apply_filters(self, subquery: Any) -> Any:
        """
        Applies the filters to the given subquery.
        """
        model = getattr(subquery, '_primary_entity', None)
        if not model:
            raise ValueError("Cannot determine the primary entity for filtering")
        
        conditions = []
        attrs = self.dict(exclude_unset=True)
        
        for attr, value in attrs.items():
            if value is None:
                continue
            
            suffix = next((suf for suf in self.suffix_handlers if attr.endswith(suf)), '')
            base_attr = attr[:-len(suffix)] if suffix else attr

            if not hasattr(model, base_attr) and suffix != '_ids':
                logger.warning("Attribute %s not found in model %s.", base_attr, model)
                continue

            _attribute = getattr(model, base_attr, None)
            if not isinstance(_attribute, InstrumentedAttribute):
                logger.warning("%s is not a valid column in model %s.", attr, model)
                continue

            handler_method = getattr(self, self.suffix_handlers.get(suffix, ''), None)
            condition = handler_method(model, base_attr, value) if handler_method else _attribute == value
            
            if condition is not None:
                conditions.append(condition)
        
        return subquery.where(and_(*conditions)) if conditions else subquery

    def handle_relation_ids(self, model, relation_name: str, value: List[Any]):
        """Handles filtering by related entity IDs."""
        if not hasattr(model, relation_name):
            logger.warning("Relationship %s not found in model %s.", relation_name, model)
            return None
        
        relation_attr = getattr(model, relation_name)
        if not isinstance(relation_attr, InstrumentedAttribute):
            logger.warning("%s is not a valid relationship in model %s.", relation_name, model)
            return None
        
        relation_prop = relation_attr.property
        related_model = relation_prop.mapper.class_
        related_pk = next(iter(related_model.__table__.primary_key.columns))
        
        return relation_attr.any(related_pk.in_(value)) if relation_prop.uselist else relation_attr.in_(value)

    def handle_in(self, _attribute: Any, value: List[Any]) -> Any:
        return _attribute.in_(value)

    def handle_less_equal(self, _attribute: Any, value: Any) -> Any:
        return _attribute <= value

    def handle_greater_equal(self, _attribute: Any, value: Any) -> Any:
        return _attribute >= value

    def handle_less_than(self, _attribute: Any, value: Any) -> Any:
        return _attribute < value

    def handle_greater_than(self, _attribute: Any, value: Any) -> Any:
        return _attribute > value

    def handle_not_equal(self, _attribute: Any, value: Any) -> Any:
        return _attribute != value

    def handle_like(self, _attribute: Any, value: str) -> Any:
        return _attribute.like(f"%{value}%")

    def handle_ilike(self, _attribute: Any, value: str) -> Any:
        return _attribute.ilike(f"%{value}%")