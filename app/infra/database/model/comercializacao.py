from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ProcessamentoModel(Base):
    """Modelo para a tabela de comercializacao de uva."""
    __tablename__ = "comercializacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    control = Column(String(300), nullable=False)
    cultivar = Column(String(300), nullable=False)
    ano = Column(Integer)
    valor = Column(Float)
    data_acesso = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Processamento {self.control}>"