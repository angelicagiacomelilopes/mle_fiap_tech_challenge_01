from pydantic import BaseModel, Field
from typing import Optional

class ExportacaoRequestDTO(BaseModel):
    ano: Optional[int] = Field(
        None,
        ge=1970,
        le=2023,
        description="Ano da exportacao (entre 1970 e 2023)"
    )
    tipo: Optional[str] = Field(
        None,
        description="ID do tipo para filtrar"
    )
    pais: Optional[str] = Field(
        None,
        description="ID do pais para filtrar"
    ) 