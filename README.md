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

## Por que Estes 4 Padrões?

Dentre os 23 padrões GoF, selecionamos estes quatro porque endereçam diretamente as necessidades arquiteturais do pipeline:

**Padrões escolhidos cobrem as três categorias:**
- **Criacional (Factory Method):** instanciação de leitores baseada em extensões de arquivo
- **Estrutural (Decorator):** adição dinâmica de comportamentos (cache, compressão, criptografia)
- **Comportamental (Chain of Responsibility + Template Method):** organização do fluxo de transformações e do algoritmo geral

**Por que os outros 19 padrões não se aplicam:**
- **Criacionais não escolhidos:** Abstract Factory seria complexo demais para um único tipo de produto; Singleton não temos recursos globais; Builder/Prototype não há construção complexa de objetos
- **Estruturais não escolhidos:** Adapter/Bridge/Facade não há sistemas legados para adaptar; Composite não há estruturas hierárquicas; Flyweight não há compartilhamento massivo de objetos; Proxy não há controle de acesso remoto
- **Comportamentais não escolhidos:** Command/Memento/Observer/State/Strategy/Visitor não há necessidade de desfazer operações, observar eventos, gerenciar estados ou variar algoritmos dinamicamente; Interpreter/Iterator/Mediator não há gramáticas, coleções customizadas ou comunicação complexa entre objetos

Os quatro padrões escolhidos resolvem problemas reais do projeto (criação polimórfica, composição de funcionalidades, pipeline de transformações, algoritmo reutilizável) sem adicionar complexidade desnecessária.

## Justificativa para Cada Padrão

Justificativa detalhada para cada padrão utilizado, explicando:

01. **Por que o padrão foi escolhido** — por que ele se encaixa neste contexto específico.  
02. **Qual problema ele resolve** — qual dor do código ele endereça.  
03. **Quais benefícios ele traz** — ganhos para arquitetura/manutenibilidade/escalabilidade.  
04. **Como o código seria diferente** — o que pioraria se o padrão não fosse empregado.

### 1.Factory Method (Criacional)

**01. Por que o padrão foi escolhido**  
O pipeline precisa instanciar leitores diferentes (TXT, CSV, JSON) baseado na extensão do arquivo recebida dinamicamente via linha de comando. O Factory Method encapsula essa decisão na classe `LeitorArquivoFactory`, que mantém um dicionário `_mapa` associando extensões aos tipos concretos. A implementação trata arquivos com dupla extensão (`.txt.gz`, `.csv.enc`), extraindo `extensoes[-2]` quando detecta sufixos de compressão/criptografia.

**02. Qual problema ele resolve**  
Elimina condicionais `if/elif` espalhadas pelo código para descobrir o leitor correto. Sem o padrão, cada processador replicaria a lógica de detecção de extensões, violando o princípio Open/Closed. Adicionar suporte a `.xml` exigiria modificar todos os pontos de instanciação. O Factory Method centraliza essa complexidade em um único método `criar()`.

**03. Quais benefícios ele traz**  
- **Extensibilidade:** novos formatos entram apenas registrando no `_mapa` (ex.: `".xml": LeitorXML`) sem tocar no código cliente
- **Desacoplamento:** processadores dependem da interface abstrata `LeitorArquivo`, não de implementações concretas
- **Manutenibilidade:** lógica de detecção de extensões duplas (`caminho.suffixes`) fica isolada e testável
- **Consistência:** um único ponto de criação garante comportamento uniforme em todo o sistema

**04. Como o código seria diferente**  
Cada processador teria blocos `if/elif` duplicados para instanciar leitores. A lógica de arquivos comprimidos estaria espalhada e inconsistente (alguns lugares esqueceriam de verificar `len(extensoes) >= 2`). Evoluir o pipeline para suportar novos formatos seria arriscado e trabalhoso, exigindo localizar e modificar múltiplos pontos de instanciação.

### 2.Decorator (Estrutural)

**01. Por que o padrão foi escolhido**  
Precisávamos adicionar comportamentos opcionais aos leitores (cache, descompressão `.gz`, descriptografia `.enc`) sem multiplicar subclasses para cada combinação. A implementação usa `LeitorDecorator` como base que delega para `self._leitor`, permitindo compor funcionalidades dinamicamente: `LeitorComCache(LeitorComDescriptografia(LeitorComDescompressao(leitor)))`.

**02. Qual problema ele resolve**  
Impede a explosão combinatória de classes. Sem decorators, precisaríamos criar subclasses para cada combinação possível: `LeitorCSVComCache`, `LeitorCSVComDescompressao`, `LeitorCSVComCacheEDescompressao`, etc. Para 3 funcionalidades e 3 formatos, teríamos O(3 × 2³) = 24 classes. O Decorator reduz isso a 6 classes (3 decorators + 3 leitores base).

**03. Quais benefícios ele traz**  
- **Composição flexível:** cada processador monta cadeias diferentes (`ProcessadorTextoPadrao` usa cache+descriptografia+descompressão; `ProcessadorTextoSuave` usa apenas descompressão)
- **Extensibilidade:** adicionar `LeitorComValidacao` não requer modificar classes existentes, apenas estender `LeitorDecorator`
- **Separação de responsabilidades:** lógica de cache fica em `LeitorComCache`, lógica de `gzip` fica em `LeitorComDescompressao`, parsing permanece isolado
- **Controle dinâmico:** flag `--sem-cache` desabilita decorator via `usar_cache=not args.sem_cache` sem criar classes separadas

