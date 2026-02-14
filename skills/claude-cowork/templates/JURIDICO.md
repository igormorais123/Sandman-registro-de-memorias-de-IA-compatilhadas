# ⚖️ Templates Jurídicos

Templates base para documentos jurídicos. Substitua os campos em [BRACKETS].

> ⚠️ **AVISO:** Estes templates são pontos de partida. Sempre revise com advogado antes de usar em processos reais.

---

## 1. Petição Inicial

### 📄 Estrutura Base

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO DA [NÚMERO] VARA [CÍVEL/CRIMINAL/TRABALHISTA/ETC] DA COMARCA DE [CIDADE] - [ESTADO]

[NOME COMPLETO DO AUTOR], [NACIONALIDADE], [ESTADO CIVIL], [PROFISSÃO], portador(a) do RG nº [NÚMERO] e inscrito(a) no CPF sob o nº [NÚMERO], residente e domiciliado(a) na [ENDEREÇO COMPLETO], CEP [NÚMERO], e-mail [EMAIL], vem, respeitosamente, à presença de Vossa Excelência, por seu(sua) advogado(a) infra-assinado(a) (procuração anexa), propor a presente

AÇÃO [TIPO DA AÇÃO]

em face de [NOME COMPLETO DO RÉU], [QUALIFICAÇÃO COMPLETA], residente e domiciliado(a) na [ENDEREÇO COMPLETO], pelos fatos e fundamentos a seguir expostos:

I - DOS FATOS

[Narrar cronologicamente os fatos que deram origem à ação]

II - DO DIREITO

[Fundamentação jurídica com citação de leis, doutrinas e jurisprudências]

Art. [X] do [CÓDIGO/LEI]: "[transcrição do artigo]"

Nesse sentido, a jurisprudência:
"[EMENTA DO JULGADO]" (Tribunal, Número do processo, Relator, Data)

III - DOS PEDIDOS

Ante o exposto, requer:

a) A citação do(a) réu(ré) para, querendo, contestar a presente ação;

b) A procedência total dos pedidos para [ESPECIFICAR CADA PEDIDO];

c) A condenação do(a) réu(ré) ao pagamento de custas processuais e honorários advocatícios;

d) [OUTROS PEDIDOS ESPECÍFICOS];

e) A produção de todas as provas admitidas em direito, especialmente [ESPECIFICAR].

Dá-se à causa o valor de R$ [VALOR] ([VALOR POR EXTENSO]).

Termos em que,
Pede deferimento.

[CIDADE], [DATA].

_______________________________
[NOME DO ADVOGADO]
OAB/[UF] nº [NÚMERO]
```

### 🤖 Prompt para Claude Elaborar

```
Preciso de uma petição inicial com os seguintes dados:

PARTES:
- Autor: [nome, CPF, RG, endereço, profissão, estado civil]
- Réu: [nome, CPF/CNPJ, endereço]

TIPO DE AÇÃO: [ex: indenização, cobrança, divórcio, etc.]

FATOS (me conte a história):
"""
[Descreva o que aconteceu, com datas e detalhes]
"""

VALOR DA CAUSA: R$ [valor]

PEDIDOS ESPECÍFICOS:
[O que você quer que o juiz determine]

Elabore uma petição inicial completa com:
1. Qualificação das partes
2. Fatos narrados cronologicamente
3. Fundamentação jurídica (cite artigos de lei aplicáveis)
4. Pedidos claros e específicos
5. Requerimentos processuais padrão
```

---

## 2. Contestação

### 📄 Estrutura Base

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO DA [NÚMERO] VARA [TIPO] DA COMARCA DE [CIDADE] - [ESTADO]

Processo nº [NÚMERO DO PROCESSO]

[NOME COMPLETO DO RÉU], já qualificado(a) nos autos da AÇÃO [TIPO] que lhe move [NOME DO AUTOR], vem, respeitosamente, à presença de Vossa Excelência, por seu(sua) advogado(a) infra-assinado(a), apresentar

CONTESTAÇÃO

nos termos do art. 335 e seguintes do CPC, pelos fatos e fundamentos a seguir expostos:

I - SÍNTESE DA INICIAL

[Breve resumo do que o autor alega]

II - PRELIMINARES (se houver)

[Ex: Inépcia da inicial, ilegitimidade, incompetência, etc.]

III - NO MÉRITO

[Refutação ponto a ponto das alegações do autor]

3.1 - Da improcedência do pedido de [X]
[Argumentação]

3.2 - Da inexistência de [Y]
[Argumentação]

IV - DOS PEDIDOS

Ante o exposto, requer:

a) O acolhimento das preliminares arguidas, com a extinção do feito sem resolução do mérito;

b) Caso superadas as preliminares, a total improcedência dos pedidos formulados na inicial;

c) A condenação do(a) autor(a) ao pagamento das custas processuais e honorários advocatícios;

d) A produção de todas as provas admitidas em direito.

Termos em que,
Pede deferimento.

[CIDADE], [DATA].

_______________________________
[NOME DO ADVOGADO]
OAB/[UF] nº [NÚMERO]
```

