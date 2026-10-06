# Publicação e diagnóstico

## Antes da mudança

Revise o diff, execute os controles do README e abra as páginas localmente. Teste a navegação em tela pequena, o menu por teclado, o formulário, o retorno à página inicial e os vídeos. Abrir o link do WhatsApp não comprova que uma mensagem foi enviada.

Registre o commit anterior e confira no GitHub qual branch/pasta ou workflow alimenta o Pages. A existência de `.nojekyll` não comprova a configuração atual do serviço. Os controles acrescentados a este repositório fazem validação e não alteram a configuração de hospedagem.

## Depois da publicação

1. Verifique o status da execução de Pages no GitHub.
2. Abra a URL pública indicada pelo próprio Pages, incluindo uma página de segmento e `/links/`.
3. Confira carregamento de CSS/JavaScript, console do navegador e respostas HTTP de arquivos.
4. Teste o formulário com dados fictícios e confira o texto gerado antes de qualquer envio.
5. Registre o commit publicado e o resultado das verificações.

## Investigação de falhas

| Sintoma | Onde começar |
| --- | --- |
| HTML abre, CSS falha | Caminho relativo, nome do arquivo e resposta da requisição |
| Página interna retorna 404 | Caminho da pasta, `index.html`, maiúsculas/minúsculas e base da URL |
| Vídeo não aparece | Permissões do Drive, URL de preview e mensagens de CSP no navegador |
| Formulário não abre WhatsApp | Validação dos campos, JavaScript e bloqueio de pop-up |
| Mudança não aparece | Commit publicado, execução de Pages e cache do navegador |

## Retorno

Identifique o commit que introduziu a falha. Prepare a reversão dessa mudança em branch e Pull Request, preservando alterações posteriores de outras pessoas. Depois de revisar, publique pela mesma configuração de Pages e repita as verificações. Não reescreva o histórico da branch para recuperar uma versão.

## Evidências de portfólio

Ao apresentar o projeto, mostre um Pull Request, a execução do CI, a organização dos arquivos e uma demonstração real. Qualquer resultado de performance ou acessibilidade deve registrar a ferramenta, a data e o cenário de medição. Os controles atuais não geram uma nota de Lighthouse nem comprovam acessibilidade completa.
