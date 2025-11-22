# Análise dos 23 Padrões GoF

## I.Padrões de Criação

### 1. Singleton

O Singleton garante que uma classe possua apenas uma instância ativa e forneça acesso global a ela; sua estrutura consiste em um construtor privado, um atributo estático que armazena a única instância e um método público estático que controla sua criação. Ele é utilizado quando se precisa centralizar recursos, como gerenciadores de configuração, caches ou logs. Como variações, existem o eager singleton (instância criada no carregamento da classe), lazy singleton (criando sob demanda), uso de sincronização, e o padrão Initialization-on-demand holder, considerado a forma mais segura e eficiente. É útil, porém deve ser aplicado com moderação para não gerar acoplamento excessivo.

### 2. Factory Method

O Factory Method define um método de criação que pode ser sobrescrito por subclasses para decidir qual classe concreta será instanciada, estruturando-se em um Creator (que declara o factory) e ConcreteCreators (que implementam a criação), além dos Products e ConcreteProducts. Ele é indicado quando é necessário permitir que subclasses escolham quais objetos criar, favorecendo extensibilidade. Como variações, pode aparecer como método estático, registro de tipos ou criação baseada em parâmetros. Esse padrão reduz dependência direta de classes concretas e facilita adição de novos produtos.

### 3. Abstract Factory

O Abstract Factory fornece uma interface para criar famílias de objetos relacionados sem especificar suas classes concretas; sua estrutura inclui uma fábrica abstrata com vários métodos de criação, fábricas concretas que produzem versões compatíveis dos produtos e os próprios produtos concretos. É útil quando se deseja garantir consistência entre objetos que pertencem ao mesmo “tema” ou “família”, como sistemas de GUI, drivers ou estilos. Suas variações incluem fábricas configuráveis, fábricas registradas e integração com padrões como Singleton ou Builder. Ele permite alternar famílias inteiras de produtos com mínima modificação no código cliente.

### 4. Builder

O Builder separa o processo de construção de um objeto complexo de sua representação final, permitindo montar objetos passo a passo; sua estrutura envolve um Builder (que declara as etapas), ConcreteBuilders (que implementam as etapas), um Director (que coordena a montagem) e o Product. Ele é útil quando objetos têm muitos parâmetros ou precisam de construção parcelada e legível. Entre as variações estão Builders fluentes, eliminação do Director e Builders híbridos com Factory. Esse padrão é ideal para objetos imutáveis e configurações complexas que exigem flexibilidade.

### 5. Prototype

O Prototype cria novos objetos a partir da clonagem de um protótipo existente, cuja estrutura inclui uma interface com o método clone(), protótipos concretos e, opcionalmente, um registro de protótipos. É empregado quando criar objetos do zero é caro ou complexo, ou quando se deseja configurar dinamicamente novos tipos sem depender de hierarquias extensas. Possui variações como clonagem superficial (shallow) e profunda (deep clone), além de registros para reutilização. Ele é eficiente em sistemas que exigem muitas duplicações de objetos complexos.

## II. Padrões Estruturais

### 6. Adapter

O Adapter converte a interface de uma classe em outra esperada pelo cliente, permitindo compatibilidade entre componentes que não foram projetados para trabalhar juntos; sua estrutura envolve o Target (interface esperada), o Adaptee (classe existente incompatível) e o Adapter (que adapta chamadas). É útil quando se integra sistemas legados ou bibliotecas externas. Existem duas variações: class adapter (herança) e object adapter (composição), sendo esta última mais flexível. Ele permite reaproveitar código antigo sem grandes alterações estruturais.

### 7. Bridge

O Bridge separa a abstração de sua implementação ao dividir o sistema em duas hierarquias independentes: uma para a abstração (Abstraction e RefinedAbstraction) e outra para a implementação (Implementor e ConcreteImplementor). É recomendado quando tanto as abstrações quanto as implementações podem variar, evitando explosões de subclasses combinando ambas. Suas variações incluem troca dinâmica de implementações, múltiplos níveis de abstração e integração com fábricas. Esse padrão reduz acoplamento e aumenta flexibilidade arquitetural.

