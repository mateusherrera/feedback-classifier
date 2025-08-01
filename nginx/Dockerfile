# Última versão da imagem oficial do Nginx
FROM nginx:latest

# Removndo o arquivo de configuração padrão
RUN rm /etc/nginx/conf.d/*

# Copiando o certificado SSL e a chave privada
COPY ssl/ /etc/nginx/ssl/

# Copiando arquivo de configuração customizado
COPY nginx.conf /etc/nginx/conf.d/

# Export porta 443
EXPOSE 443
