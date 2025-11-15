"""Template Method responsável por orquestrar o pipeline de processamento."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from .decorators import LeitorComCache, LeitorComDescompressao, LeitorComDescriptografia
from .etapas import (
    EtapaProcessamento,
    FiltraLinhasInvalidasEtapa,
    NormalizaAcentosEtapa,
    PadronizaEspacosEtapa,
    RemoveStopWordsEtapa,
)
from .leitores import LeitorArquivo, LeitorArquivoFactory


class ProcessadorArquivo(ABC):
    """Define o algoritmo geral `ler -> transformar -> salvar`."""

    def __init__(self, caminho_entrada: str | Path, caminho_saida: str | Path):
        self.caminho_entrada = Path(caminho_entrada)
        self.caminho_saida = Path(caminho_saida)

    def executar(self) -> List[str]:
        leitor = self._decorar_leitor(self._criar_leitor())
        dados = self._ler(leitor)
        dados_transformados = self._processar(dados)
        self._salvar(dados_transformados)
        return dados_transformados

    def _ler(self, leitor: LeitorArquivo) -> List[str]:
        return leitor.ler()

    def _processar(self, dados: List[str]) -> List[str]:
        cadeia = self._montar_cadeia()
        if cadeia is None:
            return dados
        return cadeia.executar(dados)

    def _salvar(self, dados: List[str]) -> None:
        texto = "\n".join(dados)
        self.caminho_saida.parent.mkdir(parents=True, exist_ok=True)
        self.caminho_saida.write_text(texto, encoding="utf-8")

    @abstractmethod
    def _criar_leitor(self) -> LeitorArquivo:
        ...

    def _decorar_leitor(self, leitor: LeitorArquivo) -> LeitorArquivo:
        return leitor

    def _montar_cadeia(self) -> Optional[EtapaProcessamento]:
        return None


class ProcessadorTextoPadrao(ProcessadorArquivo):
    """Configuração padrão com todos os comportamentos extras ligados."""

    def __init__(self, caminho_entrada: str | Path, caminho_saida: str | Path, usar_cache: bool = True):
        super().__init__(caminho_entrada, caminho_saida)
        self.usar_cache = usar_cache

    def _criar_leitor(self) -> LeitorArquivo:
        return LeitorArquivoFactory.criar(self.caminho_entrada)

    def _decorar_leitor(self, leitor: LeitorArquivo) -> LeitorArquivo:
        decorado: LeitorArquivo = LeitorComDescompressao(leitor)
        decorado = LeitorComDescriptografia(decorado)
        if self.usar_cache:
            decorado = LeitorComCache(decorado)
        return decorado

    def _montar_cadeia(self) -> Optional[EtapaProcessamento]:
        return PadronizaEspacosEtapa(
            NormalizaAcentosEtapa(
                RemoveStopWordsEtapa(
                    FiltraLinhasInvalidasEtapa()
                )
            )
        )


class ProcessadorTextoSuave(ProcessadorArquivo):
    """Variação que mostra a flexibilidade do Template Method."""

    def _criar_leitor(self) -> LeitorArquivo:
        return LeitorArquivoFactory.criar(self.caminho_entrada)

    def _decorar_leitor(self, leitor: LeitorArquivo) -> LeitorArquivo:
        # Apenas descompressão automática nesta variação mais simples
        return LeitorComDescompressao(leitor)

    def _montar_cadeia(self) -> Optional[EtapaProcessamento]:
        return PadronizaEspacosEtapa()

    def _salvar(self, dados: List[str]) -> None:
        # Sobrescreve para registrar contagem de linhas junto ao resultado
        texto = "\n".join(dados)
        resumo = f"linhas_processadas={len(dados)}\n{texto}" if dados else "linhas_processadas=0"
        self.caminho_saida.parent.mkdir(parents=True, exist_ok=True)
        self.caminho_saida.write_text(resumo, encoding="utf-8")
