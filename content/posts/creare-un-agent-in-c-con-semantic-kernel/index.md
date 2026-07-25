---
title: Creare un Agent in C# con Semantic Kernel
date: 2025-08-10T15:29:00
lastmod: 2025-08-14T16:23:11
draft: false
slug: creare-un-agent-in-c-con-semantic-kernel
tags:
  - agent
  - ai
  - c
  - net
  - semantic-kernel
categories:
  - Uncategorized
---

<!-- wp:paragraph -->
<p>&nbsp;Ciao a tutti,</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>In questo post voglio condividere come implementare un agent in c# sfruttando il&nbsp;<a href="https://learn.microsoft.com/en-us/semantic-kernel/overview/">semantic Kernel</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Ma partiamo dalle basi, cos' è un Agent? e a cosa ci serve?</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Cos'è un Agent?</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Un agent può essere inteso come un sistema in grado di prendere decisioni in modo autonomo, seguendo obiettivi e regole che gli sono stati dati, sfruttando le informazioni in un suo possesso.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>A Cosa ci servono gli Agent?</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Gli agent ci possono aiutare ad automatizzare tutta una serie di operazioni e a velocizzare il nostro lavoro quotidiano.&nbsp;<br>Il caso più banale è quello dell'operatore di customer care, che deve recuperare e verificare la situazione del cliente, a seguito della richiesta del cliente, bene queste sono operazioni che può eseguire un Agent addestrato a fare ciò.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Cos'è Il Semantic Kernel ?</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Il Semantic Kernel è un Framework che permette l'integrazione dell'AI all'interno di vari linguaggi di programmazione questo ci permette appunto di sviluppare agent, ma non solo gli agent sono solo una parte di ciò che possiamo fare con il Semantic Kernel</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Costruiamo un semplice agente</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Bene a questo punto vi mostro gli step per costruire un agent.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Per sviluppare questo piccolo progetto, ho usato come modello "llama3.2" su un Container con Ollama,</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>STEP 1 Creazione del progetto e aggiunta dei pacchetti necessari.</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Creiamo una console e andiamo ad aggiungere i seguenti pacchetti nuget</p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code -->
<pre class="wp-block-syntaxhighlighter-code">
Microsoft.SemanticKernel
Microsoft.SemanticKernel.Core
Microsoft.SemanticKernel.Agents.Core
Microsoft.SemanticKernel.Connectors.Ollama  → in pre-release
</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:paragraph -->
<p><strong>STEP 2 Creazione dell'agent</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Ora possiamo già procedere con la creazione dell'agent,</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Andremo a Instanziare l'agent e a dargli le istruzioni, nel mio caso gli ho detto di inventare storie divertenti.</p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code -->
<pre class="wp-block-syntaxhighlighter-code">
using System.ComponentModel;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.ChatCompletion;

var builder = Kernel.CreateBuilder();

// Add the Ollama chat completion service
// Ensure you have Ollama running and the model "llama3.2:3b" is available
// You can change the model name and URI as needed
builder.AddOllamaChatCompletion("llama3.2:3b", new Uri("http://localhost:11434"));

var kernel = builder.Build();

ChatCompletionAgent agent = new() // 👈🏼 Definition of the agent
{
    Instructions = "You are an agent who creates funny stories.",
    Name = "Story Agent",
    Description = "This agent can create funny stories based on user input.",
    Kernel = kernel
};
</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:paragraph -->
<p><strong>STEP 3 Interazione con l'agent</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>è il momento di scrivere l'interazione con l'agent, io ho simulato un chatbot botta e risposta giusto per divertirmi un po<br><br></p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code -->
<pre class="wp-block-syntaxhighlighter-code">
string userMessage = string.Empty;

do
{
    Console.WriteLine("What kind of story would you like me to tell you? Type 'exit' to stop the chat.");
    userMessage = Console.ReadLine();

    if (!string.IsNullOrEmpty(userMessage) &amp;&amp; userMessage != "exit")
    {
        ChatHistory chat =
        [
            new ChatMessageContent(AuthorRole.User, userMessage)
        ];

        await foreach (var response in agent.InvokeAsync(chat))
        {
            chat.Add(response);
            Console.WriteLine(response.Message.Content);
        }

        userMessage = string.Empty;
    }

}
while (userMessage != "exit");
</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:paragraph -->
<p>A questo punto la console può essere eseguita e testata.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Integrazione con Function</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Ovviamente per rendere l'agent più centrato sui nostri obiettivi, possiamo definire delle funzioni custom con le quali lui andrà a recuperare le informazioni.&nbsp;<br>Ad esempio il recupero delle informazioni relative al cliente stesso, all'interno dei sistemi. Di seguito ho simulato un esempio dell'utilizzo delle funzioni</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>STEP 4 Definire le funzioni</strong></p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code -->
<pre class="wp-block-syntaxhighlighter-code">
[Description("Get the residence city from the user")]
string GetCity(string name)
{
    return "Roma";
}

[Description("Get the age of a user")]
int GetUserAge(string name)
{
    return 25;
}
</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:paragraph -->
<p><strong><em>Definite le funzioni le associamo al nostro agent</em></strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Andiamo ad aggiungere ai plugin le funzioni che abbiamo scritto sopra, in modo tale che questo possa invocarle quando necessario</p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code -->
<pre class="wp-block-syntaxhighlighter-code">
agent.Kernel.Plugins.Add(GetCity);
agent.Kernel.Plugins.Add(GetUserAge);
</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:paragraph -->
<p><strong><em>Definire gli arguments nella definizione dell'agent</em></strong></p>
<!-- /wp:paragraph -->

<!-- wp:syntaxhighlighter/code -->
<pre class="wp-block-syntaxhighlighter-code">
ChatCompletionAgent agent = new() // 👈🏼 Definition of the agent
{
    Instructions = "You are an agent who creates funny stories. If you find any 
       information related to the user through plugins or tools, include it in 
       the story to make it more personal and engaging.",
    Name = "Story Agent",
    Description = "This agent can create funny stories based on user input.",
    Kernel = kernel,
    Arguments = new KernelArguments(new PromptExecutionSettings
    {
        FunctionChoiceBehavior = FunctionChoiceBehavior.Auto()
    }) // 👈🏼 Set the function choice behavior to auto
};
</pre>
<!-- /wp:syntaxhighlighter/code -->

<!-- wp:paragraph -->
<p>In questo modo abbiamo detto al nostro agent, che può recuperare informazioni tramite le&nbsp; funzioni che abbiamo definito.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Conclusioni</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Con questo post volevo, condividere come implementare un Agent, e le sue potenzialità..&nbsp; Ovviamente anche io sto ancora studiando e questo progetto di test è in continua evoluzione, per cui vi lascio anche il link al Repository github.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list"><!-- wp:list-item -->
<li>🔗 <a href="https://github.com/f-mantua/MyAgent">MyAgent su GitHub</a></li>
<!-- /wp:list-item --></ul>
<!-- /wp:list -->
