# Use uma imagem oficial Python como base
FROM python:3.8-slim

# Definir diretório de trabalho no container
WORKDIR /app

# Copie os arquivos necessários para o container
COPY admin.py /app/
COPY requirements.txt /app/
COPY ipconfigadmin.py .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Definir porta padrão para o servidor
EXPOSE 5234

# Comando para executar quando o container for iniciado
CMD ["python", "admin.py"]

#docker run -it admin -->>> executar docker no modo interativo