### 🤖 Prompt para Claude Elaborar

```
Preciso contestar uma ação. Dados:

PROCESSO: [número]
TIPO DE AÇÃO: [tipo]
AUTOR: [nome]
RÉU (meu cliente): [nome]

O QUE O AUTOR ALEGA:
"""
[Resuma os principais pontos da petição inicial]
"""

NOSSA VERSÃO DOS FATOS:
"""
[Conte a versão do seu cliente]
"""

PONTOS FRACOS DA INICIAL (se identificados):
[Liste inconsistências, falta de provas, etc.]

PROVAS QUE TEMOS:
[Liste documentos, testemunhas, etc.]

Elabore uma contestação com:
1. Síntese da inicial
2. Preliminares (se cabíveis)
3. Refutação ponto a ponto no mérito
4. Pedidos adequados
```

---

## 3. Recurso de Apelação

### 📄 Estrutura Base

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO DA [NÚMERO] VARA [TIPO] DA COMARCA DE [CIDADE] - [ESTADO]

Processo nº [NÚMERO DO PROCESSO]

[NOME DO APELANTE], já qualificado(a) nos autos, inconformado(a) com a r. sentença de fls. [X], vem, respeitosamente, interpor

RECURSO DE APELAÇÃO

requerendo seja o presente recebido e processado, remetendo-se os autos ao Egrégio Tribunal de Justiça do Estado de [UF], onde serão apresentadas as razões recursais.

Termos em que,
Pede deferimento.

[CIDADE], [DATA].

_______________________________
[NOME DO ADVOGADO]
OAB/[UF] nº [NÚMERO]

---

EGRÉGIO TRIBUNAL DE JUSTIÇA DO ESTADO DE [UF]
COLENDA CÂMARA CÍVEL

RAZÕES DE APELAÇÃO

Processo nº [NÚMERO]
Apelante: [NOME]
Apelado: [NOME]

I - DA TEMPESTIVIDADE

O presente recurso é tempestivo, tendo em vista que a intimação da sentença ocorreu em [DATA], sendo o prazo de 15 dias úteis encerrado em [DATA].

II - DO CABIMENTO

O recurso de apelação é cabível contra sentença, nos termos do art. 1.009 do CPC.

III - DA SÍNTESE PROCESSUAL

[Breve histórico do processo]

IV - DA SENTENÇA RECORRIDA

[Resumo da decisão e seus fundamentos]

V - DAS RAZÕES DO INCONFORMISMO

5.1 - [PRIMEIRO ARGUMENTO]
[Desenvolvimento]

5.2 - [SEGUNDO ARGUMENTO]
[Desenvolvimento]

VI - DO PREQUESTIONAMENTO

Para fins de prequestionamento, indica-se violação aos seguintes dispositivos: [ARTIGOS].

VII - DOS PEDIDOS

Ante o exposto, requer:

a) O recebimento e processamento do presente recurso;

b) O provimento da apelação para reformar a sentença, [ESPECIFICAR O QUE SE PRETENDE];

c) A condenação do apelado ao pagamento das custas e honorários.

[CIDADE], [DATA].

_______________________________
[NOME DO ADVOGADO]
OAB/[UF] nº [NÚMERO]
```

### 🤖 Prompt para Claude Elaborar

```
Preciso recorrer de uma sentença. Dados:

PROCESSO: [número]
VARA/COMARCA: [identificação]
PARTES: Apelante [nome] x Apelado [nome]

DATA DA INTIMAÇÃO: [data]

A SENTENÇA DECIDIU:
"""
[Resuma o que o juiz decidiu]
"""