### 8. Composite

O Composite organiza objetos em estruturas de árvore permitindo tratar elementos individuais (Leaf) e composições (Composite) de forma uniforme, todos implementando uma interface comum (Component). Ele é indicado para representar estruturas hierárquicas como árvores de diretórios, menus ou interfaces gráficas. Possui variações transparent (operações para filhos expostas na interface Component) e safe (somente Composite gerencia filhos). Esse padrão facilita operações recursivas e torna o sistema altamente extensível.

### 9. Decorator

O Decorator adiciona comportamentos a objetos de forma dinâmica envolvendo-os em “camadas” de objetos decoradores, cuja estrutura inclui Component (interface comum), ConcreteComponent (objeto original), Decorator (classe base que envolve o componente) e ConcreteDecorators (funções extras). Ele é útil quando se deseja extender funcionalidades sem herança rígida. Suas variações permitem empilhar vários decoradores, adicionar estados internos ou controlar ordem de execução. É amplamente usado para adicionar responsabilidades opcionais de forma modular.

### 10. Facade

O Facade fornece uma interface simplificada para um conjunto de subsistemas complexos; sua estrutura inclui a classe Facade, que coordena chamadas a várias classes internas. Ele é usado quando se deseja reduzir a complexidade percebida pelo cliente, organizar camadas e diminuir acoplamento. Variações incluem múltiplas fachadas por módulo e fachadas complementares com subsistemas diferentes. Esse padrão melhora a legibilidade e facilita integração entre módulos.

### 11. Flyweight

O Flyweight reduz o consumo de memória compartilhando partes imutáveis de objetos utilizados em grande quantidade, separando estado intrínseco (compartilhado) e extrínseco (fornecido externamente). Sua estrutura inclui a FlyweightFactory, que gerencia instâncias compartilhadas, e objetos Flyweight que evitam duplicação. É ideal em sistemas com milhões de objetos visualmente similares, como caracteres de texto, tiles de jogos ou ícones. Como variações, existem flyweights compartilhados, não compartilhados e híbridos. Ele otimiza desempenho em aplicações de grande escala.

### 12. Proxy

O Proxy atua como substituto de outro objeto controlando seu acesso; sua estrutura inclui Subject (interface comum), RealSubject (objeto real) e Proxy (que intercepta ou gerencia chamadas). É usado para lazy loading, cache, autenticação e acesso remoto. Entre suas variações estão o Virtual Proxy, Remote Proxy, Protection Proxy e Cache Proxy. Ele permite adicionar comportamentos sem alterar o objeto real, isolando responsabilidades de acesso, segurança e otimização.

## III. Padrões Comportamentais

### 13. Chain of Responsibility

O Chain of Responsibility cria uma cadeia de objetos responsáveis por processar uma requisição ou repassá-la adiante; sua estrutura inclui Handler (interface), ConcreteHandlers e referência ao próximo handler. É útil para pipelines de validação, interceptação e processamento. Suas variações incluem cadeias dinâmicas, encadeamento automático e integração com Mediator. Ele permite adicionar e remover etapas sem alterar o emissor da requisição.

### 14. Command

O Command encapsula uma operação como objeto, permitindo armazenar, desfazer, copiar e agendar ações; sua estrutura inclui Command, ConcreteCommands, Receiver, Invoker e Client. Ele é ideal para sistemas com undo/redo, macros, filas e logs de ações. Entre variações estão MacroCommands, comandos com estado, comandos assíncronos e integração com Memento para undo. O padrão desacopla a solicitação da execução, permitindo grande flexibilidade.

### 15. Interpreter

