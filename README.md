# Pipeline de Processamento de Arquivos de Texto

POWERSHELL
~~~
$datasets = @{
    "relatorio_vendas.csv" = "saida\relatorio_vendas.txt"
    "agenda_eventos.csv"   = "saida\agenda_eventos.txt"
    "feedbacks.csv"        = "saida\feedbacks.txt"
    "lista_tarefas.csv"    = "saida\lista_tarefas.txt"
    "stopwords_demo.csv"   = "saida\stopwords_demo.txt"
}
foreach ($entry in $datasets.GetEnumerator()) {
    $entrada = Join-Path "dados" $entry.Key
    $saida   = $entry.Value
    python main.py $entrada $saida --modo padrao
    Write-Host "`nPrévia de $($entry.Key):"
    Get-Content $saida | Select-Object -First 3
}
~~~



Este projeto demonstra um pipeline simples para leitura, transformação e persistência de arquivos de texto (TXT, CSV e JSON) em Python. Embora o domínio seja pequeno, ele foi planejado para mostrar, de forma explícita, como quatro padrões clássicos da GoF respondem melhor ao problema do que as demais opções do catálogo.

## Justificativa para Cada Padrão

Justificativa detalhada para cada padrão utilizado, explicando:

01. **Por que o padrão foi escolhido** — por que ele se encaixa neste contexto específico.  
02. **Qual problema ele resolve** — qual dor do código ele endereça.  
03. **Quais benefícios ele traz** — ganhos para arquitetura/manutenibilidade/escalabilidade.  
04. **Como o código seria diferente** — o que pioraria se o padrão não fosse empregado.

### Factory Method (Criacional)
- **Por que o padrão foi escolhido:** precisamos instanciar leitores diferentes de acordo com a extensão recebida em tempo de execução, e o Factory Method encapsula essa decisão em uma única classe (`LeitorArquivoFactory`).
- **Qual problema ele resolve:** elimina condicionais espalhadas pelo código para descobrir o leitor correto e centraliza a regra de mapeamento de extensões, inclusive para arquivos com dupla extensão (`.txt.gz`, `.txt.enc`).
- **Quais benefícios ele traz:** facilita adicionar novos formatos sem tocar nas partes que consomem o leitor; melhora a manutenibilidade porque há um ponto único de criação e reduz o acoplamento entre o processador e os leitores concretos.
- **Como o código seria diferente:** teríamos `if/elif` por toda parte, duplicando lógica de detecção de extensão; cada processador precisaria conhecer todos os leitores e seria mais difícil evoluir o pipeline sem risco de regressão.

### Decorator (Estrutural)
- **Por que o padrão foi escolhido:** queríamos adicionar comportamentos opcionais (cache, descompressão, descriptografia) ao leitor sem multiplicar subclasses para cada combinação possível.
- **Qual problema ele resolve:** impede que a lógica de leitura fique inflada com preocupações ortogonais; cada funcionalidade extra fica em um decorator independente que pode ser combinado dinamicamente.
- **Quais benefícios ele traz:** possibilita estender o comportamento sem modificar as classes existentes, dá flexibilidade para ativar/desativar recursos via composição, e mantém a interface do leitor consistente, o que simplifica testes e manutenção.
- **Como o código seria diferente:** precisaríamos criar subclasses do leitor para toda combinação (ex.: `LeitorCSVComCacheEDescompressao`), aumentando exponencialmente o número de classes e tornando o código rígido a mudanças.

### Chain of Responsibility (Comportamental)
- **Por que o padrão foi escolhido:** o pipeline de transformação é composto por várias etapas sequenciais que devem ser combinadas e reordenadas sem impactar umas às outras.
- **Qual problema ele resolve:** desacopla cada etapa (normalizar acentos, remover stopwords, filtrar invalidados) e permite que cada uma processe e delegue ao próximo handler de forma transparente.
- **Quais benefícios ele traz:** permite montar cadeias diferentes conforme o processador, facilita adicionar/remover etapas sem quebrar as demais, e deixa explícito o fluxo de filtros, aumentando a clareza e a capacidade de extensão.
- **Como o código seria diferente:** teríamos um método monolítico com todas as transformações em sequência, difícil de ler, testar e modificar; qualquer alteração em uma etapa exigiria alterar o bloco inteiro.

### Template Method (Comportamental)
- **Por que o padrão foi escolhido:** todo processamento compartilha o esqueleto `ler -> processar -> salvar`, mas cada variação pode customizar pontos específicos (decoradores, cadeia de etapas, formato de saída).
- **Qual problema ele resolve:** define o algoritmo geral em `ProcessadorArquivo` e garante que as subclasses só precisem sobrescrever ganchos específicos, mantendo o fluxo coerente e evitando duplicação.
- **Quais benefícios ele traz:** deixa o fluxo explícito, reduz duplicidade entre diferentes processadores, facilita criar novas variantes do pipeline e mantém a arquitetura extensível sem abrir mão da consistência.
- **Como o código seria diferente:** cada processador teria de implementar o fluxo completo manualmente, aumentando o risco de inconsistências (por exemplo, esquecer de salvar ou de aplicar a cadeia) e dificultando a evolução do pipeline.

## Benefícios combinados
- **Extensibilidade guiada:** novos formatos entram pela fábrica; novos adornos (cache, compressão) são adicionados como decorators e novas etapas de transformação entram na cadeia.
- **Baixo acoplamento:** cada padrão limita o impacto de mudanças a um ponto único, facilitando manutenção.
- **Clareza arquitetural:** o Template Method deixa explícito o fluxo macro, enquanto Factory/Decorator/Chain detalham as variações micro.

Os quatro padrões escolhidos cobrem dimensões complementares (criação, estrutura e comportamento), oferecendo o melhor equilíbrio entre simplicidade e flexibilidade para o projeto proposto.
