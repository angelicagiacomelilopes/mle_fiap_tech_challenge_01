from pydantic import BaseModel, Field
from typing import Optional

class ProcessamentoRequestDTO(BaseModel):
    ano: Optional[int] = Field(
        None,
        ge=1970,
        le=2023,
        description="Ano da processamento (entre 1970 e 2023)"
    )
    tipo: Optional[str] = Field(
        None,
        description="ID do tipo para filtrar"
    )
    subtipo: Optional[str] = Field(
        None,
        description="ID do subtipo para filtrar"
    )
    cultivar: Optional[str] = Field(
        None,
        description="ID da cultivar para filtrar"
    )