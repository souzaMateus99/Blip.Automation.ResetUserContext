# Blip.Script.ResetUserContext
Esse script reinicia o contexto e deleta todas as variáveis dos usuários da plataforma de chatbot da [take blip](https://www.take.net/blip/)
## Como usar
Para usar esse script basta adicionar os dados requeridos pelo [arquivo de configuração](configuration/config.json)

> ℹ️ Esse arquivo de configuração utiliza a estrutura [json](https://www.devmedia.com.br/o-que-e-json/23166)

> ⚠️ Não alterar a estrutura original do arquivo de configuração

### Dados para colocar no arquivo de configuração
- **bot -> authorizationKeys** `(string array)`: Chaves de autenticações dos bots que o usuário será reiniciado
- **user -> userIds** `(string array)`: IDs de usuários que terão os contextos reiniciados
- **user -> isClearAll** `(boolean: true|false)`: Se é para limpar **TODOS** os usuários localizados no chatbot
  - > ℹ️ Caso essa propriedade esteja com valor `true` (verdadeiro), será ignorado os IDs de usuários que estarão na propriedade `userIds` e o script buscará e limpará o contexto de todos os usuários que entraram em contato com o chatbot