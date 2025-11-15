"""Componentes relacionados ao Factory Method e aos leitores concretos."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
import csv
import io
import json
from typing import List, Type


class LeitorArquivo(ABC):
    """Define a interface comum usada pelo Template Method."""

    def __init__(self, caminho: str | Path):
        self.caminho = Path(caminho)

    def ler(self) -> List[str]:
        conteudo = self._abrir()
        return self._interpretar(conteudo)

    def _abrir(self) -> str:
        return self.caminho.read_text(encoding="utf-8")

    @abstractmethod
    def _interpretar(self, conteudo: str) -> List[str]:
        ...


class LeitorTXT(LeitorArquivo):
    def _interpretar(self, conteudo: str) -> List[str]:
        return [linha.strip() for linha in conteudo.splitlines() if linha.strip()]


class LeitorCSV(LeitorArquivo):
    def _interpretar(self, conteudo: str) -> List[str]:
        resultado: List[str] = []
        leitor = csv.DictReader(io.StringIO(conteudo))
        if leitor.fieldnames is None:
            return resultado
        for linha in leitor:
            campos_validos = [f"{chave}={valor}" for chave, valor in linha.items() if valor]
            if campos_validos:
                resultado.append(" | ".join(campos_validos))
        return resultado


class LeitorJSON(LeitorArquivo):
    def _interpretar(self, conteudo: str) -> List[str]:
        bruto = json.loads(conteudo)
        if isinstance(bruto, list):
            return [self._serializar(item) for item in bruto]
        return [self._serializar(bruto)]

    def _serializar(self, item: object) -> str:
        if isinstance(item, str):
            return item
        return json.dumps(item, ensure_ascii=False)


class LeitorArquivoFactory:
    """Factory Method centraliza a criação dos leitores concretos."""

    _mapa: dict[str, Type[LeitorArquivo]] = {
        ".txt": LeitorTXT,
        ".csv": LeitorCSV,
        ".json": LeitorJSON,
    }

    @classmethod
    def criar(cls, caminho: str | Path) -> LeitorArquivo:
        caminho = Path(caminho)
        extensoes = [suf.lower() for suf in caminho.suffixes]
        extensao_util = extensoes[-1] if extensoes else caminho.suffix.lower()
        # arquivos comprimidos/criptografados costumam ter uma "dupla" extensão
        if extensao_util in {".gz", ".enc"} and len(extensoes) >= 2:
            extensao_util = extensoes[-2]
        leitor_cls = cls._mapa.get(extensao_util)
        if leitor_cls is None:
            raise ValueError(f"Extensão não suportada: {extensao_util}")
        return leitor_cls(caminho)
