# app/dto/producao_dto.py
from pydantic import BaseModel, Field
from typing import Optional

class ProducaoRequestDTO(BaseModel):
    ano: Optional[int] = Field(
        None,
        ge=1970,
        le=2023,
        description="Ano da produção (entre 1970 e 2023)"
    )
    produto: Optional[str] = Field(
        None,
        description="ID do produto para filtrar"
    )
    categoria: Optional[str] = Field(
        None,
        description="ID da categoria para filtrar"
    )