POR QUE DISCORDAMOS:
"""
[Explique os pontos de discordância]
"""

O QUE QUEREMOS NO RECURSO:
[Reforma total, parcial, anulação?]

FUNDAMENTOS LEGAIS QUE PODEMOS USAR:
[Se souber, liste artigos violados]

Elabore a apelação com:
1. Petição de interposição
2. Razões recursais completas
3. Argumentação jurídica sólida
4. Prequestionamento
5. Pedidos claros
```

---

## 4. Contrato de Prestação de Serviços

### 📄 Template Completo

```
CONTRATO DE PRESTAÇÃO DE SERVIÇOS

IDENTIFICAÇÃO DAS PARTES

CONTRATANTE: [NOME/RAZÃO SOCIAL], [pessoa física/jurídica], inscrito(a) no [CPF/CNPJ] sob o nº [NÚMERO], com sede/residente em [ENDEREÇO COMPLETO], doravante denominado(a) CONTRATANTE.

CONTRATADO(A): [NOME/RAZÃO SOCIAL], [pessoa física/jurídica], inscrito(a) no [CPF/CNPJ] sob o nº [NÚMERO], com sede/residente em [ENDEREÇO COMPLETO], doravante denominado(a) CONTRATADO(A).

As partes acima identificadas têm, entre si, justo e acertado o presente Contrato de Prestação de Serviços, que se regerá pelas cláusulas seguintes e pelas condições descritas no presente.

CLÁUSULA 1ª - DO OBJETO

O presente contrato tem como objeto a prestação de serviços de [DESCRIÇÃO DETALHADA DOS SERVIÇOS], conforme especificações abaixo:

a) [SERVIÇO/ENTREGÁVEL 1];
b) [SERVIÇO/ENTREGÁVEL 2];
c) [SERVIÇO/ENTREGÁVEL 3].

CLÁUSULA 2ª - DO PRAZO

O presente contrato terá vigência de [PERÍODO], com início em [DATA_INÍCIO] e término em [DATA_FIM], podendo ser prorrogado mediante termo aditivo assinado por ambas as partes.

CLÁUSULA 3ª - DO VALOR E FORMA DE PAGAMENTO

3.1 - Pela prestação dos serviços objeto deste contrato, o(a) CONTRATANTE pagará ao(à) CONTRATADO(A) o valor total de R$ [VALOR] ([VALOR POR EXTENSO]).

3.2 - O pagamento será efetuado da seguinte forma:
[  ] À vista, até [DATA]
[  ] Em [X] parcelas de R$ [VALOR], com vencimento em [DATAS]
[  ] [OUTRA FORMA]

3.3 - Dados bancários para pagamento:
Banco: [BANCO]
Agência: [AGÊNCIA]
Conta: [CONTA]
PIX: [CHAVE]
Titular: [NOME]

3.4 - Em caso de atraso, incidirá multa de [X]% e juros de [Y]% ao mês.

CLÁUSULA 4ª - DAS OBRIGAÇÕES DO CONTRATANTE

a) Fornecer as informações necessárias à execução dos serviços;
b) Efetuar os pagamentos nas datas acordadas;
c) [OUTRAS OBRIGAÇÕES ESPECÍFICAS].

CLÁUSULA 5ª - DAS OBRIGAÇÕES DO CONTRATADO

a) Executar os serviços conforme especificado;
b) Cumprir os prazos estabelecidos;
c) Manter sigilo sobre informações confidenciais;
d) [OUTRAS OBRIGAÇÕES ESPECÍFICAS].

CLÁUSULA 6ª - DA CONFIDENCIALIDADE

As partes se comprometem a manter sigilo sobre todas as informações confidenciais trocadas em razão deste contrato, durante sua vigência e pelo período de [X] anos após seu término.

CLÁUSULA 7ª - DA RESCISÃO

7.1 - O presente contrato poderá ser rescindido:
a) Por acordo entre as partes;
b) Por descumprimento de qualquer cláusula;
c) Por qualquer das partes, mediante aviso prévio de [X] dias.

7.2 - Em caso de rescisão por culpa de uma das partes, a parte culpada pagará multa de [X]% do valor total do contrato.

CLÁUSULA 8ª - DA PROPRIEDADE INTELECTUAL

[DEFINIR A QUEM PERTENCERÁ O RESULTADO DO TRABALHO]

