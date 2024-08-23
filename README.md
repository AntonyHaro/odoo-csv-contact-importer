# Importador de Contatos para Odoo

Este repositório contém um script Python que importa contatos a partir de um arquivo CSV para o Odoo usando a API XML-RPC. O script autentica-se com o servidor Odoo, lê o arquivo CSV, valida os dados, mapeia os países e estados para seus respectivos IDs, e cria os contatos na base de dados do Odoo.

## Índice

- [Requisitos](#requisitos)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do CSV](#estrutura-do-csv)
- [Funcionalidades](#funcionalidades)
- [Erros Comuns e Soluções](#erros-comuns-e-soluções)
- [Contribuição](#contribuição)

## Requisitos

- Python 3.6 ou superior
- Biblioteca `xmlrpc.client` 
- Biblioteca `python-dotenv` para carregar variáveis de ambiente de um arquivo `.env`
- Servidor Odoo acessível via API XML-RPC

## Configuração

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/odoo-contact-importer.git
   cd odoo-contact-importer
   ```

2. **Instale as dependências:**

   Utilize `pip` para instalar a biblioteca `python-dotenv`:

   ```bash
   pip install python-dotenv
   ```

3. **Configurar variáveis de ambiente:**

   Crie um arquivo `.env` na raiz do projeto com as seguintes informações:

   ```bash
   ODOO_URL=https://seu-odoo.com
   ODOO_DB=nome_do_banco
   ODOO_USERNAME=seu_usuario@dominio.com
   ODOO_PASSWORD=sua_senha
   ```

   Certifique-se de substituir os valores com suas informações de acesso ao Odoo.

## Uso

1. **Prepare seu arquivo CSV:**

   Certifique-se de que seu arquivo CSV (`file.csv`) está formatado corretamente. Veja a [estrutura do CSV](#estrutura-do-csv) para mais detalhes.

2. **Execute o script:**

   No diretório do projeto, execute o script.

3. **Verifique a saída:**

   O script irá autenticar com o servidor Odoo, ler o arquivo CSV, validar os dados e tentar criar cada contato. Ele imprimirá no terminal o status de cada operação.

## Estrutura do CSV

O arquivo CSV deve ter a seguinte estrutura de cabeçalhos (em qualquer ordem):

- `name`: Nome do contato (obrigatório)
- `is_company`: Se é uma empresa (verdadeiro/falso)
- `company_name`: Nome da empresa (se aplicável)
- `country_name`: Nome do país (obrigatório)
- `state_name`: Nome do estado
- `zip`: Código postal
- `city`: Cidade
- `street`: Endereço
- `phone`: Telefone
- `mobile`: Celular
- `email`: E-mail (obrigatório)
- `vat`: Número de VAT 

### Exemplo de CSV:

```csv
name,is_company,company_name,country_name,state_name,zip,city,street,phone,mobile,email,vat
John Doe,false,,United States,California,90001,Los Angeles,123 Main St.,555-1234,555-5678,johndoe@example.com,US123456789
```

## Funcionalidades

- **Autenticação com o Odoo:** O script se autentica usando a API XML-RPC.
- **Leitura e validação de CSV:** Lê um arquivo CSV e valida os registros, ignorando aqueles que não possuem informações essenciais.
- **Mapeamento de País e Estado:** Mapeia os nomes de países e estados para seus IDs no Odoo.
- **Criação de contatos:** Cria os contatos válidos na base de dados do Odoo.

## Erros Comuns e Soluções

- **Erro de Autenticação:** Verifique se as credenciais e a URL no arquivo `.env` estão corretas.
- **Arquivo CSV não encontrado:** Certifique-se de que o arquivo CSV está no diretório correto ou forneça o caminho completo.
- **País ou Estado não encontrado:** Verifique se os nomes de país e estado no CSV correspondem exatamente aos registros no Odoo.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

1. Faça um fork do projeto
2. Crie sua feature branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Faça o push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---
👤👤👤 | 💼📈🤝