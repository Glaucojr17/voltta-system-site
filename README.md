# VOLTTA System — site institucional

Site da VOLTTA System, desenvolvido para apresentar as soluções da empresa, explicar sua aplicação em diferentes segmentos e encaminhar interessados para uma conversa pelo WhatsApp. Inclui páginas para mercadinhos, restaurantes, hotéis e salões, além de uma central de links.

Este repositório contém o frontend institucional. O painel exibido na página inicial é ilustrativo; o ERP e os serviços de negócio são projetos separados.

## Tecnologias e decisões

- HTML, CSS e JavaScript sem framework ou etapa de build da aplicação.
- Arquivos estáticos compatíveis com GitHub Pages.
- Formulário com validação no navegador e montagem de mensagem para WhatsApp; não há API de cadastro neste repositório.
- Navegação responsiva, link para pular ao conteúdo, controle de menu por teclado e tratamento de preferência por movimento reduzido.
- Política de conteúdo declarada no HTML e permissão específica de iframe do Google Drive nas páginas com vídeos.

Essas escolhas mantêm a publicação simples e reduzem a quantidade de componentes a sustentar. O custo dessa abordagem é a repetição de parte da estrutura entre páginas, que precisa ser considerada ao alterar menus, contatos e estilos.

## Executar localmente

```bash
git clone https://github.com/Glaucojr17/voltta-system-site.git
cd voltta-system-site
python3 -m http.server 8000 --bind 127.0.0.1
```

Acesse `http://127.0.0.1:8000`. Execute o comando na raiz do repositório para manter os caminhos relativos dos arquivos. Não é necessário `npm install`.

## Estrutura

| Caminho | Responsabilidade |
| --- | --- |
| `index.html` | Apresentação, soluções, segmentos e formulário |
| `assets/styles.css` | Identidade visual e estilos principais |
| `assets/script.js` | Menu, animações e encaminhamento ao WhatsApp |
| `segmentos/` | Páginas específicas, com vídeos incorporados |
| `links/index.html` | Central de acesso aos recursos da empresa |
| `404.html` | Página de erro estática |
| `tools/check_site.py` | Verificação local de links, arquivos e metadados |
| `.github/workflows/validate.yml` | Pipeline de validação, sem deploy |

## Verificar antes de publicar

Requisitos dos controles: Python 3.10+ e Node.js. O site continua sem dependências de build.

```bash
python3 -m unittest discover -s tests -v
python3 tools/check_site.py
node --check assets/script.js
```

O verificador examina arquivos e âncoras referenciados pelo HTML, título, idioma, viewport e presença de um H1 por página. Ele conhece o prefixo `/voltta-system-site/` usado nos links absolutos da página 404; em outra configuração de Pages, ajuste `--base-path`. Os testes incluem casos válidos e falhas deliberadas. URLs externas não são acessadas; CSS, contraste, layout, entrega de mensagens e comportamento em navegador exigem verificação separada.

O workflow repete esses controles em pushes e Pull Requests. Ele não publica o site e não substitui a configuração de Pages da conta.

## Manutenção e limites conhecidos

- A validação do formulário acontece no navegador. A pessoa precisa concluir o envio no WhatsApp.
- Os vídeos dependem da disponibilidade e das permissões dos arquivos no Google Drive.
- Existem diretivas `noindex, nofollow` nas páginas. A decisão de indexação deve ser revista antes de uma campanha de busca orgânica; elas foram preservadas nesta melhoria de documentação.
- Não há backend, banco de dados, testes de navegador ou métricas de performance aferidas neste repositório.
- Consulte o [runbook de publicação e recuperação](docs/OPERACAO.md) para a sequência de verificações.

Autor: [Glauco Junior](https://github.com/Glaucojr17). Este projeto demonstra desenvolvimento web, organização de uma entrega estática e controles automatizados de qualidade.
