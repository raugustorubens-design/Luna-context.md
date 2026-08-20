# O terminal do Forge como cockpit de verdade

**19/08/2026 · nota de desenho, antes de virar pacote**

---

## O que a sua captura já mostra

```
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
```

O shell está de pé, mas **sem controle de trabalho**. Na prática:

- `Ctrl+C` não interrompe o processo em primeiro plano de forma confiável
- `Ctrl+Z`, `fg`, `bg` não funcionam
- Programa interativo — `psql`, `gh auth login`, editor de texto — se comporta mal ou trava
- Processo que continua rodando depois de você fechar a aba fica órfão

**É o primeiro item.** Sem isso, qualquer ferramenta que a gente instale vai funcionar pela
metade. A causa é o pseudo-terminal não estar sendo alocado como sessão com terminal de
controle — coisa de configuração do processo, não de biblioteca nova.

---

## O que falta para rodar o que o VS Code roda

### 1 · As ferramentas precisam estar na imagem

`/app` é o contêiner de produção construído pelo nixpacks. **O que for instalado à mão some
no próximo deploy.**

Então `gh`, `railway`, `supabase`, `psql` e companhia entram no `Dockerfile` ou na
configuração do nixpacks — não por `npm install -g` numa sessão.

O `git` e o `node`/`pnpm` já estão. O resto não.

### 2 · Credenciais como variável de ambiente

Cada ferramenta lê a sua:

| Ferramenta | Lê |
|---|---|
| `gh` | `GH_TOKEN` |
| `railway` | `RAILWAY_TOKEN` |
| `supabase` | `SUPABASE_ACCESS_TOKEN` |
| `psql` | string de conexão |

**Nenhuma dessas deve ficar no repositório.** Vão no painel do Railway, como as chaves de
API que já estão lá.

### 3 · O `/app` provavelmente não é um clone

O Explorer mostra `.github` e `.gitignore`, mas deploy por nixpacks costuma copiar arquivos
sem trazer o `.git`. **Sem `.git` e sem remoto configurado, não há `git push` nem
`git status` útil.**

Conferir isso é o primeiro comando a rodar: se `git status` responder *"not a git
repository"*, o cockpit precisa de um clone próprio, num diretório separado do build.

---

## O problema que eu levantaria antes de construir

**O VS Code roda na sua máquina. Isto roda no servidor que atende o seu produto.**

Com `gh`, `railway` e `supabase` autenticados nesse terminal, quem tiver acesso a ele tem:

- Escrita em todos os seus repositórios
- Controle da infraestrutura — incluindo apagar serviço e banco
- Acesso ao banco de produção, com dado de ronda e, em breve, dado de cliente

E o que separa isso da internet é **um login do Google com um e-mail na allowlist**.

Não é alarmismo: é medir o raio. Hoje, um `rm -rf` distraído ou uma migração errada derruba
o produto, porque o terminal está **dentro** do contêiner que serve as páginas.

### O que eu recomendaria

**Um serviço separado no Railway para o cockpit.** Mesmas ferramentas, mesmas credenciais,
mas isolado: se algo der errado ali, o `luna-frontend` continua servindo.

Custa um serviço a mais e resolve o pior cenário. E como o Forge acessa o terminal por
WebSocket, apontar para outro endereço é mudança pequena — bem menor que fazer depois.

**Se preferir manter no mesmo contêiner**, então valem duas travas mínimas:

- Credencial de escrita **só na sessão**, entregue quando você pede, não permanente no
  ambiente
- Uma lista curta de comandos bloqueados, do tipo que apaga infraestrutura sem confirmação

Nenhuma das duas é perfeita. A separação de serviço é.

---

## Ordem que faz sentido

**1 · Controle de trabalho no shell.** Sem isso o resto funciona pela metade, e é o menor
dos itens.

**2 · Verificar se `/app` é um clone.** Um comando. Define se o cockpit precisa de diretório
próprio.

**3 · Decidir onde o cockpit roda** — mesmo contêiner ou serviço separado. É sua, e muda o
que se constrói depois.

**4 · `gh` e `git` com credencial.** É o que você mais usa, e o que fecha o laço com o
Builder: revisar PR, abrir Issue, conferir estado, tudo de dentro do Forge.

**5 · `railway` e `supabase`.** Depois, e com a decisão do item 3 tomada — são as duas com
maior poder de estrago.

O item 4 sozinho já entrega boa parte do valor: hoje você alterna entre o Forge, o GitHub no
celular e o painel do Railway. Com `gh` no terminal, uma coisa a menos.

---

## O que decidir antes do pacote

**Serviço separado ou mesmo contêiner?** É a única que trava o desenho. As outras seguem
de qualquer jeito.

Minha recomendação é serviço separado, e o argumento é simples: o dia em que um comando
errado derrubar o produto vai custar mais que o serviço a mais custa por ano.
