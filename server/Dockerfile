# Use uma imagem oficial Python como base
FROM python:3.8-slim

# Definir diretório de trabalho no container
WORKDIR /app

# Copie os arquivos necessários para o container
COPY server.py /app/
COPY requirements.txt /app/

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Definir porta padrão para o servidor
EXPOSE 8000

# Comando para executar quando o container for iniciado
CMD ["python", "server.py"]