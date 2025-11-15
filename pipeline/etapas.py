"""Implementação da Chain of Responsibility para o pipeline de texto."""
from __future__ import annotations

from abc import ABC, abstractmethod
import re
import unicodedata
from typing import List, Optional


class EtapaProcessamento(ABC):
    """Cada etapa decide como tratar os dados antes de delegar para a próxima."""

    def __init__(self, proximo: Optional["EtapaProcessamento"] = None):
        self._proximo = proximo

    def executar(self, dados: List[str]) -> List[str]:
        resultado = self._processar(dados)
        if self._proximo:
            return self._proximo.executar(resultado)
        return resultado

    @abstractmethod
    def _processar(self, dados: List[str]) -> List[str]:
        ...


class NormalizaAcentosEtapa(EtapaProcessamento):
    def _processar(self, dados: List[str]) -> List[str]:
        normalizados: List[str] = []
        for linha in dados:
            texto = unicodedata.normalize("NFD", linha)
            texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
            normalizados.append(texto)
        return normalizados


class RemoveStopWordsEtapa(EtapaProcessamento):
    def __init__(self, proximo: Optional[EtapaProcessamento] = None, stopwords: Optional[List[str]] = None):
        super().__init__(proximo)
        self._stopwords = stopwords or ["de", "da", "do", "a", "o", "e"]

    def _processar(self, dados: List[str]) -> List[str]:
        padrao = re.compile(r"\\b(" + "|".join(map(re.escape, self._stopwords)) + r")\\b", re.IGNORECASE)
        return [padrao.sub("", linha).strip() for linha in dados]


class FiltraLinhasInvalidasEtapa(EtapaProcessamento):
    def _processar(self, dados: List[str]) -> List[str]:
        return [linha for linha in dados if len(linha.strip()) >= 3]


class PadronizaEspacosEtapa(EtapaProcessamento):
    def _processar(self, dados: List[str]) -> List[str]:
        return [re.sub(r"\s+", " ", linha).strip() for linha in dados]