CLÁUSULA 9ª - DO FORO

Fica eleito o foro da Comarca de [CIDADE/UF] para dirimir quaisquer dúvidas oriundas do presente contrato, com renúncia expressa a qualquer outro, por mais privilegiado que seja.

E por estarem assim justos e contratados, firmam o presente instrumento em 2 (duas) vias de igual teor.

[CIDADE], [DATA].

_______________________________
CONTRATANTE
[NOME]
[CPF/CNPJ]

_______________________________
CONTRATADO(A)
[NOME]
[CPF/CNPJ]

TESTEMUNHAS:

1. _______________________________
   Nome:
   CPF:

2. _______________________________
   Nome:
   CPF:
```

### 🤖 Prompt para Claude Adaptar

```
Preciso de um contrato de prestação de serviços:

CONTRATANTE: [nome, CPF/CNPJ, endereço]
CONTRATADO: [nome, CPF/CNPJ, endereço]

SERVIÇO A SER PRESTADO:
"""
[Descreva detalhadamente o que será feito]
"""

VALOR: R$ [valor]
FORMA DE PAGAMENTO: [à vista, parcelado, por entrega, etc.]

PRAZO: [duração do contrato]

NECESSIDADES ESPECIAIS:
- [ ] Cláusula de exclusividade
- [ ] Cláusula de não-concorrência
- [ ] Cláusula de confidencialidade reforçada
- [ ] Multa por rescisão: [%]
- [ ] Propriedade intelectual: [cliente/prestador/compartilhada]
- [ ] [outras necessidades]

Adapte o contrato modelo incluindo todas as cláusulas necessárias.
```

---

## 5. Procuração Ad Judicia

### 📄 Template

```
PROCURAÇÃO AD JUDICIA

OUTORGANTE: [NOME COMPLETO], [nacionalidade], [estado civil], [profissão], portador(a) do RG nº [NÚMERO], inscrito(a) no CPF sob o nº [NÚMERO], residente e domiciliado(a) na [ENDEREÇO COMPLETO], CEP [NÚMERO].

OUTORGADO(A): [NOME DO ADVOGADO], advogado(a), inscrito(a) na OAB/[UF] sob o nº [NÚMERO], com escritório profissional na [ENDEREÇO COMPLETO], onde recebe intimações.

PODERES: Por este instrumento particular de procuração, o(a) OUTORGANTE nomeia e constitui seu(sua) bastante procurador(a) o(a) OUTORGADO(A), a quem confere amplos poderes para o foro em geral, com a cláusula "AD JUDICIA ET EXTRA", para representá-lo(a) em qualquer Juízo, Instância ou Tribunal, podendo propor ações, contestar, reconvir, transigir, desistir, renunciar, receber e dar quitação, firmar compromissos, acordos, receber citações e intimações, interpor recursos, substabelecer com ou sem reserva de poderes, e praticar todos os demais atos necessários ao fiel cumprimento deste mandato.

FINALIDADE: [ESPECIFICAR SE FOR PARA PROCESSO ESPECÍFICO]
Processo nº: [NÚMERO, se aplicável]
Vara/Tribunal: [IDENTIFICAÇÃO, se aplicável]

[CIDADE], [DATA].

_______________________________
[NOME DO OUTORGANTE]
[CPF]
```

### 📄 Procuração Particular (fins diversos)

```
PROCURAÇÃO PARTICULAR

OUTORGANTE: [NOME COMPLETO], [nacionalidade], [estado civil], [profissão], portador(a) do RG nº [NÚMERO], inscrito(a) no CPF sob o nº [NÚMERO], residente e domiciliado(a) na [ENDEREÇO COMPLETO].

OUTORGADO(A): [NOME COMPLETO], [nacionalidade], [estado civil], [profissão], portador(a) do RG nº [NÚMERO], inscrito(a) no CPF sob o nº [NÚMERO], residente e domiciliado(a) na [ENDEREÇO COMPLETO].

PODERES: O(A) OUTORGANTE, pelo presente instrumento, nomeia e constitui seu(sua) bastante procurador(a) o(a) acima qualificado(a), conferindo-lhe poderes para, em seu nome:

[ESPECIFICAR OS PODERES, ex:]
- Representá-lo(a) perante [ÓRGÃO/EMPRESA];
- Assinar documentos relativos a [ASSUNTO];
- Receber valores até o montante de R$ [VALOR];
- [OUTROS PODERES ESPECÍFICOS].

