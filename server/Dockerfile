# Utilize uma imagem base com Python 3.8
FROM python:3.8

# Cria um diretório de trabalho
WORKDIR /app

# Copie os arquivos para o container
COPY server.py .
COPY ipconfig.py .

# Expõe a porta que o servidor vai rodar
EXPOSE 5234

# Comando para rodar o servidor
CMD ["python", "server.py"]

