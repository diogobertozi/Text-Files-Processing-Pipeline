"""Decorators que acrescentam comportamentos aos leitores."""
from __future__ import annotations

import base64
import gzip
from typing import List, Optional

from .leitores import LeitorArquivo


class LeitorDecorator(LeitorArquivo):
    """Classe base para os decorators; mantém a mesma interface do componente."""

    def __init__(self, leitor: LeitorArquivo):
        super().__init__(leitor.caminho)
        self._leitor = leitor

    def _abrir(self) -> str:
        return self._leitor._abrir()

    def _interpretar(self, conteudo: str) -> List[str]:
        return self._leitor._interpretar(conteudo)


class LeitorComCache(LeitorDecorator):
    """Evita reprocessar o arquivo ao reutilizar o mesmo leitor."""

    def __init__(self, leitor: LeitorArquivo):
        super().__init__(leitor)
        self._cache: Optional[List[str]] = None

    def ler(self) -> List[str]:
        if self._cache is None:
            self._cache = super().ler()
        return list(self._cache)


class LeitorComDescompressao(LeitorDecorator):
    """Lê arquivos comprimidos (.gz) sem alterar o restante do código."""

    def _abrir(self) -> str:
        if ".gz" in [suf.lower() for suf in self.caminho.suffixes]:
            with gzip.open(self.caminho, "rt", encoding="utf-8") as arquivo:
                return arquivo.read()
        return super()._abrir()


class LeitorComDescriptografia(LeitorDecorator):
    """Traduz conteúdos base64 (.enc) antes da interpretação."""

    def _abrir(self) -> str:
        if ".enc" in [suf.lower() for suf in self.caminho.suffixes]:
            bruto = super()._abrir()
            dados = base64.b64decode(bruto.encode("utf-8"))
            return dados.decode("utf-8")
        return super()._abrir()
