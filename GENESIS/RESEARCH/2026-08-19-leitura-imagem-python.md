# Leitura de imagem em Python — o que dá e o que não dá

**19/08/2026 · nota de escopo**

Sua regra do Sense vale aqui inteira: **lógica determinística, IA só onde não é coberta.**
E boa parte do que hoje se pede ao modelo não precisa de modelo.

---

## O que Python resolve sem IA nenhuma

### Procedência — EXIF

Data e hora reais da captura, coordenadas de GPS, orientação, modelo do aparelho.

**Isso é valor de auditoria, não conveniência.** Uma foto com coordenada e horário
carimbados prova onde e quando o achado foi registrado. Hoje o relatório afirma; com EXIF,
ele demonstra.

*Ressalva:* coordenada de planta de cliente é dado sensível. Guardar sim, **exibir no
relatório só se o cliente quiser** — e nunca no material de nível gratuito.

### Qualidade — antes de virar evidência

- **Foco**, por variância do laplaciano — foto tremida não serve de prova
- **Exposição** — escura ou estourada demais, o achado não aparece
- **Proporção** — detecta panorâmica, e é o que decide o teto de 1280 ou 2000 px

Isso permite avisar **na hora**: *"esta foto está desfocada, quer refazer?"* — enquanto a
pessoa ainda está na frente do problema. Refazer em campo custa dez segundos; descobrir na
revisão custa uma volta à planta.

### Duplicata — por impressão perceptual

Compara fotos por semelhança visual, não por bytes. Detecta *"esta é a mesma foto do achado
3"* mesmo com enquadramento levemente diferente.

Resolve um problema real da ronda longa: a mesma condição fotografada duas vezes em pontos
diferentes da caminhada.

### Texto na imagem — OCR

**É o mais forte para o seu domínio**, e é o que eu construiria primeiro.

Placa de equipamento, etiqueta de inspeção de extintor, data de validade, número de série,
identificação de painel. Tudo isso é **texto impresso em superfície plana** — o caso em que
o reconhecimento acerta bem.

E aí liga direto com o Sense: OCR lê `VALIDADE 03/2026` na etiqueta do extintor →
comparação de data → **vencido**. Sinal completo, com evidência citável, e **zero chamada de
modelo**.

### Código de barras e QR

Se os ativos tiverem etiqueta, a foto passa a identificar o equipamento sozinha. Amarra o
achado ao ativo sem ninguém digitar.

---

## O que Python não faz sem modelo

Julgamento sobre a cena:

- *"o trabalhador está sem cinto"*
- *"o guarda-corpo está irregular"*
- *"há material empilhado além da altura segura"*

Isso é percepção semântica. Não há biblioteca determinística que resolva — e tentar por
regra de cor ou forma produz falso positivo em quantidade que destrói a confiança no aviso.

**Aqui a IA fica**, e é o lugar certo dela: entrada suja, saída interpretada, com o humano
ratificando.

---

## O que isso muda no custo

Hoje toda foto vai ao modelo. Com a camada determinística antes:

- Foto desfocada nem chega a ser lida — o modelo não é chamado
- Duplicata não é lida duas vezes
- Etiqueta com validade legível resolve por OCR e regra de data

**A cota do Groq deixa de ser o gargalo**, e a taxa de cobertura determinística — o
indicador de saúde que você definiu para o Sense — passa a ter de onde subir.

---

## Onde isso roda

**No cliente ou no servidor?** As duas, com destinos diferentes:

| Verificação | Onde | Por quê |
|---|---|---|
| Foco, exposição, proporção | **cliente** | Precisa avisar antes de anexar. E não gasta rede |
| Duplicata na mesma ronda | **cliente** | Compara com o que já está na tela |
| EXIF | **cliente**, preservado no envio | Hoje a compressão descarta os metadados |
| OCR | **servidor** | Biblioteca pesada demais para o navegador |
| Código de barras | cliente | Leve, e dá resposta imediata |

**Um alerta:** a compressão atual redesenha a foto num canvas, e isso **apaga o EXIF**. Se
quiser procedência, os metadados precisam ser lidos **antes** de comprimir e viajar
separados. É mudança pequena e fácil de esquecer.

---

## O que eu construiria primeiro

**1 · EXIF preservado.** Data, hora e coordenada de cada foto. Barato, e transforma o
relatório de afirmação em demonstração.

**2 · Aviso de foco e exposição no cliente.** Evita evidência inútil, e o ganho aparece na
primeira ronda.

**3 · OCR de etiqueta.** É onde o seu domínio ganha mais — e é o primeiro sinal do Sense que
funciona sem depender de dado que ainda não existe.

O item 3 sozinho já entrega uma coisa que a IA de hoje não faz: **ler a validade e comparar
com a data**, com evidência citável e resposta defensável em auditoria.

---

## Uma nota sobre modelo local

Existe a opção de rodar um modelo de visão na sua própria infraestrutura, em vez do Groq.
Tira a dependência e a cota, mas troca por custo de máquina e manutenção.

**Não vale agora.** O Groq resolve, e a camada determinística acima reduz muito mais chamada
do que trocar de provedor reduziria custo.