PRAZO: Esta procuração é válida por [PERÍODO/até revogação expressa].

[CIDADE], [DATA].

_______________________________
[NOME DO OUTORGANTE]

TESTEMUNHAS:

1. _______________________________
   Nome:
   CPF:

2. _______________________________
   Nome:
   CPF:
```

### 🤖 Prompt para Claude Gerar

```
Preciso de uma procuração:

TIPO: [ ] Ad Judicia (para advogado) [ ] Particular (outros fins)

OUTORGANTE (quem dá os poderes):
[nome completo, CPF, RG, endereço, profissão, estado civil]

OUTORGADO (quem recebe os poderes):
[nome completo, CPF, RG, endereço, profissão/OAB]

FINALIDADE:
[Descreva para que serve a procuração]

PODERES ESPECÍFICOS NECESSÁRIOS:
[Liste o que a pessoa poderá fazer em seu nome]

PRAZO: [determinado/indeterminado]

Gere a procuração adequada ao caso.
```

---

## 6. Notificação Extrajudicial

### 📄 Template

```
NOTIFICAÇÃO EXTRAJUDICIAL

NOTIFICANTE: [NOME COMPLETO OU RAZÃO SOCIAL], [CPF/CNPJ], com endereço na [ENDEREÇO COMPLETO].

NOTIFICADO(A): [NOME COMPLETO OU RAZÃO SOCIAL], [CPF/CNPJ], com endereço na [ENDEREÇO COMPLETO].

Pelo presente instrumento, o(a) NOTIFICANTE vem, formal e respeitosamente, NOTIFICAR Vossa Senhoria sobre o que segue:

1. DOS FATOS

[Descrever a situação que originou a notificação, com datas e detalhes relevantes]

2. DO DIREITO

[Fundamentação legal, se aplicável]

3. DA NOTIFICAÇÃO

Diante do exposto, NOTIFICA-SE Vossa Senhoria para, no prazo de [X] dias a contar do recebimento desta:

a) [AÇÃO REQUERIDA 1];
b) [AÇÃO REQUERIDA 2];
c) [AÇÃO REQUERIDA 3].

4. DAS CONSEQUÊNCIAS

O não atendimento desta notificação no prazo estipulado acarretará a adoção das medidas judiciais cabíveis, sem necessidade de novo aviso, podendo o(a) NOTIFICANTE:

[  ] Ingressar com ação judicial competente;
[  ] Inscrever o nome do(a) NOTIFICADO(A) em cadastros de proteção ao crédito;
[  ] Comunicar aos órgãos competentes;
[  ] [OUTRAS CONSEQUÊNCIAS].

5. DA PROVA

Esta notificação comprova a ciência inequívoca do(a) NOTIFICADO(A) sobre os fatos e obrigações aqui descritos, servindo como prova pré-constituída para eventual ação judicial.

[CIDADE], [DATA].

_______________________________
[NOME DO NOTIFICANTE]
[CPF/CNPJ]

---
COMPROVANTE DE RECEBIMENTO

Recebi a presente notificação em [DATA].

_______________________________
[NOME DO NOTIFICADO]
ou representante legal
```

### 🤖 Prompt para Claude Elaborar

```
Preciso enviar uma notificação extrajudicial:

NOTIFICANTE (quem envia): [nome, CPF/CNPJ, endereço]
NOTIFICADO (quem recebe): [nome, CPF/CNPJ, endereço]

SITUAÇÃO:
"""
[Descreva detalhadamente o problema]
"""

O QUE QUERO QUE A PESSOA FAÇA:
[Liste as ações exigidas]

PRAZO PARA CUMPRIMENTO: [dias]

O QUE FAREI SE NÃO CUMPRIR:
[Processo, Serasa, denúncia, etc.]

TOM DESEJADO: [formal/firme/diplomático]

Elabore uma notificação extrajudicial clara e juridicamente adequada.
```

---

## ⚠️ Avisos Importantes

1. **Não substitui advogado** - Use como ponto de partida, não como produto final
2. **Revise sempre** - Cada caso tem peculiaridades
3. **Atualize as leis** - A legislação muda
4. **Consulte um profissional** - Para processos reais, contrate advogado

---

*Templates jurídicos para uso com Claude | Versão base para adaptação*