O Interpreter modela linguagens simples usando classes que representam regras gramaticais; sua estrutura inclui Expression (interface), TerminalExpressions, NonTerminalExpressions e o Context. Ele é indicado para DSLs, linguagens matemáticas ou regras repetitivas. Suas variações incluem interpretadores com otimização, construção de ASTs e integração com Composite. É poderoso, porém pode ficar complexo para gramáticas grandes.

### 16. Iterator

O Iterator permite percorrer coleções sem expor sua estrutura interna; sua estrutura possui Iterator (com métodos next e hasNext) e Aggregate (que fornece iteradores). Ele é usado quando se deseja padronizar percursos, permitir múltiplas iterações e manter encapsulamento. Suas variações incluem iteradores internos, externos, reversos, imutáveis e fail-fast. O padrão garante traversal seguro e independente da estrutura física da coleção.

### 17. Mediator

O Mediator centraliza a comunicação entre objetos, reduzindo dependências diretas; sua estrutura possui Mediator, ConcreteMediator e Colleagues que interagem apenas com o mediador. É recomendado em sistemas onde muitos objetos precisam se comunicar, como UIs complexas. Variações incluem mediadores distribuídos e integração com Observer para notificações. O padrão melhora organização e reduz acoplamento entre componentes.

### 18. Memento

O Memento salva o estado interno de um objeto sem violar encapsulamento, permitindo restaurá-lo posteriormente; sua estrutura inclui Originator (que cria mementos), Memento (que armazena o estado) e Caretaker (que guarda mementos). É útil em sistemas com undo/redo, checkpoints e recuperação de falhas. Variações incluem mementos completos, diferenciais e externos. Ele separa lógica de estado da lógica de restauração, preservando privacidade dos dados internos.

### 19. Observer

O Observer estabelece dependência um-para-muitos onde mudanças em um objeto (Subject) notificam automaticamente os Observers; sua estrutura contém métodos para registrar, remover e notificar observadores. É ideal para eventos, notificações, interfaces gráficas e integração modular. Suas variações incluem padrão push/pull, listeners fracos e broadcast. Ele desacopla emissor e receptores, tornando o sistema reativo.

### 20. State

O State permite que um objeto altere seu comportamento quando seu estado interno muda, representando cada estado como um objeto separado; sua estrutura inclui Context (que mantém o estado atual) e State/ConcreteStates com comportamentos distintos. Ele é usado para máquinas de estado, fluxos condicionais e objetos que mudam de comportamento dinamicamente. Suas variações incluem transições internas, externas e estados compartilhados. O padrão organiza código que, sem ele, seria dominado por condicionais gigantes.

### 21. Strategy

O Strategy encapsula algoritmos intercambiáveis em classes separadas, permitindo que o Context selecione a estratégia adequada em tempo de execução. Sua estrutura inclui Strategy (interface) e ConcreteStrategies implementando algoritmos diferentes. É usado quando múltiplas variações de comportamento precisam ser trocadas dinamicamente. Variações incluem estratégias compostas, configuráveis ou selecionadas automaticamente. Ele evita condicionais múltiplas e aumenta flexibilidade.

### 22. Template Method

O Template Method define o esqueleto de um algoritmo em um método final da superclasse, permitindo que subclasses redefinam etapas específicas; sua estrutura contém operações primitivas (abstratas ou com implementação padrão) e o método template que organiza a execução. É útil para padronizar processos semelhantes com pequenas variações. Variações incluem hooks, etapas opcionais e integração com Strategy. Ele garante consistência e reaproveitamento de lógica.

### 23. Visitor

O Visitor separa operações de uma estrutura de objetos permitindo adicionar novos comportamentos sem modificar as classes originais; sua estrutura inclui Visitor (com métodos específicos para cada elemento), Element (com accept) e ConcreteElements. É ideal quando a estrutura é estável e muitas operações diferentes precisam ser executadas sobre ela. Suas variações incluem visitors reflexivos, acíclicos e compostos. Ele facilita expansão funcional, porém exige atualização para novos tipos de elementos.

