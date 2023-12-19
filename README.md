# esi-next-hit

Projeto final para a disciplina de Engenharia de Sistemas de Informação (EACH - USP, 2023). A aplicação em questão é uma versão bem simplificada de um "Spotify".

# Setup

É necessário ter **Python 3.10** ou mais recente instalado.

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
```

```bash
. venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```

Agora, faça o setup da aplicação com o seguinte comando:

```bash
python setup.py
```

# Execução

Para executar a aplicação, você precisará iniciar tanto o servidor (_backend_) quanto o cliente (_frontend_).

## Servidor

Para iniciar o servidor, execute o seguinte comando:

```bash
python backend.py
```

## Cliente

Para iniciar o cliente, execute o seguinte comando:

```bash
python -m streamlit run frontend.py
```

# Testes

Para executar os testes, execute o seguinte comando:

```bash
pytest
```

Os métodos do _backend_ contam com testes unitários completos, além de um teste de ponta-a-ponta (end-to-end) que simular a utilização normal de um usuário, invocando a maior parte dos _endpoints_ disponíveis.