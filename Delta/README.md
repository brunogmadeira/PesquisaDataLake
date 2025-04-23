
# Comandos Necessários e Utilizados no Projeto

## 1. Instalação do Poetry

Instalação do Poetry (caso não esteja instalado):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verificar a versão do Poetry:
```bash
poetry --version
```

Criar o ambiente virtual e instalar dependências:
```bash
poetry install
```

Ativar o ambiente virtual (Poetry 2.0 ou posterior):
```bash
poetry env activate
```

## 2. Instalação de Dependências com Poetry

Adicionar dependências ao projeto:
```bash
poetry add pyspark@3.5.0 delta-spark@3.0.0 ipykernel jupyterlab
```

## 3. Configuração do Hadoop no Windows

Variáveis de ambiente para o Hadoop:
Adicione estas linhas no seu script Python (antes da criação de sessão spark) ou no seu terminal:

```python
import os
os.environ['HADOOP_HOME'] = 'C:\hadoop'
os.environ['PATH'] = os.environ['HADOOP_HOME'] + '\bin;' + os.environ['PATH']
```

## 4. Configuração do Spark com Delta

Inicialização do Spark com Delta:
Adicione as configurações Delta quando inicializar o SparkSession:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder     .appName("Delta Lake Example")     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")     .getOrCreate()
```

## 5. Testes de Escrita de Dados em Delta e Parquet

Criar DataFrame em PySpark:
```python
data = [("João", 25), ("Maria", 30), ("José", 35)]
columns = ["Nome", "Idade"]
df = spark.createDataFrame(data, columns)
```

Salvar como Delta:
```python
df.write.format("delta").mode("overwrite").save("C:/tmp/delta-teste")
```

## 6. Comandos para Configuração do Hadoop (Winutils)

Baixar o winutils.exe no diretório C:\hadoop\bin:
```bash
curl -L https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.6/bin/winutils.exe -o /c/hadoop/bin/winutils.exe
```

Configuração do caminho no terminal:
```bash
set HADOOP_HOME=C:\hadoop
set PATH=%HADOOP_HOME%\bin;%PATH%
```

## 7. Comandos de Diagnóstico e Debug

Verificar a versão do Python:
```bash
python --version
```

Verificar a versão do PySpark (lá no python):
```python
import pyspark
print(pyspark.__version__)
```

Verificar a versão do Delta (no Python):
```python
import delta
print(delta.__version__)
```

## 8. Comandos de Erro e Soluções

Para resolver o erro `java.lang.UnsatisfiedLinkError`:
- Configurar corretamente o diretório `winutils.exe` no ambiente, com as variáveis `HADOOP_HOME` e `PATH` adequadas.

## 9. Ativar o Ambiente do Poetry (Se necessário)

Em vez do comando `poetry shell`, utilize:
```bash
poetry env activate
```
Ou diretamente no terminal:
```bash
poetry run jupyter lab
```
Esse comando ativa o ambiente e abre o Jupyter Lab dentro do ambiente virtual configurado com Poetry.

## Comandos úteis para o ambiente de desenvolvimento

Ativar ambiente do Poetry:
```bash
poetry env activate
```

Executar Jupyter Lab:
```bash
poetry run jupyter lab
```

Instalar dependências (Poetry):
```bash
poetry install
```

Adicionar dependências:
```bash
poetry add <package_name>
```

Importante: Não se esqueça de configurar corretamente as variáveis de ambiente (HADOOP_HOME e PATH) no seu terminal ou script Python para que o Hadoop funcione corretamente no Windows.

Quando tudo funciona corretamente, ele pode te redirecionar para um jupyter local, ou abrir o VSCodeStudio onde possui o link (acessado ctrl +click). Comece um novo notebook Python3 e pode começar a programar;

### -> Preparação da sessão:

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("DeltaLakeTest")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")  # <- Aqui é a correção importante
    .getOrCreate()
)
```

### -> Criação de tabela:

```python
# Exemplo de dados para o DataFrame
data = [("João", 25), ("Maria", 30), ("José", 35)]
columns = ["Nome", "Idade"]

# Criando o DataFrame
df = spark.createDataFrame(data, columns)

# Salvando a tabela Delta
df.write.format("delta").mode("overwrite").save("/tmp/delta/clientes")
```

### -> Insert:

```python
# Novos dados para inserir
novos_dados = [("Carlos", 40), ("Ana", 28)]
novos_df = spark.createDataFrame(novos_dados, columns)

# Inserindo dados na tabela Delta
novos_df.write.format("delta").mode("append").save("/tmp/delta/clientes")
```

### -> Update:

```python
from delta.tables import DeltaTable
from pyspark.sql.functions import col

# Carregando a tabela Delta existente
deltaTable = DeltaTable.forPath(spark, "/tmp/delta/clientes")

# Realizando o update
deltaTable.update(
    condition = col("Nome") == "João",  # Condição para o update
    set = { "Idade": "29" }  # Novo valor para a coluna
)
```

### -> Delete:

```python
# Deletando registros com base em uma condição
deltaTable.delete(
    condition = col("Nome") == "José"
)
```

### -> Verificar dados após alterações:

```python
# Lendo e exibindo os dados da tabela Delta
df_resultado = spark.read.format("delta").load("/tmp/delta/clientes")
df_resultado.show()
```