## Comparações entre os Padrões GoF

A análise comparativa entre os padrões de projeto é essencial para compreender suas relações conceituais, diferenças estruturais e possibilidades de integração. Embora cada padrão tenha sido concebido para resolver um problema específico dentro do design orientado a objetos, muitos deles apresentam proximidades funcionais ou estruturais que frequentemente levam a dúvidas na escolha do mais adequado. A seguir, são discutidos os principais pares e grupos de padrões que mantêm relações de similaridade, contraste ou complementaridade.

### 4.1 Strategy e State
Os padrões Strategy e State possuem estruturas muito semelhantes, baseadas em interfaces comuns e múltiplas classes concretas. Contudo, diferem significativamente quanto à intenção: o Strategy permite selecionar, de forma explícita, diferentes algoritmos para um mesmo contexto, enquanto o State representa mudanças automáticas de comportamento motivadas por alterações internas no estado do objeto. Assim, o primeiro é orientado a decisões externas do cliente, e o segundo reflete transições internas do objeto. Embora não sejam normalmente combinados, ambos são frequentemente confundidos devido à similaridade estrutural.

### 4.2 Decorator, Proxy e Adapter
Os padrões Decorator, Proxy e Adapter compartilham o uso de composição e a ideia de “envolvimento” (wrapping) de objetos, o que os torna semelhantes no aspecto estrutural. Entretanto, suas finalidades são distintas: o Decorator adiciona responsabilidades de maneira dinâmica, o Proxy controla e restringe o acesso ao objeto real (incluindo autenticação, cache ou carregamento tardio), e o Adapter converte interfaces incompatíveis para possibilitar reutilização de código. Em termos de integração, Decorator e Proxy podem coexistir, enquanto o Adapter é geralmente utilizado apenas para compatibilização e não para extensão comportamental.

### 4.3 Abstract Factory, Factory Method, Builder e Prototype
Os padrões de criação apresentam pontos de convergência, pois todos visam controlar o processo de instanciação. Ainda assim, cada um aborda uma necessidade distinta: o Factory Method delega às subclasses a decisão sobre qual produto criar; o Abstract Factory organiza a criação de famílias de objetos relacionados; o Builder estrutura a criação incremental de objetos complexos; e o Prototype viabiliza a criação por meio da clonagem de instâncias existentes. Esses padrões podem atuar em conjunto — por exemplo, Builders podem ser gerados por uma Abstract Factory, ou uma Factory pode retornar objetos Prototype clonados — sendo comum sua combinação em arquiteturas flexíveis.

### 4.4 Template Method e Strategy
Embora ambos tratem da variação de comportamento dentro de um algoritmo, Template Method e Strategy divergem quanto ao mecanismo de extensão. O Template Method utiliza herança para permitir que subclasses substituam determinadas etapas de um processo padronizado, enquanto o Strategy favorece composição, permitindo que o algoritmo seja trocado dinamicamente em tempo de execução. Logo, o Template Method garante uma estrutura fixa, ao passo que o Strategy privilegia a flexibilidade. Há casos em que ambos podem ser combinados, utilizando-se estratégias parametrizáveis em etapas específicas do template.

### 4.5 Composite e Decorator
Composite e Decorator compartilham o uso de uma interface comum para tratar objetos individualmente ou agrupados, o que pode gerar confusão. However, o Composite organiza objetos em estruturas hierárquicas do tipo árvore, permitindo representar relações do tipo “todo-parte”, enquanto o Decorator adiciona funcionalidades de forma incremental sem alterar a estrutura hierárquica. Esses padrões podem ser usados simultaneamente, por exemplo, quando elementos individuais ou composições inteiras precisam receber comportamentos adicionais dinamicamente.

