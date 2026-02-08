---
title: Mcp Server custom in c#
date: 2025-09-16T08:00:00
lastmod: 2025-09-16T08:11:58
draft: false
slug: mcp-server-custom-in-c
tags:
  - ai
  - dotnet
  - mcp
categories:
  - Uncategorized
---

<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Cos'è MCP?</h6>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>A partire da novembre 2024 Anthropic a rilasciato il <strong>Model Context Protocol (MCP)</strong>, in modo tale di permettere agli LLM di reperire informazioni dalle nostre applicazioni locali, operazione che prima si poteva fare soltanto definendo dei tool all'interno dei nostri applicativi.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Vantaggi rispetto ai tools</h6>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Ovviamente le stesse operazioni possono essere fatte tramite i tools, ma un server MCP ci da in più la riusabilità e il disaccopiamento. <br>In sintesi Non dobbiamo cambiare il codice dei nostri agent e possiamo esporre un server Mcp a più agent.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p></p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":4} -->
<h4 class="wp-block-heading">Implementazione di un MCP Server Custom in C#</h4>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Ora andremo a vedere come possiamo implementare un MCP Server Custom e farlo utilizzare al nostro agente</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Setup del progetto</h6>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>
per l'implementazione è necessario usare il pacchetto <a href="https://github.com/modelcontextprotocol">ModelContextProtocol</a>  presente su Nuget in Preview
La libreria oltre ad essere disponibile in c# è disponibile anche per altri linguaggi (Typescript,Python,Java,ecc....)



Ma partiamo con lo sviluppo:
Creiamo il nostro progetto, in c# (io ho usa la RC1 di .net10) e importiamo i pacchetti nuget
</p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code {"className":"block-code-decorator"} -->
<pre class="wp-block-syntaxhighlighter-code block-code-decorator">ModelContextProtocol
ModelContextProtocol.AspNetCore</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:paragraph -->
<p></p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Implementazione dei tools</h6>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>
Per implementare i tool del nostro server MCP sarà sufficiente andare ad implementare una classe e utilizzare il decoratore:
</p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code {"className":"wp-block-code"} -->
<pre class="wp-block-syntaxhighlighter-code wp-block-code">McpServerToolType</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:paragraph -->
<p>
e su ogni singolo tool da esporre usiamo il decoratore
</p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code {"className":"wp-block-code"} -->
<pre class="wp-block-syntaxhighlighter-code wp-block-code">McpServerTool</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:paragraph -->
<p>è importante anche utilizzare delle descrizioni chiare, che danno più indicazioni possibili su cosa fa il nostro tool. Per far si che i nostri agent, siano in grado di riconoscere quali tool andare a chiamare, qui vi mostro una classe con all'interno un tool come esempio, che si limita a tornare la stringa ricevuta in input con una personalizzazine.</p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code {"language":"csharp"} -->
<pre class="wp-block-syntaxhighlighter-code">using ModelContextProtocol.Server;

namespace McpHttpServer.tools
{
    /// 
    /// MCP Tools collection for this server
    /// 
    [McpServerToolType]

    public class McpSampleTools
    {
        private readonly ServerConfig _config;

        public McpSampleTools(ServerConfig config)
        {
            _config = config;
            Console.WriteLine("McpSampleTools initialized with configuration.");
            Console.WriteLine("Tool settings:"+ _config.ServerSettings.Name);
        }
        /// 
        /// Echo tool - returns the provided text
        /// 
        /// The text to echo back
        /// The echoed text
                [McpServerTool]
        [Description("Echo back the provided text")]
        public  string Echo(
            [Description("The text to echo back")] string text)
        {
            Console.WriteLine($"Echo called with text: {text} Config Server Name: {_config.ServerSettings.Name}");
            return $"Dal server mcp {_config.ServerSettings.Name}: {text} ";
        }
    }

}</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Implementazione Server MCP Server</h6>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Una volta implementati i nostri tool, non ci resta che tirare su allo startup della nostra applicazione il nostro server MCP e questo lo facciamo con le righe di codice che seguono:</p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code {"language":"csharp"} -->
<pre class="wp-block-syntaxhighlighter-code">uilder.Services.AddMcpServer(options =&gt;
{
    options.ServerInfo = new()
    { 
        Name = config.ServerSettings.Name,
        Version = config.ServerSettings.Version
    };
})
    .WithHttpTransport() // Use HTTP transport
    .WithToolsFromAssembly(); // Register tools from the current assembly



var app = builder.Build();

// Map MCP endpoints
app.MapMcp();</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:paragraph -->
<p>In estrema sintesi quello che andiamo a fare è definire un serverMCP ("AddMcpServer") e poi gli diciamo che dobbiamo recuperare i tool dall'assembly "WithToolsFromAssembly" questo metodo, recupera i tools con i decoratori e li espone nell'mcp server, e infine gli indichiamo il trasporto che deve essere http,  ci sono anche altri tipi di trasporti  (stdio,sse). </p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Nel mio codice ho aggiunto anche app.MapMcp appunto per andare a mappare l'endpoint dedicato al nostro MCP Server quindi avremo url della nostra applicazione /MCP</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p></p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":6} -->
<h6 class="wp-block-heading">Utilizzo Server MCP</h6>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Bene ma una volta che abbiamo eseguito lo sviluppo e esponiamo come andiamo a testare il nostro server mcp? la soluzione più rapida è quella di andarlo ad integrare all'interno della finestra del nostro client in visual studio code, quindi all'interno della forder .vscode aggiungiamo un file denominato mcp.json e aggiungiamo le seguenti righe:</p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code {"language":"as3"} -->
<pre class="wp-block-syntaxhighlighter-code">{
    "servers": {
    "nomemioserver": {
        "type": "http", //Transport Type
        "url": "http://urlmioserver/"
    }
}
}</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:paragraph -->
<p></p>
<!-- /wp:paragraph -->
