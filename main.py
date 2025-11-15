from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.processador import ProcessadorTextoPadrao, ProcessadorTextoSuave


def _construir_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Pipeline de leitura e transformação de arquivos usando "
            "Factory Method, Decorator, Chain of Responsibility e Template Method"
        )
    )
    parser.add_argument("entrada", help="Arquivo de entrada (txt, csv, json, gz ou enc)")
    parser.add_argument("saida", help="Arquivo onde o resultado será persistido")
    parser.add_argument(
        "--modo",
        choices=["padrao", "suave"],
        default="padrao",
        help="Escolhe qual variação do Template Method executar",
    )
    parser.add_argument(
        "--sem-cache",
        action="store_true",
        help="Desabilita o decorator de cache no modo padrão",
    )
    return parser.parse_args()


def main() -> None:
    args = _construir_argumentos()
    caminho_entrada = Path(args.entrada)
    caminho_saida = Path(args.saida)

    if args.modo == "padrao":
        processador = ProcessadorTextoPadrao(
            caminho_entrada,
            caminho_saida,
            usar_cache=not args.sem_cache,
        )
    else:
        processador = ProcessadorTextoSuave(caminho_entrada, caminho_saida)

    linhas = processador.executar()
    print(f"Processamento finalizado: {len(linhas)} linhas geradas em {caminho_saida}")


if __name__ == "__main__":
    main()