### 4.6 Composite e Visitor
O Visitor é frequentemente aplicado a estruturas Composite, pois separa operações de uma árvore sem modificar suas classes internas. O Composite organiza a hierarquia e facilita a navegação, enquanto o Visitor adiciona comportamentos especializados — como cálculos, verificações ou transformações — sem violar o princípio de responsabilidade única. Assim, a relação entre eles é predominantemente complementar, sendo comum encontrá-los integrados em compiladores, interpretadores e sistemas de modelagem complexa.

### 4.7 Command e Chain of Responsibility
Ambos os padrões lidam com solicitação e processamento, mas abordam o problema sob perspectivas diferentes. O Command encapsula solicitações como objetos, permitindo que sejam armazenadas, enfileiradas ou desfeitas, enquanto a Chain of Responsibility distribui a responsabilidade de lidar com uma requisição ao longo de uma cadeia de manipuladores. A integração entre ambos é útil em pipelines de execução, onde comandos podem ser submetidos a cadeias de validação ou transformação.

### 4.8 Command e Memento
Os padrões Command e Memento apresentam forte relação conceitual quando se trata de mecanismos de desfazer (undo) e refazer (redo). O Command representa a ação em si, encapsulando a operação a ser executada; já o Memento captura o estado do objeto antes da execução do comando. A combinação é natural: comandos podem gerar mementos automaticamente, possibilitando rever estados anteriores e garantindo a integridade do estado restaurado.

### 4.9 Mediator e Observer
Embora ambos reduzam o acoplamento entre objetos, o Mediator e o Observer diferem na forma como organizam a comunicação. O Observer estabelece uma relação de dependência um-para-muitos, na qual alterações no sujeito resultam em notificações automáticas aos observadores. Já o Mediator centraliza o diálogo entre diversos objetos, evitando a criação de redes complexas de dependências circulares. Os dois padrões podem ser combinados quando o mediador utiliza observadores para coordenar notificações entre componentes de forma eficiente.

### 4.10 Proxy e Flyweight
Proxy e Flyweight envolvem algum nível de intermediação, mas seus objetivos são distintos. O Proxy regula o acesso ao objeto real, fornecendo mecanismos adicionais de segurança, cache ou retardamento de carga. O Flyweight, por sua vez, visa diminuir o consumo de memória ao compartilhar partes imutáveis de objetos que aparecem em grande quantidade. Embora possam ser utilizados em conjunto, suas finalidades raramente se sobrepõem, já que um busca controle de acesso e o outro otimização de recursos.

### 4.11 Adapter e Facade
Adapter e Facade são frequentemente confundidos, mas desempenham papéis diferentes no contexto da simplificação de interfaces. O Adapter converte a interface de um componente existente para torná-la compatível com um cliente específico, focando na adaptação funcional. Por outro lado, a Facade fornece uma interface mais simples e unificada para um subsistema complexo, sem alterar a interface original das classes internas. Assim, enquanto o Adapter resolve incompatibilidades, o Facade resolve excesso de complexidade. Ambos podem ser combinados, sendo comum que uma fachada utilize adaptadores internamente.

### 4.12 Iterator e Composite
Iterator e Composite lidam com estruturas que podem ser percorridas de forma uniforme, mas cada um desempenha uma função distinta. O Composite organiza objetos em uma hierarquia, enquanto o Iterator fornece um mecanismo padronizado de navegação. A integração entre esses padrões é bastante comum: estruturas compostas geralmente implementam iteradores para facilitar o acesso recursivo aos seus elementos internos, mantendo o encapsulamento e a abstração.

### 4.13 Flyweight e Prototype
Ambos podem estar relacionados ao desempenho, porém com objetivos opostos. O Prototype reduz o custo de criação duplicando objetos existentes, enquanto o Flyweight reduz o custo de memória compartilhando partes imutáveis entre várias instâncias. Esses padrões dificilmente são combinados, mas a compreensão de sua distinção é crucial para a escolha correta: duplicar objetos (Prototype) não é adequado quando se deseja compartilhá-los (Flyweight), e vice-versa.
