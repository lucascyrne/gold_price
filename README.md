# Gold Price Fetcher

Este projeto é um script em Python que busca o preço do ouro e o apresenta em uma interface gráfica simples.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Quandl**: Biblioteca para obter dados financeiros.
- **PyQt5**: Biblioteca para criação da interface gráfica.
- **Matplotlib**: Biblioteca para visualização de dados.

## Requisitos

- Python 3.x
- Bibliotecas listadas em `requirements.txt`

## Instalação

1. Clone o repositório:

   ```bash
   git clone git@github.com:lucascyrne/gold_price.git
   cd gold-price
   ```

2. Crie um ambiente virtual e ative-o:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure a chave da API do Quandl:
   - Crie um arquivo `config.py` na raiz do projeto com o seguinte conteúdo:
     ```python
     quandl.ApiConfig.api_key = "SUA_CHAVE_DA_API"
     ```

## Uso

Execute o script principal:

```bash
python main.py
```

A interface gráfica será aberta, mostrando o preço do ouro para diferentes intervalos de tempo. Use os botões para selecionar o intervalo desejado.

## Estrutura do Projeto

- `main.py`: Script principal que inicializa a interface gráfica e gerencia as interações.
- `data/data_fetcher.py`: Script responsável por buscar os dados do preço do ouro.
- `utils/`: Diretório contendo scripts auxiliares para formatação de data, tratamento de erros, e gestão de gestos.
- `styles.py`: Arquivo contendo o estilo da interface gráfica.

## Funcionalidades

- **Botões de Intervalo**: Selecione o intervalo de tempo para visualizar o preço do ouro (1 semana, 1 mês, 1 ano, todos os dados).
- **Gráfico Interativo**: Visualize o preço do ouro em um gráfico interativo.
- **Atualização Automática**: O preço do ouro é buscado automaticamente ao iniciar a aplicação.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para obter mais informações.
