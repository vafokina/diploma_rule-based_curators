FROM node:alpine
WORKDIR /usr/app/front
EXPOSE 3000
COPY curators-ui/ ./
RUN npm install bootstrap
RUN npm install
CMD ["npm", "start"]