**04. Como o código seria diferente**  
Cada leitor teria métodos `_abrir()` inflados com condicionais aninhados verificando cache, descompressão e descriptografia simultaneamente. Isso violaria o Single Responsibility Principle, dificultaria testes (mockar `gzip` e `base64` em testes de CSV) e tornaria impossível desabilitar funcionalidades seletivamente por processador.

### 3.Chain of Responsibility (Comportamental)

**01. Por que o padrão foi escolhido**  
O pipeline precisa aplicar múltiplas transformações sequenciais (normalizar acentos via `unicodedata`, remover stopwords com regex, filtrar linhas inválidas, padronizar espaços) que devem ser combinadas e reordenadas sem impactar umas às outras. A implementação define `EtapaProcessamento` com `self._proximo` e método `executar()` que processa localmente e delega: `PadronizaEspacosEtapa(NormalizaAcentosEtapa(RemoveStopWordsEtapa(FiltraLinhasInvalidasEtapa())))`.

**02. Qual problema ele resolve**  
Desacopla cada etapa de transformação e evita métodos monolíticos com todas as transformações mescladas. Sem o padrão, teríamos um método `_processar()` de 50+ linhas com lógica de normalização, remoção de stopwords, filtragem e padronização entrelaçadas, violando o Single Responsibility Principle e impossibilitando testes isolados de cada transformação.

**03. Quais benefícios ele traz**  
- **Modularidade testável:** cada etapa é testada isoladamente (ex.: `NormalizaAcentosEtapa().executar(['café'])` → `['cafe']`)
- **Flexibilidade de composição:** `ProcessadorTextoPadrao` usa a cadeia completa; `ProcessadorTextoSuave` usa apenas `PadronizaEspacosEtapa()`
- **Reordenação trivial:** trocar ordem das etapas requer apenas reorganizar a construção da cadeia
- **Extensibilidade:** adicionar `ConverteParaMaiusculasEtapa` não modifica etapas existentes, apenas se insere na cadeia
- **Parametrização:** `RemoveStopWordsEtapa` aceita lista customizada de stopwords no construtor

**04. Como o código seria diferente**  
Todas as transformações estariam em um único método `_processar()` com loops aninhados e lógica entrelaçada. Impossível testar cada transformação isoladamente, reutilizar etapas entre processadores, ou reordenar transformações sem reescrever o método inteiro. Adicionar novas etapas violaria o princípio Open/Closed ao exigir modificação do método existente.

### 4. Template Method (Comportamental)

**01. Por que o padrão foi escolhido**  
Todo processamento compartilha o esqueleto algorítmico `criar leitor → decorar → ler → processar → salvar`, mas cada variação customiza pontos específicos. O Template Method define o fluxo em `ProcessadorArquivo.executar()` com hooks (`_criar_leitor`, `_decorar_leitor`, `_montar_cadeia`, `_salvar`) que subclasses sobrescrevem: `ProcessadorTextoPadrao` aplica cache+descriptografia+descompressão+cadeia completa; `ProcessadorTextoSuave` aplica apenas descompressão+padronização.

**02. Qual problema ele resolve**  
Evita duplicação do algoritmo em cada processador. Sem o padrão, cada classe implementaria manualmente os passos `criar → decorar → ler → processar → salvar`, duplicando código e arriscando inconsistências (ex.: esquecer de chamar `parent.mkdir()` antes de salvar). Qualquer mudança no fluxo (adicionar logging, tratamento de exceções) exigiria modificar todas as subclasses.

**03. Quais benefícios ele traz**  
- **Consistência garantida:** todas as subclasses executam a mesma sequência de passos porque herdam `executar()`
- **Redução de duplicação:** o algoritmo de 11 linhas é implementado uma vez na classe base ao invés de ser replicado em N processadores
- **Extensibilidade controlada:** criar novos processadores requer apenas sobrescrever hooks específicos (`_montar_cadeia`, `_decorar_leitor`)
- **Manutenção centralizada:** evoluções no fluxo (criar diretórios, validações) são implementadas uma vez e beneficiam todas as subclasses
- **Documentação explícita:** o método `executar()` serve como especificação clara do protocolo de processamento

**04. Como o código seria diferente**  
Cada processador teria 30-50 linhas duplicadas com o fluxo completo. Inconsistências surgiriam facilmente (ex.: `ProcessadorTextoSuave` esquecendo de salvar). Adicionar tratamento de exceções ou logging exigiria modificar N classes. Com 5 processadores, teríamos ~200 linhas duplicadas reduzíveis a 11 linhas no Template Method.

## Benefícios combinados
- **Extensibilidade guiada:** novos formatos entram pela fábrica; novos adornos (cache, compressão) são adicionados como decorators e novas etapas de transformação entram na cadeia.
- **Baixo acoplamento:** cada padrão limita o impacto de mudanças a um ponto único, facilitando manutenção.
- **Clareza arquitetural:** o Template Method deixa explícito o fluxo macro, enquanto Factory/Decorator/Chain detalham as variações micro.

Os quatro padrões escolhidos cobrem dimensões complementares (criação, estrutura e comportamento), oferecendo o melhor equilíbrio entre simplicidade e flexibilidade para o projeto proposto.
